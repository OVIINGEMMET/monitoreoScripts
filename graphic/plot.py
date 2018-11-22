from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot, plot_mpl
import plotly
import plotly.graph_objs as go
import plotly.io as pio
plotly.io.orca.config.executable = '~/anaconda2/envs/django/bin/ '
plotly.io.orca.config.save()

x = ['day 1', 'day 1', 'day 1', 'day 1', 'day 1', 'day 1',
     'day 2', 'day 2', 'day 2', 'day 2', 'day 2', 'day 2']

trace0 = go.Box(
    y=[0.2, 0.2, 0.6, 1.0, 0.5, 0.4, 0.2, 0.7, 0.9, 0.1, 0.5, 0.3],
    x=x,
    name='kale',
    marker=dict(
        color='#3D9970'
    )
)
trace1 = go.Box(
    y=[0.6, 0.7, 0.3, 0.6, 0.0, 0.5, 0.7, 0.9, 0.5, 0.8, 0.7, 0.2],
    x=x,
    name='radishes',
    marker=dict(
        color='#FF4136'
    )
)
trace2 = go.Box(
    y=[0.1, 0.3, 0.1, 0.9, 0.6, 0.6, 0.9, 1.0, 0.3, 0.6, 0.8, 0.5],
    x=x,
    name='carrots',
    marker=dict(
        color='#FF851B'
    )
)
data = [trace0, trace1, trace2]
layout = go.Layout(
    yaxis=dict(
        title='normalized moisture',
        zeroline=False
    ),
    boxmode='group'
)
fig = go.Figure(data=data, layout=layout,)
pio.write_image(fig, 'fig1.png')
#plot(fig, auto_open=False, image='png', image_filename='plot_image', output_type='file')
#plot_mpl(fig, image='png')
