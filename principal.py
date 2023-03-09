from dash import Dash, dcc, html
import plotly.express as px
# import tclab
import pandas as pd

app = Dash(__name__)

data = {
    'col1': [1, 2, 3, 4, 5, 6, 7, 8, 9],
    'col2': [1, 2, 3, 4, 5, 6, 7, 8, 9] 
}

df = pd.DataFrame.from_records(data=data)
fig = px.scatter(df, x='col1', y='col2')

app.layout = html.Div([
    dcc.Input(id='user_input', placeholder="Enter a value:", type='number', value=''),
    html.Div(id='user_output', type='hidden'),
    dcc.Graph(id='ambient-output', figure=fig),
    # dcc.Input(id='ambient-info-input')    
])

if __name__ == '__main__':
    app.run_server(debug=True)

#@app.callback(
#    Output('ambient-info-output','figure'),
#    Input('ambient-info-input','value')
#)
#def update_figure(ambient-variation):
