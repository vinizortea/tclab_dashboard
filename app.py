from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import tclab
import pandas as pd
#import numpy as np

app = Dash(__name__)

measuring_time = 20
heating_time = 10

lab = tclab.TCLab()
data = tclab.Historian(lab.sources)
for t in tclab.clock(measuring_time):
    lab.Q1(100 if t <= heating_time else 0)
    data.update(t)     

df = pd.DataFrame.from_records(data.log, columns=data.columns)
fig = px.scatter(df, x='Time', y='T1')

app.layout = html.Div([
    dcc.Graph(id='ambient-output',figure=fig),
    #dcc.Input(id='ambient-info-input')    
])

if __name__ == '__main__':
    app.run_server(debug=True)

#@app.callback(
#    Output('ambient-info-output','figure'),
#    Input('ambient-info-input','value')
#)
#def update_figure(ambient-variation):

