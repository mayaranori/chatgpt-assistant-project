# 🧠 Assistente ChatGPT - Projeto Exclusivo
Bem-vindo ao projeto Assistente ChatGPT! Este projeto foi desenvolvido de forma exclusiva por Mayara Nori para demonstrar a implementação de um assistente virtual utilizando a API do ChatGPT, integração com banco de dados e funcionalidades específicas de atendimento e captação de leads.

## 📜 Autoria e Direitos
Este projeto é de autoria exclusiva de Mayara Nori. Todos os direitos estão reservados.

Qualquer cópia, distribuição ou uso do código deste projeto sem a devida autorização prévia é estritamente proibida. Se você estiver interessado em colaborar ou utilizar partes deste projeto para fins educacionais ou comerciais, entre em contato diretamente com o autor.

## 📖 Visão Geral do Projeto
O Assistente ChatGPT foi projetado para oferecer uma experiência interativa de chatbot, utilizando inteligência artificial para captar leads, agendar demonstrações e fornecer informações personalizadas sobre produtos e serviços. Esta solução é altamente adaptável e pode ser integrada em diversos contextos de atendimento ao cliente.

## 🚀 Funcionalidades Principais
- **Captação de Leads**: Coleta de informações de contato do usuário e armazenamento em banco de dados.
- **Integração com Banco de Dados**: Utiliza SQLite para armazenar e recuperar informações de leads, produtos e planos.
- **Respostas Personalizadas**: Identifica menções de produtos específicos na mensagem do usuário e retorna benefícios e valores relacionados. Isso é gerenciado pelo arquivo `chatgpt_assistant.py`.
- **Agendamento de Demonstrações**: Coleta preferências de horário e armazena informações de contato para agendamento.

## 🛠️ Tecnologias Utilizadas
- **Python**: Linguagem de programação principal utilizada para desenvolver o assistente.
- **SQLite**: Banco de dados para armazenamento de leads, informações de produtos e planos.
- **API do ChatGPT**: Para implementação do assistente virtual com inteligência artificial.
- **VS Code**: Editor de código utilizado no desenvolvimento do projeto.

## 📁 Estrutura do Projeto

```plaintext
AssistenteChatGPT/
├── database/
│   └── assistente.db         # Banco de dados SQLite com informações de produtos, planos e leads.
    └── create_db.py          # Script para criação do banco de dados e tabelas iniciais. 
├── src/
│   ├── app.py                # Arquivo principal para interações básicas com o assistente.
│   ├── chatgpt_assistant.py  # Funções avançadas para gerenciamento de leads , respostas personalizadas.
└── docs/
    └── README.md             # Documentação do projeto.
```


## Pré-requisitos

Para executar este projeto, você precisará ter os seguintes softwares instalados:

 ```bash
- Python 3.7+
- Biblioteca `openai`
- Biblioteca `sqlite3`
- Biblioteca `aiohttp`
 ```

## Configuração

1. Insira a sua chave de API do OpenAI nos arquivos app.py e chatgpt_assistant.py:
 ```bash
openai.api_key = "your-openai-api-key"
 ```
2. Certifique-se de que o caminho do banco de dados no arquivo chatgpt_assistant.py esteja correto:
 ```bash
DATABASE_PATH = 'database/assistente.db'
 ```
## 📚 Como Executar o Projeto

1. Clone o repositório:
 ```bash
 git clone https://github.com/seu-usuario/assistente-chatgpt.git
 ```

2. Navegue até o diretório do projeto:
 ```bash
cd assistente-chatgpt
 ```
3. Instale as dependências necessárias: Certifique-se de ter o Python instalado e execute o comando:
 ```bash
pip install -r requirements.txt
 ```
4. Crie o banco de dados: Se ainda não tiver o banco de dados assistente.db, crie-o utilizando o script fornecido em database/create_db.py. Para isso, execute o seguinte comando:
 ```bash
python database/create_db.py
 ```
5. Execute o assistente básico:
 ```bash
python src/app.py
 ```
6. Para iniciar o assistente completo com funcionalidades adicionais, execute o arquivo chatgpt_assistant.py:
 ```bash
python src/chatgpt_assistant.py
 ```
Isso permitirá a execução do assistente com integração ao banco de dados e suporte a funções como agendamento de demonstrações e captura de leads.

7. Interaja com o assistente: Siga as instruções no terminal ou utilize uma interface gráfica para testar as funcionalidades do chatbot.

## 📝 Exemplos de Uso

### Captação de Leads
O assistente pode capturar informações como nome, e-mail e telefone para adicionar novos leads ao banco de dados. Exemplo de diálogo:

- **Usuário:** "Estou interessado em saber quais os planos de assinatura."
- **Assistente:** "Traz a lista de planos e valores disponiveis"

### Agendamento de Demonstrações e Captação de Leads
O assistente é capaz de agendar demonstrações de produtos com base nas preferências de horário fornecidas pelo usuário. Exemplo de diálogo:

- **Usuário:** "Gostaria de agendar uma demonstração."
- **Assistente:** "Para fornecer uma proposta personalizada sobre a AssistBot, é melhor conversarmos diretamente. Posso agendar uma demonstração gratuita para você, onde nossa equipe poderá entender suas necessidades e apresentar uma solução adequada. Qual seria o melhor horário para você?."
- **Usuário: Segunda feira, 10 de outubro, 15hs
- **Assistente:** Perfeito! Antes de finalizarmos, posso saber o seu nome completo? 
- **Usuário:** Nome Sobrenome
- **Assistente:** E qual o seu e-mail para que possamos enviar a confirmação do agendamento? 
- **Usuário:** nome@email.com
- **Assistente:** Por fim, poderia fornecer um número de telefone para contato caso precisemos ajustar o horário? 
- **Usuário:** (ddd)123 456 789
- **Assistente**: Agendado para segunda! Entraremos em contato com você em breve, Nome Sobrenome. Obrigado pelo interesse!

### Respostas Personalizadas
O assistente retorna informações personalizadas com base nas consultas do usuário sobre produtos específicos. Exemplo de diálogo:

- **Usuário:** "Quais os beneficios do AssistBot Standard?"
- **Assistente:** "Aqui estão alguns benefícios do produto AssistBot Standard: Suporte 24/7."

## 🌟 Diferenciais do Projeto

- **Flexibilidade:** O assistente pode ser facilmente adaptado para diferentes tipos de negócios e necessidades.
- **Integração Completa:** O projeto inclui integração com banco de dados e lógica de negócios para atender a múltiplas funcionalidades.
- **Documentação Completa:** A documentação do projeto cobre desde a instalação até exemplos de uso e detalhes de implementação.

## 📃 Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo LICENSE para obter detalhes. Mesmo com esta licença, reitera-se que a autoria e os direitos sobre o projeto são reservados a Mayara Nori. Qualquer utilização do código para fins comerciais ou de redistribuição deve ser precedida de autorização.

## 📧 Contato
Para quaisquer dúvidas ou interesse em colaborar com o projeto, entre em contato:

Email: mayara.consultech@gmail.com
LinkedIn: https://www.linkedin.com/in/mayaranori/
