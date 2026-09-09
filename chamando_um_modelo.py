import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage

load_dotenv()

question_user = input('')

model = init_chat_model(model= 'gemini-3.1-flash-lite',
                        model_provider= 'google_genai',
                        api_key = os.getenv("GEMINI_API_KEY"))

# model = ChatGoogleGenerativeAI(model= 'gemini-3.1-flash-lite',
#                                api_key = os.getenv('GEMINI_API_KEY'),
#                                generation_config={
#                                    "temperature": 0
#                                })

messages = [
    SystemMessage(content="Você é um especialista em Langchain-google-genai. Responda de forma atualizada as perguntas para um usuario iniciante."),
    HumanMessage(question_user)
    ]

response = model.invoke(messages)

print(response.text)


