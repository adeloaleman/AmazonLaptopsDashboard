# Important: States:  https://plot.ly/dash/state
# See this app can be very helfull:   https://dash-gallery.plotly.host/dash-nlp/
# This one has the loading animation: https://dash-gallery.plotly.host/dash-molecule-3d-viewer/
# Esta puede tener la respuesta para la puta scrollbar: https://dash-gallery.plotly.host/dash-needle-plot/
# https://dash-gallery.plotly.host/dash-molecule-3d-viewer/

import numpy  as np
import pandas as pd
import collections
import json

import plotly.graph_objs as go
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from   dash.dependencies import Input, Output, State
from   dash import no_update
from   dash.exceptions import PreventUpdate

from components.navbar   import navbar, navbar2
from components.sidebar  import sidebar
from components.plots    import textfield, wordCloud, img_wordCloud, wordCountBarChart, avgReviewsBarChart, avgPricesBarChart, avgVsPriceBubbleChart




external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://www.w3schools.com/w3css/4/w3.css',    # Para la sidebar https://www.w3schools.com/w3css/w3css_sidebar.asp   https://www.w3schools.com/w3css/tryit.asp?filename=tryw3css_sidebar_shift
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'  # Incluye el icon del Globe  https://www.w3schools.com/icons/tryit.asp?filename=tryicons_fa-globe
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


data = pd.read_json('./data/amazon_data.json')
brands = [ {"label": b, "value": b} for b in  list(set(data['brand'])) ]
first_brand = list(set(data['brand']))[1]


brand_series_list = data['brand']+' - '+data['series']
brand_series_list = list(set(brand_series_list))

brand_list = [ i.split()[0] for i in brand_series_list ]
brand_series = pd.DataFrame({'brand':brand_list,'brand_series':brand_series_list})

brand_series_all = brand_series['brand_series']
brand_series_all = list(set(brand_series_all))
brand_series_all = sorted(brand_series_all)
brand_series_dropdown = [ {"label": s, "value": s} for s in  brand_series_all ]


brand_series = data.query('brand in @first_brand')['brand']+' - '+data.query('brand in @first_brand')['series']
brand_series = list(set(brand_series))
brand_series_value = sorted(brand_series)

series_first_brand = [ ' '.join(i.split()[2:]) for i in brand_series_value ]

text = ' '.join(data[data['brand']==first_brand]['reviews_one_string'])

cloud = wordCloud(text)
imgCloud = img_wordCloud(cloud)

hist = html.Div([dcc.Graph(
    id='histo',
    style={'width': 'calc(100% - 50px)', 'height':'350px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'},
    figure=wordCountBarChart(text,30), config={'displayModeBar': False}
)])

file = open('testfile.txt','w') 
file.write('0')
file.close()

def resetfile(val):
    file = open('testfile.txt','w') 
    file.write(val)
    file.close()
    f = open('testfile.txt','r') 
    return  f.read()


minPrice = round(int(data.describe()['price'].loc['min']))
if minPrice%10 != 0:
        minPrice_base10 = minPrice-(minPrice%10)
else:
        minPrice_base10 = minPrice


maxPrice = round(int(data.describe()['price'].loc['max']))
if maxPrice%10 != 0:

        maxPrice_base10 = maxPrice+(10-(maxPrice%10))
else:
        maxPrice_base10 = maxPrice


marks_list = list(range(minPrice_base10, maxPrice_base10))
arr = np.array(marks_list)

numElems = 5
idx = np.round(np.linspace(0, len(arr) - 1, numElems)).astype(int)
marks_list5 = list(arr[idx])

marks_list5[0] = minPrice_base10
marks_list5[len(marks_list5)-1] = maxPrice_base10
for i in range(1,len(marks_list5)-1):
    if marks_list5[i]%25 != 0:
        if marks_list5[i]%25 <= 25/2:
            marks_list5[i] = marks_list5[i] - marks_list5[i]%25
        else:
            marks_list5[i] = marks_list5[i] + (25 - marks_list5[i]%25)


