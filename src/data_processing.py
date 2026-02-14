
from typing import List, Dict, Callable
import pandas as pd

class FilterStrategy:
    """Class base (interface implícita) para estratégias de filtro."""
    def apply(self, data: List[Dict]) -> List[Dict]:
        raise NotImplementedError

class ConditionFilter(FilterStrategy):
    """Filtra produtos com base na condição (ex: apenas 'Novo')."""
    def __init__(self, condition: str = "Novo"):
        self.condition = condition.lower()

    def apply(self, data: List[Dict]) -> List[Dict]:
        # Normaliza a condição para comparação
        return [
            item for item in data 
            if self.condition in item.get("Condição", "").lower()
        ]

class NegativeKeywordFilter(FilterStrategy):
    """Remove produtos que contenham palavras indesejadas no título."""
    def __init__(self, keywords: List[str]):
        self.keywords = [k.lower() for k in keywords]

    def apply(self, data: List[Dict]) -> List[Dict]:
        filtered_data = []
        for item in data:
            title = item.get("Título", "").lower()
            if not any(k in title for k in self.keywords):
                filtered_data.append(item)
        return filtered_data

class LogisticsFilter(FilterStrategy):
    """Filtra produtos por tipo de logística (Ex: 'Full', 'Flex', 'Normal')."""
    def __init__(self, logistics_types: List[str]):
        # Normaliza para lowercase
        self.target_types = [t.lower() for t in logistics_types]

    def apply(self, data: List[Dict]) -> List[Dict]:
        if not self.target_types:
            return data
            
        return [
            item for item in data 
            if item.get("Logística", "").lower() in self.target_types
        ]

class DataProcessor:
    """
    Responsável por processar e limpar os dados brutos do scraping.
    Segue o princípio Open/Closed permitindo adicionar filtros dinamicamente.
    """
    def __init__(self):
        self.filters: List[FilterStrategy] = []

    def add_filter(self, filter_strategy: FilterStrategy):
        self.filters.append(filter_strategy)

    def process(self, raw_data: List[Dict]) -> List[Dict]:
        if not raw_data:
            return []
        
        processed_data = raw_data
        for filter_strategy in self.filters:
            processed_data = filter_strategy.apply(processed_data)
        
        return processed_data

    @staticmethod
    def to_dataframe(data: List[Dict]) -> pd.DataFrame:
        if not data:
            return pd.DataFrame()
        return pd.DataFrame(data)

if __name__ == "__main__":
    # Teste simples
    mock_data = [
        {"Título": "iPhone 15 Novo", "Condição": "Novo"},
        {"Título": "iPhone 15 Usado (Quebrado)", "Condição": "Usado"},
        {"Título": "Capa para iPhone 15", "Condição": "Novo"}
    ]
    
    processor = DataProcessor()
    processor.add_filter(ConditionFilter("Novo"))
    processor.add_filter(NegativeKeywordFilter(["capa", "vidro", "película"]))
    
    result = processor.process(mock_data)
    print(f"Entrada: {len(mock_data)} -> Saída: {len(result)}")
    print(result)
