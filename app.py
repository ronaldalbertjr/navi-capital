import streamlit as st
import esg_fin
import ambiental
import principal 
from multipage import MultiPage

app = MultiPage()

## titulo principal
st.title("Hackaton Navi-Capital")

app.add_page("Hackaton Navi-Capital", principal.app)
app.add_page("ESG x métrica financeira", esg_fin.app)
app.add_page("Análise Ambiental", ambiental.app)

app.run()