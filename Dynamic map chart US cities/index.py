import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd


cities = pd.read_csv('us-cities-top-1k.csv')

cities1 = cities[['State', 'lat', 'lon']]

list_locations = cities1.set_index('State')[['lat', 'lon']].T.to_dict('dict')



app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div([

html.Div([
        html.Div([
            html.Div([
                html.H3('Scattermapbox Map Chart', style = {'margin-bottom': '0px', 'color': 'black'}),
            ])
        ], className = "create_container1 four columns", id = "title"),

    ], id = "header", className = "row flex-display", style = {"margin-bottom": "5px"}),

html.Div([
        html.Div([


            html.P('Select State', className = 'fix_label', style = {'color': 'black', 'margin-top': '2px'}),
            dcc.Dropdown(id = 'select_state2',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True},
                         value = 'Michigan',
                         placeholder = 'Select state',
                         options = [{'label': c, 'value': c}
                                    for c in (cities['State'].unique())], className = 'dcc_compon'),


            ], className = "create_container2 four columns", style = {'margin-bottom': '20px', "margin-top": "20px"}),

    ], className = "row flex-display"),

            html.Div([
                html.Div([

                    dcc.Graph(id = 'map_6',
                              config = {'displayModeBar': 'hover'}),

                ], className = "create_container2 eight columns", style = {'height': '610px'}),

            ], className = "row flex-display"),

], id="mainContainer", style={"display": "flex", "flex-direction": "column"})


@app.callback(Output('map_6', 'figure'),
              [Input('select_state2', 'value')])
def update_graph(select_state2):
    cities1 = cities.groupby(['State', 'City', 'lat', 'lon'])['Population'].sum().reset_index()
    cities2 = cities1[cities1['State'] == select_state2]

    if select_state2:
        zoom = 5
        zoom_lat = list_locations[select_state2]['lat']
        zoom_lon = list_locations[select_state2]['lon']

    return {
        'data': [go.Scattermapbox(
            lon = cities2['lon'],
            lat = cities2['lat'],
            mode = 'markers',
            marker=go.scattermapbox.Marker(
                size = 12,
                color = cities2['Population'],
                colorscale = 'HSV',
                showscale = False,
                sizemode = 'area'),

            hoverinfo = 'text',
            hovertext =
            '<b>State</b>: ' + cities2['State'].astype(str) + '<br>' +
            '<b>City</b>: ' + cities2['City'].astype(str) + '<br>' +
            '<b>Lat</b>: ' + [f'{x:.4f}' for x in cities2['lat']] + '<br>' +
            '<b>Long</b>: ' + [f'{x:.4f}' for x in cities2['lon']] + '<br>' +
            '<b>Population</b>: ' + [f'{x:,.0f}' for x in cities2['Population']] + '<br>'

        )],

        'layout': go.Layout(
            height = 580,
             margin={"r": 0, "t": 0, "l": 0, "b": 0},
             hovermode='closest',
             mapbox=dict(
                accesstoken='pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw',  # Create free account on Mapbox site and paste here access token
                center=dict(lat=zoom_lat, lon=zoom_lon),
                style='open-street-map',
                # style='dark',
                zoom=zoom,
                bearing = 0
             ),
             autosize=True,

        )

    }


if __name__ == "__main__":
    app.run_server(debug=True)
