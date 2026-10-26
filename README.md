# Desafio QA Automation

Automação de API (Parte 1) e UI (Parte 2) sobre o https://demoqa.com, com Python, Behave (BDD), Requests e Selenium.

## Pré-requisitos
- Python 3.10+
- Google Chrome (apenas para os cenários de UI)

## Instalação
```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Execução
```bash
behave                          # tudo
behave --tags=@api              # somente API
behave features/api             # idem, por caminho
HEADLESS=true behave --tags=@ui # UI sem abrir o navegador
```

## Relatório Allure
```bash
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results features
allure serve reports/allure-results
```

## Estrutura
```
api/        clients HTTP (um método por endpoint)
features/   cenários Gherkin (api/ e ui/) e steps
pages/      Page Objects (UI)
utils/      config e geração de dados (Faker)
resources/  upload.txt usado no Practice Form
```

## Parte 1 – Fluxo de API
Criar usuário → gerar token → confirmar autorização → listar livros → reservar 2 livros → detalhar usuário com os livros reservados.
Todos os steps rodam em um único cenário, compartilhando estado via `context`.
