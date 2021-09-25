import streamlit as st

st.write("""
        # Hackaton Navi-Capital
        Ferramenta para ajudar investidores a avaliar a pontuação ESG de empresas
        """
)

def select_company():
    company = st.sidebar.selectbox("Escolha uma empresa:",
            ['Navi Capital', 'BITS Capital', 'Itau']
            )

    return company


selected_company = select_company()

st.write("""# {}""".format(selected_company))
