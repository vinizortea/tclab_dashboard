from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import tclab
import pandas as pd


def grafico_temperatura(lab, data, potencia, tempo_medicao:int, tempo_aquecimento:int):

    for t in tclab.clock(tempo_medicao):
        lab.Q1(potencia if t <= tempo_aquecimento else 0)
        data.update(t)

    df = pd.DataFrame.from_records(data.log, columns=data.columns)
    fig = px.line(df, x='Time', y='T1',markers=True)

    return fig 
