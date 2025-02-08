import markdown
from website import Website
from modelOpenAi import ModelOpenAI
import json
import unicodedata 
from xhtml2pdf import pisa

openAi = ModelOpenAI()
openAi.initialize_model()

SOURCE_TITLE = "CreativeWin"
SOURCE_URL = "https://creativewin.net"

link_system_prompt = "You are provided with a list of links found on a webpage. \
You are able to decide which of the links would be most relevant to include in a brochure about the company, \
such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
link_system_prompt += "You should respond in JSON as in this example:"
link_system_prompt += """
{
  "links": [
    {"type": "about page", "url": "https://full.url/goes/here/about"},
    {"type": "careers page": "url": "https://another.full.url/careers"}
  ]
}
"""

def get_links_user_prompt(website):
    user_prompt = f"Here is the list of links on the website of {website.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(website.links)
    return user_prompt
    
def brochure_source_links(website):
    response = openAi.chat([
        {"role": "system", "content": link_system_prompt},
        {"role": "user", "content": get_links_user_prompt(website)}
    ], 'json')
    return json.loads(response)


def get_all_details(url):
    website = Website(url)
    result = "Landing page:\n"
    result += website.get_contents()
    links = brochure_source_links(website) 
    print("Found links:", links)
    for link in links["links"]:
        result += f"\n\n{link['type']}\n"
        result += Website(link["url"]).get_contents()
    return result
  
 
system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a company website \
and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
Include details of company culture, customers and careers/jobs if you have the information." 
  
def get_brochure_user_prompt(company_name, url):
    user_prompt = f"You are looking at a company called: {company_name}\n"
    user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
    user_prompt += get_all_details(url)
    user_prompt = user_prompt[:5_000] # Truncate if more than 5,000 characters
    return user_prompt  

def clean_text(text):
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
  
def create_brochure(company_name, url):
    response = openAi.chat([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
    ])

    response = clean_text(response)
    response = markdown.markdown(response)
    
    with open('brochure.pdf', 'wb') as output_file:
     pisa.CreatePDF(response, output_file)
    
 

create_brochure(SOURCE_TITLE, SOURCE_URL)