import dash_html_components as html


sidebarMenu3 = html.Div([
    html.Div(
        id='sidebarMenu3',
        className='modal',
        style={'display': 'none'}, children=[
        html.Div(
            className='modal-content',
            style={'textAlign': 'center'}, children=[
            html.Div(
                children=[
                'Hola. This page is in progress. Please check back later for additional changes',
            ]),
            html.Hr(),
            html.Button('Close', id='menu3CloseButton')
        ]),
    ])
])


sidebar = html.Div(
    children=[
        html.Div(
            id='sidebar',
            className='w3-sidebar w3-bar-block w3-card w3-animate-left',
            style={
                'position': 'absolute',
                'margin-top':'-50pt',
                'display':'none',
                'background-color': 'black', #E6E6FA  #007bff,
                'margin-top':'500pt',
                'padding-top':'500pt'
            },
            children=[
                html.Div(
                    style={'padding-top':'3pt','background-color': '#fff', 'color':'black', 'font-family':'"roboto"', 'font-size':' 18px', 'font-weight':'400', 'letter-spacing':'normal', 'line-height':'20px'},  #E6E6FA  #007bff, #f3faff
                    children=[
                        html.Div(
                            style={'position':'relative', 'height':'50pt'},
                            children=[
                                html.A(
                                    id='menuHome',
                                    style={'position': 'absolute', 'top': '50%', 'transform': 'translateY(-50%)', 'background-color': '#E6E6FA', 'color':'#3367d6','font-weight':'700'}, #007bff,
                                    href='home', className='w3-bar-item w3-button',
                                    children='Home'
                                ),
                            ]
                        ),
                        html.Div(
                            style={'position':'relative', 'height':'50pt'},
                            children=[
                                html.A(
                                    style={'position': 'absolute', 'top': '50%', 'transform': 'translateY(-50%)'},
                                    href='#', className='w3-bar-item w3-button',
                                    children='Sentiment Analysis'
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

