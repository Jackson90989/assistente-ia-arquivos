import os
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize
from gpt4all import GPT4All

nltk.download('punkt')

class Chatbot:
    def __init__(self, model_path):
        self.model = GPT4All(model_name=model_path)
        self.chat_history = []  # (role, message)
        self.response_cache = {}
        self.excel_data = None  # guarda dados do excel

    def classify_intent(self, query):
        q = query.lower()
        if any(w in q for w in ["arquivo", "excel", "csv", "ler", "dados"]):
            return "analisar_arquivo"
        if any(w in q for w in ["olá", "oi", "bom dia", "tudo bem"]):
            return "saudacao"
        if any(w in q for w in ["ajuda", "suporte", "problema", "erro"]):
            return "suporte"
        return "geral"

    def build_prompt(self, query):
        # Prompt simples, pode ser melhorado
        prompt = "Você é um assistente inteligente.\n"
        if self.excel_data is not None:
            prompt += f"Dados da planilha:\n{self.excel_data}\n"
        prompt += f"Usuário: {query}\nAssistente:"
        return prompt

    def ask(self, query):
        intent = self.classify_intent(query)
        if intent == "saudacao":
            response = "Olá! Como posso ajudar você hoje?"
        elif intent == "analisar_arquivo" and self.excel_data is not None:
            prompt = self.build_prompt(query)
            response = self.model.generate(prompt).strip()
        else:
            if query in self.response_cache:
                response = self.response_cache[query]
            else:
                prompt = self.build_prompt(query)
                response = self.model.generate(prompt).strip()
                self.response_cache[query] = response
        self.chat_history.append(("user", query))
        self.chat_history.append(("bot", response))
        return response

    def load_excel(self, file):
        df = pd.read_excel(file)
        self.excel_data = df.head(20).to_string()  # pega só as 20 primeiras linhas pra evitar prompt gigante
        self.chat_history.append(("bot", "Arquivo Excel carregado com sucesso!"))


