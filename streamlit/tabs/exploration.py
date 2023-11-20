import streamlit as st
import os
import pandas as pd

title = "Exploration"
sidebar_name = "Exploration"

# Import des jeux de données
dir_path = os.path.dirname(os.path.realpath(__file__))

csv_path = os.path.join(dir_path, "../../data/world-happiness-report.csv")
df1 = pd.read_csv(csv_path)
df1.index = df1.index + 1

csv_path = os.path.join(dir_path, "../../data/world-happiness-report-2021.csv")
df2_full = pd.read_csv(csv_path)
df2_full.index = df2_full.index + 1

def run():

    dir_path = os.path.dirname(os.path.realpath(__file__))
    img_path = os.path.join(dir_path, "../assets/happiness_explo.png")
    st.image(img_path)

    st.title(title)

    st.markdown("---")
    
    st.markdown("Nous avons utilisé les données fournies dans les différentes éditions du ***World Happiness Report*** depuis 2012, bien que certaines données \
                remontent à 2005. Le rapport est basé sur huit indicateurs permettant d'établir l'indicateur global de qualité de vie, le ***Life Ladder***. \
                Ce dernier mesure le bien-être et s'appuie sur des questions posées aux habitants des pays, qui évaluent leur vie sur une échelle de 0 à 10.\
                C'est l'**indicateur principal**, dérivé des suivants dont les descriptions sont décrites ci-après.")
                
    st.markdown(
    """
    La première table à disposition "World-hapiness-report" contient des données de 2005 à 2020 du ***Life Ladder*** et des variables suivantes : 
    - ***Country name*** : nom du pays
    - ***year*** : année d'évaluation des données
    - ***log GDP per capita*** : PIB enregistré par habitant  qui donne des informations sur la taille de l’économie et ses performances.
    - ***Social support*** : un soutien social ou le fait d'avoir quelqu'un sur qui compter en cas de difficultés.
    - ***Healthy life expectancy at birth*** : espérance de vie en bonne santé  à la naissance
    - ***Freedom to make life choices*** : mesure la liberté qu'a une personne de prendre des décisions concernant sa propre vie
    - ***Generosity*** : mesure la générosité de la population
    - ***Perceptions of corruption*** : comment les habitants perçoivent le pays au niveau de la corruption
    - ***Positive affect*** : positivité de la population
    - ***Negative affect*** : négativité de la population
    """)
    
    agree = st.checkbox('Afficher la table "World-hapiness-report"')
    if agree:
        df1['year'] = df1['year'].astype(float).map('{:.0f}'.format)
        st.write(df1.head(5))
        st.write(df1.shape)
    
    st.markdown(
    """
    La deuxième table à disposition "World-hapiness-report-2021" contient des données de 2021 du ***Ladder score*** (équivalent au ***Life Ladder***) ainsi que mes variables \
        suivantes : 
    - ***Country name*** : nom du pays
    - ***Regional indicator*** : indicateur régional / continent
    - ***Standard error of ladder score*** : erreur type du score du bien-être
    - ***upperwhisker*** : intervalle de confiance supérieur du score de bonheur
    - ***lowerwhisker*** : intervalle de confiance inférieur du score de bonheur
    - ***log GDP per capita*** : PIB enregistré par habitant  qui donne des informations sur la taille de l’économie et ses performances.
    - ***Social support*** : un soutien social ou le fait d'avoir quelqu'un sur qui compter en cas de difficultés.
    - ***Healthy life expectancy at birth*** : espérance de vie en bonne santé à la naissance
    - ***Freedom to make life choices*** : mesure la liberté qu'a une personne de prendre des décisions concernant sa propre vie
    - ***Generosity*** : mesure la générosité de la population
    - ***Perceptions of corruption*** : comment les habitants perçoivent le pays au niveau de la corruption
    - ***Ladder score in Dystopia*** : La dystopie est un pays imaginaire qui compte les habitants les moins heureux du monde. 
    - ***Dystopia + residual*** : les résidus, ou composantes inexpliquées, diffèrent pour chaque pays, reflétant la mesure dans laquelle les six variables\
        sur-expliquent ou sous-expliquent les évaluations de vie moyennes pour 2019-2021. Ces résidus ont une valeur moyenne proche de zéro sur l’ensemble \
            des pays
    """)

    agree = st.checkbox('Afficher la table "World_hapiness_report-2021"')
    if agree:
        st.write(df2_full.head(5))
        st.write(df2_full.shape)
        