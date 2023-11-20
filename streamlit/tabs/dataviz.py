import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import folium
from streamlit_folium import folium_static
from streamlit_folium import st_folium
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import os

title = "Visualisation"
sidebar_name = "Visualisation"

def load_data(file_path):
    return pd.read_csv(file_path)

def run():

    dir_path = os.path.dirname(os.path.realpath(__file__))
    img_path = os.path.join(dir_path, "../assets/happiness_squared.png")
    st.image(img_path)

    st.title(title)
    
    # Import des jeux de données
    dir_path = os.path.dirname(os.path.realpath(__file__))
    csv_paths = {
        "global": "../../data/df_global.csv",
        "mean_region": "../../data/df_global_mean_region.csv",
        "df_global_groupby_year": "../../data/df_global_groupby_year.csv",
        "df_global_carte": "../../data/df_global_carte.csv",
        "df_global_mean": "../../data/df_global_mean.csv",
        "country_list": "../../data/country_list.csv",
    }
    data = {name: load_data(os.path.join(dir_path, path)) for name, path in csv_paths.items()}
    df_global = data["global"]
    df_global_mean_region = data["mean_region"]
    df_global_groupby_year = data["df_global_groupby_year"]
    df_global_carte = data["df_global_carte"]
    df_global_mean = data["df_global_mean"]
    df_country_list = data["country_list"]
    
    # Arrondissement des scores de Life Ladder à une décimale
    df_global_mean_region['Life Ladder']=np.round(df_global_mean_region['Life Ladder'],1)
    df_global_mean_region=df_global_mean_region[['Country name','Regional indicator','Life Ladder']]

    selected_chart = st.radio(' ', ['Cartographie du bonheur'
    , 'Corrélation des indicateurs', 'Évolution des variables au fil du temps'])

    if selected_chart == 'Cartographie du bonheur':

            st.header("Les nuances du bonheur à l'échelle planétaire")

            # Import du GeoJSON qui nous servira pour les fontières de la map
            geojson_data = os.path.join(dir_path, "../../data/countries.geojson")
            with open(geojson_data, encoding='utf-8') as f:
                geojson_data=f.read()

            selected_year = st.slider('Sélectionnez l\'année', min_value=int(df_global_carte['year'].min()), max_value=int(df_global_carte['year'].max()))

            # Filtre le DataFrame en fonction de l'année sélectionnée
            filtered_df = df_global_carte[df_global_carte['year'] == selected_year]

            #On créer la map
            m = folium.Map(location=[0, 0], zoom_start=1.3)

            # On ajoute les couleurs en fonction du score de Life Ladder de df_global
            folium.Choropleth(
            geo_data=geojson_data,
            name='choropleth',
            data=filtered_df,
            columns=['Country name', 'Life Ladder'],  
            key_on='feature.properties.ADMIN',  
            fill_color='RdYlGn', 
            fill_opacity=0.7,
            line_opacity=0.2,
            nan_fill_color='white',
            legend_name='Score de bonheur'
            ).add_to(m)

            if st.button('Afficher la carte toutes années confondues'):
                m_all_years = folium.Map(location=[0,0], zoom_start=1.3)
                folium.Choropleth(
                geo_data=geojson_data,
                name='choropleth',
                data=df_global_carte,
                columns=['Country name', 'Life Ladder'],  
                key_on='feature.properties.ADMIN',  
                fill_color='RdYlGn', 
                fill_opacity=0.7,
                line_opacity=0.2,
                nan_fill_color='white',
                legend_name='Score de bonheur'
                ).add_to(m_all_years)


                folium_static(m_all_years)
            else:
                folium_static(m)

            # Boxplot de Life Ladder par continent
            st.subheader("Inégalité du score de Life Ladder parmi les continents")  
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.boxplot(x='Regional indicator', y='Life Ladder', data=df_global_mean_region, ax=ax,color="#aad3df")
            plt.xticks(rotation=45)

            ax.set_facecolor('white') 
            ax.grid(True, linestyle='--', alpha=0.3, color='#bae0fc')  # Grille bleu très clair

            ax.set_xlabel('Régions')
            ax.set_ylabel('Life Ladder')
            ax.set_title('Boxplot de Life Ladder par région')
            # Ajouter le graphique à Streamlit
            st.pyplot(fig)

    elif selected_chart == 'Corrélation des indicateurs':

        sns.set()
        fig, ax = plt.subplots(figsize=(10, 8))
        heatmap = sns.heatmap(df_global_mean.corr(), annot=True, cmap='Blues', fmt='.2f', linewidths=.5, ax=ax)

        # Ajout de la heatmap à Streamlit
        st.subheader("Quels indicateurs économiques et sociaux influent le plus sur le score de bonheur ?")
        st.pyplot(fig)

        st.subheader("Dans quelle mesure peut-on voir l'influence d'une variable sur le bonheur des habitants d'un pays ?")

        indicators_list3 = df_global.columns.difference(['year']).difference(['Country name']).difference(['Regional indicator']).difference(['Life Ladder'])
        selected_indicators3 = st.multiselect('Sélectionnez l\'indicateur à afficher:', indicators_list3)

        for indicator3 in selected_indicators3:
            # Création du graphique avec Plotly Express
            fig = px.scatter(df_global, x=indicator3, y='Life Ladder', color='Regional indicator', hover_data=['Country name'])
            # Affichage du graphique dans Streamlit
            st.plotly_chart(fig)    

    elif selected_chart == 'Évolution des variables au fil du temps':
        # Titre de l'application Streamlit
        st.subheader("Évolution des indicateurs au Fil du Temps")
        # Liste des indicateurs
        indicators_list = df_global_groupby_year.columns.difference(['Year'])
        selected_indicators = st.multiselect('Sélectionnez les indicateurs à afficher:', indicators_list)
        # Création du graphique
        fig, ax = plt.subplots(figsize=(10, 6))
        for indicator in selected_indicators:
            ax.plot(df_global_groupby_year['Year'], df_global_groupby_year[indicator], label=indicator)
        # Mise en forme du graphique
        ax.set_xlabel('Année')
        ax.set_ylabel('Valeur normalisée de l\'indicateur')
        ax.set_title('Évolution des indicateurs au fil des années')
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7,color='#bae0fc')
        ax.set_facecolor('#ffffff')
        # Ajout du graphique à Streamlit
        st.pyplot(fig)

        # Titre de l'application Streamlit
        st.subheader("Zoom par pays")
        Country_list = df_country_list['Country name']
        selected_Country = st.multiselect('Sélectionnez un pays à afficher:', Country_list)
        
        indicators_list2 = df_global.columns.difference(['year']).difference(['Country name'])
        selected_indicators2 = st.multiselect('Sélectionnez les indicateurs à afficher:', indicators_list2)

        selected_chart = st.radio(' ', ['Données normalisées'
        , 'Données non normalisées'])

        if selected_chart == 'Données normalisées':

            df_global_filtered = df_global[df_global['Country name'].isin(selected_Country)]

            normalized_df = (df_global_filtered.iloc[:, 3:] - df_global_filtered.iloc[:, 3:].min()) / (df_global_filtered.iloc[:, 3:].max() - df_global_filtered.iloc[:, 3:].min())
            normalized_df = pd.concat([df_global_filtered[['Country name','Regional indicator','year']], normalized_df], axis=1)

            # Création du graphique
            fig, ax = plt.subplots(figsize=(10, 6))
            for indicator2 in selected_indicators2:
                ax.plot(normalized_df['year'], normalized_df[indicator2], label=indicator2)
            # Mise en forme du graphique
            ax.set_xlabel('Année')
            ax.set_ylabel('Valeur normalisée de l\'indicateur')
            ax.set_title('Évolution des indicateurs au fil des années')
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.7,color='#bae0fc')
            ax.set_facecolor('#ffffff')
            # Ajout du graphique à Streamlit
            st.pyplot(fig)

        elif selected_chart == 'Données non normalisées':
            df_global_filtered = df_global[df_global['Country name'].isin(selected_Country)]
                    
            # Création du graphique
            fig, ax = plt.subplots(figsize=(10, 6))
            for indicator2 in selected_indicators2:
                ax.plot(df_global_filtered['year'], df_global_filtered[indicator2], label=indicator2)
            # Mise en forme du graphique
            ax.set_xlabel('Année')
            ax.set_ylabel('Valeur de l\'indicateur')
            ax.set_title('Évolution des indicateurs au fil des années')
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.7,color='#bae0fc')
            ax.set_facecolor('#ffffff')
            # Ajout du graphique à Streamlit
            st.pyplot(fig)

    else : None