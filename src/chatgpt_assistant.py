import re
import sqlite3
import openai
import asyncio
from aiohttp import ClientSession
from datetime import datetime

openai.api_key = 'your-openai-api-key'

DATABASE_PATH = 'database/assistente.db'

async def conectar_bd():
    """Conecta ao banco de dados SQLite e retorna a conexão."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
    
async def salvar_lead_no_banco(lead_info):
    """Salva as informações do lead no banco de dados de forma assíncrona."""
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, salvar_lead_no_banco_sync, lead_info)

def salvar_lead_no_banco_sync(lead_info):
    """Função sincrona para salvar o lead no banco de dados."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        nome= str(lead_info['nome'])
        email= str(lead_info['email'])
        telefone= str(lead_info['telefone'])
        insertdate =str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  
        
        # Inserting datas in Leads table
        cursor.execute(f"""
            INSERT INTO Leads (nome, email, telefone, data_captura)
            VALUES ('{nome}', '{email}','{telefone}','{insertdate}')
        """)

        conn.commit()
        print("Lead salvo com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao salvar lead: {e}")
    finally:
        conn.close()


async def identificar_produto(user_message):
    """Identifica o produto mencionado na mensagem do usuário."""
    conn = await conectar_bd()
    produto_nome = None
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT nome FROM Produtos")
            produtos = cursor.fetchall()

            for produto in produtos:
                nome_produto = produto[0].lower()
                if nome_produto in user_message.lower():
                    produto_nome = produto[0]
                    print(f"Produto identificado: {produto_nome}")
                    break
        except sqlite3.Error as e:
            print(f"Erro ao identificar produto: {e}")
        finally:
            conn.close()
    return produto_nome

async def buscar_beneficios(produto_nome=None):
    """Busca benefícios de um produto específico no banco de dados.
    Se nenhum produto for especificado, retorna os benefícios gerais.
    """
    conn = await conectar_bd()
    if conn:
        try:
            cursor = conn.cursor()
            if produto_nome:
                print(f"Buscando benefícios para o produto: {produto_nome}")
                cursor.execute("""
                    SELECT b.beneficio
                    FROM Beneficios b
                    JOIN Produtos p ON b.produto_id = p.id
                    WHERE p.nome = ?
                """, (produto_nome,))
                beneficios = cursor.fetchall()
                print(f"Benefícios encontrados: {beneficios}")
                if beneficios:
                    return f"Aqui estão alguns benefícios do produto {produto_nome}:\n" + "\n".join([beneficio[0] for beneficio in beneficios])
                else:
                    return f"Não encontrei benefícios para o produto '{produto_nome}'."
            else:
                return ("A AssistBot oferece vários benefícios, incluindo: chatbots personalizados para responder perguntas comuns e gerenciar agendamentos, "
                        "integração com plataformas de mensagens populares, e soluções adaptadas para melhorar a eficiência do atendimento ao cliente. "
                        "Nossa plataforma também pode ser integrada com sistemas de CRM e outras ferramentas que você já utiliza.")
        except sqlite3.Error as e:
            print(f"Erro ao buscar benefícios: {e}")
            return "Houve um erro ao buscar os benefícios."
        finally:
            conn.close()
    else:
        return "Não foi possível conectar ao banco de dados."

