from dash import Dash, dcc, html, Input, Output, State, callback, ctx
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import tclab
import pandas as pd

from utils import graficos

lab = [0]
data = [0]

def tclab_conditions(n_intervals,potencia,button_state,component_id):

    lab[0].Q1(potencia)
    data[0].update(n_intervals)
    # data_append = {
    #     "Time": n_intervals,
    #     "T1": lab[0].T1
    # }

    df = pd.DataFrame.from_records(data[0].log, columns=data[0].columns)
    data_append = {
        "Time": df.iloc[-1:]["Time"],
        "T1": df.iloc[-1:]["T1"]
    }

    if button_state == "Parar" and component_id == "action-button":
        print("dentro do if fechar")
        lab[0].close()

    return data_append

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
                    dbc.Button("Submeter",id="action-button",size="sm",color="success"),
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
                ]),
                dcc.Interval(
                    id="interval-component",
                    disabled=True,
                    interval=1000,
                    n_intervals=0
                ),
            ]),
        ],
        width={"size":10, "offset":0}
        ),
    ],
    justify="center"
    ),
],fluid=False),

@callback(
    Output("grafico-temperatura","extendData"),
    Output("interval-component","disabled"),
    Output("interval-component","n_intervals"),
    Output("action-button","children"),

    Input("action-button","n_clicks"),
    Input("interval-component","n_intervals"),

    State("action-button","children"),
    State("grafico-temperatura","figure"),
    State('potencia','value'),

    prevent_initial_call = True
)
def trigger_update_graph(n_clicks,n_intervals,button_state,figure,potencia):
    component_id = ctx.triggered_id

    if(component_id == "action-button"):

        if(button_state == "Submeter"):

            lab[0] = tclab.TCLab()
            data[0] = tclab.Historian(lab[0].sources)

            button_state_aux = button_state
        
            return tclab_conditions(n_intervals,potencia,button_state_aux,component_id),False,0,"Parar"
        
        elif(button_state == "Parar"):
    
            button_state_aux = button_state

            return tclab_conditions(n_intervals,potencia,button_state_aux,component_id),True,0,"Submeter"

    elif(component_id == "interval-component"):

        return tclab_conditions(n_intervals,potencia,button_state,component_id),False,n_intervals,"Parar"
    
# Utilizar outro tipo de data que não seja o Dataframe,
# usar o mesmo do exemplo do cara do stackoverflow (padrão do python e dash)


# Ver dcc.Interval para atualizar página automaticamente, se precisar.
# Pode ajudar, ou não.
# progress bar long_callback para att automaticamente
