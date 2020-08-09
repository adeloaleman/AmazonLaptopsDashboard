# Important: States:  https://plot.ly/dash/state
# See this app can be very helfull:   https://dash-gallery.plotly.host/dash-nlp/
# This one has the loading animation: https://dash-gallery.plotly.host/dash-molecule-3d-viewer/
# Esta puede tener la respuesta para la puta scrollbar: https://dash-gallery.plotly.host/dash-needle-plot/
# https://dash-gallery.plotly.host/dash-molecule-3d-viewer/
# Colores: https://www.w3schools.com/colors/colors_names.asp

import numpy  as np
import pandas as pd
import collections
import json
from textblob import TextBlob

import plotly.graph_objs as go
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from   dash.dependencies import Input, Output, State
from   dash import no_update
from   dash.exceptions import PreventUpdate

from app import app

from  components.navbar   import navbar, navbar2
from  components.sidebar  import sidebar
from  components.plots    import textfield, wordCloud, img_wordCloud, wordCountBarChart, avgReviewsBarChart, avgPricesBarChart, avgVsPriceBubbleChart, emotionsBarChart, sentimetsDonutChart, createSentimentDf, ConfusionMatrixHeatmap, getSentimentAnalysis, classif_report_heatmap, roc_curve_chart, review_length_histogram, confusion_matrix_pie_chart



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

text = ' '.join(data[data['brand']==first_brand]['review_one_string'])

hist = html.Div([dcc.Graph(
    id='histo',
    style={'width': 'calc(100% - 50px)', 'height':'350px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'},
    figure=wordCountBarChart(text,30), config={'displayModeBar': False}
)])

file = open('testfile.txt','w') 
file.write('0')
file.close()


######################################################################################################################### 
# Hice este cambio aqui hay que revisar bien si no genera problemas 
######################################################################################################################### 
def resetfile(val):
    file = open('testfile.txt','w') 
    file.write(val)
    file.close()
    f = open('testfile.txt','r') 
    res = f.read()
    f.close()
    return  res
# def resetfile(val):
#     file = open('testfile.txt','w') 
#     file.write(val)
#     file.close()
#     f = open('testfile.txt','r') 
#     return  f.read()


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
styleDict1 = {'color': 'red',     'font-size':'14pt', 'font-weight':'normal'}
styleDict2 = {'color': '#696b6e', 'font-size':'13pt'} 
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



sentiment_df = createSentimentDf(data)
sentiment_analysis_textblob = getSentimentAnalysis(sentiment_df, 'textblob')
sentiment_analysis_vader    = getSentimentAnalysis(sentiment_df, 'vader')
sentiment_analysis_subj     = getSentimentAnalysis(sentiment_df, 'subjectivity')




# Loading the nbayes model from a file:
import pickle

# This function «pre_processing» has been defining in «utils.py». It can no be defined in this file because we are passing this function as an argument to our pipeline machine learning model. So, in order to be able to save the ML model on disc for later use, the functions passed to the pipeline must be defined in another file and imported here (from utils import pre_processing)
from utils import pre_processing

with open('nbayes_model_wang.pkl', 'rb') as file:
    nbayes_model_wang = pickle.load(file)

# Making prediction using the model loaded
y_pred = nbayes_model_wang.predict(sentiment_analysis_textblob['title_text'])
# y_pred = sentiment_analysis_textblob['rating']



