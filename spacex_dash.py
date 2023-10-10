import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import plotly.express as px

data = pd.read_csv("spacex_launch_dash.csv")

min_payload = data['Payload Mass (kg)'].min()
max_payload = data['Payload Mass (kg)'].max()

app = dash.Dash(__name__)

app.layout = html.Div([
        html.H1("SpaceX Launch Records Dashboard", style = {'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
        html.Div([
            html.Label("Select Site"),
            html.Div([dcc.Dropdown(id = 'site-dropdown',
                options = [{'label': 'All Sites', 'value': 'All Sites'},
                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                    {'label': 'KSC SLC-39A', 'value': 'KSC LC-39A'},
                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
                value = 'All Sites',
                placeholder = 'Select A Site'
            )])
        ]),
        html.Br(),
        html.Div(dcc.Graph(id = 'success-pie-chart')),
        html.P("Payload Range (Kg)"),
        html.Div([dcc.RangeSlider(id = 'payload-slider',
            min = 0, max = 10000, step = 2500,
            marks = {0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
            value = [min_payload, max_payload])]),
        html.Br(),
        html.Div(dcc.Graph(id = 'success-payload-scatter-chart'))
])

@app.callback(
    Output(component_id = 'success-pie-chart', component_property = 'figure'),
    Input(component_id = 'site-dropdown', component_property = 'value'))

def update_pie_output(entered_site):

    if entered_site == 'All Sites':
        fig = px.pie(data, names = 'Launch Site', values = 'class', title = 'Total Successful Launches for All Sites')
        return fig

    else:
        df = data[data['Launch Site'] == entered_site]
        fig = px.pie(df, names = 'class', title = 'Total Successful Launches for the Site {}'.format(entered_site))
        return fig

@app.callback(
    Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
    [Input(component_id = 'site-dropdown', component_property = 'value'),
    Input(component_id = 'payload-slider', component_property = 'value')])

def update_payload_output(selected_site, payloads):

    if selected_site == 'All Sites':
        fig = px.scatter(data, x = 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category', title = 'Correlation Between Payload and Success for All Sites')
        return fig

    else:
        df = data[data['Launch Site'] == selected_site]
        fig = px.scatter(df, x = 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category', title = 'Correlation Between Payload and Success for the Site {}'.format(selected_site))
        return fig

if __name__ == '__main__':
    app.run_server(debug = True)
