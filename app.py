"""

    Copyright (C) 2023 - PRESENT  Zhengyu Peng
    E-mail: zpeng.me@gmail.com
    Website: https://zpeng.me

    `                      `
    -:.                  -#:
    -//:.              -###:
    -////:.          -#####:
    -/:.://:.      -###++##:
    ..   `://:-  -###+. :##:
           `:/+####+.   :##:
    .::::::::/+###.     :##:
    .////-----+##:    `:###:
     `-//:.   :##:  `:###/.
       `-//:. :##:`:###/.
         `-//:+######/.
           `-/+####/.
             `+##+.
              :##:
              :##:
              :##:
              :##:
              :##:
               .+:

"""


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import numpy as np
import plotly.io as pio

from dash.exceptions import PreventUpdate

from roc.tools import roc_pd, roc_snr

from layout.layout import get_app_layout

app = dash.Dash(__name__,
                meta_tags=[{
                    'name': 'viewport',
                    'content': 'width=device-width,initial-scale=1'
                }]
                )

app.layout = get_app_layout


@app.callback(
    output=dict(
        fig=Output('scatter', 'figure'),
        minsnr_container=Output('minsnr-container', 'children'),
    ),
    inputs=dict(
        pd=Input('pd', 'value'),
        pfa=Input('pfa', 'value'),
        n=Input('channels', 'value'),
        model=Input('integration', 'value'),
    ),
    state=dict(
        min_pd=State('pd', 'min'),
        max_pd=State('pd', 'max'),
        min_pfa=State('pfa', 'min'),
        max_pfa=State('pfa', 'max'),
    )
)
def gain_plot(pd, pfa, n, model, min_pd, max_pd, min_pfa, max_pfa):

    if pd is None:
        print('None pd')
        raise PreventUpdate
    elif pd < min_pd or pd > max_pd:
        print('pd out of region')
        raise PreventUpdate

    if pfa is None:
        print('None pfa')
        raise PreventUpdate
    elif pfa < min_pfa or pfa > max_pfa:
        print('pfa out of region')
        raise PreventUpdate

    n_array = np.arange(1, n+1)
    nci_gain = np.zeros((len(model), n), dtype=np.float64)
    fig_data = []
    minsnr_container = []
    for m_idx, mod in enumerate(model):
        minsnr = roc_snr(pfa, pd, 1, mod)
        minsnr_container.append(dbc.FormText(
            mod+': '+str(round(minsnr, 3))+' dB'))
        for idx in range(1, n+1):
            nci_gain[m_idx, idx-1] = minsnr - \
                roc_snr(pfa, pd, n_array[idx-1], mod)
        fig_data.append(
            {'mode': 'lines',
             'type': 'scatter',
             'x': n_array,
             'y': nci_gain[m_idx, :],
             'name': mod}
        )

    return dict(fig={'data': fig_data,
                     'layout': {'template': pio.templates['plotly'],
                                'height': 700,
                                'uirevision': 'no_change',
                                'title': 'Pd = '+str(pd)+', Pfa = '+str(pfa),
                                'xaxis': dict(title='Number of Channels'),
                                'yaxis': dict(title='Integration Gain (dB)')}
                     },
                minsnr_container=minsnr_container)


if __name__ == '__main__':
    app.run_server(debug=True, threaded=True, processes=1, host='0.0.0.0')
