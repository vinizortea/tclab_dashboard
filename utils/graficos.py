from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import tclab
import pandas as pd


def grafico_temperatura(lab, data, potencia, medicao, aquecimento):

    for t in tclab.clock(medicao):
        lab.Q1(potencia if t <= aquecimento else 0)
        data.update(t)

    df = pd.DataFrame.from_records(data.log, columns=data.columns)
    fig = px.line(df, x='Time', y='T1')

    return fig 
