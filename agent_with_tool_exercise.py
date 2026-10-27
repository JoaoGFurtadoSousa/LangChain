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
        titular = dados_usuario['titular']
        saldo = dados_usuario['saldo']
        return {"titular": titular,
                "saldo": saldo}
    
    except KeyError:
        return {"sucess": False,
        "error": "Account not found",
        "detail": "Usuario não encontrado"}


@tool(description="Tool responsavel por consultar o extrato de um individuo atraves do id recebido por parametro")
def consultar_extrato(id_cliente: int) -> dict:
    try: 
        dados_usuario = contas[id_cliente]
        titular = dados_usuario['titular']
        extrato = dados_usuario['extrato']
        return {"titular": titular,
                "extrato": extrato}
        
    except KeyError:
        return {"sucess": False,
                "error": "Account not found",
                "detail": "Usuario não encontrado"}


@tool(description="Tool responsavel por realizar transações entre clientes. Como parametro são utilizados o id_cliente que irá enviar o dinheiro; destinatario_id é o id de quem irá receber e o valor enviado de uma conta para a outra")
def transferir_valor(id_cliente: int, destinatario_id:int, valor_a_ser_enviado:float) -> dict:
    
    if id_cliente == destinatario_id:
        return {"success":False,
                "error":"A client cannot send to themselves",
                'detail': 'O cliente não pode realizar uma transação para esta mesma conta. Digite uma outra conta valida'}
    
    if valor_a_ser_enviado <= 0:
        
        return {"success": False,
                "error": "Value cannot be negative",
                "detail": "O valor a ser enviado não pode ser menor que zero."}
    
    
    try: 
        dados_usuario = contas[id_cliente]       
        dados_destinatario = contas[destinatario_id]
        try:
            saldo_cliente = dados_usuario['saldo']

            if saldo_cliente < valor_a_ser_enviado:
                    return {"success": False,
                            "error": "The balance cannot be less than the transferable amount.",
                            "detail": f"Saldo do Cliente {dados_usuario["titular"]} não pode ser inferior ao valor enviado."}
            
            dados_usuario['saldo'] = saldo_cliente - valor_a_ser_enviado
            dados_usuario['extrato'].append({"tipo": "saida", "valor": valor_a_ser_enviado})
            dados_destinatario['saldo'] += valor_a_ser_enviado
            dados_destinatario['extrato'].append({"tipo": "entrada", "valor": valor_a_ser_enviado})
            
            return dados_usuario
        except Exception as error:
            return error
    except KeyError:
         return {"sucess": False,
                "error": "Account not found",
                "detail": "Usuario não encontrado"}
    
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
                     tools= [consulta_saldo, consultar_extrato, transferir_valor])



for chunk, metadata in agent.stream({"messages": [HumanMessage(user_input),]},
                                    stream_mode = "messages"):
    if metadata.get("langgraph_node") == "model":
        if chunk.text:
            print(chunk.text, flush=True, end="")

