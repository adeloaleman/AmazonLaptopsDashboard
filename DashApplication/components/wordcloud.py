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


data = pd.read_json('./data/data.json')




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




def img_histoWords(text,number):
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




def aveReviews(thedata):
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




def avgReviews(data,brands_selected,series_selected):
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




def avgPrices(data,brands_selected,series_selected):
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
        go.Bar(name='All items',    x=brands, y=price_total_list, text=price_total_list),
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




def avgVsPrice():
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




# def img_histoWords(cloud):
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
# text = ' '.join(data[data['brand']=='Samsung']['reviews_one_string'])




# cloud = wordCloud(text)
# imgCloud = img_wordCloud(cloud)
# imgHistoWords = img_histoWords(text,50)
textfield = dcc.Textarea(id='text-field', style={'height': 250, 'width': '100%'}, value=lorem.paragraph())



