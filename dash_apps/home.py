import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime
from .app import app


delta = (datetime(2020, 12, 31).date() - datetime.now().date()).days

percent = round(100 * (182 - delta)/ 182)

progress = dbc.Progress(f'{percent}%', id='progress', value=percent, style={"height": "50px"})

layout = dbc.Container([dbc.Row(dbc.Col(html.H1('COUNTDOWN', className="text-center"))),
                        progress,
                        dbc.Row(dbc.Col(html.H2(f'Only {delta} days remaining!!', id='time-left', className="text-center")))])


