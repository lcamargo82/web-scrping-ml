
import os
import json
import PIL.Image
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

        # Carregar imagem com PIL
        try:
            image = PIL.Image.open(image_path)
        except Exception as e:
            print(f"Erro ao abrir imagem com PIL: {e}")
            return []
        
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

        # Descoberta dinâmica de modelos (para evitar erros de nome/versão)
        chosen_model = None
        
        try:
            print("Buscando modelos disponíveis na conta...")
            available_models = list(client.models.list())
            
            # Prioridade: Procurar por modelos "flash" (mais rápidos/baratos)
            # Ordenar para pegar versões mais recentes ou estáveis se possível
            # Ex: gemini-1.5-flash, gemini-2.0-flash, etc.
            
            flash_models = [m.name for m in available_models if "flash" in m.name.lower() and "gemini" in m.name.lower()]
            other_gemini = [m.name for m in available_models if "gemini" in m.name.lower() and m.name not in flash_models]
            
            # Tentar Flash primeiro, depois outros
            candidate_models = flash_models + other_gemini
            
            if not candidate_models:
                # Fallback hardcoded se a listagem falhar ou não retornar nada útil
                candidate_models = ["gemini-1.5-flash", "gemini-2.0-flash-exp", "gemini-pro-vision"]
            
            print(f"Candidatos encontrados: {candidate_models}")

            response = None
            last_error = None

            for model_name in candidate_models:
                # Pular modelos de audio-only se houver (o nome geralmente indica)
                if "audio" in model_name.lower() and "speech" not in model_name.lower(): 
                   # Alguns modelos 2.5 flash native audio podem não aceitar texto/imagem genérico, mas vamos tentar se for o único
                   pass

                print(f"Tentando usar modelo: {model_name}...")
                try:
                    response = client.models.generate_content(
                        model=model_name, 
                        contents=[image, prompt]
                    )
                    print(f"Sucesso com modelo: {model_name}")
                    chosen_model = model_name
                    break 
                except Exception as e:
                    print(f"Falha ao usar modelo {model_name}: {e}")
                    last_error = e
            
            if not response:
                print(f"Todos os modelos falharam. Último erro: {last_error}")
                return []

        except Exception as e:
            print(f"Erro na descoberta/uso de modelos: {e}")
            return []

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
