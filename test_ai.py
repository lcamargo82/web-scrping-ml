
from src.analysis_ai import analyze_image
import os
import glob

def test():
    files = glob.glob("input/*.png")
    if not files:
        print("Imagem não encontrada em input/")
        return

    img_path = files[0]
    print(f"Analisando imagem: {img_path}")
    keywords = analyze_image(img_path)
    print("\nKeywords Geradas:")
    print(keywords)

if __name__ == "__main__":
    test()
