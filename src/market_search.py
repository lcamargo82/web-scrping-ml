
import requests
from bs4 import BeautifulSoup
import re

def search_mercadolibre(query, limit=10):
    """
    Busca produtos no Mercado Livre via Web Scraping (HTML).
    Contorna limitações da API pública.
    """
    # Formata a query para URL (ex: "caixa de som" -> "caixa-de-som")
    formatted_query = query.replace(" ", "-")
    url = f"https://lista.mercadolivre.com.br/{formatted_query}"
    
    # Headers de navegador real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        # "Accept-Encoding": "gzip, deflate, br", # Removido para evitar problemas de compressão não tratada
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.mercadolivre.com.br/",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Connection": "keep-alive"
    }

    print(f"    (Scraping: {url})")
    
    try:
        session = requests.Session()
        session.headers.update(headers)
        
        # Visita a home primeiro para pegar cookies
        print("    (Visitando home page para cookies...)")
        session.get("https://www.mercadolivre.com.br/")

        response = session.get(url)
        response.raise_for_status()
        
        # Debug: Salvar HTML para análise
        # with open("debug_last_search.html", "w", encoding="utf-8") as f:
        #     f.write(response.text)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tenta encontrar os cards de produtos
        results = soup.find_all('li', class_='ui-search-layout__item', limit=limit)
        
        # Fallback para div que agrupa items no layout novo "Poly" (grid)
        if not results:
             results = soup.find_all('div', class_='poly-card', limit=limit)
        
        print(f"    (Items encontrados no HTML: {len(results)})")

        products = []
        for item in results:
            try:
                # TÍTULO & LINK
                title_tag = item.find('a', class_='poly-component__title') or \
                            item.find('h2', class_='ui-search-item__title') or \
                            item.find('a', class_='ui-search-item__group__element ui-search-link__title-card')
                
                if title_tag:
                    title = title_tag.get_text().strip()
                    link = title_tag['href']
                else:
                    title = "Título não encontrado"
                    link = ""
                
                # PREÇO
                price_container = item.find('div', class_='ui-search-price__second-line') or \
                                  item.find('div', class_='poly-price__current') or \
                                  item.find('div', class_='ui-search-price__second-line') # Fallback
                
                price = 0.0
                if price_container:
                    price_fraction = price_container.find('span', class_='andes-money-amount__fraction')
                    if price_fraction:
                        price_text = price_fraction.get_text().strip()
                        clean_price = price_text.replace('.', '').replace(',', '.')
                        try:
                            price = float(clean_price)
                        except ValueError:
                             price = 0.0

                # VENDEDOR
                seller = "N/A (Via Scraping)"

                # LOGÍSTICA (Full, Flex, Normal)
                logistics_types = []
                
                # 1. Tenta identificar FULL explicitamente (Label ou Texto)
                full_label = item.find('span', class_='ui-search-item__fulfillment-label')
                shipping_tag = item.find('span', class_='poly-component__shipping') or \
                               item.find('div', class_='poly-component__shipping')
                
                shipping_text = shipping_tag.get_text().strip().lower() if shipping_tag else ""
                
                if full_label or "full" in shipping_text:
                    logistics_types.append("Full")
                
                # 2. Tenta identificar FLEX
                if "chegará hoje" in shipping_text or "chegará amanhã" in shipping_text or "flex" in shipping_text:
                    logistics_types.append("Flex")

                # Se não for Full nem Flex, assume Normal se houver info de envio, ou deixa vazio/Normal
                if not logistics_types:
                    logistics_types.append("Normal")
                
                logistics = ", ".join(logistics_types)

                # CONDIÇÃO (Novo/Recondicionado)
                condition_tag = item.find('span', class_='poly-component__item-condition')
                condition = condition_tag.get_text().strip() if condition_tag else "Novo"

                # ATRIBUTOS (Tentativa de extração)
                attributes = []
                # Tenta achar lista de atributos (comum em list view, raro em grid)
                attr_list = item.find('ul', class_='ui-search-card-attributes') or \
                            item.find('ul', class_='poly-component__attributes-list')
                
                if attr_list:
                    for li in attr_list.find_all('li'):
                        attributes.append(li.get_text().strip())
                
                description = ", ".join(attributes) if attributes else ""

                # IMAGEM (Extração da URL)
                image_url = ""
                image_tag = item.find('img', class_='ui-search-result-image__element') or \
                            item.find('img', class_='poly-component__picture')
                
                if image_tag:
                    # Tenta pegar 'data-src' (lazy load) ou 'src'
                    image_url = image_tag.get('data-src') or image_tag.get('src') or ""

                products.append({
                    "Termo de Busca": query,
                    "Título": title,
                    "Preço (R$)": price,
                    "Link": link,
                    "Vendedor": seller, 
                    "Logística": logistics,
                    "Condição": condition,
                    "Descrição/Atributos": description,
                    "Vendas (Aprox)": "Ver no Site",
                    "Imagem URL": image_url,
                    "ID": "N/A"
                })
            
            except Exception as e:
                # Se falhar em um item, ignora
                with open("scraping_errors.log", "a", encoding="utf-8") as err_file:
                    err_file.write(f"Item Error: {e}\n")
                    import traceback
                    err_file.write(traceback.format_exc() + "\n")
                print(f"    [DEBUG] Erro gravado em log.")
                continue
                
        return products

    except Exception as e:
        print(f"Erro no scraping para '{query}': {e}")
        return []

if __name__ == "__main__":
    import json
    # Teste rápido com termo problemático
    query = "Lâmpada LED Bluetooth Altonex WJ-L2 RGB Som"
    print(f"Testando busca por: '{query}'")
    res = search_mercadolibre(query, limit=10)
    
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("Resultados salvos em results.json")
