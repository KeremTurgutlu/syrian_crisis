import plotly.graph_objs as go
import numpy as np

def filled_ts_plot(data):
    """
    Returns figure for filled time series scatter plot.
    Data should have "date" and "Value" columns.

    Inputs:
        data (pd.DataFrame): data with date and value info

    Returns:
        fig (dict): figure dict to plot in plotly
    """

    # create plotly data
    plotly_data = [
        go.Scatter(
            x=data.date,
            y=data.Value,
            fill='tozeroy')
    ]

    # create custom layout
    plotly_layout = go.Layout(
        title="Global Number of Asylum Seekers Originating From Syria",

        xaxis=dict(
            title='Date',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),

        yaxis=dict(
            title='Number of Refugees',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )

    # create figure
    fig = dict(data=plotly_data, layout=plotly_layout)
    return fig


def grouped_bar_chart(data, group_cols):
    """
    Returns plotly figure for grouped bar chart

    Inputs:
        data (pd.DataFrame): data
        group_cols (list): list of columns names to use as groups
    Returns:
        fig (dict): figure dict to plot in plotly
    """
    traces = []
    for stat in group_cols:
        trace = go.Bar(
            x=list(data.index),
            y=list(data[stat].values),
            name=f'{stat}'
        )
        traces.append(trace)

    layout = go.Layout(
        barmode='group',
        title='Distribution of Different Groups By Year',
        xaxis={'title': 'Year'},
        yaxis={'title': 'Number of Refugees'}
    )

    fig = go.Figure(data=traces, layout=layout)
    return fig


def cloropleth_map(data, code_col='CODE', value_col='total',
                   name_col='Country / territory of asylum/residence',
                   title='Syrian Refugees Around Globe 2016'):
    """
    Returns plotly figure for cloropleth map

    Inputs:
        data (pd.DataFrame): main data
        code_col (str): column name for country codes
        value_col: value column for fills
        name_col: name column for text attribute

    Returns:
        fig (dict): plotly figure
    """

    data = [dict(
        type='choropleth',
        locations=data[code_col],
        z=data[value_col],
        text=data[name_col],
        colorscale=[[0, "rgb(5, 10, 172)"], [0.35, "rgb(40, 60, 190)"],
                    [0.5, "rgb(70, 100, 245)"],
                    [0.6, "rgb(90, 120, 245)"], [0.7, "rgb(106, 137, 247)"],
                    [1, "rgb(220, 220, 220)"]],
        autocolorscale=False,
        reversescale=True,
        marker=dict(
            line=dict(
                color='rgb(180,180,180)',
                width=0.5
            )),
        colorbar=dict(
            autotick=False,
            title='Number of Refugees'),
    )]

    layout = dict(
        title=title,
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection=dict(
                type='Mercator'
            )
        )
    )

    fig = dict(data=data, layout=layout)
    return fig


def bubble_map_plot(data, attributes, colors,
                    title='Asylum Applications Around the World',
                    country_col='Country / territory of asylum/residence'):
    """
    Creates bubble map fig with different attributes/stats together

    Inputs:
        data (pd.DataFrame): main data
        attributes (dict): enumerated dict 0: attribute 1 1: attribute 2
        colors (list): list of colors to use
        title (str): title for the map
        country_col (str): column name to create country labels
    Returns:
        fig : plotly figure
    """

    cases = []
    for i in range(len(attributes)):
        cases.append(go.Scattergeo(
            lon=data['lng'],  # -(max(range(6,10))-i),
            lat=data['lat'],
            text=(data[country_col].astype('str') + " " +
                  attributes[i] +
                  ':' + data[attributes[i]].astype('str')),
            name=attributes[i],
            marker=dict(
                size=np.log(data[attributes[i]]) * 3,
                color=colors[i],
                line=dict(width=0)
            )
        )
        )

    layout = go.Layout(
        title=title,
        geo=dict(
            resolution=100,
            scope='world',
            showframe=False,
            showcoastlines=True,
            showland=True,
            landcolor="0.20442906574394465, 0.29301038062283735, 0.35649365628604385)",
            countrycolor="rgb(255, 255, 255)",
            coastlinecolor="rgb(255, 255, 255)",
            showcountries=True,
            projection=dict(
                type='Mercator'
            )
        ),
        legend=dict(
            traceorder='reversed'
        )
    )

    fig = go.Figure(layout=layout, data=cases)
    return fig