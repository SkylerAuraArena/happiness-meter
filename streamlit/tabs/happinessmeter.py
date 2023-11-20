import streamlit as st
import pandas as pd
import numpy as np
import sklearn
from joblib import load
import os
from sklearn.preprocessing import MinMaxScaler
import pickle
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import os

title = "Happiness Meter"
sidebar_name = "Happiness Meter"
prediction = "Happiness Score :"

cols=['Log GDP per capita','Social support','Healthy life expectancy at birth','Freedom to make life choices','Generosity',
    'Perceptions of corruption','Positive affect','Negative affect']

dir_path = os.path.dirname(os.path.realpath(__file__))
csv_path = os.path.join(dir_path, "../../data/data2022.csv")
df_country = pd.read_csv(csv_path, sep=';')

def normalize_array(df):
    scaler=MinMaxScaler()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    scaler_path = os.path.join(dir_path, "../../models/scaler.pkl")
    loaded_scaler = load(scaler_path)
    with open(scaler_path, 'rb') as file:
        loaded_scaler = pickle.load(file)
    df[cols]=loaded_scaler.transform(df[cols])
    return df

def predict(continent, gdp, socsup, life_exp, freedom, generosity, corruption, positive, negative):
    # La colonne pour l'Europe Centrale et de l'Est est supprimée car elle est la référence.
    X_test = pd.DataFrame({
        'Log GDP per capita': [gdp],
        'Social support': [socsup],
        'Healthy life expectancy at birth': [life_exp],
        'Freedom to make life choices': [freedom],
        'Generosity': [generosity],
        'Perceptions of corruption': [corruption],
        'Positive affect': [positive],
        'Negative affect': [negative],
        'Regional indicator_Commonwealth of Independent States': [0],
        'Regional indicator_East Asia': [0],
        'Regional indicator_Latin America and Caribbean': [0],
        'Regional indicator_Middle East and North Africa': [0],
        'Regional indicator_North America and ANZ': [0],
        'Regional indicator_South Asia': [0],
        'Regional indicator_Southeast Asia': [0],
        'Regional indicator_Sub-Saharan Africa': [0],
        'Regional indicator_Western Europe': [0]
    })
    if continent != 'Central and eastern Europe':
        X_test['Regional indicator_' + continent] = 1
    X_test = normalize_array(X_test)
    # Chemin absolu vers le dossier contenant app.py
    model_path = os.path.join(dir_path, "../../models/happinessmeter.joblib")
    loaded_model = load(model_path)
    return loaded_model.predict(X_test)

def find_life_ladder_closest_countries(predicted_value, df, num_countries=5):
    # Calculer la différence absolue entre la valeur prédite et chaque valeur dans le dataframe
    # Nettoyer la chaîne de caractères pour enlever les crochets
    predicted_value = predicted_value.strip("[]")
    # Convertir la chaîne de caractères nettoyée en flottant
    predicted_value = float(predicted_value)
    # Convertir la colonne en string si ce n'est pas déjà le cas
    if df['Life Ladder'].dtype != 'O':  # 'O' signifie object
        df['Life Ladder'] = df['Life Ladder'].astype(str)

    # Remplacer les virgules par des points
    df['Life Ladder'] = df['Life Ladder'].str.replace(',', '.')
    df = df.sort_values(by='Life Ladder', ascending=False).reset_index(drop=True)
    df.index = df.index + 1
    # Convertir la colonne en numérique
    df['Life Ladder'] = pd.to_numeric(df['Life Ladder'], errors='coerce')
    # Calculer la différence
    df['Difference'] = df['Life Ladder'].apply(lambda x: abs(x - predicted_value))
    # Trier le dataframe par différence et prendre les premiers pays
    closest_countries = df.sort_values('Difference').head(num_countries)
    return closest_countries

