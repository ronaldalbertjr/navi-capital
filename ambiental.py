import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as ex



### abrir dataframes desejados
df_companies = pd.read_csv("datasets/companies_br.csv")
df_companies_financials = pd.read_csv("datasets/companies_financials_br.csv")
esg_scores = pd.read_csv("datasets/esg_scores_history_br.csv")
env_data = pd.read_csv("datasets/environmental_data_history_br.csv")

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

def select_env_company():
    dict_nomes = {}
    for i in env_data['company_id'].unique():
        if i in df_companies['company_id'].unique():
            dict_nomes[df_companies[df_companies['company_id']==i]['company_name'].values[0]] = i
    
    company = st.sidebar.selectbox("Escolha uma empresa:",
            dict_nomes.keys()
            )

    #return df_companies[df_companies['company_id']==company].company_id.values[0] ,company

    return company, dict_nomes[company]

def select_envdata_item(company_id):
    data_item = st.sidebar.selectbox("Escolha um Indicador",
            env_data['data_item_name'].unique()
            )

    data_item2 = st.sidebar.selectbox("Escolha um segundo Indicador ambiental",
            env_data['data_item_name'].unique()
            )
    return data_item, data_item2

def get_env_by_year(company_id, data_item):    
    return_df =  env_data[(env_data['data_item_name'] == data_item) & (env_data['company_id']==company_id)]

    return return_df

def generate_env_graph(fin_df):
    # fig = go.Figure(data = go.Scatter(x=fin_df['fiscal_year'], y=fin_df['data_item_value']))
    # fig.update_layout(text = f"{fin_df['unit'].iloc[0]} por ano")
    # fig.update_xaxes(nticks = len(fin_df['fiscal_year'].values))

    fig = ex.line(x=fin_df['fiscal_year'], y=fin_df['data_item_value'], title = f"{fin_df['unit'].iloc[0]} por ano",
    labels = {'x': 'Year', 'y': f"Value, in {fin_df['unit'].iloc[0]}"})

    return fig

def generate_env_scatter(df1, df2, env_item, env_item2):
    fig = ex.scatter(x=df1['data_item_value'], y=df2['data_item_value'],
    title="Gráfico de dispersão dos indicadores escolhidos",
    labels = {'x': f"{env_item}",'y': f"{env_item2}"})

    return fig


def app ():
    
    st.write("""
        Ferramenta para ajudar investidores a avaliar a pontuação ESG de empresas
        """
)
    #select_industry = select_industry()

    cp, cp_env_id = select_env_company()

    st.write("""# Empresa escolhida: {}""".format(cp))

    env_item, env_item2 = select_envdata_item(cp_env_id)

    df_1 = get_env_by_year(cp_env_id, env_item)
    df_2 = get_env_by_year(cp_env_id, env_item2)
    figg1 = generate_env_graph(df_1)
    figg2 = generate_env_graph(df_2)
    figg3 = generate_env_scatter(df_1, df_2, env_item, env_item2)
    st.plotly_chart(figg1)
    st.plotly_chart(figg2)
    st.plotly_chart(figg3)