async def buscar_valores(produto_nome=None):
    """Busca valores de um produto específico no banco de dados.
    Se nenhum produto for especificado, retorna uma mensagem genérica sobre preços.
    """
    conn = await conectar_bd()
    if conn:
        try:
            cursor = conn.cursor()
            if produto_nome:
                print(f"Buscando valores para o produto: {produto_nome}")
                cursor.execute("""
                    SELECT b.preco
                    FROM Planos b
                    JOIN Produtos p ON b.id = p.id
                    WHERE p.nome = ?
                """, (produto_nome,))
                valores = cursor.fetchall()
                print(f"Valor encontrado: {valores}")
                if valores:
                    return f"O valor do produto {produto_nome} é a partir de:\n" + "\n".join([str(valor[0]) for valor in valores]) + "\nPara fornecer uma proposta personalizada sobre os custos da AssistBot, é melhor conversarmos diretamente. Posso agendar uma demonstração gratuita para você, onde nossa equipe poderá entender suas necessidades e apresentar uma solução adequada. Qual seria o melhor horário para você?"
                else:
                    return f"Não encontrei valores para o produto '{produto_nome}'."
            else:
                return ("Para fornecer uma proposta personalizada sobre os custos da AssistBot, é melhor conversarmos diretamente. Posso agendar uma demonstração gratuita para você, onde nossa equipe poderá entender suas necessidades e apresentar uma solução adequada. Qual seria o melhor horário para você?")
        except sqlite3.Error as e:
            print(f"Erro ao buscar valores: {e}")
            return "Houve um erro ao buscar os valores."
        finally:
            conn.close()
    else:
        return "Não foi possível conectar ao banco de dados."
    
async def buscar_planos():
    """Busca os planos disponíveis no banco de dados."""
    conn = await conectar_bd()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT nome_plano, preco FROM Planos")
            planos = cursor.fetchall()
            if planos:
                return "Aqui estão os planos disponíveis:\n" + "\n".join([f"{plano[0]}: R${plano[1]}" for plano in planos])
            else:
                return "Atualmente, não há planos disponíveis."
        except sqlite3.Error as e:
            print(f"Erro ao buscar planos: {e}")
            return "Houve um erro ao buscar os planos."
        finally:
            conn.close()
    else:
        return "Não foi possível conectar ao banco de dados."
    
def validar_dados(nome, email, telefone):
    """Valida o nome, email e telefone fornecidos pelo usuário."""
    # Validar nome
    if not nome or len(nome.split()) < 2:
        return False, "Por favor, insira seu nome completo."

    # Validar email
    padrao_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(padrao_email, email):
        return False, "Por favor, insira um endereço de email válido."

    # Validar telefone
    padrao_telefone = r'^\+?1?\d{9,15}$'
    if not re.match(padrao_telefone, telefone):
        return False, "Por favor, insira um número de telefone válido."

    return True, "Dados válidos."


async def agendar_demonstracao(user_message=None):
    """Pergunta ao usuário sobre o melhor horário para agendar uma demonstração."""
    if user_message:
        # Regex para identificar uma data ou horário (simplificado)
        data_horario = re.search(r'\b(\d{1,2}[:h]?\d{0,2})\b|\b(segunda|terça|quarta|quinta|sexta|sábado|domingo)\b', user_message.lower())
    
        if data_horario:
            # Captura o nome, email e telefone do usuário
            while True:
                nome = input("Assistente: Perfeito! Antes de finalizarmos, posso saber o seu nome completo? \nVocê: ")
                email = input("Assistente: E qual o seu e-mail para que possamos enviar a confirmação do agendamento? \nVocê: ")
                telefone = input("Assistente: Por fim, poderia fornecer um número de telefone para contato caso precisemos ajustar o horário? \nVocê: ")
                
                valido, mensagem = validar_dados(nome, email, telefone)
                if valido:
                    break
                else:
                    print(f"Assistente: {mensagem} Por favor, tente novamente.")
            
            # Armazenar as informações no banco de dados
            lead_info = {
                "nome": nome,
                "email": email,
                "telefone": telefone,
                "data_horario": data_horario.group()
            }

            await salvar_lead_no_banco(lead_info)
            
            return f"Agendado para {data_horario.group()}! Entraremos em contato com você em breve, {nome}. Obrigado pelo interesse!"
    
    return ("Para fornecer uma proposta personalizada sobre a AssistBot, "
            "é melhor conversarmos diretamente. Posso agendar uma demonstração gratuita para você, "
            "onde nossa equipe poderá entender suas necessidades e apresentar uma solução adequada. "
            "Qual seria o melhor horário para você?")
    
