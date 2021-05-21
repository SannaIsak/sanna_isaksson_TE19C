import plotly.express as px 
import dash
import dash_core_components as dcc
import dash_html_components as HTML
import pandas as pd 
import numpy as np
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = dash.Dash(__name__)

# läser in data med pandas
df = pd.read_csv("C:/Users/sanna.isaksson/Documents/GitHub/sanna_isaksson_TE19C/Slutprojekt/National_Total_Deaths_by_Age_Group.csv")
df_daily_deaths = pd.read_csv("Slutprojekt/National_Daily_Deaths.csv")

# cirkeldiagramet
part = [] 
ages = df["Age_Group"].unique() # unique() - väljer alla unika värden i kolumn "Age_group"

# loopar igenom csv filen
for index,col in df.iterrows():
    deaths = col["Total_Deaths"] / col["Total_Cases"] # räknar ut andelen som dött av covid-19
    non_deaths = 1 - deaths
    part.append([deaths, non_deaths]) # append() - lägger till i lista part

labels = ["Döda", "Smittade"]
colors = ["tomato","palegreen"]

fig = px.pie() # definerar variabeln fig för funktion update_figure

# linjediagramet

fig2 = px.line(x=df_daily_deaths["Date"], y=df_daily_deaths["National_Daily_Deaths"], title="Antal döda varje dag från 11 mars 2020 till 11 Februari 2021")
fig2.update_xaxes(title="Datum")
fig2.update_yaxes(title="Antal")
fig2.update_traces(line_color="seagreen")

# stapeldiagram

df_Total_Cases = df["Total_Cases"].tolist() # tolist() - lägger de valda värdena från csv filen i en lista
df_Total_ICU = df["Total_ICU_Admissions"].tolist()
df_Total_Deaths = df["Total_Deaths"].tolist()

# funktion som visar en figur (stapeldiagram)
def bar_diag(data, row_num, col_num, color, text):
    fig3.add_trace( # add_trace - för subplot med plotly
        go.Bar(x=ages, y=data, marker_color=color, name=text),
        row=row_num, col=col_num)
    fig3.update_layout(height=500, width=1200, title_text="Hur covid-19 påverkat människor per åldersgrupp", xaxis_title="Åldersgrupp", yaxis_title="Antal")

fig3 = make_subplots(rows=1, cols=3)
bar_diag(df_Total_Cases,1,1,"palegreen", "Totalt antal fall") # bar_diag - kallar på funktionen med olika värden
bar_diag(df_Total_ICU,1,2, "mediumseagreen", "Totalt antal intensivvårdspatienter")
bar_diag(df_Total_Deaths,1,3, "seagreen", "Totalt antal döda")

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
        value="0-9",
        style = {'width':600}
    ),

    HTML.Div(children=[ 
    dcc.Graph(
        id = "graph",
        figure = fig,
        style = {'width':600, 'display': 'inline-block'}
        ),
    dcc.Graph(
        id = "graph2",
        figure = fig2,
        style = {'width':600, 'display': 'inline-block'}
        )
    ]),

    HTML.Div(
        dcc.Graph(
        id = "graph3",
        figure = fig3
        )
    )
])

@app.callback(
    Output("graph", "figure"),
    [Input("drop", "value")]
)
# funktion som visar en figur (cirkeldiagram) beroende på variabeln value
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
                    color_discrete_map={"Smittade":"palegreen", "Döda":"mediumseagreen"})
    fig.update_layout(transition_duration=500)
    return fig

if __name__ == "__main__":
    app.run_server(debug = True)