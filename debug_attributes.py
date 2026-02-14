
import requests
from bs4 import BeautifulSoup

def debug_attributes():
    url = "https://lista.mercadolivre.com.br/caixa-de-som-bluetooth"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.mercadolivre.com.br/",
    }
    
    print(f"Scraping {url}...")
    session = requests.Session()
    session.headers.update(headers)
    session.get("https://www.mercadolivre.com.br/") # Cookies
    response = session.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('li', class_='ui-search-layout__item', limit=1)
    
    if not items:
        items = soup.find_all('div', class_='poly-card', limit=1)

    with open("debug_attrs_utf8.txt", "w", encoding="utf-8") as f:
        if items:
            item = items[0]
            f.write("--- ITEM HTML START ---\n")
            f.write(item.prettify()[:5000])  # Limit size
            f.write("\n--- ITEM HTML END ---\n")
            
            # Tentativa de achar atributos
            attrs = item.find_all('li', class_='ui-search-card-attributes__attribute')
            if attrs:
                f.write("\nFOUND ATTRIBUTES (ui-search-card-attributes__attribute):\n")
                for li in attrs:
                    f.write(f"- {li.get_text().strip()}\n")
            
            poly_attrs = item.find('ul', class_='poly-component__attributes-list')
            if poly_attrs:
                f.write("\nFOUND ATTRIBUTES (poly-component__attributes-list):\n")
                for li in poly_attrs.find_all('li'):
                    f.write(f"- {li.get_text().strip()}\n")
        else:
            f.write("No items found.")

if __name__ == "__main__":
    debug_attributes()
