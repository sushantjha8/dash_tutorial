import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_canvas
from dash_canvas import DashCanvas
from dash_canvas.utils import (array_to_data_url, parse_jsonstring,
                              watershed_segmentation)
from skimage import io, color, img_as_ubyte
import numpy as np

#create dash app
app = dash.Dash(__name__)
filename = 'https://raw.githubusercontent.com/plotly/datasets/master/mitochondria.jpg'

canvas_width = 300
#read image using io.imread
img = io.imread(filename, as_gray=True)

app.layout = html.Div([
    html.H6('Annotate the two objects and the background'),
    html.Div([
      #more https://dash.plotly.com/canvas
    DashCanvas(id='segmentation-canvas',
               tool='line',
               lineWidth=5,
               filename=filename,
               width=canvas_width,
               ),
    ], className="five columns"),
    html.Div([
    html.Img(id='segmentation-img', width=300),
    ], className="five columns"),
    ])


@app.callback(Output('segmentation-img', 'src'),
              [Input('segmentation-canvas', 'json_data')])
def segmentation(string):
    if string:
        mask = parse_jsonstring(string, img.shape)
        seg = watershed_segmentation(img, mask)
        src = color.label2rgb(seg, image=img)
    else:
        raise PreventUpdate
    return array_to_data_url(img_as_ubyte(src))


if __name__ == '__main__':
    app.run_server(debug=True)
