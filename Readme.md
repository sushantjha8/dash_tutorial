# Dash Tutorial By Dashmin

## Layout


## CallBacks
        The "inputs" and "outputs" of our application interface are described declaratively through the app.callback decorator.
    In Dash, the inputs and outputs of our application are simply the properties of a particular component
        `### Reactive programming

        app.layout = html.Div([
            dcc.Graph(id='graph-with-slider'),
            dcc.Slider(
                id='year-slider',
                min=df['year'].min(),
                max=df['year'].max(),
                value=df['year'].min(),
                marks={str(year): str(year) for year in df['year'].unique()},
                step=None
            )
        ])



        #### here call back 

        @app.callback(
            Output('graph-with-slider', 'figure'),
            [Input('year-slider', 'value')])
        def update_figure(selected_year):
            filtered_df = df[df.year == selected_year]
            traces = []
            for i in filtered_df.continent.unique():
                df_by_continent = filtered_df[filtered_df['continent'] == i]
                traces.append(dict(
                    x=df_by_continent['gdpPercap'],
                    y=df_by_continent['lifeExp'],
                    text=df_by_continent['country'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ))

            return {
                'data': traces,
                'layout': dict(
                    xaxis={'type': 'log', 'title': 'GDP Per Capita',
                        'range':[2.3, 4.8]},
                    yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest',
                    transition = {'duration': 500},
                )
            }

        ### multiple input single output

        @app.callback(
            Output('graph-with-slider', 'figure'),
            [Input('year-slider', 'value')])
        def update_figure(selected_year):
            filtered_df = df[df.year == selected_year]
            traces = []
            for i in filtered_df.continent.unique():
                df_by_continent = filtered_df[filtered_df['continent'] == i]
                traces.append(dict(
                    x=df_by_continent['gdpPercap'],
                    y=df_by_continent['lifeExp'],
                    text=df_by_continent['country'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ))

            return {
                'data': traces,
                'layout': dict(
                    xaxis={'type': 'log', 'title': 'GDP Per Capita',
                        'range':[2.3, 4.8]},
                    yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest',
                    transition = {'duration': 500},
                )
            }

        ### multiple outputs from single inputs



        app.layout = html.Div([
            dcc.Input(
                id='num-multi',
                type='number',
                value=5
            ),
            html.Table([
                html.Tr([html.Td(['x', html.Sup(2)]), html.Td(id='square')]),
                html.Tr([html.Td(['x', html.Sup(3)]), html.Td(id='cube')]),
                html.Tr([html.Td([2, html.Sup('x')]), html.Td(id='twos')]),
                html.Tr([html.Td([3, html.Sup('x')]), html.Td(id='threes')]),
                html.Tr([html.Td(['x', html.Sup('x')]), html.Td(id='x^x')]),
            ]),
        ])


        @app.callback(
            [Output('square', 'children'),
            Output('cube', 'children'),
            Output('twos', 'children'),
            Output('threes', 'children'),
            Output('x^x', 'children')],
            [Input('num-multi', 'value')])
        def callback_a(x):
            return x**2, x**3, 2**x, 3**x, x**x
`
## Advnce Callbacks with state

### In this example, the callback function is fired whenever any of the attributes described by the dash.dependencies.Input change. Try it for yourself by entering data in the inputs above.

       app.layout = html.Div([
    dcc.Input(id='input-1-state', type='text', value='Montréal'),
    dcc.Input(id='input-2-state', type='text', value='Canada'),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Div(id='output-state')
        ])


@app.callback(Output('output-state', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value'),
               State('input-2-state', 'value')])
def update_output(n_clicks, input1, input2):
    return u'''
        The Button has been pressed {} times,
        Input 1 is "{}",
        and Input 2 is "{}"
    '''.format(n_clicks, input1, input2)


### dash.dependencies.State 
    allows you to pass along extra values without firing the callbacks. Here's the same example as above but with the dcc.Input as dash.dependencies.State and a button as dash.dependencies.Input.

### In certain situations, you don't want to update the callback output. You can achieve this by raising a PreventUpdate exception in the callback function.

app.layout = html.Div([
    html.Button('Click here to see the content', id='show-secret'),
    html.Div(id='body-div')
])

@app.callback(
    Output(component_id='body-div', component_property='children'),
    [Input(component_id='show-secret', component_property='n_clicks')]
)
def update_output(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        return "Elephants are the only animal that can't jump"


## state based code snipet

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.P('Enter a composite number to see its prime factors'),
    dcc.Input(id='num', type='number', debounce=True, min=1, step=1),
    html.P(id='err', style={'color': 'red'}),
    html.P(id='out')
])

@app.callback(
    [Output('out', 'children'), Output('err', 'children')],
    [Input('num', 'value')]
)
def show_factors(num):
    if num is None:
        # PreventUpdate prevents ALL outputs updating
        raise dash.exceptions.PreventUpdate

    factors = prime_factors(num)
    if len(factors) == 1:
        # dash.no_update prevents any single output updating
        # (note: it's OK to use for a single-output callback too)
        return dash.no_update, '{} is prime!'.format(num)

    return '{} is {}'.format(num, ' * '.join(str(n) for n in factors)), ''

def prime_factors(num):
    n, i, out = num, 2, []
    while i * i <= n:
        if n % i == 0:
            n = int(n / i)
            out.append(i)
        else:
            i += 1 if i == 2 else 2
    out.append(n)
    return out

    # DASH GRAPH

    