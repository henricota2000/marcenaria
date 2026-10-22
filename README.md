# Marcenaria Project

This is a web application built using the Django framework for the UNIVESP Integrator Project (Marcenaria Nunes).

## Project Structure

- `prime/`: App principal com views, models e templates.
- `setup/`: Configurações globais do projeto Django (settings, urls, wsgi, etc.).
- `venv/`: Ambiente virtual Python.
- `manage.py`: Utilitário de linha de comando do Django.
- `requirements.txt`: Lista de dependências do projeto.

## Requirements

- Python 3.8 or higher
- Django 6.1.2 (or compatible version listed in requirements.txt)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/henricota2000/marcenaria
    cd marcenaria
    ```
    
2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
 
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Project

1. Apply migrations:
    ```bash
    python manage.py migrate
    ```

2. Run the development server:
    ```bash
    python manage.py runserver
    ```

3. Open your browser and navigate to:
    *http://127.0.0.1:8000/*