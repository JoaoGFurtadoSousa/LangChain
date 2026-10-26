from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage
from dotenv import load_dotenv
import os, uuid, json

load_dotenv()

user_input = input("Como podemos te ajudar hoje? Informe sua solicitação e seu ID: ")

session_id = f"ses_{uuid.uuid4().hex}"

contas = {
    1: {
        "titular": "Carlos",
        "saldo": 1500.00,
        "extrato": [
            {"tipo": "entrada", "valor": 500.00},
            {"tipo": "saida", "valor": 200.00}
        ]
    },
    2: {
        "titular": "Ana",
        "saldo": 800.00,
        "extrato": []
    },
    3: {
        "titular": "Pedro",
        "saldo": 250.00,
        "extrato": []
    }
}


@tool(description="Tool responsavel por consultar o saldo de um individuo atraves do id recebido por parametro")
def consulta_saldo(id_cliente: int) -> dict:
    try: 
        dados_usuario = contas[id_cliente]
        del dados_usuario[id_cliente]['extrato']
        return dados_usuario[id_cliente]
    except KeyError:
        error = {'detail': 'Usuario não encontrado'}
        return ValueError(json.dumps(error))


model = init_chat_model(model=os.getenv("OPENCODE_MODEL"),
                        model_provider="openai",
                        api_key=os.getenv("OPENCODE_API_KEY"),
                        base_url=os.getenv("OPENCODE_BASE_URL"),
                        default_headers={
                        "x-opencode-session": session_id,
                        "User-Agent": "langchain-learning-agent/1.0"
                        }
                        )

agent = create_agent(model = model,
                     system_prompt= "Voce é um auxiliar financeiro que deve ser bastante compreensivo com os usuarios. Utilize as tools listadas para realizar a operação desejada por cada usuario. Sempre fale o nome do usuario do id e em seguinte o resultado da operação",
                     tools= [consulta_saldo])

for chunk, metadata in agent.stream({"messages": [HumanMessage(user_input),]},
                                    stream_mode = "messages"):
    if metadata.get("langgraph_node") == "model":
        if chunk.text:
            print(chunk.text, flush=True, end="")

# response = agent.invoke(input= {'messages': [HumanMessage(user_input),] })
# print(response["messages"][-1].content)

#consulta_saldo.invoke({"id_cliente": 1})
