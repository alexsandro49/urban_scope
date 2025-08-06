# 📊 Urban Scope

**Urban Scope** é um projeto exemplo de uma aplicação web desenvolvida com HTML, CSS, Django e Postgres.
O objetivo é demonstrar boas práticas na criação de interfaces modernas e reativas para visualização e exploração de dados geográficos e empresariais, incluindo informações sobre distritos, municípios, estados e empresas.

---

## 📸 Preview

![Imagem da tela de login](https://github.com/alexsandro49/urban_scope/blob/main/screenshot-1.png)
![Imagem da tela de registro](https://github.com/alexsandro49/urban_scope/blob/main/screenshot-2.png)
![Imagem do projeto em execução](https://github.com/alexsandro49/urban_scope/blob/main/screenshot-3.png)

---

## 🚀 Tecnologias utilizadas
### Front-end:
- [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)
### Back-end:
- [Python](https://www.python.org)
- [Django](https://www.djangoproject.com)
- [Postgres](https://www.postgresql.org)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## 🧱 Funcionalidades

- Listagem de estados, municípios e distritos
- Exibição de dados detalhados sobre cada localidade
- Consulta paginada
- Suporte a filtros
- Design responsivo e adaptado para diferentes dispositivos

---

## 📁 Estrutura de Pastas
```
├── assets/            # Imagens e arquivos de mídia do projeto
├── companies/         # App responsável pelos dados de empresas
├── districts/         # App responsável pelos dados dos distritos
├── municipalities/    # App responsável pelos dados dos municípios
├── scripts/           # Scripts utilitários
├── states/            # App responsável pelos dados dos Estados
├── static/            # Arquivos estáticos
├── templates/         # Templates HTML utilizados nas views do projeto
├── urban_scope/       # Diretório principal do projeto Django 
├── Empresas0.zip      # Arquivo com os dados da tabela de empresas
├── manage.py          # Script de gerenciamento principal do Django
```

## Como executar o projeto:
1. Clone o repositório na sua máquina:
   ```
   git clone https://github.com/alexsandro49/urban_scope.git
   ```
2. Entre na pasta do repositório:
   ```
   cd urban_scope/
   ```
3. Prepare as variáveis de ambiente:
   ```
   cp ./.env.example ./.env   ```
4. Para a exibição dos dados das empresas, é necessario adicionar este arquivo na raiz do projeto.
   ```
   https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/2025-05/Empresas0.zip
   ```
5. Execute o projeto utilizando o docker compose:
   ```
   docker compose up -d
   ```
6. Aplique as migrações no banco de dados:
   ```
   docker compose exec django-web python manage.py migrate
   ```
7. Execute os scripts para carregar os dados no banco.

## Como executar os scripts:
1. Script para carregar os dados geográficos:
   ```
   docker compose exec django-web python manage.py runscript fetch_with_api
   ```
2. Script para carregar os dados das empresas:
   ```
   docker compose exec django-web python manage.py runscript fetch_with_csv
   ```
3. Script para carregar os dados das empresas (com parâmetro):
   ```
   docker compose exec django-web python manage.py runscript fetch_with_csv --script-args --batch-size=value
   ```

#### A execução do segundo script é consideravelmente pesada, visto a quantidade de dados que é processada (~1GB), por padrão o algoritmo processa o arquivo em pedaços de 100k, utilize o parâmetro opcional para indicar valores menores, para contornar possíveis travamentos durante a execução.

#### O projeto estará disponível em http://localhost:8000/

## 🖥️ Hardware de teste
O projeto foi desenvolvido e testado no seguinte ambiente:
- **Processador:** AMD Ryzen 5 7535HS (6 núcleos, 12 threads)
- **Memória RAM:** 16 GB DDR5
- **Armazenamento:** SSD NVMe 500 GB
- **Sistema Operacional:** Ubuntu 24.04 LTS
- **Docker:** 28.3.3
- **Python:** 3.13.5
- **PostgreSQL:** 17.5

## 📈 Resultados
Durante os testes:
- **Carregamento de dados geográficos (API IBGE):** ~2 minutos.
- **Carregamento de dados das empresas (~1GB, batch 100k):** ~6 minutos.

## Referências
- [Django documentation](https://docs.djangoproject.com/en/5.2)
- [Python Django Full Course for Beginners](https://youtu.be/Rp5vd34d-z4?si=RzjbkEAGPIgKrzMx)
- [API de localidades - IBGE](https://servicodados.ibge.gov.br/api/docs/localidades)
- [Cadastro Nacional da Pessoa Jurídica - CNPJ](https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/2025-05/)
- [Dicionário de Dados do Cadastro Nacional da Pessoa Jurídica](https://www.gov.br/receitafederal/dados/cnpj-metadados.pdf)
- [Fact icons created by Freepik - Flaticon](https://www.flaticon.com/free-icons/fact)

## License
- [MIT](https://github.com/alexsandro49/pizz-app/blob/main/LICENSE)