def find_closest_countries(predicted_values, df, num_countries=5):
    # Calcule la différence absolue entre les variables et chaque valeur dans le dataframe
    closest_countries = []
    # Normalisation des valeurs
    values_dict = {col: [val] for col, val in zip(cols, predicted_values)}
    df_predicted_values = pd.DataFrame(values_dict)
    # Transforme le dataframe en liste
    predicted_values = df_predicted_values.values.tolist()[0]

    for i, v in enumerate(cols):
        # Convertion de la chaîne de caractères nettoyée en flottant
        predicted_value = float(predicted_values[i])
        # Convertion de la colonne en string si ce n'est pas déjà le cas
        if df[v].dtype != 'O':  # 'O' signifie object
            df[v] = df[v].astype(str)
        # Remplacement des virgules par des points
        df[v] = df[v].str.replace(',', '.')
        df = df.sort_values(by=v, ascending=False).reset_index(drop=True)
        df.index = df.index + 1
        # Convertion de la colonne en valeurs numériques
        df[v] = pd.to_numeric(df[v], errors='coerce')
        # Calculer la différence
        df['Difference'] = df[v].apply(lambda x: abs(x - predicted_value))
        # Trie le dataframe par différence et prendre les premiers pays
        closest_countries.append(df.sort_values('Difference').head(num_countries))
    return closest_countries

def run():

    dir_path = os.path.dirname(os.path.realpath(__file__))
    img_path = os.path.join(dir_path, "../assets/happiness_meter.png")
    st.image(img_path)

    st.title(title)

    st.markdown("---")
    
    st.markdown("Veuillez sélectionner les valeurs afin d'obtenir le score de bonheur correspondant. Les valeurs par défaut correspondent aux moyennes de chaque variable.")

    continent = st.selectbox(label='Sélectionner le continent à attribuer pour la prédiction :',
    options=('Central and eastern Europe', 'Commonwealth of Independent States', 'East Asia', 'Latin America and Caribbean', 'Middle East and North Africa', 'North America and ANZ', 'South Asia', 'Southeast Asia', 'Sub-Saharan Africa', 'Western Europe'))
    gdp = st.slider(label='Log GDP per capita', min_value=0.00, max_value=13.00, value=9.38)
    socsup = st.slider(label='Social support level', min_value=0.00, max_value=10.00, value=8.13) / 10
    life_exp = st.slider(label='Healthy life expectancy at birth', min_value=0.00, max_value=100.00, value=63.60)
    freedom = st.slider(label='Freedom to make life choices', min_value=0.00, max_value=10.00, value=7.47) / 10
    generosity = st.slider(label='Generosity', min_value=-1.00, max_value=10.00, value=-0.01) / 10
    corruption = st.slider(label='Perception of corruption', min_value=0.00, max_value=10.00, value=7.40) / 10
    positive = st.slider(label='Positive affects', min_value=0.00, max_value=10.00, value=7.10) / 10
    negative = st.slider(label='Negative affects', min_value=0.00, max_value=10.00, value=2.68) / 10
    trigger = st.button(label="Prédire", type="primary")
    if trigger:
        prediction = str(predict(continent, gdp, socsup, life_exp, freedom, generosity, corruption, positive, negative))
        st.write('Le niveau de bien-être prédit est de ', prediction.strip("[]"))
        # Compare avec les pays du dataframe
        life_ladder_closest_countries = find_life_ladder_closest_countries(prediction, df_country)
        st.write(f'Pays ayant eu un niveau de bien-être le plus proche en 2022 (sur {len(df_country)} pays) :')
        st.dataframe(life_ladder_closest_countries[['Country name', 'Life Ladder','Difference']])

        closest_countries = find_closest_countries([gdp, socsup, life_exp, freedom, generosity, corruption, positive, negative], df_country)
        for i in range(len(cols) - 1):
            st.write(f'Pays ayant eu un niveau de {cols[i]} le plus proche en 2022 (sur {len(df_country)} pays) :')
            st.dataframe(closest_countries[i][['Country name', 'Life Ladder', cols[i], 'Difference']])