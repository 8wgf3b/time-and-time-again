import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime
from .app import app


progress = dbc.Progress(id='progress', style={"height": "50px"})

layout = dbc.Container([dbc.Row(dbc.Col(html.H1('COUNTDOWN', className="text-center"))),
                        progress,
                        dbc.Row(dbc.Col(html.H2(id='time-left', className="text-center"))),
                        dcc.Interval(id='hourly-update', interval=3600*1000, n_intervals=0)
                        ])


@app.callback([Output('time-left', 'children'), Output('progress', 'children'), Output('progress', 'value')],
              [Input('hourly-update', 'n_intervals')])
def update_progress(n):
    delta = (datetime(2020, 12, 31).date() - datetime.now().date()).days
    percent = round(100 * (182 - delta)/ 182)
    return f'Only {delta} days remaining!!', f'{percent}%', percent               
