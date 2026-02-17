# Guia de Deploy - Streamlit Cloud

Este guia explica como colocar seu "Garimpo ML com IA" online usando a plataforma gratuita **Streamlit Community Cloud**.

## 1. Preparação (Importante!)

Antes de fazer o deploy, certifique-se de que seu projeto está no GitHub.

1.  **requirements.txt**: Já está atualizado com todas as dependências necessárias.
2.  **API Key**: Você precisará da sua `GEMINI_API_KEY`. Não a publique no GitHub!

## 2. Subir para o GitHub

Se ainda não fez:

1.  Crie um repositório no [GitHub](https://github.com/new).
2.  No terminal do seu projeto:
    ```bash
    git init
    git add .
    git commit -m "Upload inicial"
    git branch -M main
    git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPO.git
    git push -u origin main
    ```

## 3. Configurar no Streamlit Cloud

1.  Acesse [share.streamlit.io](https://share.streamlit.io/) e faça login (com sua conta GitHub).
2.  Clique em **"New app"**.
3.  Preencha os campos:
    *   **Repository**: Selecione o repositório que você acabou de criar.
    *   **Branch**: `main`
    *   **Main file path**: `src/app.py` (Importante: a pasta é `src`!)
4.  **NÃO CLIQUE EM DEPLOY AINDA!** Clique em **"Advanced settings"**.

### Configurando a Chave de API (Segredos)

No menu "Advanced settings", vá para a seção **"Secrets"**.
Cole o seguinte conteúdo (usando sua chave real):

```toml
GEMINI_API_KEY = "SUA_CHAVE_AQUI_XZY_123"
```

*Isso garante que sua chave funcione na nuvem sem precisar estar no código público.*

## 4. Finalizar

1.  Clique em **"Save"** nos segredos.
2.  Agora clique em **"Deploy!"**.

O Streamlit vai instalar as dependências e iniciar o app. Isso pode levar alguns minutos na primeira vez.

## Solução de Problemas Comuns

*   **Erro de "ModuleNotFoundError"**: Verifique se o `requirements.txt` está na raiz do repositório.
*   **Erro de API Key**: Verifique se a chave foi colada corretamente nos "Secrets" e não tem aspas extras incorretas.
*   **Erro de Caminho**: Se o app não abrir, verifique se o "Main file path" está apontando corretamente para `src/app.py`.
