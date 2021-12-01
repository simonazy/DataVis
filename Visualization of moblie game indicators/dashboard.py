#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 16:24:19 2020

@author: bravery_simon
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
import numpy as np

app = dash.Dash(
    meta_tags=[{"name": "viewport", "content": "width=device-width"}])

df = pd.read_csv('./topline_metrics.csv')
df.drop_duplicates(subset=None, keep='first', inplace=True)
df['DAU/TRU'] = df['DAU']/df['TRU']
df['Date.1'] = pd.to_datetime(df['Date'])
df['month'] = df['Date.1'].apply(lambda x: x.strftime('%m/%Y'))
all_month = df['month'].unique()

app.layout = html.Div([
    dcc.Store(id="aggregate_data"),
    # empty Div to trigger javascript file for graph resizing
    html.Div(id="output-clientside"),
    # ---------------- title -----------------------
    html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.H1(
                                "A Game Dataset",
                                style={"margin-bottom": "0px"},
                            ),
                            html.H3(
                                "Dashboard Overview", style={"margin-top": "0px"}
                            ),
                        ]
                    )
                ],
                className="one-half column",
                id="title",
            ),
            html.Div(
                [
                    html.A(
                        html.Button("My presentation", id="learn-more-button"),
                        href="/assets/presentation.pdf", download='presentation.pdf'
                    )
                ],
                className="one-third column",
                id="button",
            ),
        ],
        id="header",
        className="row flex-display",
        style={"margin-bottom": "25px", 'textAlign': 'center'},
    ),
    # --------------------- country filter ---------------------
    html.Div([
        html.P(
            "Choose your country:",
            className="control_label",
        ),
        dcc.Dropdown(
            id='crossfiltery-column',
            options=[{'label': i, 'value': i}
                     for i in df['Country'].unique()],
            value=df['Country'].unique()[0]
        ),
        html.P(
            "* This country filter is effective for all figures in the dashboard.",
            className="control_label",
        ),

    ], style={
        'borderTop': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px 390px',
        'width': '20%',
        'display': 'inline-block',
        'vertical-align': 'top',
        "margin-bottom": "65px"
    },
        className='pretty_container four columns'),
    # ---------------- 1st figure (TRUDAUDAU/TRU) ----------
    html.Div([
        dcc.RadioItems(
            id='crossfilter-yaxis-type',
            options=[{'label': i, 'value': i}
                     for i in ['TRU', 'DAU', 'DAU/TRU']],
            value='DAU',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'Japan'}]}
        )
    ], style={'width': '75%', 'display': 'inline-block', 'padding': '20px 20px'}),

    # ---- empty figure for pretty layout + 2nd figure (overall time speed) ---------
    html.Div([
    ], style={
        # 'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px 420px',
        'width': '20%',
        'display': 'inline-block',
        'vertical-align': 'top',
        "margin-bottom": "65px"
    },
        className='pretty_container four columns'),


    html.Div([
        dcc.Graph(
            id='time-spent-histogram',
            hoverData={'points': [{'customdata': 'Japan'}]}
        ),
    ], style={'width': '75%', 'display': 'inline-block', 'padding': '20px 20px',
              'textAlign': 'right'}),

    # ---- empty figure for pretty layout + 3rd figure (time speed per month) ---------
    html.Div([
    ], style={
        # 'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px 460px',
        'width': '20%',
        'display': 'inline-block',
        'vertical-align': 'top',
        "margin-bottom": "65px"
    },
        className='pretty_container four columns'),

    html.Div([
        html.Div([
            dcc.Graph(id='return-histogram'),
        ], style={'display': 'inline-block', 'width': '99%'}),

        html.Div(dcc.Slider(
            id='month-slider',
            min=0,
            max=len(all_month),
            step=None,
            value=len(all_month)//2,
            marks={i: {'label': str(all_month[i]), 'style':{
                'transform': 'rotate(45deg)'}} for i in range(len(all_month))}
        ), style={'width': '99%', 'padding': '0px 20px 20px 20px'}),
    ],
        style={'width': '75%', 'display': 'inline-block', 'padding': '20px 20px',
               'textAlign': 'right'}),

    # ---- empty figure for pretty layout + 4nd figure (conversion rate) ---------
    html.Div([
    ], style={
        # 'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px 460px',
        'width': '20%',
        'display': 'inline-block',
        'vertical-align': 'top',
        "margin-bottom": "65px"
    },
        className='pretty_container four columns'),

    html.Div([
        dcc.Graph(
            id='conversion-rate',
            hoverData={'points': [{'customdata': 'Japan'}]}
        ),
    ], style={'width': '75%', 'display': 'inline-block', 'padding': '20px 20px'}),


    # ---- empty figure for pretty layout + 5nd figure (heatmap correlation) ---------
    # ---- empty figure for pretty layout + 6nd figure (return month histogram) ---------
    html.Div([
    ], style={
        # 'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px 460px',
        'width': '20%',
        'display': 'inline-block',
        'vertical-align': 'top',
        "margin-bottom": "65px"
    },
        className='pretty_container four columns'),

    html.Div([
        html.Div([
            dcc.Graph(
                id='correlation-heatmap',
                hoverData={'points': [{'customdata': 'Japan'}]}
            ),
        ], style={'width': '45%', 'display': 'inline-block', 'padding': '00px 00px'}),

        html.Div([
            dcc.Graph(id='return-month-histogram'),
        ], style={'display': 'inline-block', 'width': '45%', 'padding': '00px 00px 00px 00px'}),
    ],
        style={'width': '75%', 'display': 'inline-block', })


])


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfiltery-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     ])
def update_graph(column_name, yaxis_type):
    dff = df[df['Country'] == column_name]
    dff_ios = dff[dff['Platform'] == 'IOS(All)']
    dff_an = dff[dff['Platform'] == 'Android(All)']

    return {
        'data': [go.Scatter(
            x=dff['Date'], y=dff_ios[yaxis_type],
            mode='lines+markers',
            name='IOS',
            marker={
                'size': 5,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        ),
            go.Scatter(
            x=dff['Date'], y=dff_an[yaxis_type],
            mode='lines+markers',
            name='Android',
            marker={
                'size': 5,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Date',
            },
            yaxis={
                'title': yaxis_type,
            },
            margin={'l': 60, 'b': 30, 't': 30, 'r': 0},
            height=450,
            hovermode='closest',
            title='Change of Number of Users over Time'
        )
    }


@app.callback(
    dash.dependencies.Output('time-spent-histogram', 'figure'),
    [
        dash.dependencies.Input('crossfiltery-column', 'value'),
    ])
def update_graph(country):
    dff = df[df['Country'] == country]
    dff_ios = dff[dff['Platform'] == 'IOS(All)']
    dff_an = dff[dff['Platform'] == 'Android(All)']
    return {
        'data': [
            go.Histogram(x=dff_ios['Time Spend Per Day(seconds)'], name='IOS'),
            go.Histogram(
                x=dff_an['Time Spend Per Day(seconds)'], name='Android'),
        ],
        'layout': go.Layout(
            xaxis={
                'title': 'Time Spend Per Day (seconds)',
            },
            yaxis={
                'title': 'Count',
            },
            margin={'l': 40, 'b': 30, 't': 30, 'r': 0},
            height=450,
            hovermode='closest',
            title='The Overall Distribution of Time Spend Per Day (Seconds) '
        )
    }


@app.callback(
    dash.dependencies.Output('correlation-heatmap', 'figure'),
    [
        dash.dependencies.Input('crossfiltery-column', 'value'),
    ])
def update_graph(country):
    dff = df[df['Country'] == country]

    dff['bought_items'] = dff['Trans']*dff['Items Per Trans']
    dff['dau_items'] = dff['Items per DAU']*dff['DAU']
    dff['dead_items'] = dff['Items']-dff['dau_items']
    dff['free_items'] = dff['Items']-dff['bought_items']

    corr = dff[['bought_items', 'dau_items', 'dead_items',
                'free_items', 'DAU', 'TRU', 'Trans', 'Cash Flow']].corr()

    x = list(corr.columns)
    y = list(corr.columns)
    z = np.array(corr)

    return {
        'data': [
            # ), colorscale='coolwarm')
            go.Heatmap(x=x, y=y, z=z, text=z, type='heatmap')
        ],
        'layout': go.Layout(
            xaxis={
                #                'title': 'Time Spend Per Day (seconds)',
            },
            yaxis={
                #                'title': 'Count',
            },
            margin={'l': 90, 'b': 60, 't': 30, 'r': 20},
            height=450,
            #            hovermode='closest'
            title='Correlation Matrix'
        )
    }


@app.callback(
    dash.dependencies.Output('conversion-rate', 'figure'),
    [
        dash.dependencies.Input('crossfiltery-column', 'value'),
    ])
def update_graph(country):
    dff = df[df['Country'] == country]
    dff_ios = dff[dff['Platform'] == 'IOS(All)']
    ios_ucl = dff_ios['Conversion'].mean() + 3*dff_ios['Conversion'].std()
    ios_lcl = dff_ios['Conversion'].mean() - 3*dff_ios['Conversion'].std()
    dff_an = dff[dff['Platform'] == 'Android(All)']
    an_ucl = dff_an['Conversion'].mean() + 3*dff_an['Conversion'].std()
    an_lcl = dff_an['Conversion'].mean() - 3*dff_an['Conversion'].std()

    return {
        'data': [
            go.Scatter(
                x=dff['Date'], y=dff_ios['Conversion'],
                mode='lines+markers',
                name='IOS',
                marker={
                    'size': 5,
                    'opacity': 0.5,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                line=dict(color='green')
            ),
            go.Scatter(
                x=dff['Date'], y=[ios_ucl for i in list(dff_ios['Date'])],
                mode='lines',
                name='IOS Upper Limit Control Line',
                line=dict(
                    color=('green'),
                    width=2,
                    dash='dash'),
            ),
            go.Scatter(
                x=dff['Date'], y=[ios_lcl for i in list(dff_ios['Date'])],
                mode='lines',
                name='IOS Lower Limit Control Line',
                line=dict(
                    color=('green'),
                    width=2,
                    dash='dash'),
            ),
            # -----------------------------------
            go.Scatter(
                x=dff['Date'], y=dff_an['Conversion'],
                mode='lines+markers',
                name='Android',
                marker={
                    'size': 5,
                    'opacity': 0.5,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                line=dict(color='red')
            ),
            go.Scatter(
                x=dff['Date'], y=[an_ucl for i in list(dff_an['Date'])],
                mode='lines',
                name='Android Upper Limit Control Line',
                line=dict(
                    color=('red'),
                    width=2,
                    dash='dash'),
            ),
            go.Scatter(
                x=dff['Date'], y=[an_lcl for i in list(dff_an['Date'])],
                mode='lines',
                name='Android Lower Limit Control Line',
                line=dict(
                    color=('red'),
                    width=2,
                    dash='dash'),
            ),
        ],
        'layout': go.Layout(
            xaxis={
                'title': 'Date',
            },
            yaxis={
                'title': 'Conversion',
            },
            margin={'l': 40, 'b': 30, 't': 30, 'r': 0},
            height=450,
            title='Change of Conversion Rate over Time'
        )
    }


@app.callback(
    dash.dependencies.Output('return-histogram', 'figure'),
    [
        dash.dependencies.Input('crossfiltery-column', 'value'),
        dash.dependencies.Input('month-slider', 'value'),
    ])
def update_graph(country, month):
    dff = df[df['Country'] == country]
    # print('type', type(all_month[month]))
    # print('month', month)
    # assert 1==0
    dff = dff[dff['month'] == all_month[month]]
    dff_ios = dff[dff['Platform'] == 'IOS(All)']
    dff_an = dff[dff['Platform'] == 'Android(All)']
    return {
        'data': [
            go.Histogram(x=dff_ios['Time Spend Per Day(seconds)'], name='IOS'),
            go.Histogram(
                x=dff_an['Time Spend Per Day(seconds)'], name='Android'),
        ],
        'layout': go.Layout(
            xaxis={
                'title': 'Time Spend Per Day(seconds)',
            },
            yaxis={
                'title': 'Count',
            },
            margin={'l': 40, 'b': 30, 't': 30, 'r': 0},
            height=450,
            hovermode='closest',
            title='The Monthly Distribution of Time Spend Per Day (Seconds) '
        )
    }


@app.callback(
    dash.dependencies.Output('return-month-histogram', 'figure'),
    [
        dash.dependencies.Input('crossfiltery-column', 'value'),
    ])
def update_graph(country):
    dff = df[df['Country'] == country]
    dff_ios = dff[dff['Platform'] == 'IOS(All)']
    grouped_month_ios = dff_ios.groupby('month')
    dff_an = dff[dff['Platform'] == 'Android(All)']
    grouped_month_an = dff_an.groupby('month')

    return {
        'data': [
            go.Bar(name='IOS',
                   x=grouped_month_ios.DAU.sum().index,
                   y=grouped_month_ios.DAU.sum().values),
            go.Bar(name='Android',
                   x=grouped_month_an.DAU.sum().index,
                   y=grouped_month_an.DAU.sum().values)
        ],
        'layout': go.Layout(
            xaxis={
                'title': 'Monthly Return Customer',
            },
            yaxis={
                'title': 'Count',
            },
            margin={'l': 60, 'b': 80, 't': 30, 'r': 0},
            height=450,
            hovermode='closest',
            title='Monthly Returned Customers'
        )
    }

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server()
