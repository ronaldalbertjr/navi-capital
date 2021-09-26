import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
#from sklearn.linear_model import LinearRegression



### abrir dataframes desejados
df_companies = pd.read_csv("datasets/companies_br.csv")
df_companies_financials = pd.read_csv("datasets/companies_financials_br.csv")
esg_scores = pd.read_csv("datasets/esg_scores_history_br.csv")

### manipulacao dos dataframes
esg_scores = esg_scores[esg_scores.score_value != 0]
esg_scores = esg_scores.dropna()
esg_scores.drop_duplicates(subset=['assessment_year', 'company_id', 'aspect'], inplace = True)

df_companies = df_companies[df_companies.company_id.isin(esg_scores.company_id.unique())] ##ja tirou companhias repetidas


df_companies_financials['ref_year'] = pd.to_datetime(df_companies_financials.ref_date).dt.year
df_companies_financials['real_data_item_values'] = df_companies_financials['data_item_value'] * df_companies_financials.unit_value
df_companies_financials.drop_duplicates(subset=['ref_year', 'company_id', 'data_item'], inplace = True)

#### adicionando alternativa de nenhuma industria
df = df_companies.sort_values(by='industry')
industries = df['industry'].unique()
industries  = np.insert(industries, 0, 'Não dividir por indústria' ) ### ou apenas um traço como -?

def select_industry():
    industry = st.sidebar.selectbox("Escolha uma indústria:", 
               industries
        	   )
    return industry


def app ():
    
    st.write("""
        Ferramenta para ajudar investidores a avaliar a pontuação ESG de empresas
        """
)
    select_industry = select_industry()

    st.write("""# oi {}""".format(select_industry))

