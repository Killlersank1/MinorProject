import pandas as pd
import dash
import dash_table
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import datetime
import flask
import plotly.express as px 
import plotly.graph_objs as go # (need to pip install plotly==4.4.1)

df = pd.read_csv('sales_updated.csv')
df['Ship Date'] = pd.to_datetime(df['Ship Date'])
resampled = df.resample('M',on = 'Ship Date').sum().reset_index()
resampled['month']=resampled['Ship Date'].apply(lambda x : x.strftime('%B'))
#df = pd.DataFrame()
#df['Ship ']
app = dash.Dash()
# ---------------------------------------------------------------
app.layout = html.Div([
    
    # a header and a paragraph --------------------------
    html.Div([
        html.H1("SUPERMARKET SALES ANALYSIS AND PREDICTION"),

    ],
        style={'padding': '30px',
               'backgroundColor': '#8ADAD0',
            #    'color': '#6A6A6A',
               'textAlign':'center',
               'opacity':'0.8'
               }),
    #Sub Title---------------------------------------------------
    html.Div([
        html.H2("Number of sales"),
        ],
        style={'width': '49%', 'display': 'inline-block',
               'backgroundColor': '#BEE6E1',
               'opacity': '0.6',
               'color': '#000000',
               
         }),
         #Data Table Title --------------------------------------
    html.Div([
        html.H2("Profits : "),
        ],
        style={
            'width': '51%', 'display': 'inline-block',
            'left-padding' : '3em',
            'backgroundColor': '#BEE6E1',
            'opacity': '0.6',
            'color': '#000000',       
         }),
    # For Tabs--------------------------------------------------
    html.Div([
        dcc.Tabs(
            id='my_Tab',
            value='Category',
            children=[
                dcc.Tab(label='Category', value='Category'),
                dcc.Tab(label='Sub-Category', value='Sub-Category')
            ], 

             style= {'width': '49%', 'display': 'inline-block',
                     'backgroundColor': '#f3f3f3'}
        ),
    ]),
    # PieChart--------------------------------------------------
    html.Div([
        dcc.Graph(id='the_graph',)
    ],
        style={'width': '49%', 'display': 'inline-block',
               'backgroundColor': '#22C1AD'
               }
    ),
    #Drop Down For Data table----------------------------------------------
    html.Div([
        #Dropdown---------------------------------------------------
        html.Div([
            dcc.Dropdown(
            id='year-dropdown',
         options=[
            {'label': '2014', 'value': '2014'},
            {'label': '2015', 'value': '2015'},
            {'label': '2016', 'value': '2016'},
            {'label': '2017', 'value': '2017'},
            {'label': '2018', 'value': '2018'}
        ],
            value='2014',
            searchable = True,
            clearable = False
            ),
        html.Button(
            'Update',
            id = 'editing-datatable',
            n_clicks = 0
        )
        ]
        ),
        html.Div([
        dash_table.DataTable(
            id = 'year-datatable', 
            columns = [
                {'name' : 'Month', 'id' : 'month'},
                {'name' : 'Profit', 'id' : 'Profit'}
            ],
            page_size = 12
            )
        ],
            
    ),   
    ],
     style={'width': '50%', 'display': 'inline-block',
               'backgroundColor': '#F3F3F3', 'float':'right',
               }   
    ),
    
    
    # Bar Graph--------------------------------------------
    html.Div([
        dcc.Graph(
            id='graph-with-slider'),
        dcc.Slider(
            id='year-slider',
            min=df['year'].min(),
            max=df['year'].max(),
            value=df['year'].min(),
            # color=df['Category'],
            marks={str(year): str(year) for year in df['year'].unique()},
            step=None
        )
    ],
        style={
        'backgroundColor':  '#f3f3f3',
        'padding': '20px',
        'color': '#ffffff'

    },),
    # a footer
    html.Div([
        

    ],
        style={'padding': '30px',
               'backgroundColor': '#f3f3f3',
               
               }),


],
    style={
    'backgroundColor': '#f3f3f3',
    
  
},)

# ---------------------------------------------------------------

# Pie Chart---------------------------


@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='my_Tab', component_property='value')]
)
def update_graph(my_Tab):
    dff = df
    piechart = px.pie(
        data_frame=dff,
        names=my_Tab,
        #values = 'Sub-Category',
        hole=.3,  
    )
    return (piechart)

# Bar Graph---------------------------------


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]
    traces = []
    for i in filtered_df.Category.unique():
        df_by_Category = filtered_df[filtered_df['Category'] == i]
        traces.append(dict(
            x=df_by_Category['month'],
            y=df_by_Category['Sales'],
            type='bar',
            opacity=0.7,
            marker={
                'size': 00,
                'line': {'width': 0, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'type': 'bar', 'title': 'Months',
                   },
            yaxis={'title': 'Sales(in Thousand)'},
            x_label=df_by_Category['month'],
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            transition={'duration': 500},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'

        )
    }
@app.callback(
    Output('year-datatable', 'data'),
    [Input('year-dropdown', 'value'),
    Input('editing-datatable', 'n_clicks')]
    )
def update_datatable(year_value,n_clicks):
    if n_clicks > 0 :
        filtered_df = df[df['year'] == year_value]
        resampled_df = filtered_df.resample('M',on = 'Ship Date').sum().reset_index()
        resampled_df['month'] = resampled_df['Ship Date'].apply(lambda x : x.month)
        return resampled_df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)