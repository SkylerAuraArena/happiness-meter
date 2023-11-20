import streamlit as st
import os

title = "Conclusion & perspectives"
sidebar_name = "Conclusion"

def run():

    dir_path = os.path.dirname(os.path.realpath(__file__))
    img_path = os.path.join(dir_path, "../assets/happiness_conclusions.png")
    st.image(img_path)

    st.title(title)

    st.markdown("---")

    st.write("#### ***Il n’y a point de chemin vers le bonheur. Le bonheur, c’est le chemin.*** – Anonyme")

    st.write("### Conclusion")

    st.write("""Notre analyse a tenté de déterminer les facteurs qui influencent le niveau de bonheur des populations ou plutôt leur qualité de vie. Sans définir le bonheur de manière catégorique, le rapport identifie des critères contribuant à l'amélioration générale de la qualité de vie et du sentiment de satisfaction générale des populations.""")
    st.write("""Les résultats obtenus ont permis de développer un simulateur de prédiction de la qualité de vie ou ***Life Ladder***. Ce modèle, entraîné sur les données de 2006 à 2021 pour 166 pays, est capable de prédire cet indice en fonction de sous-paramètres dont les valeurs peuvent varier. Ainsi, le simulateur peut être utilisé pour des simulations ou pour évaluer les variations de la qualité de vie en fonction de la modification de ces paramètres.""")

    bullet_points = [
    "Le coefficient de ***Gini*** (mesure des inégalités)",
    "Le rapport sur la liberté de la presse de ***Reporter sans Frontières***",
    "L’index de liberté économique de la fondation ***Heritage***"
    ]

    st.write("### Perspectives")
    st.write("Afin de poursuivre cette étude, il serait intéressant d'approfondir l'analyse en croisant les données du rapport initial avec celles d'autres études telles que :")
    st.write("".join([f"- {item}\n" for item in bullet_points]))