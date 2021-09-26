import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
#from sklearn.linear_model import LinearRegression
import interface
import ambiental

from multipage import MultiPage

app = MultiPage()

## titulo principal
st.title("Hackaton Navi-Capital")

app.add_page("Análise Empresa: ESG x métrica financeira", interface.app())
app.add_page("Análise Ambiental", ambiental.app())

app.run()