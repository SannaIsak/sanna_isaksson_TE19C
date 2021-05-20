import plotly.express as px 
import dash
import dash_core_components as dcc
import dash_html_components as HTML
import pandas as pd 
import numpy as np
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

df = pd.read_csv("C:/Users/sanna.isaksson/Documents/GitHub/sanna_isaksson_TE19C/Slutprojekt/National_Total_Deaths_by_Age_Group.csv")

part = []
ages = df["Age_Group"].unique() 

for index,col in df.iterrows():
    deaths = col["Total_Deaths"] / col["Total_Cases"]
    non_deaths = 1 - deaths
    part.append([deaths, non_deaths])

labels = ["Döda", "Smittade"]
colors = ["tomato","palegreen"]

fig = px.pie()

# utseendet
app.layout = HTML.Div(children=[
    HTML.H1(children = "Olika data för covid-19 fall"), 

    dcc.Dropdown(
        id = "drop",
        options = [
        dict(label = "0-9", value="0-9"), 
        dict(label = "10-19", value="10-19"),
        dict(label = "20-29", value="20-29"),
        dict(label = "30-39", value="30-39"),
        dict(label = "40-49", value="40-49"),
        dict(label = "50-59", value="50-59"),
        dict(label = "60-69", value="60-69"),
        dict(label = "70-79", value="70-79"),
        dict(label = "80-89", value="80-89"),
        dict(label = "90+", value="90+")],
        value="0-9"
    ),

    dcc.Graph(
        id = "graph",
        figure = fig
    )
])

@app.callback(
    Output("graph", "figure"),
    [Input("drop", "value")]
)
def update_figure(value):
    if value == "0-9": df_pie = part[0]
    elif value == "10-19": df_pie = part[1]
    elif value == "20-29": df_pie = part[2]
    elif value == "30-39": df_pie = part[3]
    elif value == "40-49": df_pie = part[4]
    elif value == "50-59": df_pie = part[5]
    elif value == "60-69": df_pie = part[6]
    elif value == "70-79": df_pie = part[7]
    elif value == "80-89": df_pie = part[8]
    elif value == "90+": df_pie = part[9]

    fig = px.pie(values=df_pie, names=labels, color=labels, title=f"Andel smittade vs döda från åldern {value}", 
                    color_discrete_map={"Smittade":"palegreen", "Döda":"tomato"})
    fig.update_layout(transition_duration=500)
    return fig

if __name__ == "__main__":
    app.run_server(debug = True)