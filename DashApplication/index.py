import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from   app  import app
import app1_home
import app2_sentiment


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/home':
        return app1_home.layout
    elif pathname == '/sentiment':
        return app2_sentiment.layout
    else:
        return app1_home.layout

if __name__ == '__main__':
    app.run_server(debug=True, port=8552)
    # app.run_server(debug=True, host='0.0.0.0')

server = app.server