
import os
import json
from google import genai
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

def analyze_image(image_path, user_context=None):
    """
    Analisa uma imagem usando o Google Gemini (via google-genai SDK)
    e retorna palavras-chave para busca. 
    Aceita um contexto opcional do usuário.
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
        
        # Montar contexto extra se houver
        context_str = ""
        if user_context:
            context_str = f"CONTEXTO ADICIONAL FORNECIDO PELO USUÁRIO (Use-o para refinar a busca): {user_context}"

        # Prompt otimizado para extração de keywords
        prompt = f"""
        Você é um especialista em e-commerce brasileiro. Analise esta imagem de produto e sugira EXATAMENTE 3 termos de busca (keywords) ALTAMENTE ESPECÍFICOS para encontrar este item exato no Mercado Livre.
        
        {context_str}

        Regras:
        1. Identifique Marca e Modelo se visíveis (ex: "JBL Flip 6" em vez de "Caixa de som").
        2. Inclua características distintivas (ex: "prova d'água", "20W", "portátil").
        3. Evite termos genéricos como "qualidade", "bom", "barato".
        4. O primeiro termo deve ser o mais específico possível (Marca + Modelo + Cor/Ref).
        
        Retorne APENAS um JSON válido no formato: {{"keywords": ["termo 1", "termo 2", "termo 3"]}}
        Não use formatação Markdown (```json) ou texto extra. Apenas o JSON puro.
        """

        # Geração de conteúdo (Nova SDK)
        # Usando gemini-2.0-flash experimental ou fallback para 1.5
        # Vou usar 'gemini-1.5-flash' que é estável, ou 'gemini-2.0-flash-exp' se disponível.
        # O código original usava 'gemini-flash-latest', manterei ou ajustarei para algo mais robusto.
        model_name = "gemini-2.0-flash-exp" # Tentativa de modelo mais capaz, ou fallback
        # Melhor usar um alias conhecido ou o que estava antes se funcionava
        # O código anterior usava "gemini-flash-latest". 
        
        response = client.models.generate_content(
            model="gemini-2.0-flash", # Upgrade para 2.0 Flash se disponível, ou voltar para 1.5
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
