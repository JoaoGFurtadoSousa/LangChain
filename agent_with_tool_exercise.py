from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

@tool('consulta_saldo', description='Tool que retorna o saldo do cliente de acordo com o id recebido')
def consulta_saldo(conta:dict, id_cliente: int) -> int:
    print(conta)
    # saldo_cliente = conta[id_cliente]
    # print(saldo_cliente)
    

model = init_chat_model(model= 'gemini-3.5-flash-lite',
                        model_provider='google_genai')

agent = create_agent(model = model,
                     system_prompt= 'Voce é um assistente financeiro e deve auxiliar o usuario de forma clara e prestativa com as solicitações. Uitlize linguagem facil, pois o publico alvo será idosos.',
                     tools=[])

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


print(consulta_saldo.invoke(1))