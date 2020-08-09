import dash_html_components as html
import dash_core_components as dcc

import numpy as np
import pandas as pd
from wordcloud import WordCloud, ImageColorGenerator
import plotly.graph_objs as go
import base64
import lorem
import io
from collections import Counter
import plotly.express as px
import plotly.figure_factory as ff

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score


data = pd.read_json('./data/amazon_data.json')




def wordCloud(text):
    cloud = WordCloud(width=800, height=400, background_color="black",
                max_words=500,
                random_state=42, mode='RGBA'
                ).generate(text)
    return cloud


def img_wordCloud(cloud):
    image = cloud.to_image()
    print(image.size)
    byte_io = io.BytesIO()
    image.save(byte_io, 'PNG')
    byte_io.seek(0)
    data_uri = base64.b64encode(byte_io.getvalue()).decode('utf-8').replace('\n', '')
    src = 'data:image/png;base64,{0}'.format(data_uri)

    div = (
        html.Div(
            style={'height':'350px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'},
            children=[
                html.Img(
                    style={'height':'350px', 'width': '100%', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'},
                    src=src, width=image.size[0], height=image.size[1]
                ),
            ],
        )
    )

    return div




def wordCountBarChart(text,number):
    lista=text.split()
    counts = Counter(lista)
    dic = dict(counts.items())
    df = pd.DataFrame({'word':list(dic.keys()),'count':list(dic.values())})
    df = df.sort_values(by=['count'],ascending=True)

    fig = go.Figure([
        go.Bar(
            x=df['count'].tail(number), y=df['word'].tail(number), orientation='h', text='count'
        )
    ])
    fig.update_layout(
        # autosize=False,
        margin=go.layout.Margin(l=5, r=5, t=5, b=5),
        uniformtext_minsize=8, uniformtext_mode='hide',
        font=dict(
            # family="Courier New, monospace",
            size=17,
            color="black"
        )
    )
    fig.update_yaxes(automargin=True)

    return fig




def aveReviewsBarChart(thedata):
    ave = []
    ave = thedata.groupby('brand').describe()['average_customer_reviews']
    ave = ave.reset_index()
    ave = ave[['brand','mean']]
    ave['mean'] = ave['mean'].round(2)
    ave = ave.sort_values(by=['mean'],ascending=False)

    # https://plotly.com/python/bar-charts/
    # https://plotly.com/python/colorscales/
    fig = px.bar(ave, x='brand', y='mean', color='mean', text='mean',
                labels={'mean':'Ave. customer reviews','brand':'Brand'}, height=400)

    fig.update_layout(
        margin=go.layout.Margin(l=5, r=5, t=5, b=0), xaxis_tickangle=-20,
        uniformtext_minsize=8, uniformtext_mode='hide', coloraxis_showscale=False,
        yaxis=dict(
            title='Ave. customer reviews',
            titlefont_size=18,
            tickfont_size=20,
        ),
        xaxis=dict(
            title=None,
            titlefont_size=18,
            tickfont_size=20,
        ),
        font=dict(
            # family="Courier New, monospace",
            size=20,
            color="black"
        )
    )

    return fig



def avgReviewsBarChart(data,brands_selected,series_selected):
    brand_series_review_selected = data.query('brand in @brands_selected & series in @series_selected')[['brand','series','average_customer_reviews']]

    review_total = []
    review_total = data.groupby('brand').describe()['average_customer_reviews']
    review_total = review_total.reset_index()
    review_total = review_total[['brand','mean']]
    review_total['mean'] = review_total['mean'].round(2)
    review_total = review_total.sort_values(by=['mean'],ascending=False)
    
    if (len(brands_selected) !=0  and  len(series_selected) != 0):
        review_selected = []
        review_selected = brand_series_review_selected.groupby('brand').describe()['average_customer_reviews']
        review_selected = review_selected.reset_index()
        review_selected = review_selected[['brand','mean']]
        review_selected['mean'] = review_selected['mean'].round(2)
        review_selected = review_selected.sort_values(by=['mean'],ascending=False)    

        review_total_selected = pd.merge(review_total,review_selected,on='brand',how='outer')

        review_total_list = list(review_total_selected['mean_x'])
        review_selected_list = list(review_total_selected['mean_y'])
        brands = list(review_total_selected['brand'])
    else:
        review_total_list = list(review_total['mean'])
        review_selected_list = [None] * len(review_total_list)
        brands = list(review_total['brand'])

    
    fig = go.Figure(data=[
        go.Bar(name='All items',    x=brands, y=review_total_list, text=review_total_list),
        go.Bar(name='Selected items', x=brands, y=review_selected_list, text=review_selected_list)
    ])

    fig.update_traces(texttemplate='%{text:.3s}', textposition='inside')

    fig.update_layout(
        margin=go.layout.Margin(l=5, r=5, t=20, b=0), xaxis_tickangle=-20,
        uniformtext_minsize=8, uniformtext_mode='hide', coloraxis_showscale=False,
        yaxis=dict(
            title='Avg. customer reviews (1-5)',
            # title='Avg. customer reviews rating (1-5)',
            titlefont_size=18,
            tickfont_size=1,
        ),
        xaxis=dict(
            title=None,
            titlefont_size=18,
            tickfont_size=15,
        ),
        font=dict(
            # family="Courier New, monospace",
            size=20,
            color="black"
        ),
        legend_orientation="h",
        legend=dict(x=.19, y=1.15)
    )

    return fig




def avgPricesBarChart(data,brands_selected,series_selected):
    brand_series_price_selected = data.query('brand in @brands_selected & series in @series_selected')[['brand','series','price']]

    price_total = []
    price_total = data.groupby('brand').describe()['price']
    price_total = price_total.reset_index()
    price_total = price_total[['brand','mean']]
    price_total['mean'] = price_total['mean'].round(2)
    price_total = price_total.sort_values(by=['mean'],ascending=False)
    
    if (len(brands_selected) !=0  and  len(series_selected) != 0):
        price_selected = []
        price_selected = brand_series_price_selected.groupby('brand').describe()['price']
        price_selected = price_selected.reset_index()
        price_selected = price_selected[['brand','mean']]
        price_selected['mean'] = price_selected['mean'].round(2)
        price_selected = price_selected.sort_values(by=['mean'],ascending=False)    

        price_total_selected = pd.merge(price_total,price_selected,on='brand',how='outer')

        price_total_list = list(price_total_selected['mean_x'])
        price_selected_list = list(price_total_selected['mean_y'])
        brands = list(price_total_selected['brand'])
    else:
        price_total_list = list(price_total['mean'])
        price_selected_list = [None] * len(price_total_list)
        brands = list(price_total['brand'])

    
    fig = go.Figure(data=[
        go.Bar(name='All items',      x=brands, y=price_total_list, text=price_total_list),
        go.Bar(name='Selected items', x=brands, y=price_selected_list, text=price_selected_list)
    ])

    fig.update_traces(texttemplate='%{text:.3s} $', textposition='inside')

    fig.update_layout(
        margin=go.layout.Margin(l=5, r=5, t=20, b=0), xaxis_tickangle=-20,
        uniformtext_minsize=8, uniformtext_mode='hide', coloraxis_showscale=False,
        yaxis=dict(
            title='Avg. price ($)',
            titlefont_size=18,
            tickfont_size=13,
        ),
        xaxis=dict(
            title=None,
            titlefont_size=18,
            tickfont_size=15,
        ),
        font=dict(
            size=20,
            color="black"
        ),
        legend_orientation="h",
        legend=dict(x=.13, y=1.15)
    )

    return fig




def avgVsPriceBubbleChart():
    fig = px.scatter(data, x="price", y="average_customer_reviews",
                    size="average_customer_reviews", color="brand",
                    hover_name="brand", log_x=False, size_max=30)

    fig.update_layout(
            margin=go.layout.Margin(l=5, r=5, t=10, b=0), xaxis_tickangle=0,
            uniformtext_minsize=8, uniformtext_mode='hide', coloraxis_showscale=False,
            yaxis=dict(
                title='Avg. customer reviews (1-5)',
                titlefont_size=18,
                tickfont_size=13,
            ),
            xaxis=dict(
                title='Prices ($)',
                titlefont_size=18,
                tickfont_size=15,
            ),
            font=dict(
                size=20,
                color="black"
            ),
            legend_title="Brand",
    )

    return fig




# def wordCountBarChart(cloud):
#     x = np.array(list(cloud.words_.keys()))
#     y = np.array(list(cloud.words_.values()))
#     order = np.argsort(y)[::-1]
#     # x = x[order]
#     # y = y[order]
#     trace = go.Bar(x=x, y=y)
#     layout = go.Layout(margin=go.layout.Margin(l=0, r=0, t=0, b=0))  #, title='Relative frequency of words/bigrams')
#     fig = go.Figure(data=[trace], layout=layout)
#     div = html.Div([
#         dcc.Graph(id='word-freq', figure=fig, config={'displayModeBar': False})
#     ])
#     return div
# text = ' '.join(data[data['brand']=='Samsung']['review_one_string'])




# This function, unlike the one above, allows plotting the Emotion analysis using the vector of emotions related to the review. 
# In «data_analysis.ipynb» we are performing the emotion analysis for all the reviews and storing the corresponding emotion vector for each entry. 
# This has been done because this analysis requires considerable computational time. So, if this analysis is performed in real-time when running the Web application, this would make the Web Application very slow.
def emotionsBarChart(sentiment_df):
    emo = pd.Series([np.array(lista) for lista in sentiment_df['emotions']])
    emoSum = emo.sum()
    counterEmo_df = pd.DataFrame({'emotion': 'anger anticipation disgust fear joy negative positive sadness surprise trust'.split(),
                                  'count':    emoSum})
    counterEmo_df = counterEmo_df.sort_values(by=['count'],ascending=True)

    fig = go.Figure([
        go.Bar(
            x=counterEmo_df['count'], y=counterEmo_df['emotion'], orientation='h', text='count'
        )
    ])
    fig.update_layout(
        # autosize=False,
        margin=go.layout.Margin(l=5, r=5, t=5, b=5),
        uniformtext_minsize=8, uniformtext_mode='hide',
        font=dict(
            # family="Courier New, monospace",
            size=17,
            color="black"
        )
    )
    fig.update_yaxes(automargin=True)
    fig.update_traces(marker_color='#007bff')

    return fig


# def emotionsBarChart(text):
#     filepath = ('data/NRC-Sentiment-Emotion-Lexicons/'
#                 'NRC-Emotion-Lexicon-v0.92/'
#                 'NRC-Emotion-Lexicon-Wordlevel-v0.92.txt')
            
#     lexiEmo_df0  = pd.read_csv(filepath,
#                             names=["word", "emotion", "association"],
#                             sep='\t')

#     lexiEmo_df  = lexiEmo_df0.pivot(index='word',
#                                     columns='emotion',
#                                     values='association').reset_index()

#     counterEmo = pd.Series(data=np.zeros(11).astype(int),index=lexiEmo_df.columns)
#     counterEmo.drop(index=['word'],inplace=True)

#     # text = amazon_data['review_one_string'].iloc[0]
#     text_list = [word for word in text.split()]
#     # text_list = [word for word in 'esta es una prueba'.split()]

#     # palabra = 'abandon'
#     # palabras = ['abandon','abandoned','abacus']# palabra = 'abandon'
#     # palabras = ['abandon','abandoned','abacus']
#     for palabra in text_list:
#         if palabra in lexiEmo_df['word'].tolist():
#             i = lexiEmo_df.index[lexiEmo_df['word'] == palabra].tolist()
#             vectorEmo = lexiEmo_df.iloc[i[0]]
#             vectorEmo.drop(index=['word'],inplace=True)
#             counterEmo = counterEmo + vectorEmo

#     # if palabra in lexiEmo_df['word'].tolist():
#     #     i = lexiEmo_df.index[lexiEmo_df['word'] == palabra].tolist()
#     #     vectorEmo = lexiEmo_df.iloc[i[0]]
#     #     vectorEmo.drop(index=['word'],inplace=True)

#     counterEmo_df = pd.DataFrame(counterEmo)
#     counterEmo_df = counterEmo_df.rename(columns={0:'count'})
#     counterEmo_df = counterEmo_df.reset_index()

#     counterEmo_df = counterEmo_df.sort_values(by=['count'],ascending=True)

#     fig = go.Figure([
#         go.Bar(
#             x=counterEmo_df['count'], y=counterEmo_df['emotion'], orientation='h', text='count'
#         )
#     ])
#     # fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
#     #               marker_line_width=1.5, opacity=0.6)
#     # fig.update_traces(marker_color='#a8113c')
#     fig.update_layout(
#         # autosize=False,
#         margin=go.layout.Margin(l=5, r=5, t=5, b=5),
#         uniformtext_minsize=8, uniformtext_mode='hide',
#         font=dict(
#             # family="Courier New, monospace",
#             size=17,
#             color="black"
#         )
#     )
#     fig.update_yaxes(automargin=True)
#     fig.update_traces(marker_color='#007bff')

#     return fig



# This function returns a list
def concaLists(serie_entry):
        return [value for lista in serie_entry.tolist() for value in lista]

# This function return a dataset with only review details with sentiment analysis
def createSentimentDf(data):
    brand, series, price  = [], [], []
    for  n  in  range(len(data)):
        brand  += [data['brand'].iloc[n]]  * data['number_of_reviews'].iloc[n] 
        series += [data['series'].iloc[n]] * data['number_of_reviews'].iloc[n] 
        price  += [data['price'].iloc[n]]  * data['number_of_reviews'].iloc[n] 

    return   pd.DataFrame({'title'                            : concaLists(data['review_title']),
                           'text'                             : concaLists(data['review_text']),
                           'title_text'                       : concaLists(data['review_title_text']),
                           'rating'                           : concaLists(data['review_rating']),
                           'polarity_title_textblob'          : concaLists(data['polarity_title_textblob']),
                           'subjectivity_title_textblob'      : concaLists(data['subjectivity_title_textblob']),
                           'polarity_title_vader'             : concaLists(data['polarity_title_vader']),
                           'polarity_text_textblob'           : concaLists(data['polarity_text_textblob']),
                           'subjectivity_text_textblob'       : concaLists(data['subjectivity_text_textblob']),
                           'polarity_text_vader'              : concaLists(data['polarity_text_vader']),
                           'polarity_title_text_textblob'     : concaLists(data['polarity_title_text_textblob']),
                           'subjectivity_title_text_textblob' : concaLists(data['subjectivity_title_text_textblob']),
                           'polarity_title_text_vader'        : concaLists(data['polarity_title_text_vader']),
                           'emotions'                         : concaLists(data['emotions']),
                           'length_title_text'                : concaLists(data['length_title_text']),
                           'brand'                            : brand,
                           'series'                           : series,
                           'price'                            : price
                           })



def sentimetsDonutChart(y, labels, title1, title1_size, colors):
    
    if labels[0] == 'Pos.':
        n_pos = len(y[y == 'positive'])
        n_neg = len(y[y == 'negative'])
    else:
        n_pos = len(y[y == 'objective'])
        n_neg = len(y[y == 'subjective'])
            
    values = [n_pos, n_neg]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
    fig.update_layout(
        margin=go.layout.Margin(l=0, r=0, t=10, b=10),
        showlegend=False,
        annotations=[dict(text=title1, x=0.5, y=0.5, font_size=title1_size, showarrow=False)])
    fig.update_traces(textinfo='label+percent', textfont_size=18, 
                      marker=dict(colors=colors) )
    return fig



# This function takes the «reviews dataframe with sentiment polarities» and a «sentiment_library» argument:
#  * Removes the neutral reviews based on the customer rating (an Amazon customer
#    rating of 3 is considered a neutral review),
#  * Labels the Sentiment polarity as «positive» or «negative» depending on the polarity score
#    given by TextBlob or Vader.
#  * Return a new dataframe with 2 columns: 
#     - The true sentiment given by the «Amazon customer rating» (y_true)
#     - The predicted Sentiment given by the Sentiment Analysis library (y_pred)

def getSentimentAnalysis(reviews_sent_polarities, sentiment_library):

    if sentiment_library == 'textblob':
        polarity_columns = 'polarity_title_text_textblob'
        # Here we remove the neutral entries
        sent_analysis_df = reviews_sent_polarities[ (reviews_sent_polarities['rating'] != 3) ][['title_text','rating',polarity_columns]]
        # display(sent_analysis_df)
        # Because we have alredy removed the neutral entris and so there are no «rating = 3» or «polarity_title_text_textblob = 0», we can select the «positive» and «negative» polarities this way:
        sent_analysis_df['rating'] = ['positive' if polarity > 3 else 'negative' for polarity in sent_analysis_df['rating'].tolist()]
        sent_analysis_df[polarity_columns] = ['positive' if polarity > 0 else 'negative' for polarity in sent_analysis_df[polarity_columns].tolist()]
        # display(sent_analysis_df)

    elif sentiment_library == 'vader':
        polarity_columns = 'polarity_title_text_vader'
        sent_analysis_df = reviews_sent_polarities[ (reviews_sent_polarities['rating'] != 3) ][['title_text','rating',polarity_columns]]
        # display(sent_analysis_df)
        sent_analysis_df['rating'] = ['positive' if polarity > 3 else 'negative' for polarity in sent_analysis_df['rating'].tolist()]
        sent_analysis_df[polarity_columns] = ['positive' if polarity > 0 else 'negative' for polarity in sent_analysis_df[polarity_columns].tolist()]
        # display(sent_analysis_df)

    else:
        polarity_columns = 'subjectivity_title_text_textblob'
        sent_analysis_df = reviews_sent_polarities[ (reviews_sent_polarities['rating'] != 3) ][['title_text','rating',polarity_columns]]
        # display(sent_analysis_df)
        sent_analysis_df['rating'] = ['positive' if polarity > 3 else 'negative' for polarity in sent_analysis_df['rating'].tolist()]
        sent_analysis_df[polarity_columns] = ['objective' if subjectivity > 0.5 else 'subjective' for subjectivity in sent_analysis_df[polarity_columns].tolist()]
        # display(sent_analysis_df)

    return sent_analysis_df




# https://plotly.com/python/annotated-heatmap/#simple-annotated-heatmap
# https://stackoverflow.com/questions/60860121/plotly-how-to-make-an-annotated-confusion-matrix-using-a-heatmap

# This function takes:
# * y_true: The Amazon customer rating («positive» / «negative»)
# * y_pred: the Sentiment polarity («positive» / «negative») predicted
# Return nice visualization of the Confusion Matrix using a Heatmap chart
def ConfusionMatrixHeatmap(y_true, y_pred):
    cm = pd.DataFrame(
        confusion_matrix(y_true, y_pred, labels=['positive','negative']), 
        index   = ['Actual:positive',    'Actual:negative'   ], 
        columns = ['Predicted:positive', 'Predicted:negative'],
    )

    TP = cm['Predicted:positive']['Actual:positive']
    FN = cm['Predicted:negative']['Actual:positive']
    FP = cm['Predicted:positive']['Actual:negative']
    TN = cm['Predicted:negative']['Actual:negative']

    cm_anotations = [['TP<br />{}'.format(TP),'FN<br />{}'.format(FN)],
                    ['FP<br />{}'.format(FP),'TN<br />{}'.format(TN)]]
    cm_colors = [[0,1],[1,0]]
    fig = ff.create_annotated_heatmap(
        cm_colors, 
        x=['Positive', 'Negative'], 
        y=['Positive', 'Negative'], 
        annotation_text=cm_anotations, 
        colorscale = [[0, '#6495ED'], [1, '#b35050']],
    )
    fig['layout']['yaxis']['autorange'] = "reversed"
    fig.update_layout(
        yaxis=dict(
                title='Current  value',
                titlefont_size=20,
                tickfont_size=20,
                color="black",
        ),
        xaxis=dict(
                title='Predicted  value',
                titlefont_size=20,
                tickfont_size=20,
                color="black",
        ),
        font=dict(
            size=25,
        )
    )
    fig.update_layout(margin=dict(t=1, b=1, r=1, l=1), yaxis_tickangle=-90)

    return fig



def confusion_matrix_pie_chart(y_true, y_pred):
    cm = pd.DataFrame(
        confusion_matrix(y_true, y_pred, labels=['positive','negative']), 
        index   = ['Actual:positive',    'Actual:negative'   ], 
        columns = ['Predicted:positive', 'Predicted:negative'],
    )
    
    TP = cm['Predicted:positive']['Actual:positive']
    FN = cm['Predicted:negative']['Actual:positive']
    FP = cm['Predicted:positive']['Actual:negative']
    TN = cm['Predicted:negative']['Actual:negative']
    
    values = [TP,    TN,   FP,   FN]
    labels = ['TP', 'TN', 'FP', 'FN']

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, direction='clockwise', sort=False )])
    fig.update_layout(
        margin=go.layout.Margin(l=0, r=0, t=10, b=10),
        showlegend=False,
        # annotations=[dict(text=title1, x=0.5, y=0.5, font_size=title1_size, showarrow=False)]
    )
    fig.update_traces(textinfo='label+percent', textfont_size=18, 
                      marker=dict(colors=['#6495ED','#007bff','#b35050','#9c2828']) )
    
    return fig




