from dash import html, dcc
import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR],
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
                            'height' : '28px',
                        }),
                        href="https://www.ufrgs.br/gimscop/",
                ),
            )
            ),

            # Adiciona página ao dropdown
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Pagina 1", href=dash.page_registry['pages.pagina_1']['path']),
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

if __name__ == '__main__':
    import socket
    host = socket.gethostbyname(socket.gethostname())

    app.run_server(debug=True, host=host, dev_tools_ui=True, port=3000)
# "Port 3000 so you can run 2 app at the same time" disse o cara do vídeo.
#  Testar com o Tclab para ver se funciona.

