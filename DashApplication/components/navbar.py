import dash_html_components as html
import dash_bootstrap_components as dbc


search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type='search', placeholder='Search', style={'max-height':'24pt','font-size':'10pt'})),
        dbc.Col(
            dbc.Button('Search', color='secondary', className='ml-2', style={'max-height':'24pt','font-size':'10pt'}),
            width='auto',
           
        ),
    ],
    no_gutters=True,
    className='ml-auto flex-nowrap mt-3 mt-md-0',
    align='center',
)


navbar = dbc.Navbar(
    className='noSelection',
    style={'max-height': '34pt','position':'fixed','width':'100%','z-index': '150'},
    children=[
        html.A(
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            html.Button(
                                id='sidebarButton',
                                style={
                                    'font-weight':'normal', 'font-size':'17pt', 'color':'white',
                                    'padding': '0px 3px 10px 4px',
                                    'border-width':'0pt',
                                    'margin-right':'20pt', 
                                    'margin-top':'3pt', 
                                    'outline':'none',
                                },
                                children='☰'
                            ),
                        ]
                    ),
                    dbc.Col(dbc.NavbarBrand(
                        className='ml-2',
                        children=[
                            html.Div(
                                children=[
                                    html.I(
                                        className='fa fa-globe',
                                        style={'font-size':'36px', 'color': '#E6E6FA',},  #E6E6FA  #ADD8E6  #f3faff  # rgb(29, 161, 242)
                                        children=''
                                    ),
                                    html.Span(
                                        style={'font-size':'14pt','font-weigth':'normal','position': 'relative', 'top':'1.5pt'},
                                        children=[
                                            #' Ⓢ', ' §',
                                        ]
                                    ),
                                    html.I(
                                        style={'color':'#E6E6FA', 'font-family':'"roboto"', 'font-size':' 24px', 'font-weight':'500', 'letter-spacing':'normal', 'line-height':'20px'},  #E6E6FA  #007bff, #f3faff
                                        # style={'font-size':'20px', 'color': '#E6E6FA', 'font-weigth':'normal'},  #E6E6FA  #ADD8E6  #f3faff  # rgb(29, 161, 242)
                                        children=' Amazon Laptops Dashboard'
                                    ),
                                    # html.Span(
                                        # style={'font-size':'13pt','font-weigth':'normal','position': 'relative', 'top':'1.5pt'},
                                        # children=[
                                            # ' sinfronteras',
                                        # ]
                                    # ),
                                ]
                            )
                        ]
                    )),
                ],
                align='center',
                no_gutters=True,
            ),
            # href='https://plot.ly',
        ),
        dbc.NavbarToggler(id='navbar-toggler'),
        dbc.Collapse(search_bar, id='navbar-collapse', navbar=True,style={'max-height':'5pt',},),
    ],
    color='primary',
    # color='dark',
    dark=True,
)


navbar2 = html.Div(
    id='navbar2',
    style={
        'position': 'static',
        # 'background-color': '#007bff'  #E6E6FA,  rgb(29, 161, 242)
        'background-color': '#E6E6FA',
        'min-height':'15pt',
        'max-height':'15pt',
    },
)