async def respond_to_user(user_message):
    """Responde ao usuário com base na mensagem fornecida."""
    
    user_message_lower = user_message.lower()
    
    if "olá" in user_message_lower or "boa tarde" in user_message_lower or "ola" in user_message_lower or "bom dia" in user_message_lower or "boa noite" in user_message_lower:
        return "Olá! Sou o assistente da AssistBot. Como posso ajudar você hoje? Se tiver alguma pergunta sobre a AssistBot, seus recursos ou como começar, estou aqui para ajudar!"
    
    if "quanto custa" in user_message_lower or "qual valor" in user_message_lower or "qual o valor" in user_message_lower:
        produto_nome = await identificar_produto(user_message)
        if produto_nome:
            return await buscar_valores(produto_nome)
        else:
            return await buscar_valores()

    if "o que é" in user_message_lower or "o que é a AssistBot" in user_message_lower:
        return "A AssistBot é uma plataforma avançada de chatbots projetada para melhorar a eficiência e a interação com os clientes. Nossos chatbots personalizados ajudam a responder perguntas comuns, gerenciar agendamentos e integrar-se com suas plataformas de comunicação existentes. Gostaria de saber mais sobre algum recurso específico ou prefere agendar uma demonstração para ver tudo em ação?"

    if "benefícios" in user_message_lower or "beneficios" in user_message_lower:
        produto_nome = await identificar_produto(user_message)
        if produto_nome:
            return await buscar_beneficios(produto_nome)
        else:
            return await buscar_beneficios()

    if "como ajuda" in user_message_lower or "como a AssistBot pode ajudar" in user_message_lower:
        return "A AssistBot pode ajudar sua empresa a melhorar o atendimento ao cliente, automatizar respostas a perguntas frequentes, agendar compromissos e integrar-se com suas plataformas de comunicação existentes. Isso resulta em uma maior eficiência operacional e uma melhor experiência para seus clientes."

    if "setores" in user_message_lower or "para quais setores" in user_message_lower or "nichos" in user_message_lower:
        return "A AssistBot é adequada para uma ampla gama de setores, incluindo serviços ao cliente, varejo, saúde, educação e muito mais. Nossos chatbots podem ser personalizados para atender às necessidades específicas de qualquer setor, oferecendo soluções que melhoram a interação com os clientes e otimizam os processos internos."

    if "como começar" in user_message_lower:
        return "Ótimo que você quer começar com a AssistBot! O primeiro passo é entender suas necessidades para oferecer uma solução personalizada. Posso agendar uma demonstração para você? Assim, nossa equipe poderá mostrar como a AssistBot pode atender às suas necessidades e responder a todas as suas perguntas. Qual horário seria conveniente para você?"
    
    if "quais os planos" in user_message_lower or "quais planos" in user_message_lower or "planos disponíveis" in user_message_lower:
        return await buscar_planos()
    
    # Captura a intenção de agendamento
    if "agendar" in user_message_lower or "demonstração" in user_message_lower:
        return await agendar_demonstracao(user_message)

    # Captura possível resposta com horário/dia para agendamento
    if re.search(r'\b(\d{1,2}[:h]?\d{0,2})\b|\b(segunda|terça|quarta|quinta|sexta|sábado|domingo)\b', user_message_lower):
        return await agendar_demonstracao(user_message)

    return "Desculpe, não entendi sua pergunta. Por favor, diga-me como posso ajudá-lo ou peça uma demonstração."

async def chat_with_user():
    """Inicia o chat com o usuário."""
    print("Bem-vindo ao AssistBot! Olá! 😊 Sou a May, assistente da AssistBot. Estou aqui para te ajudar a automatizar o atendimento ao cliente e aumentar as conversões do seu site com nossos chatbots de IA. Como posso auxiliar você hoje?")
    while True:
        user_input = input("Você: ")
        if user_input.lower() in ["sair", "exit", "fim"]:
            print("Assistente: Obrigado por conversar conosco! Se tiver mais perguntas ou precisar de assistência adicional, estou aqui para ajudar")
            break
        response = await respond_to_user(user_input)
        print(f"Assistente: {response}")

if __name__ == "__main__":
    asyncio.run(chat_with_user())
