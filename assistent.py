#importando a biblioteca os para interagir com o sistema operacional
import os 
#importando a biblioteca streamlit para criar a interface web
import streamlit as st
#importando a biblioteca groq para utilizar o modelo de linguagem grande
from groq import Groq

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Alpha Coder",
    page_icon="👨🏾‍💻", 
    layout="wide", 
    initial_sidebar_state="expanded")


#definindo o prompt customizado para o assistente virtual
prompt_custumizado = """"Você é o "Alpha Coder", um assistente virtual 
de IA especializado em programação, com foco principal em python. Sua missão é 
ajudar os usuários a resolver problemas de codificação, fornecer explicações claras 
e concisas, e oferecer exemplos práticos de código. Você deve ser amigável.

REGRAS DE OPERAÇÃO:
1. foco em programação em python.
2. estrutura da resposta
3. explicações claras e concisas
4. exemplos práticos de código
5. detalhamento técnico
6. documentação"""

#criando o conteudo da barra lateral no streamlit
with st.sidebar:
    #Definindo o título da aplicação na barra lateral
    st.title("Alpha Coder")

    #mostrando um texto sobre o assistente virtual
    st.markdown("Um assistente virtual especializado em programação Python.")

    #Campo para inserir a chave da API
    groq_api_key = st.text_input(
        "Insira sua chave da API Groq:", type="password",
          help="Obtenha sua chave em https://console.groq.com/keys"
    )

    #adicionando linhas divisorias e explicações extras
    st.markdown("---")
    st.markdown(
        "Este assistente virtual utiliza o modelo de linguagem Groq para fornecer "
        "respostas precisas e úteis relacionadas à programação em Python."
    )

    st.markdown("---")
    st.markdown("Desenvolvido por Alan Silva")
    st.markdown("⛓️‍💥[LinkedIn](https://www.linkedin.com/in/alansilva-tech/)")
    st.link_button("✉️ Email para contato","eng.alansilva2020@gmail.com")

#título principal 
st.title("🤖 Alpha Coder")
#subtitulo
st.title("Assistente Virtual de Programação Python 🐍")

#Texto de introdução
st.caption("Faça sua pergunta sobre a limguagem Python e obtenha codigos e explicações!")

#inicializando o historico de mensagens, caso ainda não exista
if "menssages" not  in st.session_state:
    st.session_state.menssages = []

#exibe todas as mensagens no historico
for menssage in st.session_state.menssages:
    with st.chat_message(menssage["role"]):
        st.markdown(menssage["content"])

# verificando se o user forneceu a chave de API da groq
if groq_api_key:

    try:
        #criando cliente groq com a chave da API
        cliente = Groq(api_key=groq_api_key)

    except Exception as e:
        st.error(f"Erro ao inicializar o cliente Grop: {e}")
        st.stop()

#caso não tenha fornecido a chave:
elif st.session_state.menssages:
    st.warning("Por favor, insira sua chave na barra lateral para continuar.")

#capturando a entrada do usuário no chat
if prompt := st.chat_input("Qual a sua dúvida?"):

    # se não houver cliente valido, mostrar aviso
    if not cliente:
        st.warning("Por favor, insira sua chave na barra lateral para continuar.")
        st.stop()
    
    #armazena a mensagem do usuario no estado da sessão
    st.session_state.menssages.append({"role": "user", "content": prompt})

    #exibe a mensagem do usuario no chat
    with st.chat_message("user"):
        st.markdown(prompt)

    #preparando mensagens para enviar ao modelo

    menssages_para_modelo = [{"role": "system", "content": prompt_custumizado}] 
    for msg in st.session_state.menssages:
        menssages_para_modelo.append(msg)

    #cria a resposta do assistente 
    with st.chat_message("assistant"):

      with st.spinner("Pensando..."):

         try:
                #chama a API para gerar a resposta
                chat_response = cliente.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=menssages_para_modelo,
                    max_tokens=2048,
                    temperature=0.7,
            
                  )

                #obtém o conteudo da resposta
                alpha_coder_response = chat_response.choices[0].message.content

                

                 #exibe a resposta do assistente no chat
                st.markdown(alpha_coder_response)

                   #armazena a resposta do assistente no estado da sessão
                st.session_state.menssages.append(
                      {"role": "assistant", "content": alpha_coder_response}
                    )

        #caso ocorra um erro ao chamar a API
         except Exception as e:
            st.error(f"Erro ao obter resposta do modelo: {e}")



