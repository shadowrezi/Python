from os import getenv
from Bard import Chatbot
from dotenv import load_dotenv

load_dotenv()

chatbot = Chatbot(
    session_id=getenv('bard')
)
print(chatbot.ask('Hello!'))
