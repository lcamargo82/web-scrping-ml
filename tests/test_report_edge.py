
import os
import pandas as pd
import sys

# Add src to path to import ReportGenerator
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from report import ReportGenerator

def test_generate_excel_with_edge_links():
    # Setup
    output_dir = "tests/output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    generator = ReportGenerator(output_dir=output_dir)
    
    data = [
        {
            "Título": "Produto Teste",
            "Preço": 100.0,
            "Link": "https://produto.mercadolivre.com.br/MLB-123",
            "Vendas (Aprox)": 10
        }
    ]
    
    # Generate report with Edge links enabled
    filepath = generator.generate_excel(data, use_edge_browser=True)
    
    assert filepath is not None
    assert os.path.exists(filepath)
    
    print(f"Relatório gerado em: {filepath}")
    print("Verificação automática do conteúdo do link (requer inspeção manual ou biblioteca complexa para ler hyperlinks)")
    print("Para verificar, abra o arquivo e passe o mouse sobre o link. Deve começar com 'microsoft-edge:'.")

if __name__ == "__main__":
    test_generate_excel_with_edge_links()
