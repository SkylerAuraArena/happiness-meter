import streamlit as st
import os

title = "Étude du bien-être dans le monde"
sidebar_name = "Introduction"

def run():
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    img_path = os.path.join(dir_path, "../assets/happiness_rect.png")
    st.image(img_path)

    st.title(title)

    st.markdown("---")

    st.write("### Contexte")
    st.write("En 1972, le Bhoutan a introduit l'indicateur du Bonheur National en remplacement du Produit Intérieur Brut. En 2012,\
            l'Assemblée Générale des Nations Unies a adopté la résolution 66/281 proclamant le 20 mars comme Journée Internationale \
            du Bonheur.")
    st.write("Cette résolution intègre la notion de « pursuit of happiness » ou recherche du bonheur comme objectif de \
            développement pour les politiques publiques des pays membres. Cette notion est ancienne puisqu'elle est déjà présente \
            dans le préambule de la déclaration d'indépendance des États-Unis d'Amérique. Pour suivre l'évolution du bonheur dans \
            les différents pays du monde, le ***World Happiness Report*** est publié chaque année par le ***Sustainable Development Solutions \
            Network***en utilisant les données du ***Gallup World Poll***.")
    st.write("Ces données sont collectées par ***The Gallup Organization***, une \
            entreprise américaine spécialisée dans les sondages. L'ensemble des données publiées annuellement sont disponibles sur https://worldhappiness.report.")
            
    st.write("### Objectif")
    
    st.markdown("Dans ce projet, nous allons effectuer une analyse approfondie des données par le ***World Hapiness Report***. Cette enquête a \
                pour objectif d'estimer le bonheur des pays autour de la planète à l'aide de mesures socio-économiques. Nous présenterons également\
                ces données à l'aide de visualisation intéractives et réaliserons la modélisation de ces données.")

    st.write("### Problématiques")
    
    st.markdown(
    """
    L'objectif de notre analyse est de comprendre les problématiques suivantes :
    - Pourquoi certains pays sont-ils mieux classés que d'autres dans ce rapport ? Constate-t-on une continuité dans les classements ?
    - En quoi certaines variables influencent-elles plus que d'autres les résultats finaux ? Peut-on identifier des indicateurs clairs permettant d'expliquer \
        le niveau de bonheur d'un pays ?
    - Est-il possible de proposer un modèle de prédiction pour évaluer le score probable d'un pays dans une future édition du rapport ?
    """)