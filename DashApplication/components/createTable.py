import dash_html_components as html
import pandas as pd


def create_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


df_usaAgriculturalExports = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')
agricultureTable = html.Div(
    style={
        'width':'90%',
        'background-color': 'white',
        'padding':'15pt',
        'margin':'7pt'
    },
    children=[
        html.H4(children='US agriculture Exports (2011)'),
        create_table(df_usaAgriculturalExports)
    ]
)

