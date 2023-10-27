from os import getenv
from sys import argv
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = getenv('OPENAI_TOKEN')

response = openai.Completion.create(
    model='text-davinci-003',
    n=1,
    max_tokens=1000,
    temperature=0.7,
    prompt=' '.join(argv[1:])
).choices[0].text

print(response)
