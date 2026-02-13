import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def converter_audio(path: str):
    if not os.path.exists(path):
        print(f"❌ Erro: Arquivo não encontrado em {path}")
        return {"status": False, "text": "Arquivo não encontrado"}

    try:
        # --- SOLUÇÃO DO ERRO ---
        # Mapeamos extensões comuns para garantir que o Gemini saiba o que está recebendo
        mime_types = {
            '.ogg': 'audio/ogg',
            '.mp3': 'audio/mpeg',
            '.wav': 'audio/wav',
            '.m4a': 'audio/mp4',
            '.aac': 'audio/aac'
        }
        
        # Pega a extensão do arquivo (ex: .ogg)
        _, ext = os.path.splitext(path.lower())
        tipo_mime = mime_types.get(ext, "audio/ogg") # Default se não achar

        # 1. Envia o arquivo especificando explicitamente o mime_type
        arquivo_remoto = genai.upload_file(path=path, mime_type=tipo_mime)
        # -----------------------

        model = genai.GenerativeModel("gemini-1.5-flash")

        # 2. Gera a transcrição
        response = model.generate_content([
            "Transcreva este áudio na íntegra, respeitando a pontuação.",
            arquivo_remoto
        ])

        # 3. Limpeza local
        if os.path.exists(path):
            os.remove(path)
            print(f"🗑 Arquivo local removido: {path}")

        # 4. Limpeza no servidor do Google
        genai.delete_file(arquivo_remoto.name)

        return {
            "status": True,
            "text": response.text
        }

    except Exception as e:
        print(f"Erro no processo Gemini: {e}")
        if os.path.exists(path):
            os.remove(path)
        return {
            "status": False,
            "text": f"Erro: {str(e)}"
        }