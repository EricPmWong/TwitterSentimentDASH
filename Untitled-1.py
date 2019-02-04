import plotly 
import plotlywrapper as pw
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.tools as tls
stream_ids = tls.get_credentials_file()['stream_ids']
print (stream_ids)