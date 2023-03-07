from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import tclab
import pandas as pd
#import numpy as np

app = Dash(__name__)

measuring_time = 20
heating_time = 10

TCLab = tclab.setup(connected=False, speedup=1)

with TCLab() as lab:
    data = tclab.Historian(lab.sources)
    T1 = lab.T1

    df = pd.DataFrame.from_records(data.log, columns=data.columns)
    fig = px.scatter(df, x='Time', y='T1')

    app.layout = html.Div([
        dcc.Graph(id='ambient-info-output',figure=fig),
        html.Div([
            "Valor atual:",
            html.H1(id='ambient-info-input',children = T1)
        ])
    ])

    for t in tclab.clock(measuring_time):
        lab.Q1(100 if t <= heating_time else 0)
        data.update(t)
        T1 = lab.T1 

    @app.callback(
        Output('ambient-info-output','figure'),
        Input('ambient-info-input','children')
    )
    def update_figure(ambientVariation):
        df = pd.DataFrame.from_records(data.log, columns=data.columns)
        fig = px.scatter(df, x='Time', y='T1')
        return fig 
    
    if __name__ == '__main__':
        app.run_server(debug=True)