# =====================================================
# Layout
# =====================================================
layout = html.Div(
    style={'border-radius': '50px'},
    children=[
        navbar,
        html.Div(style={'min-height':'34pt'}),
        sidebar,
        navbar2,
        html.Div(
            style={
                'maxWidth': '2500px',
                'margin': '0 auto 25px',
                'border-radius': '50px'
            },
            children=[
                html.Div(
                    style={'margin-left':'50pt','margin-right':'50pt','margin-top':'-5pt','z-index': '-100', 'border-radius': '50px'},
                    children=[
                        html.Div(
                            className='divDos1',
                            children=[
                                html.Div(
                                    className='interDivSquare',
                                    # style={'background-color':'white'},
                                    children=[
                                        html.Div(
                                            children=[
                                                html.Div(
                                                    style={'color': 'black', 'font-size':'17pt','font-weight':'normal'},
                                                    children=[
                                                        "Brand"
                                                    ]
                                                ),
                                                html.Div(
                                                    id='brand_div_id22',
                                                    children=[
                                                        dcc.Dropdown(
                                                            id='brand_id',
                                                            style={'max-width': '100%','height': '10px',}, # 'border': '5.0px rgba(30,33,48,0.2)'
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
                                                    style={'color': 'black', 'font-size':'17pt','font-weight':'normal'},
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
                                    # style={'background-color':'rgba(30,33,63,0.4)'},
                                    children=[
                                        html.Div(
                                            style={'color': 'black', 'font-size':'17pt','font-weight':'normal'},
                                            children=[
                                                "Series"
                                            ]
                                        ),
                                        html.Div(
                                            style={'background-color':'rgba(30,33,48,0.2)'},
                                            children=[
                                                dcc.Dropdown(
                                                    id='brand_series_id',
                                                    style={'max-width': '100%', 'height': '10px'}, # ,'border': '5.0px rgba(30,33,48,0.2)'
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
                            className='divSquare5',
                            children=[
                                html.Div(
                                    className='interDivSquare',
                                    children=[
                                        html.Div(
                                            style={'color': 'black', 'font-size':'15pt', 'padding':'7px 0px 0px 20px'},
                                            children=[
                                                html.Div(
                                                    style={'width': 'calc(100% - 00px)', 'height':'360px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'},
                                                    children =[
                                                        dcc.Graph(
                                                            style={'height':'340px'},
                                                            id='customer_rating',
                                                            figure = sentimetsDonutChart(sentiment_analysis_textblob['rating'], ['Pos.','Neg.'],  'Customer<br />rating',  20, ['#007bff','#9c2828'] ),
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
                        # 2
                        html.Div(
                            className='divSquare5',
                            children=[
                                html.Div(
                                    className='interDivSquare',
                                    children=[
                                        html.Div(
                                            style={'width': 'calc(100% - 0px)', 'height':'360px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto',},
                                            children =[
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
                        # 3
                        html.Div(
                            className='divSquare6',
                            # style={'width':'20%'},
                            children=[
                                html.Div(
                                    className='interDivSquare',
                                    children=[
                                        html.Div(
                                            style={'width': 'calc(100% - 50px)', 'height':'360px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'},
                                            children =[
                                                dcc.Graph(
                                                    style={'height':'360px'},
                                                    id='review_length_hist',
                                                    figure=review_length_histogram(sentiment_df,'rating','length_title_text'),
                                                    config={'displayModeBar': False}
                                                )
                                            ]
                                        ),
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            style={'position': 'fixed', 'top': '50%', 'left': '50%', 'z-index': '200'},
                            children=[
                                dcc.Loading(
                                    id="loading-1",
                                    type="default",
                                    fullscreen=False,
                                    color='blue',
                                    style={'z-index': '200'},
                                    children=[
                                        html.Div(
                                            id='loading_page',
                                            style={'display':'block'}   
                                        )
                                    ]
                                )
                            ]
                        ),
                        # 4
                        html.Div(
                            className='divSquare8',
                            # style={'background-color':'white'},
                            children=[
                                html.Div(
                                    className='interDivSquare',
                                    # style={'background-color':'#007bff'},
                                    style={'background-color':'white'},
                                    children=[
                                        html.Div(
                                            style={'font-size':'22px'},
                                            children=[
                                                html.Span("Lexicon-based Sentiment Analysis using "),
                                                dcc.Link(
                                                    style={'color': 'blue','text-decoration':'none'},
                                                    href='https://textblob.readthedocs.io/en/dev/',
                                                    target='_blank',
                                                    children=[
                                                        html.Span('TextBlob '),
                                                        html.Img(
                                                            src='https://upload.wikimedia.org/wikipedia/commons/2/25/External.svg',
                                                            alt='Girl in a jacket',
                                                            style={'width':'17px','padding':'0px 0px 10px 0px'}
                                                        ),
                                                    ]
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            className='divSquare4',
                                            # style={'background-color':'#007bff'},
                                            style={'background-color':'white', 'height':'300px', 'width':'25%', 'padding': '10px 10px 10px 0px'},
                                            children=[
                                                html.Div(
                                                    style={'width': 'calc(100% - 00px)', 'height':'300px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'background-color':'white'},
                                                    children =[
                                                        html.Div(
                                                            style={'height':'300px','background-color':'white'},
                                                            children=[
                                                                dcc.Graph(
                                                                    style={'height':'300px',},
                                                                    id='polarity_textblob',
                                                                    figure = sentimetsDonutChart(sentiment_analysis_textblob['polarity_title_text_textblob'], ['Pos.','Neg.'], 'Polarity', 20, ['#6495ed','#b35050'] ),
                                                                    config={'displayModeBar': False}
                                                                ),
                                                            ]
                                                        ),
                                                        html.Div(
                                                            style={'height':'300px','background-color':'white'},
                                                            children=[
                                                                dcc.Graph(
                                                                    style={'height':'300px',},
                                                                    id='subjectivity_textblob',
                                                                    figure = sentimetsDonutChart(sentiment_analysis_subj['subjectivity_title_text_textblob'], ['Obj.','Subj.'], 'Subjectivity', 20, ['#6868a3','#9cba95'] ),
                                                                    config={'displayModeBar': False}
                                                                ),
                                                            ]
                                                        )
                                                    ]
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            className='divSquare4',
                                            # style={'background-color':'#007bff'},
                                            style={'background-color':'white', 'height':'300px', 'width':'25%', 'padding': '10px 25px 25px 25px'},
                                            children=[
                                                html.Div(
                                                    style={'width': 'calc(100% - 00px)', 'height':'300px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'},
                                                    children =[
                                                        html.Div(
                                                            style={'padding':'0px 0px 20px 0px'},
                                                            children=[
                                                                dcc.Graph(
                                                                    style={'height':'280px',},
                                                                    id='confusion_matrix_textblob',
                                                                    figure = ConfusionMatrixHeatmap(sentiment_analysis_textblob['rating'], sentiment_analysis_textblob['polarity_title_text_textblob']),
                                                                    config={'displayModeBar': False}
                                                                ),
                                                            ]
                                                        ),
                                                        html.Div(
                                                            style={'padding':'0px 0px 20px 50px'},
                                                            children=[
                                                                dcc.Graph(
                                                                    style={'height':'300px',},
                                                                    id='confusion_matrix_pie_textblob',
                                                                    figure = confusion_matrix_pie_chart(sentiment_analysis_textblob['rating'], sentiment_analysis_textblob['polarity_title_text_textblob']),
                                                                    config={'displayModeBar': False}
                                                                )
                                                            ]
                                                        ),
                                                    ]
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            className='divSquare4',
                                            # style={'background-color':'#007bff'},
                                            style={'background-color':'white', 'height':'600px', 'width':'50%', 'padding': '0px 40px 10px 40px'},
                                            children=[
                                                html.Div(
                                                    style={'width': 'calc(100% - 00px)', 'height':'300px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'},
                                                    children =[
                                                        html.Div(
                                                            style={'padding':'0px 0px 20px 0px'},
                                                            children=[
                                                                dcc.Graph(
                                                                    style={'height':'300px'},
                                                                    id='classif_report_textblob',
                                                                    figure = classif_report_heatmap(sentiment_analysis_textblob['rating'], sentiment_analysis_textblob['polarity_title_text_textblob']),
                                                                    config={'displayModeBar': False}
                                                                ),
                                                            ]
                                                        ),
                                                        html.Div(
                                                            style={'padding':'0px 80px 0px 80px'},
                                                            children=[
                                                                dcc.Graph(
                                                                    style={'height':'310px'},
                                                                    id='roc_curve_textblob',
                                                                    figure = roc_curve_chart(sentiment_analysis_textblob['rating'], sentiment_analysis_textblob['polarity_title_text_textblob']),
                                                                    config={'displayModeBar': False}
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
                        ),
                        # 5
                        html.Div(
                            className='divSquare8',
                            # style={'background-color':'white'},
                            children=[
                                html.Div(
                                    className='interDivSquare',
                                    # style={'background-color':'#007bff'},
                                    style={'background-color':'white'},
                                    children=[
                                        html.Div(
                                            style={'font-size':'22px'},
                                            children=[
                                                html.Span("Lexicon-based Sentiment Analysis using "),
                                                dcc.Link(
                                                    style={'color': 'blue','text-decoration':'none'},
                                                    href='https://pypi.org/project/vaderSentiment/',
                                                    target='_blank',
                                                    children=[
                                                        html.Span('Vader Sentiment '),
                                                        html.Img(
                                                            src='https://upload.wikimedia.org/wikipedia/commons/2/25/External.svg',
                                                            alt='Girl in a jacket',
                                                            style={'width':'17px','padding':'0px 0px 10px 0px'}
                                                        ),
                                                    ]
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            className='divSquare4',
                                            # style={'background-color':'#007bff'},
                                            style={'background-color':'white', 'height':'300px', 'width':'25%', 'padding': '10px 10px 10px 0px'},
                                            children=[
                                                html.Div(
                                                    style={'width': 'calc(100% - 00px)', 'height':'300px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'background-color':'white'},
                                                    children =[
                                                        html.Div(
                                                            style={'height':'300px','background-color':'white'},
                                                            children=[
                                                                dcc.Graph(
                                                                    style={'height':'300px'},
                                                                    id='polarity_vader',
                                                                    figure = sentimetsDonutChart(sentiment_analysis_vader['polarity_title_text_vader'], ['Pos.','Neg.'],  'Polarity', 20, ['#6495ed','#b35050'] ),
                                                                    config={'displayModeBar': False}
                                                                ),
                                                            ]
                                                        ),
                                                    ]
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            className='divSquare4',
                                            # style={'background-color':'#007bff'},
                                            style={'background-color':'white', 'height':'300px', 'width':'25%', 'padding': '10px 25px 25px 25px'},
                                            children=[
                                                html.Div(
                                                    style={'width': 'calc(100% - 00px)', 'height':'300px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'},
                                                    children =[
                                                        html.Div(
                                                            style={'padding':'0px 0px 20px 0px'},
                                                            children=[
                                                                dcc.Graph(
                                                                    style={'height':'280px',},
                                                                    id='confusion_matrix_vader',
                                                                    figure = ConfusionMatrixHeatmap(sentiment_analysis_vader['rating'], sentiment_analysis_vader['polarity_title_text_vader']),
                                                                    config={'displayModeBar': False}
                                                                ),
                                                            ]
                                                        ),
                                                        html.Div(
                                                            style={'padding':'0px 0px 20px 50px'},
                                                            children=[
                                                                dcc.Graph(
                                                                    style={'height':'300px',},
                                                                    id='confusion_matrix_pie_vader',
                                                                    figure = confusion_matrix_pie_chart(sentiment_analysis_vader['rating'], sentiment_analysis_vader['polarity_title_text_vader']),
                                                                    config={'displayModeBar': False}
                                                                )
                                                            ]
                                                        ),
                                                    ]
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            className='divSquare4',
                                            # style={'background-color':'#007bff'},
                                            style={'background-color':'white', 'height':'600px', 'width':'50%', 'padding': '0px 40px 10px 40px'},
                                            children=[
                                                html.Div(
                                                    style={'width': 'calc(100% - 00px)', 'height':'300px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'},
                                                    children =[
                                                        html.Div(
                                                            style={'padding':'0px 0px 20px 0px'},
                                                            children=[
                                                                dcc.Graph(
                                                                    style={'height':'300px'},
                                                                    id='classif_report_vader',
                                                                    figure = classif_report_heatmap(sentiment_analysis_vader['rating'], sentiment_analysis_vader['polarity_title_text_vader']),
                                                                    config={'displayModeBar': False}
                                                                ),
                                                            ]
                                                        ),
                                                        html.Div(
                                                            style={'padding':'0px 80px 0px 80px'},
                                                            children=[
                                                                dcc.Graph(
                                                                    style={'height':'310px'},
                                                                    id='roc_curve_vader',
                                                                    figure = roc_curve_chart(sentiment_analysis_vader['rating'], sentiment_analysis_vader['polarity_title_text_vader']),
                                                                    config={'displayModeBar': False}
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
                        ),
                        # 6
                        html.Div(
                            className='divSquare8',
                            # style={'background-color':'white'},
                            children=[
                                html.Div(
                                    className='interDivSquare',
                                    # style={'background-color':'#007bff'},
                                    style={'background-color':'white'},
                                    children=[
                                        html.Div(
                                            style={'font-size':'22px'},
                                            children=[
                                                html.Span("Machine Learning Sentiment Analysis using Naive Bayes"),
                                            ]
                                        ),
                                        html.Div(
                                            className='divSquare4',
                                            # style={'background-color':'#007bff'},
                                            style={'background-color':'white', 'height':'300px', 'width':'25%', 'padding': '10px 10px 10px 0px'},
                                            children=[
                                                html.Div(
                                                    style={'width': 'calc(100% - 00px)', 'height':'300px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'background-color':'white'},
                                                    children =[
                                                        html.Div(
                                                            style={'height':'300px','background-color':'white'},
                                                            children=[
                                                                dcc.Graph(
                                                                    style={'height':'300px'},
                                                                    id='polarity_nbayes',
                                                                    figure = sentimetsDonutChart(y_pred, ['Pos.','Neg.'],  'Polarity', 20, ['#6495ed','#b35050'] ),
                                                                    config={'displayModeBar': False}
                                                                ),
                                                            ]
                                                        ),
                                                    ]
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            className='divSquare4',
                                            # style={'background-color':'#007bff'},
                                            style={'background-color':'white', 'height':'300px', 'width':'25%', 'padding': '10px 25px 25px 25px'},
                                            children=[
                                                html.Div(
                                                    style={'width': 'calc(100% - 00px)', 'height':'300px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'},
                                                    children =[
                                                        html.Div(
                                                            style={'padding':'0px 0px 20px 0px'},
                                                            children=[
                                                                dcc.Graph(
                                                                    style={'height':'280px',},
                                                                    id='confusion_matrix_nbayes',
                                                                    figure = ConfusionMatrixHeatmap(sentiment_analysis_vader['rating'], y_pred),
                                                                    config={'displayModeBar': False}
                                                                ),
                                                            ]
                                                        ),
                                                        html.Div(
                                                            style={'padding':'0px 0px 20px 50px'},
                                                            children=[
                                                                dcc.Graph(
                                                                    style={'height':'300px',},
                                                                    id='confusion_matrix_pie_nbayes',
                                                                    figure = confusion_matrix_pie_chart(sentiment_analysis_vader['rating'], y_pred),
                                                                    config={'displayModeBar': False}
                                                                )
                                                            ]
                                                        ),
                                                    ]
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            className='divSquare4',
                                            # style={'background-color':'#007bff'},
                                            style={'background-color':'white', 'height':'600px', 'width':'50%', 'padding': '0px 40px 10px 40px'},
                                            children=[
                                                html.Div(
                                                    style={'width': 'calc(100% - 00px)', 'height':'300px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'},
                                                    children =[
                                                        html.Div(
                                                            style={'padding':'0px 0px 20px 0px'},
                                                            children=[
                                                                dcc.Graph(
                                                                    style={'height':'300px'},
                                                                    id='classif_report_nbayes',
                                                                    figure = classif_report_heatmap(sentiment_analysis_vader['rating'], y_pred),
                                                                    config={'displayModeBar': False}
                                                                ),
                                                            ]
                                                        ),
                                                        html.Div(
                                                            style={'padding':'0px 80px 0px 80px'},
                                                            children=[
                                                                dcc.Graph(
                                                                    style={'height':'310px'},
                                                                    id='roc_curve_nbayes',
                                                                    figure = roc_curve_chart(sentiment_analysis_vader['rating'], y_pred),
                                                                    config={'displayModeBar': False}
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
        Output(component_id='histo_div',                     component_property='children'),
        Output(component_id='brand_series_id',               component_property='value'),
        Output(component_id='customer_rating',               component_property='figure'),
        Output(component_id='brand_id',                      component_property='options'),
        Output(component_id='brand_series_id',               component_property='options'),
        Output(component_id='polarity_textblob',             component_property='figure'),
        Output(component_id='subjectivity_textblob',         component_property='figure'),
        Output(component_id='polarity_vader',                component_property='figure'),
        Output(component_id='confusion_matrix_textblob',     component_property='figure'),
        Output(component_id='confusion_matrix_vader',        component_property='figure'),
        Output(component_id='confusion_matrix_pie_textblob', component_property='figure'),
        Output(component_id='confusion_matrix_pie_vader',    component_property='figure'),
        Output(component_id='classif_report_textblob',       component_property='figure'),
        Output(component_id='classif_report_vader',          component_property='figure'),
        Output(component_id='roc_curve_textblob',            component_property='figure'),
        Output(component_id='roc_curve_vader',               component_property='figure'),
        Output(component_id='review_length_hist',            component_property='figure'),
        Output(component_id='loading_page',                  component_property='style'),
        Output(component_id='polarity_nbayes',               component_property='figure'),
        Output(component_id='confusion_matrix_nbayes',       component_property='figure'),
        Output(component_id='confusion_matrix_pie_nbayes',   component_property='figure'),
        Output(component_id='classif_report_nbayes',         component_property='figure'),
        Output(component_id='roc_curve_nbayes',              component_property='figure'),
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

    loading_page = {'display':'none'}

    dataRangePrice = data[ (data['price'] >= price[0])  &  (data['price'] <= price[1]) | (np.isnan(data['price'])) ]

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
        empty_fig = go.Figure(data=[go.Pie(labels=['',''], values=[])]) 
        customer_rating               = empty_fig
        polarity_textblob             = empty_fig
        subjectivity_textblob         = empty_fig
        polarity_vader                = empty_fig
        confusion_matrix_textblob     = empty_fig
        confusion_matrix_vader        = empty_fig
        confusion_matrix_pie_textblob = empty_fig
        confusion_matrix_pie_vader    = empty_fig
        classif_report_textblob       = empty_fig
        classif_report_vader          = empty_fig
        roc_curve_textblob            = empty_fig
        roc_curve_vader               = empty_fig
        review_length_hist            = empty_fig
        polarity_nbayes               = empty_fig
        confusion_matrix_nbayes       = empty_fig
        confusion_matrix_pie_nbayes   = empty_fig
        classif_report_nbayes         = empty_fig
        roc_curve_nbayes              = empty_fig

        return emp, no_update, customer_rating, brandsRangePriceDropdown, brand_seriesRangePriceDropdown, polarity_textblob, subjectivity_textblob, polarity_vader, confusion_matrix_textblob, confusion_matrix_vader, confusion_matrix_pie_textblob, confusion_matrix_pie_vader, classif_report_textblob, classif_report_vader, roc_curve_textblob, roc_curve_vader, review_length_hist, loading_page, polarity_nbayes, confusion_matrix_nbayes, confusion_matrix_pie_nbayes, classif_report_nbayes, roc_curve_nbayes
    
    elif len(input_value) == 0:
        file = open('testfile.txt','w') 
        file.write('2')
        file.close()

        emp = html.Div(
            style={'width': 'calc(100% - 50px)', 'height':'350px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'},
        )
        
        ser = [None] * len(input_value)
        empty_fig = go.Figure(data=[go.Pie(labels=['',''], values=[])]) 
        customer_rating               = empty_fig
        polarity_textblob             = empty_fig
        subjectivity_textblob         = empty_fig
        polarity_vader                = empty_fig
        confusion_matrix_textblob     = empty_fig
        confusion_matrix_vader        = empty_fig
        confusion_matrix_pie_textblob = empty_fig
        confusion_matrix_pie_vader    = empty_fig
        classif_report_textblob       = empty_fig
        classif_report_vader          = empty_fig
        roc_curve_textblob            = empty_fig
        roc_curve_vader               = empty_fig
        review_length_hist            = empty_fig
        polarity_nbayes               = empty_fig
        confusion_matrix_nbayes       = empty_fig
        confusion_matrix_pie_nbayes   = empty_fig
        classif_report_nbayes         = empty_fig
        roc_curve_nbayes              = empty_fig

        return emp, [], customer_rating, brandsRangePriceDropdown, brand_seriesRangePriceDropdown, polarity_textblob, subjectivity_textblob, polarity_vader, confusion_matrix_textblob, confusion_matrix_vader, confusion_matrix_pie_textblob, confusion_matrix_pie_vader, classif_report_textblob, classif_report_vader, roc_curve_textblob, roc_curve_vader, review_length_hist, loading_page, loading_page, polarity_nbayes, confusion_matrix_nbayes, confusion_matrix_pie_nbayes, classif_report_nbayes, roc_curve_nbayes

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

        dataRangePriceSeries = dataRangePrice.query('brand in @input_value & series in @ser')
        
        sentiment_df = createSentimentDf(dataRangePriceSeries)
        sentiment_analysis_vader = getSentimentAnalysis(sentiment_df, 'vader')
        sentiment_analysis_textblob = getSentimentAnalysis(sentiment_df, 'textblob')
        sentiment_analysis_subj = getSentimentAnalysis(sentiment_df, 'subjectivity')
        y_pred = nbayes_model_wang.predict(sentiment_analysis_textblob['title_text'])

        text = ' '.join(dataRangePrice.query('brand in @input_value & series in @ser')['review_one_string'])

        if text == '':
            fignada = go.Figure(data=[])

            nada = dcc.Graph(
                style={'height':'360px'},
                figure=fignada,
                config={'displayModeBar': False}
            )
            imgCloud = nada
            di = nada
            customer_rating = None
            polarity_textblob = None
            subjectivity_textblob = None
            polarity_vader = None
            confusion_matrix_textblob = None
            confusion_matrix_vader = None
            confusion_matrix_pie_textblob = None
            confusion_matrix_pie_vader = None
            classif_report_textblob = None
            classif_report_vader = None
            roc_curve_textblob = None
            roc_curve_vader = None
            review_length_hist = None
            polarity_nbayes = None 
            confusion_matrix_nbayes = None 
            confusion_matrix_pie_nbayes = None 
            classif_report_nbayes = None 
            roc_curve_nbayes = None

        else:

            imgEmotionsBarChart = emotionsBarChart(sentiment_df)

            di = html.Div(children=[dcc.Graph(
                id='histo',
                style={'width': 'calc(100% - 50px)', 'height':'360px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'},
                figure=imgEmotionsBarChart, config={'displayModeBar': False}
            )])

            customer_rating               = sentimetsDonutChart(sentiment_analysis_textblob['rating'],                       ['Pos.','Neg.'],  'Customer<br />rating',  20, ['#007bff','#9c2828'] )
            polarity_textblob             = sentimetsDonutChart(sentiment_analysis_textblob['polarity_title_text_textblob'], ['Pos.','Neg.'],  'Polarity',              20, ['#6495ed','#b35050'] )
            subjectivity_textblob         = sentimetsDonutChart(sentiment_analysis_subj['subjectivity_title_text_textblob'], ['Obj.','Subj.'], 'Subjectivity',          20, ['#6868a3','#9cba95'] )
            polarity_vader                = sentimetsDonutChart(sentiment_analysis_vader['polarity_title_text_vader'],       ['Pos.','Neg.'],  'Polarity',              20, ['#6495ed','#b35050'] )
            confusion_matrix_textblob     = ConfusionMatrixHeatmap(sentiment_analysis_textblob['rating'], sentiment_analysis_textblob['polarity_title_text_textblob'])
            confusion_matrix_vader        = ConfusionMatrixHeatmap(sentiment_analysis_vader['rating'], sentiment_analysis_vader['polarity_title_text_vader'])
            confusion_matrix_pie_textblob = confusion_matrix_pie_chart(sentiment_analysis_textblob['rating'], sentiment_analysis_textblob['polarity_title_text_textblob'])
            confusion_matrix_pie_vader    = confusion_matrix_pie_chart(sentiment_analysis_vader['rating'], sentiment_analysis_vader['polarity_title_text_vader'])
            classif_report_textblob       = classif_report_heatmap(sentiment_analysis_textblob['rating'], sentiment_analysis_textblob['polarity_title_text_textblob'])
            classif_report_vader          = classif_report_heatmap(sentiment_analysis_vader['rating'], sentiment_analysis_vader['polarity_title_text_vader'])
            roc_curve_textblob            = roc_curve_chart(sentiment_analysis_textblob['rating'], sentiment_analysis_textblob['polarity_title_text_textblob'])
            roc_curve_vader               = roc_curve_chart(sentiment_analysis_vader['rating'], sentiment_analysis_vader['polarity_title_text_vader'])
            review_length_hist            = review_length_histogram(sentiment_df,'rating','length_title_text')
            polarity_nbayes               = sentimetsDonutChart(y_pred, ['Pos.','Neg.'],  'Polarity', 20, ['#6495ed','#b35050'] )
            confusion_matrix_nbayes       = ConfusionMatrixHeatmap(sentiment_analysis_vader['rating'], y_pred)
            confusion_matrix_pie_nbayes   = confusion_matrix_pie_chart(sentiment_analysis_vader['rating'], y_pred)
            classif_report_nbayes         = classif_report_heatmap(sentiment_analysis_vader['rating'], y_pred)
            roc_curve_nbayes              = roc_curve_chart(sentiment_analysis_vader['rating'], y_pred)


        return (
            di,
            brand_series_value if   len(brand_series_value) !=0   else   input_value_series,
            go.Figure(data=[]) if text == '' else customer_rating,
            brandsRangePriceDropdown,
            brand_seriesRangePriceDropdown,
            go.Figure(data=[]) if text == '' else polarity_textblob,
            go.Figure(data=[]) if text == '' else subjectivity_textblob,
            go.Figure(data=[]) if text == '' else polarity_vader,
            go.Figure(data=[]) if text == '' else confusion_matrix_textblob,
            go.Figure(data=[]) if text == '' else confusion_matrix_vader,
            go.Figure(data=[]) if text == '' else confusion_matrix_pie_textblob,
            go.Figure(data=[]) if text == '' else confusion_matrix_pie_vader,
            go.Figure(data=[]) if text == '' else classif_report_textblob,
            go.Figure(data=[]) if text == '' else classif_report_vader,
            go.Figure(data=[]) if text == '' else roc_curve_textblob,
            go.Figure(data=[]) if text == '' else roc_curve_vader,
            go.Figure(data=[]) if text == '' else review_length_hist,
            loading_page,
            go.Figure(data=[]) if text == '' else polarity_nbayes,
            go.Figure(data=[]) if text == '' else confusion_matrix_nbayes,
            go.Figure(data=[]) if text == '' else confusion_matrix_pie_nbayes,
            go.Figure(data=[]) if text == '' else classif_report_nbayes,
            go.Figure(data=[]) if text == '' else roc_curve_nbayes,
        )
    
    else: # cuando es 3 viene de la otra
        resetfile('5000')

        ser  = [ ' '.join(i.split()[2:]) for i in input_value_series ]
        dataRangePriceSeries = dataRangePrice.query('brand in @input_value & series in @ser')

        sentiment_df = createSentimentDf(dataRangePriceSeries)
        sentiment_analysis_vader = getSentimentAnalysis(sentiment_df, 'vader')
        sentiment_analysis_textblob = getSentimentAnalysis(sentiment_df, 'textblob')
        sentiment_analysis_subj = getSentimentAnalysis(sentiment_df, 'subjectivity')
        y_pred = nbayes_model_wang.predict(sentiment_analysis_textblob['title_text'])

        text = ' '.join(dataRangePrice.query('brand in @input_value & series in @ser')['review_one_string'])

        if text == '':
            fignada = go.Figure(data=[])

            nada = dcc.Graph(
                style={'height':'360px'},
                figure=fignada,
                config={'displayModeBar': False}
            )
            imgCloud = nada
            di = nada
            customer_rating = None
            polarity_textblob = None
            subjectivity_textblob = None
            polarity_vader = None
            confusion_matrix_textblob = None
            confusion_matrix_vader = None
            confusion_matrix_pie_textblob = None
            confusion_matrix_pie_vader = None
            classif_report_textblob = None
            classif_report_vader = None
            roc_curve_textblob = None
            roc_curve_vader = None
            review_length_hist = None
            polarity_nbayes = None 
            confusion_matrix_nbayes = None 
            confusion_matrix_pie_nbayes = None 
            classif_report_nbayes = None 
            roc_curve_nbayes = None

        else:
            imgEmotionsBarChart = emotionsBarChart(sentiment_df)

            di = html.Div(children=[dcc.Graph(
                id='histo',
                style={'width': 'calc(100% - 50px)', 'height':'360px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'},
                figure=imgEmotionsBarChart, config={'displayModeBar': False}
            )])

            customer_rating               = sentimetsDonutChart(sentiment_analysis_textblob['rating'],                       ['Pos.','Neg.'],  'Customer<br />rating',  20, ['#007bff','#9c2828'] )
            polarity_textblob             = sentimetsDonutChart(sentiment_analysis_textblob['polarity_title_text_textblob'], ['Pos.','Neg.'],  'Polarity',              20, ['#6495ed','#b35050'] )
            subjectivity_textblob         = sentimetsDonutChart(sentiment_analysis_subj['subjectivity_title_text_textblob'], ['Obj.','Subj.'], 'Subjectivity',          20, ['#6868a3','#9cba95'] )
            polarity_vader                = sentimetsDonutChart(sentiment_analysis_vader['polarity_title_text_vader'],       ['Pos.','Neg.'],  'Polarity',              20, ['#6495ed','#b35050'] )
            confusion_matrix_textblob     = ConfusionMatrixHeatmap(sentiment_analysis_textblob['rating'], sentiment_analysis_textblob['polarity_title_text_textblob'])
            confusion_matrix_vader        = ConfusionMatrixHeatmap(sentiment_analysis_vader['rating'], sentiment_analysis_vader['polarity_title_text_vader'])
            confusion_matrix_pie_textblob = confusion_matrix_pie_chart(sentiment_analysis_textblob['rating'], sentiment_analysis_textblob['polarity_title_text_textblob'])
            confusion_matrix_pie_vader    = confusion_matrix_pie_chart(sentiment_analysis_vader['rating'], sentiment_analysis_vader['polarity_title_text_vader'])
            classif_report_textblob       = classif_report_heatmap(sentiment_analysis_textblob['rating'], sentiment_analysis_textblob['polarity_title_text_textblob'])
            classif_report_vader          = classif_report_heatmap(sentiment_analysis_vader['rating'], sentiment_analysis_vader['polarity_title_text_vader'])
            roc_curve_textblob            = roc_curve_chart(sentiment_analysis_textblob['rating'], sentiment_analysis_textblob['polarity_title_text_textblob'])
            roc_curve_vader               = roc_curve_chart(sentiment_analysis_vader['rating'], sentiment_analysis_vader['polarity_title_text_vader'])
            review_length_hist            = review_length_histogram(sentiment_df,'rating','length_title_text')
            polarity_nbayes               = sentimetsDonutChart(y_pred, ['Pos.','Neg.'],  'Polarity', 20, ['#6495ed','#b35050'] )
            confusion_matrix_nbayes       = ConfusionMatrixHeatmap(sentiment_analysis_vader['rating'], y_pred)
            confusion_matrix_pie_nbayes   = confusion_matrix_pie_chart(sentiment_analysis_vader['rating'], y_pred)
            classif_report_nbayes         = classif_report_heatmap(sentiment_analysis_vader['rating'], y_pred)
            roc_curve_nbayes              = roc_curve_chart(sentiment_analysis_vader['rating'], y_pred)

        return (
            di,
            no_update,
            go.Figure(data=[]) if text == '' else customer_rating,
            brandsRangePriceDropdown,
            brand_seriesRangePriceDropdown,
            go.Figure(data=[]) if text == '' else polarity_textblob,
            go.Figure(data=[]) if text == '' else subjectivity_textblob,
            go.Figure(data=[]) if text == '' else polarity_vader,
            go.Figure(data=[]) if text == '' else confusion_matrix_textblob,
            go.Figure(data=[]) if text == '' else confusion_matrix_vader,
            go.Figure(data=[]) if text == '' else confusion_matrix_pie_textblob,
            go.Figure(data=[]) if text == '' else confusion_matrix_pie_vader,
            go.Figure(data=[]) if text == '' else classif_report_textblob,
            go.Figure(data=[]) if text == '' else classif_report_vader,
            go.Figure(data=[]) if text == '' else roc_curve_textblob,
            go.Figure(data=[]) if text == '' else roc_curve_vader,
            go.Figure(data=[]) if text == '' else review_length_hist,
            loading_page,
            go.Figure(data=[]) if text == '' else polarity_nbayes,
            go.Figure(data=[]) if text == '' else confusion_matrix_nbayes,
            go.Figure(data=[]) if text == '' else confusion_matrix_pie_nbayes,
            go.Figure(data=[]) if text == '' else classif_report_nbayes,
            go.Figure(data=[]) if text == '' else roc_curve_nbayes,
        )



# Callback in charge of modifications in the Series field
@app.callback(
        Output(component_id='brand_div_id22',   component_property='children'),
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




# Callback for in charge of the Main Menu botton and Sidebar 
@app.callback(
    [
        Output('sidebar2',      'style'),
        Output('sidebarMenu32', 'style'),
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

