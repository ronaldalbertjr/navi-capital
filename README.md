# Navi Tech Journey
Repósitorio para a competição da Navi Tech Journey

# Antes de executar o aplicativo
Antes de executar a nossa solução para o Hackaton, é necessário executar todas as dependências do python necessárias para a execução.<br>
Elas estão disponiveis em [requirements.txt](requirements.txt), e podem ser instaladas por meio do comando:
```
pip install -r requirements.txt
```

Além disso, também foi construido um script batch de setup, <b>os qual deve ser executado dentro da pasta do repositório.</b>.<br>
Os scripts de batch são
```
setup.bat, para Windows
setup.sh, para Linux
```
Basicamente, os scripts de batch criam uma pasta datasets dentro do repositório, e fazem download dos seguintes datasets, presentes na AWS para dentro da pasta
```
companies_br.csv
companies_financials_br.csv
esg_scores_history_br.csv
environmental_data_history_br.csv
```

# Executando o aplicativo
Para executar o aplicativo, basta estar no diretório do repositório e executar o comando
```
streamlit run app.py
```
O aplicativo será executado no servidor local na porta 8501, e pode ser acessado em algum browser por meio da url
```
http://localhost:8501/
```