def classif_report_heatmap(y_true, y_pred):
   print('\nClassification report:')
   
   classif_report_string = classification_report(y_true, y_pred, labels=['positive','negative'], output_dict=False)
   classif_report_dic    = classification_report(y_true, y_pred, labels=['positive','negative'], output_dict=True)

   classif_report_colors = np.array([[
                  round(classif_report_dic['positive']['precision'],2),
                  classif_report_dic['positive']['recall'],
                  classif_report_dic['positive']['f1-score'],
                  .0
               ],
               [
                  classif_report_dic['negative']['precision'],
                  classif_report_dic['negative']['recall'],
                  classif_report_dic['negative']['f1-score'],
                  .0
               ],
               [
                  .0,
                  .0,
                  .0,
                  .0,
               ],
               [
                  .0,
                  .0,
                  classif_report_dic['accuracy'],
                  .0,
               ],
               [
                  classif_report_dic['macro avg']['precision'],
                  classif_report_dic['macro avg']['recall'],
                  classif_report_dic['macro avg']['f1-score'],
                  .0
               ],
               [
                  classif_report_dic['weighted avg']['precision'],
                  classif_report_dic['weighted avg']['recall'],
                  classif_report_dic['weighted avg']['f1-score'],
                  .0
               ]])

   classif_report_colors = np.round(np.array(classif_report_colors), 2)

   classif_report_anotations = [ [str(value) for value in fila] for fila in classif_report_colors]

   classif_report_anotations[2]    = [' ' for a in classif_report_anotations[2]]
   classif_report_anotations[3][0] =  ' '
   classif_report_anotations[3][1] =  ' '

   classif_report_anotations[0][3] = classif_report_dic['positive']['support']
   classif_report_anotations[1][3] = classif_report_dic['negative']['support']
   classif_report_anotations[3][3] = classif_report_dic['macro avg']['support']
   classif_report_anotations[4][3] = classif_report_dic['macro avg']['support']
   classif_report_anotations[5][3] = classif_report_dic['weighted avg']['support']

   fig = ff.create_annotated_heatmap(
      classif_report_colors, 
      x=['precision','recall','f1-score','support'],
      y=['positive','negative',' ','accuracy','macro avg','weighted avg'], 
      annotation_text=classif_report_anotations, 
      colorscale=[[ 0,  'white'],
                  [.01, 'red'],
                  [.3,  '#f75454'],
                  [.5,  '#eb8d8d'],
                  [.7,  '#a5bdfa'],
                  [.8,  '#779bf7'],
                  [.9,  '#366eff'],
                  [ 1,  '#0048ff']]
   )
   fig['layout']['yaxis']['autorange'] = "reversed"
   fig.update_layout(
      yaxis=dict(
               titlefont_size=25,
               tickfont_size=18,
               color="black",
      ),
      xaxis=dict(
               titlefont_size=25,
               tickfont_size=18,
               color="black",
      ),
      font=dict(
         size=20,
      ),
      margin=dict(t=20, b=20, r=20, l=20)
   )
   fig['data'][0]['showscale'] = True
   return fig



