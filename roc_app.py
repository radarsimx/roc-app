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

from threading import Thread
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

import numpy as np
import plotly.io as pio

from roc.tools import roc_snr

from flaskwebgui import FlaskUI

from layout.layout import get_app_layout

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width,initial-scale=1"}],
)

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
app.title = "ROC"
app.layout = get_app_layout
server = app.server


@app.callback(
    output={
        "fig": Output("scatter", "figure"),
        "minsnr_container": Output("minsnr-container", "children"),
    },
    inputs={
        "pd": Input("pd", "value"),
        "pfa": Input("pfa", "value"),
        "n": Input("channels", "value"),
        "model": Input("integration", "value"),
    },
    state={
        "min_pd": State("pd", "min"),
        "max_pd": State("pd", "max"),
        "min_pfa": State("pfa", "min"),
        "max_pfa": State("pfa", "max"),
    },
)
def gain_plot(pd, pfa, n, model, min_pd, max_pd, min_pfa, max_pfa):
    """
    Generate a plot for integration gain based on probability of detection (Pd),
    probability of false alarm (Pfa), number of channels (n), and a list of models.

    Parameters:
    - pd (float): Probability of detection.
    - pfa (float): Probability of false alarm.
    - n (int): Number of channels.
    - model (list): List of models.
    - min_pd (float): Minimum value for Pd.
    - max_pd (float): Maximum value for Pd.
    - min_pfa (float): Minimum value for Pfa.
    - max_pfa (float): Maximum value for Pfa.

    Raises:
    - PreventUpdate: If pd is None, pd is outside the range [min_pd, max_pd],
                    pfa is None, or pfa is outside the range [min_pfa, max_pfa].

    Returns:
    dict: A dictionary containing the plot data and layout, as well as minsnr_container information.
    - fig (dict): Plotly figure data and layout.
    - minsnr_container (list): List of FormText containing minimum SNR information for each model.
    """
    if pd is None:
        raise PreventUpdate
    if pd < min_pd or pd > max_pd:
        raise PreventUpdate

    if pfa is None:
        raise PreventUpdate
    if pfa < min_pfa or pfa > max_pfa:
        raise PreventUpdate

    n_array = np.arange(1, n + 1)
    nci_gain = np.zeros((len(model), n), dtype=np.float64)
    fig_data = []
    minsnr_container = []
    for m_idx, mod in enumerate(model):
        minsnr = roc_snr(pfa, pd, 1, mod)
        minsnr_container.append(
            dbc.FormText(mod + ": " + str(round(minsnr, 3)) + " dB")
        )
        for idx in range(1, n + 1):
            nci_gain[m_idx, idx - 1] = minsnr - roc_snr(pfa, pd, n_array[idx - 1], mod)
        fig_data.append(
            {
                "mode": "lines",
                "type": "scatter",
                "x": n_array,
                "y": nci_gain[m_idx, :],
                "name": mod,
            }
        )

    return {
        "fig": {
            "data": fig_data,
            "layout": {
                "template": pio.templates["plotly"],
                "uirevision": "no_change",
                "title": "Pd = " + str(pd) + ", Pfa = " + str(pfa),
                "xaxis": {"title": "Number of Channels"},
                "yaxis": {"title": "Integration Gain (dB)"},
            },
        },
        "minsnr_container": minsnr_container,
    }


def run_gui_thread():
    FlaskUI(app=server, server="flask", port=61134).run()


if __name__ == "__main__":
    # app.run_server(debug=True, threaded=True, processes=1, host='0.0.0.0')
    # FlaskUI(app=server, server="flask", port=61134).run()

    run_thread = Thread(target=run_gui_thread, name="roc app")
    run_thread.start()
