
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
            df.loc[:, "Vendas (Aprox)"] = pd.to_numeric(df["Vendas (Aprox)"], errors='coerce').fillna(0)
            df = df.sort_values(by="Vendas (Aprox)", ascending=False)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"relatorio_mercado_livre_{timestamp}.xlsx"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            # Usando xlsxwriter para melhor suporte a imagens
            with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name="Resultados")
                workbook = writer.book
                worksheet = writer.sheets["Resultados"]

                # Formatação básica
                format_center = workbook.add_format({'valign': 'vcenter', 'align': 'center'})
                format_currency = workbook.add_format({'num_format': 'R$ #,##0.00'})
                
                # Ajustar largura das colunas e formatar
                worksheet.set_column('A:Z', 20, format_center) 
                
                # Encontrar índice da coluna 'Imagem URL' e 'Imagem'
                img_url_col_idx = df.columns.get_loc("Imagem URL") if "Imagem URL" in df.columns else -1
                
                # Adicionar coluna para a imagem visual se não existir (apenas para referência visual)
                # No pandas já escrevemos "Imagem URL", vamos adicionar imagens na coluna ao lado ou na mesma
                
                if img_url_col_idx != -1:
                    print("Baixando e inserindo imagens no Excel...")
                    # Aumentar altura das linhas para caber a imagem
                    worksheet.set_default_row(100)  # Altura em pixels (aprox)
                    worksheet.set_column(img_url_col_idx, img_url_col_idx, 30) # Largura da coluna de imagem

                    import requests
                    from io import BytesIO

                    for idx, row in df.iterrows():
                        img_url = row.get("Imagem URL")
                        if img_url:
                            try:
                                response = requests.get(img_url, timeout=5)
                                if response.status_code == 200:
                                    image_data = BytesIO(response.content)
                                    # Inserir imagem na célula
                                    # row + 1 (pois header é row 0)
                                    worksheet.insert_image(idx + 1, img_url_col_idx, img_url, {
                                        'image_data': image_data,
                                        'x_scale': 0.5, 'y_scale': 0.5,
                                        'object_position': 1
                                    })
                            except Exception as e:
                                print(f"Erro ao baixar imagem {img_url}: {e}")

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
