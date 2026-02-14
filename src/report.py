
import pandas as pd
import os
from datetime import datetime

class ReportGenerator:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_excel(self, data):
        """
        Gera um arquivo Excel com os dados dos produtos.
        data: Lista de dicionários
        """
        if not data:
            print("Nenhum dado para gerar relatório.")
            return None

        df = pd.DataFrame(data)
        
        # Ordenar por vendas (se possível) ou preço
        if "Vendas (Aprox)" in df.columns:
            # Converter para numérico forçando erros a NaN e depois 0
            df["Vendas (Aprox)"] = pd.to_numeric(df["Vendas (Aprox)"], errors='coerce').fillna(0)
            df = df.sort_values(by="Vendas (Aprox)", ascending=False)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"relatorio_mercado_livre_{timestamp}.xlsx"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            # Usando ExcelWriter para formatação básica (links)
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name="Resultados")
                # Aqui poderia adicionar formatação extra se necessário
                
            print(f"Relatório gerado com sucesso: {filepath}")
            return filepath
        except Exception as e:
            print(f"Erro ao gerar Excel: {e}")
            return None

if __name__ == "__main__":
    # Teste
    gen = ReportGenerator(output_dir="../../output") # Ajuste path relativo para teste
    mock_data = [{"Título": "Teste", "Preço": 100, "Link": "http://google.com"}]
    gen.generate_excel(mock_data)
