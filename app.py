from dash import Dash, dcc, html, Input, Output, State
import dash
import tclab
import dash_bootstrap_components as dbc
from dash.long_callback import DiskcacheLongCallbackManager

import diskcache
cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)

from utils import graficos

app = dash.Dash(__name__, long_callback_manager=long_callback_manager,external_stylesheets=[dbc.themes.SOLAR],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                use_pages=True, pages_folder="pages"
                )

app.layout = html.Div([

    dbc.NavbarSimple(
        children=[
            # Adiciona logos
            dbc.NavItem(dbc.NavLink(
                html.A(
                    html.Img(
                        src=app.get_asset_url('figures/gimscop.png'),
                        style={
                            'height': '28px',
                        }),
                        href="https://www.ufrgs.br/gimscop/",
                ),
            )
            ),

            # Adiciona página ao dropdown
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Página 1", href=dash.page_registry['pages.pagina_1']['path']),
                ],
                # adiciona dropdown de navegação
                nav=True,
                in_navbar=True,
                label="Mais páginas",
                toggleClassName="text-success",
                menu_variant="dark"
            ),
        ],
        # Branding
        brand="Interface gráfica GIMSCOP",
        brand_href=dash.page_registry['pages.pagina_1']['path'],
        color="dark",
        id="navbar"
            
            
    ),
    
    dash.page_container
])

@app.long_callback(
    output = Output('grafico-temperatura','figure'),
    inputs=(State('potencia','value'),
    State('tempo_medicao','value'),
    State('tempo_aquecimento','value'),
    Input('info-button', 'n_clicks')),

    running=[
        (Output('info-button','disabled'),True,False)
    ],

    prevent_initial_call= True
    
)
def update_figure(n_clicks, potencia, tempo_medicao, tempo_aquecimento):
    lab = tclab.TCLab()
    data = tclab.Historian(lab.sources)

    return graficos.grafico_temperatura(lab, data, potencia, tempo_medicao, tempo_aquecimento)


if __name__ == '__main__':
    import socket
    host = socket.gethostbyname(socket.gethostname())

    app.run_server(debug=True, host=host, dev_tools_ui=True, port=3000)
# "Port 3000 so you can run 2 app at the same time" disse o cara do vídeo.