marksPrices = {}
styleDict   = {}
styleDict1 = {'color': 'red',     'font-size':'13pt', 'font-weight':'normal'}
styleDict2 = {'color': '#696b6e', 'font-size':'12pt'}
for i in marks_list5:
        i = int(i)
        marksValues = {}
        if i == marks_list5[0] or i == marks_list5[len(marks_list5)-1]:
                marksValues['label'] = '{}'.format(i)
                marksValues['style'] = styleDict1
        else:
                marksValues['label'] = '{}'.format(i)
                marksValues['style'] = styleDict2
        marksPrices[i] = marksValues






# =====================================================
# Layout
# =====================================================
app.layout = html.Div(
    children=[
        navbar,
        html.Div(style={'min-height':'34pt'}),
        sidebar,
        navbar2,
        html.Div(
            style={
                'maxWidth': '2500px',
                'margin': '0 auto 25px',
            },
            children=[
                html.Div(
                    style={'margin-left':'50pt','margin-right':'50pt','margin-top':'-5pt','z-index': '-100'},
                    children=[
                        # #  No borrar  # # 
                        # # dcc.Input(
                        # #     id='sincro1',
                        # #     value = resetfile('4000')
                        # # ),
                        # # dcc.Input(
                        # #     id='sincro2',
                        # #     value = 2
                        # # ),
                        # 
                        # 0.1
                        html.Div(
                            className='divDos1',
                            children=[
                                html.Div(
                                    className='interDivSquare',
                                    children=[
                                        html.Div(
                                            children=[
                                                html.Div(
                                                    style={'color': 'black', 'font-size':'15pt'},
                                                    children=[
                                                        "Brand"
                                                    ]
                                                ),
                                                html.Div(
                                                    id='brand_div_id',
                                                    children=[
                                                        dcc.Dropdown(
                                                            id='brand_id',
                                                            style={'max-width': '100%', 'height': '10px'},
                                                            options=brands,
                                                            multi=True,
                                                            value=first_brand
                                                        ),
                                                    ]    
                                                ),
                                            ]
                                        ),
                                        html.Br(), html.Br(), html.Br(),
                                        html.Div(
                                            children=[
                                                html.Div(
                                                    style={'color': 'black', 'font-size':'15pt'},
                                                    children=[
                                                        "Price ($)"
                                                    ]
                                                ),
                                                html.Div(
                                                    id='price_div_id',
                                                    children=[
                                                        dcc.RangeSlider(
                                                            id='price_id',
                                                            min=minPrice_base10,
                                                            max=maxPrice_base10,
                                                            step=10,
                                                            value=[minPrice_base10, maxPrice_base10],
                                                            marks=marksPrices,
                                                        ),
                                                    ]    
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        # 0.2
                        html.Div(
                            className='divDos2',
                            children=[
                                html.Div(
                                    className='interDivSquare',
                                    children=[
                                        html.Div(
                                            style={'color': 'black', 'font-size':'15pt'},
                                            children=[
                                                "Series"
                                            ]
                                        ),
                                        html.Div(
                                            children=[
                                                dcc.Dropdown(
                                                    id='brand_series_id',
                                                    style={'max-width': '100%', 'height': '10px'},
                                                    options=brand_series_dropdown,
                                                    multi=True,
                                                    value=brand_series_value
                                                ),
                                            ]    
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ]
                ),
                html.Div(
                    style={'margin-left':'50pt','margin-right':'50pt','margin-top':'7pt'},
                    children=[
                        # 1
                        html.Div(
                            className='divSquare1',
                            children=[
                                html.Div(
                                    className='interDivSquare',
                                    children=[
                                        html.Div(
                                            style={'width': 'calc(100% - 0px)', 'height':'360px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'},
                                            children =[
                                                dcc.Graph(
                                                    style={'height':'360px'},
                                                    id='ave_reviews',                                                        
                                                    figure=avgReviewsBarChart(data, first_brand, series_first_brand),
                                                    config={'displayModeBar': False}
                                                )
                                            ]
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        # 2
                        html.Div(
                            className='divSquare1',
                            children=[
                                html.Div(
                                    className='interDivSquare',
                                    children=[
                                        html.Div(
                                            style={'color': 'black', 'font-size':'15pt'},
                                            children=[
                                                html.Div(
                                                    style={'width': 'calc(100% - 00px)', 'height':'360px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'},
                                                    children =[
                                                        dcc.Graph(
                                                            style={'height':'360px'},
                                                            id='ave_prices',
                                                            figure=avgPricesBarChart(data, first_brand, series_first_brand),
                                                            config={'displayModeBar': False}
                                                        )
                                                    ]
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        # 3
                        html.Div(
                            className='divSquare2',
                            children=[
                                html.Div(
                                    className='interDivSquare',
                                    children=[
                                        dcc.Loading(
                                            id="loading-1",
                                            type="default",
                                            children=[
                                                html.Div(
                                                    id='cloud',
                                                    children=[
                                                        imgCloud,
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                ),
                            ]
                        ),
                        # 4
                        html.Div(
                            className='divSquare3',
                            children=[
                                html.Div(
                                    className='interDivSquare',
                                    children=[
                                        html.Div(
                                            style={'width': 'calc(100% - 50px)', 'height':'360px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'},
                                            children =[
                                                dcc.Graph(
                                                    style={'height':'360px'},
                                                    id='ave_price',                                                        
                                                    figure=avgVsPriceBubbleChart(),
                                                    config={'displayModeBar': False}
                                                )
                                            ]
                                        ),
                                    ]
                                )
                            ]
                        ),
                        # 5
                        html.Div(
                            className='divSquare2',
                            children=[
                                html.Div(
                                    className='interDivSquare',
                                    children=[
                                        dcc.Loading(
                                            id="loading-2",
                                            type="default",
                                            children=[
                                                html.Div(
                                                    id='histo_div',
                                                    style={'width': 'calc(100% - 5px)', 'height':'360px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'},
                                                    children= [
                                                        hist
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        )
    ]
)




# =====================================================
# Callback
# =====================================================

# # # # IMPORTANTE: No borrar este callback.. Puede ser importante para resolver o seguir probando el problema con el doble callback
# # Sin embargo, estaba causando que se cargara la página dos veces when refreshing the page:
# # @app.callback(
# #         Output('sincro2', 'value'),
# #     [
# #         Input('sincro1', 'value'),
# #     ], 
# # )
# # def changing_brand(sincrovalue):
# #     va = resetfile('4000')
# #     return va


@app.callback(
    [
        Output(component_id='cloud',           component_property='children'),
        Output(component_id='histo_div',       component_property='children'),
        Output(component_id='brand_series_id', component_property='value'),
        Output(component_id='ave_reviews',     component_property='figure'),
        Output(component_id='ave_prices',      component_property='figure'),
        Output(component_id='brand_id',        component_property='options'),
        Output(component_id='brand_series_id', component_property='options'),
    ],
    [
        Input(component_id='brand_id', component_property='value'),
        Input(component_id='price_id', component_property='value'),
    ],
    [
        State(component_id='brand_series_id', component_property='value'),
    ]
)
def changing_brand(input_value, price, input_value_series):
    f = open('testfile.txt','r')
    va = f.read()

    dataRangePrice = data[ (data['price'] >= price[0])  &  (data['price'] <= price[1]) ]

    brandsRangePrice = list(set(dataRangePrice['brand']))
    brandsRangePriceDropdown = [ {"label": b, "value": b} for b in  brandsRangePrice ]

    brand_series_listRangePrice = dataRangePrice['brand']+' - '+dataRangePrice['series']
    brand_series_listRangePrice = list(set(brand_series_listRangePrice))
    brand_series_listRangePrice = sorted(brand_series_listRangePrice)
    brand_seriesRangePriceDropdown = [ {"label": s, "value": s} for s in  brand_series_listRangePrice ]

    if len(input_value) == 0 and len(input_value_series) == 0:        

        emp = html.Div(
            style={'width': 'calc(100% - 50px)', 'height':'350px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'},
        )
        ser = [None] * len(input_value)
        ave_reviews = avgReviewsBarChart(dataRangePrice, input_value, ser)
        ave_prices = avgPricesBarChart(dataRangePrice, input_value, ser)
        return emp, emp, no_update, ave_reviews, ave_prices, brandsRangePriceDropdown, brand_seriesRangePriceDropdown

    elif len(input_value) == 0:
        file = open('testfile.txt','w') 
        file.write('2')
        file.close()

        emp = html.Div(
            style={'width': 'calc(100% - 50px)', 'height':'350px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'},
        )
        
        ser = [None] * len(input_value)
        ave_reviews = avgReviewsBarChart(dataRangePrice, input_value, ser)
        ave_prices = avgPricesBarChart(dataRangePrice, input_value, ser)
        return emp, emp, [], ave_reviews, ave_prices, brandsRangePriceDropdown, brand_seriesRangePriceDropdown


    elif (va != '3'):
        file = open('testfile.txt','w')
        file.write('2')
        file.close()

        # This is the values taken fron the series Dropdown:
        brand_distint = [ i.split()[0] for i in input_value_series ]
        brand_distint = list(set(brand_distint))

        brands_to_add     = list(np.setdiff1d(input_value,brand_distint))
        brands_to_suprime = list(np.setdiff1d(brand_distint,input_value))


        brand_series_value = []
        if len(brands_to_add) != 0:
            brand_series_value_to_update = dataRangePrice.query('brand in @brands_to_add')['brand']+' - '+dataRangePrice.query('brand in @brands_to_add')['series']
            brand_series_value_to_update = list(set(brand_series_value_to_update))  # aqui eliminamos los iguales

            brand_series_value = input_value_series + brand_series_value_to_update

        if len(brands_to_suprime) != 0:
            brand_series_value = [ value for value in input_value_series if value.split()[0]  not in  brands_to_suprime ]

        if len(brand_series_value) == 0:
            ser = [ ' '.join(i.split()[2:]) for i in input_value_series ]
        else:
            ser = [ ' '.join(i.split()[2:]) for i in brand_series_value ]

        text = ' '.join(dataRangePrice.query('brand in @input_value & series in @ser')['reviews_one_string'])

        if text == '':
            fignada = go.Figure(data=[])

            nada = dcc.Graph(
                style={'height':'360px'},
                figure=fignada,
                config={'displayModeBar': False}
            )
            imgCloud = nada
            di = nada
            ave_reviews = None
            ave_prices = None
        else:
            cloud = wordCloud(text)
            
            imgCloud = img_wordCloud(cloud)
            imgHistoWords = wordCountBarChart(text,30)

            di = html.Div(children=[dcc.Graph(
                id='histo',
                style={'width': 'calc(100% - 50px)', 'height':'370px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'},
                figure=imgHistoWords, config={'displayModeBar': False}
            )])

            ave_reviews = avgReviewsBarChart(dataRangePrice, input_value, ser)
            ave_prices = avgPricesBarChart(dataRangePrice, input_value, ser)

        return (
            imgCloud,
            di,
            brand_series_value if   len(brand_series_value) !=0   else   input_value_series,
            go.Figure(data=[]) if text == '' else ave_reviews,
            go.Figure(data=[]) if text == '' else ave_prices,
            brandsRangePriceDropdown,
            brand_seriesRangePriceDropdown
        )
    
    else: # cuando es 3 viene de la otra
        resetfile('5000')

        ser  = [ ' '.join(i.split()[2:]) for i in input_value_series ]
        text = ' '.join(dataRangePrice.query('brand in @input_value & series in @ser')['reviews_one_string'])

        if text == '':
            fignada = go.Figure(data=[])

            nada = dcc.Graph(
                style={'height':'360px'},
                figure=fignada,
                config={'displayModeBar': False}
            )
            imgCloud = nada
            di = nada
            ave_reviews = None
            ave_prices = None

        else:
            cloud = wordCloud(text)
            imgCloud = img_wordCloud(cloud)
            
            imgHistoWords = wordCountBarChart(text,30)

            di = html.Div(children=[dcc.Graph(
                id='histo',
                style={'width': 'calc(100% - 50px)', 'height':'370px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'},
                figure=imgHistoWords, config={'displayModeBar': False}
            )])

            ave_reviews = avgReviewsBarChart(dataRangePrice, input_value, ser)
            ave_prices = avgPricesBarChart(dataRangePrice, input_value, ser)

        return (
            imgCloud,
            di,
            no_update,
            go.Figure(data=[]) if text == '' else ave_reviews,
            go.Figure(data=[]) if text == '' else ave_prices,
            brandsRangePriceDropdown,
            brand_seriesRangePriceDropdown
        )




@app.callback(
        Output(component_id='brand_div_id',   component_property='children'),
    [
        Input(component_id='brand_series_id', component_property='value')
    ],
)
def changing_brand_series(input_value):
    f = open('testfile.txt','r') 
    va = f.read()

    if len(input_value) == 0 and va != '2':
        
        brand_distint = []

        div = dcc.Dropdown(
            id='brand_id',
            style={'max-width': '100%', 'height': '10px'},
            options=brands,
            multi=True,
            value=brand_distint
        ),

        return div

    elif va == '2':
        resetfile('5000')
        raise PreventUpdate

    else:
        file = open('testfile.txt','w') 
        file.write('3')
        file.close()

        brand_distint = [ i.split()[0] for i in input_value ]
        brand_distint = list(set(brand_distint))

        div = dcc.Dropdown(
            id='brand_id',
            style={'max-width': '100%', 'height': '10px'},
            options=brands,
            multi=True,
            value=brand_distint
        ),

        return div




@app.callback(
    [
        Output('sidebar',      'style'),
        Output('sidebarMenu3', 'style'),
    ],
    [
        Input('sidebarButton',   'n_clicks'),
        Input('menu3OpenButton', 'n_clicks'),
        Input('menu3CloseButton','n_clicks'),
        Input('menuHome',        'n_clicks'),
    ]
)
def display(n_sidebarButton, n_menu3OpenButton, n_menu3CloseButton, n_menuHome):
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id =  ctx.triggered[0]['prop_id'].split('.')[0]

    ctx_msg = json.dumps({
        'states':    ctx.states,
        'triggered': ctx.triggered,
        'inputs':    ctx.inputs
    }, indent=2)

    cl = n_sidebarButton

    if n_sidebarButton is None:
        return {'display': 'none'}, {'display': 'none'}

    elif button_id == 'sidebarButton'  and  n_sidebarButton%2 != 0:
        # cl = cl + 1
        return {'display': 'block'}, {'display': 'none'}

    elif button_id == 'menu3OpenButton'  and  n_menu3OpenButton > 0:
        return {'display': 'block'}, {'display': 'block'}

    elif button_id == 'menu3CloseButton' and n_menu3CloseButton > 0:
        return {'display': 'block'}, {'display': 'none'}

    elif button_id == 'menuHome' and n_menuHome > 0:
        # cl = cl + 1
        return {'display': 'none'}, {'display': 'none'}

    else:
        return {'display': 'none'}, {'display': 'none'}




# =====================================================
# Running the server
# =====================================================
if __name__ == '__main__':
    app.run_server(debug=True, port=8552)
    # app.run_server(debug=True, host='0.0.0.0')



