import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from dash_apps.app import app
from dash_apps import home
import yaml


with open('configs/dashurl.yml', 'r') as stream:
    urls = yaml.safe_load(stream)
    
dropdown = dbc.DropdownMenu(nav=True, label='Go to', in_navbar=True,
           children=[dbc.DropdownMenuItem(' '.join(v.split('_')).title(), href= k) for k, v in urls.items()])

navbar = dbc.NavbarSimple(brand='Time and time again ....', dark=True, color='primary',
                          children=[dropdown])


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    return globals()[urls[pathname]].layout if pathname in urls else 404


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
