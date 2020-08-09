import dash_html_components as html
import dash_core_components as dcc

#1e2130 este podría ser el color para la dard sidebar

sidebarMenu3 = html.Div([
    html.Div(
        id='sidebarMenu3',
        className='modal',
        style={'display': 'none'}, children=[
        html.Div(
            className='modal-content',
            style={'textAlign': 'center'}, children=[
            html.Div(
                style={'textAlign': 'center', 'color':'rgba(30,33,48)'},
                children=[
                'This page is in progress. Please check back later for additional changes',
            ]),
            html.Hr(),
            html.Button(
                id='menu3CloseButton',
                style={'width':'200pt','text-align': 'center','margin': 'auto', 'border': '1.0px solid white', 'color':'white' ,'background-color':'#007bff'}, #'color':'white' ,'background-color':'#007bff'
                children=[
                    'Close'
                ]
            )
        ]),
    ])
])
# 'background-color': 'transparent


sidebar = html.Div(
    # style={'background-color': 'blue'},
    children=[
        html.Div(
            id='sidebar',
            className='w3-sidebar w3-bar-block w3-card w3-animate-left',
            style={
                'position': 'absolute',
                'margin-top':'-50pt',
                'display':'none',
                'margin-top':'500pt',
                'padding-top':'500pt'
            },
            children=[
                html.Div(
                    style={'padding-top':'3pt', 'color':'white', 'font-family':'"roboto"', 'font-size':' 20px', 'font-weight':'400', 'letter-spacing':'normal', 'line-height':'20px'},  #E6E6FA  #007bff, #f3faff
                    children=[
                        html.Div(
                            style={'position':'relative', 'height':'60pt','padding-bottom':'20pt','margin-top':'30px'},
                            # style={'position':'relative', 'height':'50pt','padding-bottom':'95pt', 'margin-top':'-30px'},
                            children=[
                                html.A(
                                    id='menuHome',
                                    # style={'position': 'absolute', 'top': '50%', 'transform': 'translateY(-50%)', 'background-color': '#E6E6FA', 'color':'#3367d6','font-weight':'700'}, #007bff,
                                    children=[
                                        dcc.Link(
                                            className='w3-bar-item w3-button',
                                            # style={'position': 'absolute', 'top': '50%', 'transform': 'translateY(-50%)', 'background-color': '#E6E6FA', 'color':'#007bff','font-weight':'600', 'font-size':' 18px'}, #007bff, #3367d6
                                            href='/home', 
                                            children='Home'
                                        )
                                    ]
                                    # href='home', className='w3-bar-item w3-button',
                                    # children='Home'
                                ),
                            ]
                        ),
                        html.Div(
                            style={'position':'relative', 'height':'50pt'},
                            children=[
                                html.A(
                                    # style={'position': 'absolute', 'top': '50%', 'transform': 'translateY(-50%)'},
                                    className='w3-bar-item w3-button',
                                        children=[
                                            dcc.Link(
                                                className='w3-bar-item w3-button',
                                                style={'text-align': 'left', 'padding':'0'},
                                                href='/sentiment',
                                                children='Sentiment Analysis'
                                            )
                                        ]
                                    # href='/app2', className='w3-bar-item w3-button',
                                    # children='Sentiment Analysis'
                                ),
                            ]
                        ),
                        html.Div(
                            style={'position':'relative', 'height':'50pt'},
                            children=[
                                html.A(
                                    id='menu3OpenButton',
                                    style={'position': 'absolute', 'top': '50%', 'transform': 'translateY(-50%)'},
                                    href='#', className='w3-bar-item w3-button',
                                    children='Load a new Dataset'
                                ),
                                sidebarMenu3
                            ]
                        ),
                    ]
                )
            ]
        ),
    ]
)

