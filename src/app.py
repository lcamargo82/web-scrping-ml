
import os
import streamlit as st
import tempfile
import pandas as pd
from dotenv import load_dotenv
from analysis_ai import analyze_image
from market_search import search_mercadolibre
from report import ReportGenerator
from data_processing import DataProcessor, ConditionFilter, NegativeKeywordFilter

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Garimpo ML com IA",
    page_icon="🛍️",
    layout="wide"
)

def main():
    st.title("🛍️ Garimpo Mercado Livre com IA")
    st.markdown("Use Inteligência Artificial para identificar produtos e encontrar oportunidades no Mercado Livre.")

    # Sidebar para configurações
    st.sidebar.header("Configurações")
    
    # Verificação da API Key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.sidebar.error("⚠️ GEMINI_API_KEY não encontrada no .env")
        st.sidebar.info("Adicione sua chave API no arquivo .env para continuar.")
        return

    # Filtros
    st.sidebar.subheader("Filtros de Busca")
    condition = st.sidebar.selectbox("Condição do Produto", ["Novo", "Usado", "Qualquer"], index=0)
    
    excluded_keywords = st.sidebar.text_area(
        "Palavras-chave Negativas (separadas por vírgula)", 
        "capa, capinha, película, vidro, suporte, cabo",
        help="Produtos contendo estas palavras serão removidos dos resultados."
    )

    # Configuração de Exportação
    st.sidebar.subheader("Opções de Exportação")
    use_edge = st.sidebar.checkbox(
        "Abrir links no Microsoft Edge", 
        value=True, 
        help="Força os links da planilha a abrirem no navegador Edge (Windows)."
    )

    # Área principal
    uploaded_file = st.file_uploader("Envie a imagem do produto", type=['jpg', 'jpeg', 'png', 'webp'])
    
    # Campo para descrição do fornecedor
    user_description = st.text_area(
        "Descrição/Contexto do Produto (Recomendado)",
        placeholder="Cole aqui a descrição do catálogo do fornecedor ou detalhes como marca, modelo e cor para ajudar a IA.",
        help="Quanto mais detalhes você fornecer, melhor será a identificação do produto."
    )

    if uploaded_file is not None:
        # Mostrar imagem preview
        st.image(uploaded_file, caption="Imagem do Produto", width=300)
        
        if st.button("🔍 Analisar e Buscar"):
            with st.spinner('Analisando imagem com IA...'):
                try:
                    # Salvar arquivo temporário para passar para a função analyze_image
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name

                    # 1. Análise de IA (com contexto)
                    keywords = analyze_image(tmp_path, user_context=user_description)
                    
                    # Remover arquivo temporário
                    os.unlink(tmp_path)

                    if not keywords:
                        st.error("Não foi possível identificar o produto na imagem.")
                        return

                    st.success(f"Palavras-chave identificadas: {', '.join(keywords)}")

                    # 2. Busca e Processamento
                    progress_text = "Buscando produtos no Mercado Livre..."
                    my_bar = st.progress(0, text=progress_text)
                    
                    all_products = []
                    processor = DataProcessor()
                    
                    if condition != "Qualquer":
                        processor.add_filter(ConditionFilter(condition))
                    
                    if excluded_keywords:
                        neg_keywords_list = [k.strip() for k in excluded_keywords.split(',') if k.strip()]
                        processor.add_filter(NegativeKeywordFilter(neg_keywords_list))

                    total_keywords = len(keywords)
                    for i, term in enumerate(keywords):
                        my_bar.progress((i / total_keywords), text=f"Buscando por: {term}")
                        
                        raw_results = search_mercadolibre(term, limit=10)
                        cleaned_results = processor.process(raw_results)
                        
                        # Adicionar coluna da imagem de origem
                        for item in cleaned_results:
                            item["Imagem Origem"] = uploaded_file.name
                            
                        all_products.extend(cleaned_results)
                    
                    my_bar.progress(1.0, text="Finalizado!")
                    
                    # 3. Exibir Resultados e Gerar Relatório
                    if all_products:
                        df = pd.DataFrame(all_products)
                        
                        st.subheader(f"Resultados Encontrados ({len(df)})")
                        
                        # Exibição simplificada no Streamlit (escondendo colunas técnicas se quiser)
                        cols_to_show = ["Título", "Preço (R$)", "Condição", "Vendedor", "Logística"]
                        st.dataframe(df[cols_to_show], use_container_width=True)
                        
                        # Botão de Download
                        st.markdown("### 📥 Exportar Resultados")
                        
                        # Gerar Excel em memória ou salvar e ler
                        # Usando a classe ReportGenerator existente, mas adaptando para o Streamlit se necessário
                        # A classe ReportGenerator salva em disco. Vamos usar isso e prover o download.
                        
                        output_dir = "output"
                        if not os.path.exists(output_dir):
                            os.makedirs(output_dir)
                            
                            
                        generator = ReportGenerator(output_dir=output_dir)
                        # Gerar arquivo (com imagens)
                        with st.spinner("Gerando planilha com imagens (isso pode levar alguns segundos)..."):
                            filepath = generator.generate_excel(all_products, use_edge_browser=use_edge)
                        
                        if filepath and os.path.exists(filepath):
                            with open(filepath, "rb") as file:
                                btn = st.download_button(
                                    label="Baixar Planilha Excel (.xlsx)",
                                    data=file,
                                    file_name=os.path.basename(filepath),
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
                    else:
                        st.warning("Nenhum produto encontrado com os filtros selecionados.")

                except Exception as e:
                    st.error(f"Ocorreu um erro: {e}")
                    # st.exception(e) # Para debug

if __name__ == "__main__":
    main()
