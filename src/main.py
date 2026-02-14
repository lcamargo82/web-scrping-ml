
import os
import glob
import time
from colorama import init, Fore, Style
from analysis_ai import analyze_image
from market_search import search_mercadolibre
from report import ReportGenerator

from data_processing import DataProcessor, ConditionFilter, NegativeKeywordFilter, LogisticsFilter

# Inicializa colorama para cores no terminal Windows
init(autoreset=True)

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def main():
    print(Fore.CYAN + "=== Ferramenta de Análise de Mercado Livre ===")
    print(Fore.CYAN + "===     Garimpo de Produtos com IA     ===")
    print("-" * 50)

    # 1. Configurar Processador de Dados (Filtros)
    processor = DataProcessor()
    # Exemplo: Filtrar apenas produtos novos para ter base de preço de revenda
    processor.add_filter(ConditionFilter("Novo"))
    # Exemplo: Remover acessórios que poluem a busca de eletrônicos
    processor.add_filter(NegativeKeywordFilter(["capa", "capinha", "película", "vidro", "suporte", "cabo"]))

    # 1. Verificar imagens
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.webp']
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(INPUT_DIR, ext)))
    
    if not image_files:
        print(Fore.YELLOW + f"Nenhuma imagem encontrada na pasta '{INPUT_DIR}'.")
        print("Adicione imagens de produtos lá e execute novamente.")
        return

    print(f"Encontradas {len(image_files)} imagens para processar.")
    
    all_products = []

    # 2. Processar cada imagem
    for img_path in image_files:
        filename = os.path.basename(img_path)
        print(f"\n{Fore.GREEN}Processando: {filename}...")
        
        # A. Análise de IA
        print("  > Analisando imagem com IA...")
        keywords = analyze_image(img_path)
        
        if not keywords:
            print(Fore.RED + "  > Falha ao gerar palavras-chave.")
            continue
            
        print(f"  > Palavras-chave geradas: {Fore.YELLOW}{', '.join(keywords)}")
        
        # B. Busca no Mercado Livre e Processamento
        for term in keywords:
            print(f"  > Buscando no ML por: '{term}'...")
            raw_results = search_mercadolibre(term, limit=10)
            
            # C. Filtragem e Processamento (SOLID)
            cleaned_results = processor.process(raw_results)
            print(f"    (Filtrado: {len(raw_results)} -> {len(cleaned_results)} produtos relevantes)")
            
            # Adicionar coluna da imagem de origem
            for item in cleaned_results:
                item["Imagem Origem"] = filename
                
            all_products.extend(cleaned_results)
            time.sleep(0.5) 
            
    # 3. Gerar Relatório
    if all_products:
        print(f"\n{Fore.GREEN}Processamento concluído! Consolidando {len(all_products)} resultados...")
        generator = ReportGenerator(output_dir=OUTPUT_DIR)
        filepath = generator.generate_excel(all_products)
        
        if filepath:
            print(f"{Fore.CYAN}Planilha salva em: {filepath}")
            # Tentar abrir a pasta (Windows)
            os.startfile(OUTPUT_DIR)
    else:
        print(Fore.RED + "\nNenhum produto encontrado ou erro no processamento.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")
    except Exception as e:
        print(f"\nErro fatal: {e}")
    
    input("\nPressione ENTER para sair...")