def roc_curve_chart(y_true, y_pred):
    # auc = roc_auc_score(testy, probs)
    y_true_bin = [0 if v == 'positive' else 1 for v in y_true ]
    y_pred_bin = [0 if v == 'positive' else 1 for v in y_pred ]
    auc = roc_auc_score(y_true_bin, y_pred_bin)
    fpr, tpr, thresholds = roc_curve(y_true_bin, y_pred_bin)

    lw = 3
    trace1 = go.Scatter(x=fpr, y=tpr, 
                        mode='lines', 
                        line=dict(color='#b35050', width=lw),
                        name='ROC curve (area = %0.2f)' % auc
                    )
    trace2 = go.Scatter(x=[0, 1], y=[0, 1], 
                        mode='lines', 
                        line=dict(color='#007bff', width=lw, dash='dash'), # color='navy'
                        showlegend=False)
    layout = go.Layout(title='',
                    xaxis=dict(title='False Positive Rate'),
                    yaxis=dict(title='True Positive Rate'))
    fig = go.Figure(data=[trace1, trace2], layout=layout)

    margin=dict(t=0, b=0, r=20, l=20)

    fig.update_layout(
        # title_text='<i><b>Confusion matrix</b></i>',
        legend=dict(
            x=0.48,
            y=0.03,
            traceorder='normal',
            font=dict(
                size=20,
                color="black"
            ),
        ),
        yaxis=dict(
                # title='Current  value',
                titlefont_size=20,
                tickfont_size=18,
                color="black",
        ),
        xaxis=dict(
                # title='Predicted  value',
                titlefont_size=20,
                tickfont_size=18,
                color="black",
        ),
        font=dict(
            # family="Courier New, monospace",
            size=20,
            # color="red"
        ),
        margin=dict(t=20, b=20, r=30, l=20)
    )
    return fig



