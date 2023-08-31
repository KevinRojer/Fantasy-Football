#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 15:59:58 2023

@author: kevinrojer
"""


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
import seaborn as sns


# Define paths
project_path = os.path.dirname(os.getcwd())
data_path = os.path.join(project_path, "data")
plot_path = os.path.join(project_path, "plots")

# Check if folders exists
if not (os.path.exists(plot_path)):
    os.makedirs(plot_path)

# load data
nfl_filepath = os.path.join(data_path, "nfl-season-stats.csv")
qb_filepath = os.path.join(data_path, "qb-fantasy-sos.csv")
te_filepath = os.path.join(data_path, "te-fantasy-sos.csv")
rb_filepath = os.path.join(data_path, "rb-fantasy-sos.csv")

nfl_dat = pd.read_csv(nfl_filepath)
qb_dat = pd.read_csv(qb_filepath)
te_dat = pd.read_csv(te_filepath)
rb_dat = pd.read_csv(rb_filepath)

""" NFL Analysis """
# Create an interactive horizontal bar plot
fig = px.bar(nfl_dat, x='RushAtt', y='Team', orientation='h',
             title='2022 NFL Rushing Attemps', text='RushAtt')

# Order bars by value in ascending order
fig = fig.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
fig.write_html(os.path.join(plot_path, 'nfl_rb_attempts_2022.html'))

# Create an interactive histogram
fig = px.histogram(nfl_dat["RushAtt"], nbins=20, 
                   title='2023 NFL Rushing Attempts Distribution',
                   labels={'value': 'Rush Attempts', 'count': 'Frequency'})
fig.write_html(os.path.join(plot_path, 'nfl_rb_attempts_2022_dist.html'))

""" QB Analysis """
# Create a subset of eligible QBs
eligible_qb_data = qb_dat[qb_dat.Ovr >= 100.00].reset_index(drop=True)

# Calculate fantasy points per game
qb_fppg = pd.DataFrame({"PPG": np.nanmean(eligible_qb_data.iloc[:,3:], axis=1)})
qb_fppg = pd.merge(eligible_qb_data.loc[:, ["Name", "Team", "Ovr",]], qb_fppg, 
                   left_index=True, right_index=True)

# Now create a scatter plot with hover data
fig = px.scatter(qb_fppg, x="PPG", y="Ovr", text="Name",
                 title="2023 NFL Fantasy Quaterback Production")
fig.update_xaxes(title_text="Points per game")
fig.update_yaxes(title_text="Total Points")
fig.update_traces(textposition="top center")
fig.write_html(os.path.join(plot_path, 'fantasy_qb_performance_2023.html'))

# Now create a boxplot
traces = []
for n, d in zip(eligible_qb_data.loc[:, "Name"], eligible_qb_data.iloc[:,3:].values):
    if d is not None:
        traces.append(go.Box(y=d, name=f'{n}'))
        # Sort traces based on median
sorted_traces = sorted(traces, reverse=True, key=lambda trace: np.nanmedian(trace.y))
# Create layout
layout = go.Layout(title='2023 NFL Fantasy Quaterback Production Distribution')
# Create the figure
fig = go.Figure(data=sorted_traces, layout=layout)
fig.write_html(os.path.join(plot_path, 'fantasy_qb_performance_2023_bx.html'))


""" TE Analysis """
# Create a subset of eligible QBs
eligible_te_data = te_dat[te_dat.Ovr >= 35.00].reset_index(drop=True)

# Create an interactive histogram
fig = px.histogram(eligible_te_data["Ovr"], nbins=20, 
                   title='2023 NFL Fantasy TE Production Distribution',
                   labels={'value': 'Total Points', 'count': 'Frequency'})
fig.write_html(os.path.join(plot_path, 'fantasy_te_performance_2023_dist.html'))

# Calculate fantasy points per game
te_fppg = pd.DataFrame({"PPG": np.nanmean(eligible_te_data.iloc[:,3:], axis=1)})
te_fppg = pd.merge(eligible_te_data.loc[:, ["Name", "Team", "Ovr",]], te_fppg, 
                   left_index=True, right_index=True)

# Now create a scatter plot with hover data
fig = px.scatter(te_fppg, x="PPG", y="Ovr", text="Name",
                 title="2023 NFL Fantasy TE Production")
fig.update_xaxes(title_text="Points per game")
fig.update_yaxes(title_text="Total Points")
fig.update_traces(textposition="top center")
fig.write_html(os.path.join(plot_path, 'fantasy_te_performance_2023.html'))

# Now create a boxplot
traces = []
for n, d in zip(eligible_te_data.loc[:, "Name"], eligible_te_data.iloc[:,3:].values):
    if d is not None:
        traces.append(go.Box(y=d, name=f'{n}'))
        # Sort traces based on median
sorted_traces = sorted(traces, reverse=True, key=lambda trace: np.nanmedian(trace.y))
# Create layout
layout = go.Layout(title='2023 NFL Fantasy TE Production Distribution')
# Create the figure
fig = go.Figure(data=sorted_traces, layout=layout)
fig.write_html(os.path.join(plot_path, 'fantasy_te_performance_2023_bx.html'))

""" RB Analysis """
# Create a subset of eligible QBs
eligible_rb_data = rb_dat[rb_dat.Ovr >= 100.00].reset_index(drop=True)

# Create an interactive histogram
fig = px.histogram(eligible_rb_data["Ovr"], nbins=20, 
                   title='2023 NFL Fantasy RB Production Distribution',
                   labels={'value': 'Total Points', 'count': 'Frequency'})
fig.write_html(os.path.join(plot_path, 'fantasy_rb_performance_2023_dist.html'))

# Calculate fantasy points per game
rb_fppg = pd.DataFrame({"PPG": np.nanmean(eligible_rb_data.iloc[:,3:], axis=1)})
rb_fppg = pd.merge(eligible_rb_data.loc[:, ["Name", "Team", "Ovr",]], rb_fppg, 
                   left_index=True, right_index=True)

# Now create a scatter plot with hover data
fig = px.scatter(rb_fppg, x="PPG", y="Ovr", text="Name",
                 title="2023 NFL Fantasy RB Production")
fig.update_xaxes(title_text="Points per game")
fig.update_yaxes(title_text="Total Points")
fig.update_traces(textposition="top center")
fig.write_html(os.path.join(plot_path, 'fantasy_rb_performance_2023.html'))

# Now create a boxplot
traces = []
for n, d in zip(eligible_rb_data.loc[:, "Name"], eligible_rb_data.iloc[:,3:].values):
    if d is not None:
        traces.append(go.Box(y=d, name=f'{n}'))
        
# Sort traces based on median
sorted_traces = sorted(traces, reverse=True, key=lambda trace: np.nanmedian(trace.y))
# Create layout
layout = go.Layout(title='2023 NFL Fantasy RB Production Distribution')
# Create the figure
fig = go.Figure(data=sorted_traces, layout=layout)
fig.write_html(os.path.join(plot_path, 'fantasy_rb_performance_2023_bx.html'))
