import streamlit as st
import esg_fin
import ambiental
import principal 
from multipage import MultiPage

app = MultiPage()

## titulo principal
st.title("Navi Tech Journey")

app.add_page("Navi Tech Journey", principal.app)
app.add_page("ESG x métrica financeira", esg_fin.app)
app.add_page("Análise Ambiental", ambiental.app)

app.run()
