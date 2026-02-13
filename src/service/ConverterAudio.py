import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configura a chave (Certifique-se de que a variável é GEMINI_API_KEY no .env)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def converter_audio(path: str):
    # Verifica se o arquivo realmente existe no path fornecido antes de começar
    if not os.path.exists(path):
        print(f"❌ Erro: Arquivo não encontrado em {path}")
        return {"status": False, "text": "Arquivo não encontrado"}

    try:
        # 1. Envia o arquivo local para a API do Google
        # O Gemini aceita formatos comuns como .mp3, .wav, .m4a, etc.
        arquivo_remoto = genai.upload_file(path=path)

        # 2. Instancia o modelo
        # O 'gemini-1.5-flash' é o mais rápido e barato para transcrições
        model = genai.GenerativeModel("gemini-1.5-flash")

        # 3. Gera a transcrição com um prompt específico
        response = model.generate_content([
            "Transcreva este áudio na íntegra, respeitando a pontuação.",
            arquivo_remoto
        ])

        # 4. Limpeza: Remove o arquivo da sua máquina (seu código original fazia isso)
        os.remove(path)
        print(f"🗑 Arquivo local removido: {path}")

        # 5. Opcional: Remove o arquivo também do servidor do Google para não acumular
        genai.delete_file(arquivo_remoto.name)

        return {
            "status": True,
            "text": response.text
        }

    except Exception as e:
        print(f"Erro no processo Gemini: {e}")
        
        # Tenta remover o arquivo local mesmo se houver erro na API
        if os.path.exists(path):
            os.remove(path)
            
        return {
            "status": False,
            "text": ""
        }