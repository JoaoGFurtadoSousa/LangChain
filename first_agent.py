from re import S

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from dotenv import load_dotenv
from pydantic import BaseModel



load_dotenv()

class ExplicationAITeacher(BaseModel):
    name_student:str
    explication_for_question: str


question_user = input('Pergunta sobre Langchain: ')

model = init_chat_model(model= 'gemini-3.5-flash-lite',
                        model_provider='google_genai')

agent = create_agent(model= model,
                     system_prompt= "Você é um professor de LangChain experiente. Responda as questões de forma didatica e facil para que o aluno consiga entender da melhor forma.",
                     response_format= ExplicationAITeacher
                     )

for chunk, metadata in agent.stream({'messages': [HumanMessage(content= question_user)]},
                                    stream_mode='messages'):
    if chunk.text:
        print(chunk.text, flush=True, end="")