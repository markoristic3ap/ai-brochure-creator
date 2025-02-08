from website import Website
from modelOpenAi import ModelOpenAI

openAi = ModelOpenAI()
openAi.initialize_model()

website = Website('http://3ap.ch')

user_prompt = f"Here is the list of links on the website of {website.url} - "
user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
Do not include Terms of Service, Privacy, email links.\n"
user_prompt += "Links (some might be relative links):\n"
user_prompt += "\n".join(website.links) 

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
    
def cleanLinks():
    response = openAi.chat([
        {"role": "system", "content": link_system_prompt},
        {"role": "user", "content": user_prompt}
    ])
    print(response)
    
cleanLinks()