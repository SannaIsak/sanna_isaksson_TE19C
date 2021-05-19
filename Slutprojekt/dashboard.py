import plotly.express as px 
import dash
import dash_core_components as dcc
import dash_html_components as HTML
import pandas as pd 
import numpy as np
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# genererar mockup data
#TE19 = np.random.randint(70,100,34)
#NA19 = np.random.randint(30,100,30)
df = pd.read_csv("C:/Users/sanna.isaksson/Documents/GitHub/sanna_isaksson_TE19C/Slutprojekt/National_Total_Deaths_by_Age_Group.csv")

#df_TE19 = pd.DataFrame({"Närvaro":TE19})
#df_NA19 = pd.DataFrame({"Närvaro":NA19})

part = []
ages = df["Age_Group"].unique() 

for index,col in df.iterrows():
    deaths = col["Total_Deaths"] / col["Total_Cases"]
    non_deaths = 1 - deaths
    part.append([deaths, non_deaths])

labels = ["Döda", "Smittade"]
colors = ["tomato","palegreen"]

df_1 = pd.DataFrame({"0-9":part[0]})
df_2 = pd.DataFrame({"10-19":part[1]})

fig = px.pie(df_1, names=labels, title="Hur mångs dör")


# utseendet
app.layout = HTML.Div(children=[
    HTML.H1(children = "Närvarograd för olika klasser"), 

    dcc.Dropdown(
        id = "drop",
        options = [dict(label = "0-9", value="0-9"), dict(label = "10-19", value="10-19")],
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
    #df_test = df_1
    if value == "0-9": df_test = df_1
    elif value == "10-19": df_test = df_2
    import sys

    fig = px.pie(df_test, title=f"Andel smittade vs döda från åldern {value}")
    fig.update_layout(transition_duration=500)
    return fig

if __name__ == "__main__":
    app.run_server(debug = True)