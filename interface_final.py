import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import ipywidgets as widgets

st.write("""
        # Hackaton Navi-Capital
        Ferramenta para ajudar investidores a avaliar a pontuação ESG de empresas
        """
)

df_companies = pd.read_csv("datasets/companies_br.csv")
df_companies_financials = pd.read_csv("datasets/companies_financials_br.csv")
esg_scores = pd.read_csv("datasets/esg_scores_history_br.csv")
esg_scores = esg_scores[esg_scores.score_value != 0]
esg_scores = esg_scores.dropna()
df_companies = df_companies[df_companies.company_id.isin(esg_scores.company_id.unique())]
df_companies_financials['ref_year'] = pd.to_datetime(df_companies_financials.ref_date).dt.year
df_companies_financials['real_data_item_values'] = df_companies_financials['data_item_value'] * df_companies_financials.unit_value

#### adicionando alternativa de nenhuma industria
df = df_companies.sort_values(by='industry')
industries = df['industry'].unique()
industries  = np.insert(industries, 0, 'Não dividir por indústria' ) ### ou apenas um traço como -?

def select_industry():
    industry = st.sidebar.selectbox("Escolha uma indústria:", 
               industries
        	   )
    return industry

def select_company(industry):
    if (industry != 'Não dividir por indústria'):
        dg_companies = df_companies[df_companies['industry'] == industry]
    else:
        dg_companies = df_companies #### por ser var local isso nao iria modificar df companies ao modificar dg comapnies? ou entao copia
    company = st.sidebar.selectbox("Escolha uma empresa:",
            dg_companies.company_name.values
            )

    return dg_companies[dg_companies.company_name.eq(company)].company_id.values[0] ,company

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
    fig = go.Figure(data = go.Scatter(x=esg_df.assessment_year.values, y=esg_df.score_value.values))
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
    
    fig = go.Figure(data = go.Scatter(x=esg_fin_merged['score_value'].values, y=esg_fin_merged['real_data_item_values'].values, mode='markers'))

    fig.add_trace(
            go.Scatter(x=esg_fin_merged['score_value'].values,
                y=reg.predict(esg_fin_merged['score_value'].values.reshape(-1, 1)),
                mode='lines',
                line=go.scatter.Line(color="gray"),
                showlegend=False
            )
    )

    return fig

selected_industry = select_industry()

st.write("""# {}""".format(selected_industry))

company_id, selected_company = select_company(selected_industry)

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
fin_esg_fig = generate_esg_fin_graph(esg_score, financials_by_year)
st.plotly_chart(fin_esg_fig)