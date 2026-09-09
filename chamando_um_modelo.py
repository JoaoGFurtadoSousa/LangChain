import os
from dotenv import load_dotenv
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.messages import HumanMessage, SystemMessage

load_dotenv()

question_user = input('')

model = ChatGoogleGenerativeAI(model= 'gemini-3.1-flash-lite',
                               api_key = os.getenv('GEMINI_API_KEY'),
                               generation_config={
                                   "temperature": 0
                               })

messages = [
    SystemMessage(content="Você é um especialista em Langchain-google-genai. Responda de forma atualizada as perguntas para um usuario iniciante."),
    HumanMessage(question_user)
    ]

response = model.invoke(messages)

print(response.text)


