from dash import Dash, dcc, html, Input, Output
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
# import tclab
import pandas as pd

dash.register_page(__name__, path='/', title='Pagina_1')

data = {
    'col1': [1, 2, 3, 4, 5, 6, 7, 8, 9],
    'col2': [1, 2, 3, 4, 5, 6, 7, 8, 9] 
}

df = pd.DataFrame.from_records(data=data)
fig = px.scatter(df, x='col1', y='col2')

layout = dbc.Container([
    dbc.Card([
        dbc.CardHeader("Gráfico".upper()),
        dbc.CardBody([
            dcc.Graph(id='ambient-output', figure=fig),
        ]) 
    ])   
])

#app.layout = html.Div([
#    html.Div([
#        dcc.Input(id='user_input', placeholder="Enter a value:", type='number', value=''),
#        html.Button('Submit', id='info-button'),
#    ]),
#    dcc.Graph(id='ambient-output', figure=fig),
#    # dcc.Input(id='ambient-info-input')    
#])

#@app.callback(
#    Output('ambient-info-output','figure'),
#    State('ambient-info-input','value'),
#    Input('info-button', 'n_clicks')
#)
#def update_figure(n_clicks, value):
