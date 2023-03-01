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

import numpy as np
import plotly.io as pio

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
        fig=Output('scatter', 'figure')
    ),
    inputs=dict(
        pd=Input('pd', 'value'),
        pfa=Input('pfa', 'value'),
        n=Input('channels', 'value'),
        model=Input('integration', 'value'),
    )
)
def gain_plot(pd, pfa, n, model):
    n_array = np.arange(1, n+1)
    nci_gain = np.zeros((len(model),n), dtype=np.float64)
    fig_data = []
    for m_idx, mod in enumerate(model):
        for idx in range(1, n+1):
            nci_gain[m_idx, idx-1] = roc_snr(pfa, pd, 1, mod) - \
                roc_snr(pfa, pd, int(n_array[idx-1]), mod)
        fig_data.append(
            {'mode': 'lines',
             'type': 'scatter',
             'x': n_array,
             'y': nci_gain[m_idx, :],
             'name': mod}
        )

    return dict(fig={'data': fig_data,
                     'layout': {'template': pio.templates['plotly'],
                                'height': 650,
                                'uirevision': 'no_change'}
                     })


if __name__ == '__main__':
    app.run_server(debug=True, threaded=True, processes=1, host='0.0.0.0')
