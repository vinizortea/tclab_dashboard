from dash import Dash, dcc, html, Input, Output, State
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import tclab
import pandas as pd

from utils import graficos

dash.register_page(__name__, path='/', title='Pagina_1')

data_pag1 = {
    'col1': [1, 2, 3, 4, 5, 6, 7, 8, 9],
    'col2': [1, 2, 3, 4, 5, 6, 7, 8, 9] 
}

measuring_limit = 100
heating_limit = measuring_limit - 1

df = pd.DataFrame.from_records(data=data_pag1)
fig = px.line(df, x='col1', y='col2',markers=True)

layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            dbc.Label("Escolha potência do aquecedor: ", class_name="d-flex justify-content-center text-success"),
            dcc.Slider(id="potencia", min=0, max=100, step=5, value=0),
            dbc.Row([
                dbc.Col([
                    dcc.Input(placeholder="Tempo de medição",id="tempo_medicao",type="number",min=0,max=measuring_limit),
                ],
                width={"size":2}
                ),
                dbc.Col([
                    dcc.Input(placeholder="Tempo de aquecimento",id="tempo_aquecimento",type="number",min=0,max=heating_limit),
                ],
                width={"size":2}
                )
            ],
            justify="around",
            class_name="my-2"
            ),
            dbc.Row([
                dbc.Col([
                    dbc.Button("Submeter",id="info-button",size="sm",color="success"),
                ],
                width={"size":1}
                )
            ],
            justify="center",
            class_name="my-2"
            ),
            dbc.Card([
                dbc.CardHeader("Temperatura x Tempo".upper(),class_name="text-success text-center"),
                dbc.CardBody([
                dcc.Graph(id='grafico-temperatura', figure=fig),
                ]) 
            ]),
        ],
        width={"size":10, "offset":0}
        ),
    ],
    justify="center"
    ),
],fluid=False)

# Ver dcc.Interval para atualizar página automaticamente, se precisar.
# Pode ajudar, ou não.
# progress bar long_callback para att automaticamente
