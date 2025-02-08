

import os
from dotenv import load_dotenv
from openai import OpenAI

DEFAULT_MODEL = "gpt-4o-mini"

class ModelOpenAI():
  def __init__(self, model=DEFAULT_MODEL):
    load_dotenv(override=True)
    self.api_key = os.getenv('OPENAI_API_KEY')
    if not self.api_key:
      print("No API key was found - please check your .env file!")
    else:
      print("OpenAI API key found and looks good so far! \n\n")
      self.model = model
      self.initialize_model()

  def initialize_model(self):
    self.openai = OpenAI(api_key=self.api_key)
    

  def chat(self, prompt):
    response = self.openai.chat.completions.create(
      model = self.model,
      messages = prompt
    ) 
    return response.choices[0].message.content
