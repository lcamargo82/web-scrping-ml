
import os
import json
from google import genai
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

def analyze_image(image_path):
    """
    Analisa uma imagem usando o Google Gemini (via google-genai SDK)
    e retorna palavras-chave para busca.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Erro: GEMINI_API_KEY não encontrada no arquivo .env")
        return []

    try:
        # Configuração do Client (Nova SDK)
        client = genai.Client(api_key=api_key)

        # Upload da imagem (Nova SDK)
        # O método client.files.upload aceita 'file' como caminho ou objeto
        file_ref = client.files.upload(file=image_path)
        
        # Prompt otimizado para extração de keywords
        prompt = """
        Você é um especialista em e-commerce brasileiro. Analise esta imagem de produto e sugira EXATAMENTE 3 termos de busca (keywords) ALTAMENTE ESPECÍFICOS para encontrar este item exato no Mercado Livre.
        
        Regras:
        1. Identifique Marca e Modelo se visíveis (ex: "JBL Flip 6" em vez de "Caixa de som").
        2. Inclua características distintivas (ex: "prova d'água", "20W", "portátil").
        3. Evite termos genéricos como "qualidade", "bom", "barato".
        4. O primeiro termo deve ser o mais específico possível (Marca + Modelo + Cor/Ref).
        
        Retorne APENAS um JSON válido no formato: {"keywords": ["termo 1", "termo 2", "termo 3"]}
        Não use formatação Markdown (```json) ou texto extra. Apenas o JSON puro.
        """

        # Geração de conteúdo (Nova SDK)
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=[file_ref, prompt]
        )

        # Processamento da resposta
        response_text = response.text
        
        # Limpeza básica de Markdown se houver
        if "```json" in response_text:
            response_text = response_text.replace("```json", "").replace("```", "")
        
        data = json.loads(response_text)
        return data.get("keywords", [])

    except Exception as e:
        print(f"Erro ao analisar imagem com Gemini: {e}")
        return []


if __name__ == "__main__":
    print("Módulo de Análise de IA (Gemini) carregado.")
