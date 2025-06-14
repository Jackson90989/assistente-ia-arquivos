import streamlit as st
from chat_core import Chatbot
import os

MODEL_PATH = MODEL_PATH = os.path.join("models", "mistral-7b-instruct-v0.1.Q3_K_M.gguf")

@st.cache_resource(show_spinner=False)
def load_bot():
    return Chatbot(MODEL_PATH)

def render_message(role, message):
    if role == "user":
        st.markdown(
            f"""
            <div style="text-align:right; margin:10px;">
                <div style="display:inline-block; background-color:#0078d4; color:white; padding:10px; border-radius:15px; max-width:70%;">
                    {message}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(
            f"""
            <div style="text-align:left; margin:10px;">
                <div style="display:inline-block; background-color:#e1e1e1; color:black; padding:10px; border-radius:15px; max-width:70%;">
                    {message}
                </div>
            </div>
            """, unsafe_allow_html=True)

def main():
    st.title("🤖 Chatbot Profissional GPT4All + Excel")

    bot = load_bot()

    st.sidebar.title("Opções")
    uploaded_file = st.sidebar.file_uploader("Carregue seu arquivo Excel", type=["xls", "xlsx"])

    if uploaded_file:
        bot.load_excel(uploaded_file)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    prompt = st.text_input("Digite sua pergunta:")

    st.markdown("### Conversa")
    for role, msg in st.session_state.chat_history:
        render_message(role, msg)

    if st.button("Enviar") and prompt.strip():
        with st.spinner("Processando..."):
            response = bot.ask(prompt.strip())
        st.session_state.chat_history.append(("user", prompt.strip()))
        st.session_state.chat_history.append(("bot", response))

    if st.button("🧹 Limpar Conversa"):
        st.session_state.chat_history = []
        bot.chat_history = []
        bot.response_cache = {}

    if st.button("📋 Copiar Histórico"):
        history_text = "\n".join([f"{r}: {m}" for r, m in st.session_state.chat_history])
        st.text_area("Histórico da conversa", value=history_text, height=200)

if __name__ == "__main__":
    main()
