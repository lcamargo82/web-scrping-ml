
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.report import ReportGenerator

def test_excel_generation():
    print("Testing Excel generation with images...")
    
    # Mock data with a real image URL
    mock_data = [
        {
            "Título": "Produto Teste 1",
            "Preço (R$)": 100.0,
            "Link": "http://example.com/produto1",
            "Imagem URL": "https://via.placeholder.com/150",
            "Vendedor": "Vendedor A",
            "Logística": "Normal",
            "Condição": "Novo",
            "Descrição/Atributos": "Teste",
            "Vendas (Aprox)": "100"
        },
        {
            "Título": "Produto Teste 2 (Sem Imagem)",
            "Preço (R$)": 200.0,
            "Link": "http://example.com/produto2",
            "Imagem URL": "",
            "Vendedor": "Vendedor B",
            "Logística": "Full",
            "Condição": "Usado",
            "Descrição/Atributos": "Teste 2",
            "Vendas (Aprox)": "50"
        }
    ]
    
    output_dir = "tests/output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    generator = ReportGenerator(output_dir=output_dir)
    filepath = generator.generate_excel(mock_data)
    
    if filepath and os.path.exists(filepath):
        print(f"SUCCESS: Excel file generated at {filepath}")
    else:
        print("FAILURE: Excel generation failed")

if __name__ == "__main__":
    test_excel_generation()
