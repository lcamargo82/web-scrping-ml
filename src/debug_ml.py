
import requests

def test_search():
    url = "https://api.mercadolibre.com/sites/MLB/search"
    query = "iphone"
    
    # Teste 1: Sem headers (padrão requests)
    print("Teste 1: Sem headers...")
    try:
        r = requests.get(url, params={"q": query})
        print(f"Status: {r.status_code}")
    except Exception as e:
        print(f"Erro: {e}")

    # Teste 2: User-Agent simples
    print("\nTeste 2: User-Agent simples...")
    headers2 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        r = requests.get(url, params={"q": query}, headers=headers2)
        print(f"Status: {r.status_code}")
    except Exception as e:
        print(f"Erro: {e}")

    # Teste 3: Headers Completos
    print("\nTeste 3: Headers Completos...")
    headers3 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.mercadolivre.com.br/",
        "Connection": "keep-alive"
    }
    try:
        r = requests.get(url, params={"q": query, "limit": 1}, headers=headers3)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            print("SUCESSO!")
    except Exception as e:
        print(f"Erro: {e}")

    # Teste 4: Parâmetros Mínimos
    print("\nTeste 4: Parâmetros Mínimos...")
    headers4 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        # Removendo condition, status, limit
        r = requests.get(url, params={"q": query}, headers=headers4)
        print(f"Status: {r.status_code}")
    except Exception as e:
        print(f"Erro: {e}")

    # Teste 5: Mobile Headers
    print("\nTeste 5: Mobile Headers...")
    headers5 = {
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; Pixel 3 Build/QQ3A.200805.001)',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'Keep-Alive'
    }
    try:
        r = requests.get(url, params={"q": query}, headers=headers5)
        print(f"Status: {r.status_code}")
    except Exception as e:
        print(f"Erro: {e}")

    # Teste 6: Endpoint Categorias (Public)
    print("\nTeste 6: Categorias (Check de IP)...")
    try:
        r = requests.get("https://api.mercadolibre.com/sites/MLB/categories")
        print(f"Status: {r.status_code}")
    except Exception as e:
        print(f"Erro: {e}")

    # Teste 7: HTML Scraping (Fallback)
    print("\nTeste 7: HTML da Busca...")
    try:
        r = requests.get(f"https://lista.mercadolivre.com.br/{query}", headers=headers2)
        print(f"Status: {r.status_code}")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    test_search()