def review_length_histogram(df,column_rating,column_length,labeled=None):
    if labeled == None:
        df = df[df[column_rating] != 3]
        df['label'] = ['positive' if rating > 3 else 'negative' for rating in df[column_rating] ]

    df = df.sort_values(by=['label'], ascending=False)
    n_reviews = len(df)
    n_pos = len(df[df['label'] == 'positive'])
    n_neg = len(df[df['label'] == 'negative'])
    n_pos_percent = round((n_pos*100)/n_reviews)
    n_neg_percent = round((n_neg*100)/n_reviews)

    fig = px.histogram(df, x=column_length, color="label",  barmode="overlay", nbins=150, opacity=0.75, 
                    marginal="box",)  # or violin, rug)
    fig.update_layout(
            margin=go.layout.Margin(l=0, r=40, t=0, b=0), xaxis_tickangle=0,
            uniformtext_minsize=8, uniformtext_mode='hide', coloraxis_showscale=False,
            yaxis=dict(
                title='Count',
                titlefont_size=15,
                tickfont_size=15,
            ),
            xaxis=dict(
                title='Review length (number of characters)',
                titlefont_size=15,
                tickfont_size=15,
            ),
            font=dict(
                size=15,
                color="black"
            ),
            legend=dict(
                y=0.7,
                x=0.77,
                title='<span style="font-weight:bold; font-size:18px">{}</span> <span style="font-weight:normal; font-size:16px"> cust. reviews</span><br /><span style="color:blue">   {} ({}%)</span><br /><span style="color:red">   {} ({}%)</span>'.format(n_reviews, n_pos, n_pos_percent, n_neg, n_neg_percent),
                font=dict(
                    size=15,
                ),
            ),
        )
    return fig



