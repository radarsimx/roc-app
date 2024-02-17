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

import uuid

from dash import dcc
from dash import html

import dash_bootstrap_components as dbc

import plotly.io as pio

colorscales = [
    "Blackbody",
    "Bluered",
    "Blues",
    "Earth",
    "Electric",
    "Greens",
    "Greys",
    "Hot",
    "Jet",
    "Picnic",
    "Portland",
    "Rainbow",
    "RdBu",
    "Reds",
    "Viridis",
    "YlGnBu",
    "YlOrRd",
]

INTEGRATION = [
    "Swerling 0",
    "Swerling 1",
    "Swerling 2",
    "Swerling 3",
    "Swerling 4",
    "Coherent",
]

sidebar_pdpfa = dbc.Row(
    [
        html.H2("Pd vs. Pfa", className="mb-3"),
        html.Label(
            "Probability of detection (Pd) versus probability of false alarm (Pfa) curve.",
            className="mb-3",
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("N"),
                dbc.Input(
                    id="pdpfa-channels",
                    type="number",
                    value=1,
                    min=1,
                    max=4096,
                    step=1,
                ),
                dbc.Tooltip(
                    "Nmber of channels",
                    target="pdpfa-channels",
                    placement="top",
                ),
            ],
            # size="sm",
            className="mb-3",
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("SNR"),
                dbc.Input(
                    id="pdpfa-snr",
                    type="number",
                    value=10,
                    min=-50,
                    max=50,
                    step=0.1,
                ),
                dbc.InputGroupText("dB"),
                dbc.Tooltip(
                    "Signal-to-noise ratio",
                    target="pdpfa-snr",
                    placement="top",
                ),
            ],
            # size="sm",
            className="mb-3",
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Target"),
                dbc.Select(
                    id="pdpfa-integration",
                    options=[{"label": i, "value": i} for i in INTEGRATION],
                    value="Swerling 3",
                ),
                dbc.Tooltip(
                    "Target model",
                    target="pdpfa-integration",
                    placement="top",
                ),
            ],
            # size="sm",
            className="mb-3",
        ),
    ]
)

sidebar_gain = dbc.Row(
    [
        dbc.FormText("Pd, probability of detection"),
        dbc.Col(
            dbc.Input(
                id="pd",
                type="number",
                value=0.5,
                min=0.01,
                max=0.9999,
                step=0.0001,
                className="mb-3",
            )
        ),
        dbc.FormText("Pfa, probability of false alarm"),
        dbc.Col(
            dbc.Input(
                id="pfa",
                type="number",
                value=0.0001,
                min=0.00000001,
                max=0.1,
                step=0.00000001,
                className="mb-3",
            )
        ),
        dbc.FormText("N, number of channels"),
        dcc.Slider(
            id="channels",
            min=1,
            max=1024,
            step=1,
            value=128,
            marks=None,
            tooltip={
                "always_visible": True,
                "placement": "bottom",
            },
        ),
        dbc.FormText("Types of targets", className="mt-3"),
        dcc.Dropdown(
            id="integration",
            options=[{"label": i, "value": i} for i in INTEGRATION],
            value=["Swerling 1", "Swerling 3"],
            multi=True,
        ),
        dbc.Col(html.Hr()),
        dbc.Label("Single Channel Minimal SNR"),
        dbc.Spinner(
            dbc.Row(id="minsnr-container", children=[]),
            color="primary",
            type="grow",
        ),
    ]
)

layout_card = [
    dbc.Row(
        [
            dbc.Col(
                html.Div(id="sidebar"),
                width=3,
            ),
            dbc.Col(
                dbc.Spinner(
                    dcc.Graph(
                        id="scatter",
                        figure={
                            "data": [
                                {
                                    "mode": "lines",
                                    "type": "scatter",
                                    "x": [],
                                    "y": [],
                                }
                            ],
                            "layout": {
                                "template": pio.templates["plotly"],
                                "uirevision": "no_change",
                                "xaxis": {"title": "Number of Channels"},
                                "yaxis": {"title": "Integration Gain (dB)"},
                            },
                        },
                        style={"height": "90vh"},
                    ),
                    color="primary",
                    type="grow",
                ),
                width=9,
            ),
        ]
    )
]


card = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Pd vs. Pfa", tab_id="tab-1"),
                    dbc.Tab(label="Integration Gain", tab_id="tab-2"),
                ],
                id="card-tabs",
                active_tab="tab-1",
            )
        ),
        dbc.CardBody(html.Div(id="card-content", children=layout_card)),
    ]
)


def get_app_layout():
    """
    Get the layout for the Dash web application.

    Returns:
    dbc.Container: Dash Bootstrap container containing the layout elements.
    - dcc.Store: Dash Core Component for storing session ID data.
    - dbc.Row: Dash Bootstrap row containing a column with a card
      (assumed to be defined elsewhere as 'card_gain').
    - html.Hr: Dash HTML Horizontal Rule for visual separation.
    - dcc.Markdown: Dash Core Component for rendering Markdown text.
    """
    return dbc.Container(
        [
            dcc.Store(id="session-id", data=str(uuid.uuid4())),
            dbc.Row([dbc.Col(card)], className="my-2"),
            html.Hr(),
            dcc.Markdown("v1.0 | Powered by [Dash](https://plotly.com/dash/)"),
            html.Div(id="hidden", style= {'display': 'none'})
        ],
        fluid=True,
        className="dbc_light",
    )
