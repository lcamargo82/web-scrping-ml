
import json
from src.data_processing import DataProcessor, ConditionFilter, NegativeKeywordFilter

def verify():
    # Carrega dados reais
    with open("results.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"Dados carregados: {len(data)} itens")
    
    # Recria processador do main.py
    processor = DataProcessor()
    
    # Filtro 1: Condição
    cond_filter = ConditionFilter("Novo")
    processor.add_filter(cond_filter)
    
    # Filtro 2: Keywords Negativas
    neg_filter = NegativeKeywordFilter(["capa", "capinha", "película", "vidro", "suporte", "cabo"])
    processor.add_filter(neg_filter)
    
    # Teste passo a passo
    print("\nAdicionando Filtro de Condição ('Novo')...")
    res1 = cond_filter.apply(data)
    print(f"Itens restantes: {len(res1)}")
    if len(res1) == 0 and len(data) > 0:
        print("  -> TODOS REMOVIDOS POR CONDIÇÃO")
        print(f"  Exemplo cond: '{data[0].get('Condição')}'")

    print("\nAdicionando Filtro de Keywords Negativas...")
    res2 = neg_filter.apply(res1)
    print(f"Itens restantes: {len(res2)}")
    if len(res2) == 0 and len(res1) > 0:
        print("  -> TODOS REMOVIDOS POR KEYWORDS")
        for item in res1:
            title = item.get("Título", "").lower()
            triggered = [k for k in neg_filter.keywords if k in title]
            if triggered:
                print(f"  Item '{title}' removido por: {triggered}")

if __name__ == "__main__":
    verify()