# # Defining our stopwords list:
# import nltk
# import string
# nltk.data.path.append('/home/adelo/.nltk/nltk_data')
# from nltk.corpus import stopwords

# stopwords_brands_additionals = ['computer','computers','laptop','laptops','thing','things','machine','machines','im','dont','ive']
# stopwords_total  = stopwords.words('english') + stopwords_brands_additionals

# # The following function takes a string and an optional argument «tokenize»:
# # * It removes punctuation and stopwords from the string entered
# # * If the «tokenize» argument if not specified, the string will be tokenized so it will return 
# #   a list of the word without punctuation or stopwords
# # * If a tokenize argument is specified, the string will NOT be tokenized, so it will return
# #   a string without punctuation or stopwords
# def pre_processing(texto,tokenize=None):
#     # Removing punctuation:
#     text_process = ''.join([ char for char in texto if char not in string.punctuation ])
#     # Removing Stopwords:
#     text_process = ' '.join([ word for word in text_process.split() if word.lower() not in stopwords_total ])
#     if tokenize == None:
#         return [word for word in text_process.split()]
#     else:
#         return text_process
        


# cloud = wordCloud(text)
# imgCloud = img_wordCloud(cloud)
# imgHistoWords = wordCountBarChart(text,50)
textfield = dcc.Textarea(id='text-field', style={'height': 250, 'width': '100%'}, value=lorem.paragraph())



