import pandas as pd
import streamlit as st
import numpy as np
from plotnine import *
import plotly.express as px




players = pd.read_csv("data/players.csv")

sidebar_head = st.sidebar.header("Estadísticas Transfermarkt 5 Grandes Ligas 2022/2023")
sidebar = st.sidebar.selectbox("Escoja la opción a estudiar",
    ("-","LaLiga","Premier League","Bundesliga","Ligue 1","Serie A","Comparativa 5 Grandes Ligas")
)
players["yellows"] = players["yellow"] + players["second_yellow"]

if sidebar != "Comparativa 5 Grandes Ligas" and sidebar != "-":
    column1,column2 = st.columns(2)

    with column1:
        radio = st.radio("Escoge la variable del eje y",["goals","assists","g/a","yellows","red"])

    with column2:
        radio_x = st.radio("Escoge la variable del eje x",["Partidos","Posición","Equipo"])
        
    liga = players[players.loc[:,"player_league"] == sidebar]
    if radio_x == "Partidos":
        apps_df = liga.loc[:,["name","appearances",radio,"player_team"]]
        fig_app = px.scatter(apps_df, x = "appearances",y = radio,
                            color="player_team",
                            hover_data=["name"])
        fig_app.update_layout(
        legend_title_text="Equipo",
        xaxis_title = 'Partidos Jugados'
        )
        st.plotly_chart(fig_app)

    elif radio_x == "Posición":
        position_df = liga.loc[:,["position",radio]].groupby("position").sum().reset_index()
        fig_pos = px.bar(position_df, x = "position",y = radio,
                        color="position")
        fig_pos.update_layout(
        legend_title_text="Posición",
        xaxis_title = 'Posición',
        xaxis={'categoryorder': 'total descending'},
        yaxis={'title': radio}
        )
        st.plotly_chart(fig_pos)

    elif radio_x == "Equipo":
        team_df = liga.loc[:,["player_team",radio]].groupby("player_team").sum().reset_index()
        fig_team = px.bar(team_df, x = "player_team",y = radio)
        fig_team.update_layout(
        xaxis_title = 'Equipo'
        )
        st.plotly_chart(fig_team)


    seleccion = st.selectbox(
            'Elige el equipo que quieres ver',
    liga.loc[:,"player_team"].unique())

    if seleccion is not None:
        col1, col2 = st.columns(2)

        with col2: 
            team = players.loc[:,["name","player_team","age"]].set_index("player_team").loc[seleccion,:].dropna()
            fig =  px.density_heatmap(team, x = "age",color_continuous_scale="Greens")
            fig.update_layout(
                title="Gráfico de Densidad",
                xaxis_title="Edad",
                yaxis_title="Densidad",
            )
            st.plotly_chart(fig)

        with col1:
            st.data_editor(team.reset_index().loc[:,["name","age"]])

elif sidebar == "Comparativa 5 Grandes Ligas":
    slider = st.selectbox("Escoja su comparativa", ["-","Valor de jugador 2024", "Estadísticas Partido"])
    
    if slider == "Valor de jugador 2024":
        valor_per_league = players.loc[:,["actual_league","value"]].dropna(subset = ["actual_league"]).groupby("actual_league").sum().reset_index()
        tarta = px.pie(valor_per_league,values = valor_per_league["value"],names = valor_per_league["actual_league"].unique(),title = "Jugadores más valiosos")
        st.plotly_chart(tarta)

    elif slider == "Estadísticas Partido":
        multiselect = st.multiselect("Método", ["Por ligas", "Total Equipos"])
        radio_ligas = st.radio("Escoge la variable del eje y",["goals","assists","g/a","yellows","red"]) 

        if multiselect == ["Por ligas"]: 
            datos_ligas = players.loc[:,["player_league",radio_ligas]].groupby("player_league").sum().reset_index()
            fig_datos_ligas = px.bar(datos_ligas, x = "player_league",y = radio_ligas,
                        color="player_league",title = "Estadísticas por ligas",
                        labels={'columna_x': 'Liga'})
            fig_datos_ligas.update_layout(legend_title_text="Ligas")
            st.plotly_chart(fig_datos_ligas)

        elif multiselect == ["Total Equipos"]:
            datos_equipos = players.loc[:,["player_league","player_team",radio_ligas]].groupby(["player_league","player_team"]).sum().reset_index()
            fig_datos_teams1 = px.bar(datos_equipos, x = "player_team",y = radio_ligas,
                        color="player_league",title = "Estadísticas por equipos y ligas")
            fig_datos_teams1.update_xaxes(showline=True, showgrid=False, zeroline=False, showticklabels=False, tickmode='array', tickvals=[])
            fig_datos_teams1.update_layout(legend_title_text="Ligas")
            st.plotly_chart(fig_datos_teams1)

        elif len(multiselect) == 2:
            col1,col2 = st.columns(2)
            datos_ligas = players.loc[:,["player_league",radio_ligas]].groupby("player_league").sum().reset_index()
            fig_datos_ligas = px.bar(datos_ligas, x = "player_league",y = radio_ligas,
                        color="player_league",title = "Estadísticas por ligas")
            fig_datos_ligas.update_layout(legend_title_text="Ligas")
            st.plotly_chart(fig_datos_ligas)

            datos_equipos = players.loc[:,["player_league","player_team",radio_ligas]].groupby(["player_league","player_team"]).sum().reset_index()
            fig_datos_teams = px.bar(datos_equipos, x = "player_team",y = radio_ligas,
                        color="player_league",title = "Estadísticas por equipos y ligas",
                        labels={'columna_x': 'Liga'})
            fig_datos_teams.update_layout(legend_title_text="Ligas")
            fig_datos_teams.update_xaxes(showline=True, showgrid=False, zeroline=False, showticklabels=False, tickmode='array', tickvals=[])
            st.plotly_chart(fig_datos_teams)
            