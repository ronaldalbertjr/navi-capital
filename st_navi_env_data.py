import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as ex
from sklearn.linear_model import LinearRegression

st.write("""
        # Hackaton Navi-Capital
        Ferramenta para ajudar investidores a avaliar a pontuação ESG de empresas
        """
)
path_ = 'C:/Users/Andre/Desktop/UFRJ/analytica/navi_tech_journey/download_script'
df_companies = pd.read_csv(f"{path_}/companies_br.csv")
df_companies_financials = pd.read_csv(f"{path_}/companies_financials_br.csv")
env_data = pd.read_csv(f'{path_}/environmental_data_history_br.csv')
esg_scores = pd.read_csv(f"{path_}/esg_scores_history_br.csv")
esg_scores = esg_scores[esg_scores.score_value != 0]
esg_scores = esg_scores.dropna()
df_companies = df_companies[df_companies.company_id.isin(esg_scores.company_id.unique())]
df_companies_financials['ref_year'] = pd.to_datetime(df_companies_financials.ref_date).dt.year
df_companies_financials['real_data_item_values'] = df_companies_financials['data_item_value'] * df_companies_financials.unit_value

def select_company():
    company = st.sidebar.selectbox("Escolha uma empresa:",
            df_companies.company_name.values
            )

    return df_companies[df_companies.company_name.eq(company)].company_id.values[0] ,company

def select_data_item(company_id):
    data_item = st.sidebar.selectbox("Escolha um Indicador",
            df_companies_financials[df_companies_financials.company_id.eq(company_id)].data_item.values
            )
    return data_item

def select_esg_score(company_id):
    score = st.sidebar.selectbox("Escolha uma métrica do ESG",
            esg_scores[esg_scores.company_id.eq(company_id)].aspect.values)

    return score

def get_esg_score(company_id, esg_aspect):
    esg_score = esg_scores[esg_scores.company_id.eq(company_id) & esg_scores.aspect.eq(esg_aspect)]
    esg_score = esg_score[['assessment_year', 'score_value']]
    return esg_score

def generate_esg_graph(esg_df):
    fig = go.Figure(data = go.Scatter(x=esg_df.assessment_year.values, y=esg_df.score_value.values, line=dict(color="#ff0000")))
    fig.update_xaxes(nticks = len(esg_df.assessment_year.values))

    return fig

def get_financials_by_year(company_id, data_item):    
    return_df =  df_companies_financials[df_companies_financials.company_id.eq(company_id) & df_companies_financials.data_item.eq(data_item)][['ref_year', 'real_data_item_values']]

    return return_df    

def generate_fin_graph(fin_df):
    fig = go.Figure(data = go.Scatter(x=fin_df.ref_year.values, y=fin_df.real_data_item_values.values))
    fig.update_xaxes(nticks= len(fin_df.ref_year.values))

    return fig

def generate_esg_fin_graph(esg_df, fin_df):
    esg_fin_merged = pd.merge(esg_df, fin_df, how='inner', left_on='assessment_year', right_on='ref_year')

    reg = LinearRegression().fit(esg_fin_merged['score_value'].values.reshape(-1, 1), esg_fin_merged['real_data_item_values'].values)
    
    fig = go.Figure(data = go.Scatter(x=esg_fin_merged['score_value'].values, y=esg_fin_merged['real_data_item_values'].values, mode='markers', marker=dict(color='#00FF00'), showlegend=False))

    fig.add_trace(
            go.Scatter(x=esg_fin_merged['score_value'].values,
                y=reg.predict(esg_fin_merged['score_value'].values.reshape(-1, 1)),
                mode='lines',
                line=go.scatter.Line(color="gray"),
                showlegend=False
            )
    )

    return esg_fin_merged.corr().loc['score_value', 'real_data_item_values'], fig

#########
def select_env_company():
    company = st.sidebar.selectbox("Escolha uma empresa ambiental:",
            env_data['company_id'].unique()
            )

    return company

def select_envdata_item(company_id):
    data_item = st.sidebar.selectbox("Escolha um Indicador ambiental",
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
    fig = go.Figure(data = go.Scatter(x=fin_df['fiscal_year'], y=fin_df['data_item_value']))

    return fig

def generate_env_scatter(df1, df2):
    fig = ex.scatter(x=df1['data_item_value'], y=df2['data_item_value'])

    return fig



company_id, selected_company = select_company()

st.write("""# {}""".format(selected_company))

selected_esg_score = select_esg_score(company_id)

st.write("""# {}""".format(selected_esg_score))
esg_score = get_esg_score(company_id, selected_esg_score)

esg_fig = generate_esg_graph(esg_score)

st.write(esg_score.set_index('assessment_year'))
st.plotly_chart(esg_fig)

selected_data_item = select_data_item(company_id)
st.write("""# Indicador Financeiro: {} """.format(selected_data_item))

financials_by_year = get_financials_by_year(company_id, selected_data_item)
st.write(financials_by_year.set_index('ref_year'))

fin_fig = generate_fin_graph(financials_by_year)
st.plotly_chart(fin_fig)

st.write("""# {}  X {}""".format(selected_esg_score, selected_data_item))
corr, fin_esg_fig = generate_esg_fin_graph(esg_score, financials_by_year)
st.plotly_chart(fin_esg_fig)
st.write(''' Correlação: {}'''.format(corr))

#########--------------------- Graficos ambientais -----------------------

cp_env_id = select_env_company()

st.write("""# Empresa ambiental escolhida: {}""".format(cp_env_id))

env_item, env_item2 = select_envdata_item(cp_env_id)

df_1 = get_env_by_year(cp_env_id, env_item)
df_2 = get_env_by_year(cp_env_id, env_item2)
figg1 = generate_env_graph(df_1)
figg2 = generate_env_graph(df_2)
figg3 = generate_env_scatter(df_1, df_2)
st.plotly_chart(figg1)
st.plotly_chart(figg2)
st.plotly_chart(figg3)
