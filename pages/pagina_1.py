from dash import Dash, dcc, html, Input, Output, State, callback, ctx
import dash
import dash_bootstrap_components as dbc
from dash.long_callback import DiskcacheLongCallbackManager
import plotly.express as px
import tclab
import pandas as pd

from utils import graficos

app = dash.get_app()

lab = [0]
data = {
    "Time": [],
    "T1": []
}

# Fazer variável para ver se botão foi apertado durante execução do intervalo????

def tclab_conditions(n_intervals,potencia,button_state,component_id):

    if(button_state == "Parar" and component_id == "action-button"):
        df = pd.DataFrame(data)
        fig = px.line(df, x='Time', y='T1',markers=True)

        lab[0].U1 = 0
        lab[0].close()

        return fig


    lab[0].U1 = potencia
    
    data["Time"].append(n_intervals)
    data["T1"].append(lab[0].T1)

    print(len(data["T1"]))
    print(len(data["Time"]))

    df = pd.DataFrame(data)
    fig = px.line(df, x='Time', y='T1',markers=True)

    return fig

dash.register_page(__name__, path='/', title='Pagina_1')

fig = dict(data=[{'Time': [], 'T1': []}], )

layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            dbc.Label("Escolha potência do aquecedor: ", class_name="d-flex justify-content-center text-success"),
            dcc.Slider(id="potencia", min=0, max=100, step=5, value=0),
            # dbc.Row([
            #     dbc.Col([
            #         dcc.Input(placeholder="Tempo de medição",id="tempo_medicao",type="number",min=0,max=measuring_limit),
            #     ],
            #     width={"size":2}
            #     ),
            #     dbc.Col([
            #         dcc.Input(placeholder="Tempo de aquecimento",id="tempo_aquecimento",type="number",min=0,max=heating_limit),
            #     ],
            #     width={"size":2}
            #     )
            # ],
            # justify="around",
            # class_name="my-2"
            # ),
            dbc.Row([
                dbc.Col([
                    dbc.Button("Submeter",id="submit-button", disabled=False,size="sm",color="success"),
                ],
                width={"size":1}
                ),
                dbc.Col([
                    dbc.Button("Parar",id="stop-button", disabled=True,size="sm",color="success"),
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
                # dcc.Input(id="verify-change-on-callback",type="hidden",value=False)
            ]),
        ],
        width={"size":10, "offset":0}
        ),
    ],
    justify="center"
    ),
],fluid=False),

@callback(

    Output("interval-component","disabled"),
    Output("grafico-temperatura","figure"),
    Output("interval-component","n_intervals"),
    Output("action-button","children"),

    Input("action-button","n_clicks"),
    Input("interval-component","n_intervals"),

    State("action-button","children"),
    State("grafico-temperatura","figure"),
    State('potencia','value'),
    Input("interval-component","disabled"),

    prevent_initial_call = True
)
def trigger_update_graph(n_clicks,n_intervals,button_state,figure,potencia,disabled):
    component_id = ctx.triggered_id

    if(component_id == "action-button"):

        if(button_state == "Submeter"):

            print("entrou no if de submeter")

            lab[0] = tclab.TCLab()

            button_state_aux = button_state
        
            return False,tclab_conditions(n_intervals,potencia,button_state_aux,component_id),n_intervals,"Parar"
        
        elif(button_state == "Parar"):
    
            print("entrou no if de parar")

            button_state_aux = button_state

            return True,tclab_conditions(n_intervals,potencia,button_state_aux,component_id),n_intervals,"Submeter"

    elif(component_id == "interval-component" and disabled == False):

        print("entrou no if do interval")

        return False,tclab_conditions(n_intervals,potencia,button_state,component_id),n_intervals,"Parar"

# @app.long_callback(
#     Output("submit-button","disabled"),
#     Output("stop-button","disabled"),
#     Output("interval-component","disabled"),

#     Input("submit-button","n_clicks"),
#     Input("stop-button","n_clicks"),

#     prevent_initial_call = True
# )
# def activate_interval(n_clicks_submit,n_clicks_stop):
    
#     print("chamou")

#     button_triggered = ctx.triggered_id

#     if(button_triggered == "submit-button"):

#         lab[0] = tclab.TCLab()

#         return True,False,False
    
#     elif(button_triggered == "stop_button"):

#         return False,True,True


# @app.long_callback(

#     Output("grafico-temperatura","figure"),

#     Input("interval-component","n_intervals"),

#     State("potencia","value"),

#     cancel=[Input("stop-button","n_clicks")],

#     prevent_initial_call = True
# )
# def trigger_interval(n_clicks,n_intervals,potencia):

#     return tclab_conditions(n_intervals,potencia)
