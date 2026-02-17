# Web Scraping ML Project

Project for web scraping using Machine Learning tools.

## Setup

1.  Clone the repository.
2.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configure environment variables:
    *   Copy `.env.example` to `.env`.
    *   Fill in the necessary API keys (OpenAI, Google Gemini, etc.).

## Usage

To run the CLI version:
```bash
python src/main.py
```

To run the Web App (Streamlit):
```bash
streamlit run src/app.py
```

## Structure

*   `src`: Source code.
*   `input`: Input files (PDFs, etc.).
*   `output`: Generated files.
