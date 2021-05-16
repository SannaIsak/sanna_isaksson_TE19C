import plotly.express as px 
import dash
import dash_core_components as dcc
import dash_html_components as HTML
import pandas as pd 
import numpy as np
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# genererar mockup data
TE19 = np.random.randint(70,100,34)
NA19 = np.random.randint(30,100,30)
df = pd.read_csv("C:/Users/sanna.isaksson/Documents/GitHub/sanna_isaksson_TE19C/Slutprojekt/National_Total_Deaths_by_Age_Group.csv")

df_TE19 = pd.DataFrame({"Närvaro":TE19})
df_NA19 = pd.DataFrame({"Närvaro":NA19})

percentage = dict(

)

for index,col in df.iterrows():
    deaths = col["Total_Deaths"] / col["Total_Cases"]
    non_deaths = 1 - deaths
    percentage[col["Age_Group"]] = deaths, non_deaths

labels = ["Döda", "Smittade"]

#df_pie = pd.DataFrame(data=percentage)

fig = px.pie(df_TE19, names=labels, title="Hur mångs dör")


# utseendet
app.layout = HTML.Div(children=[
    HTML.H1(children = "Närvarograd för olika klasser"), 

    dcc.Dropdown(
        id = "drop",
        options = [dict(label = "TE19", value="TE19"), dict(label = "9-10", value="NA19")],
        value="TE19"
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
    df_test = df_NA19
    if value == "0-9": df_test = df_TE19
    elif value == "10-19": df_test = NA19
    import sys
    print(df_NA19)

    fig = px.pie(df_test, names=labels, title=f"Närvarograd för klass {value}")
    fig.update_layout(transition_duration=500)
    return fig

if __name__ == "__main__":
    app.run_server(debug = True)