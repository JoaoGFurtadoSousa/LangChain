from colorama import init
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv


load_dotenv()




pedidos = {
    1023: {
        "cliente": "Carlos",
        "produto": "Notebook",
        "status": "Em transporte"
    },
    1024: {
        "cliente": "Ana",
        "produto": "Teclado",
        "status": "Entregue"
    },
    1025: {
        "cliente": "Pedro",
        "produto": "Monitor",
        "status": "Preparando envio"
    }
}



model = init_chat_model(model= 'gemini-3.5-flash-lite',
                        model_provider='google_genai')

@tool("consulta_pedidos", description="Busca pedidos pelo ID e retorna o pedido completo")
def consulta_pedidos(id: str) -> dict:
    id = int(id)
    pedido = pedidos[id]
    return pedido

agent = create_agent(model= model,
                     tools=[consulta_pedidos],
                     system_prompt="Você é um agente especializado em consultar pedidos solicitados pelos usuarios. Utilize a tool de consulta pedidos para retorna o pedido solicitado"
                     )

# testando a tool
print(consulta_pedidos.invoke("1025"))

response = agent.invoke({'messages': HumanMessage(content= "Quero saber mais sobre o pedido 1025")})
print(response)
print('-'*20)
print(response['messages'][-1].content)
print(f'Function call: {response['messages'][1].function_call}')