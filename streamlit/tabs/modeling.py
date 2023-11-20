import streamlit as st
import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import MinMaxScaler, StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

title = "Modélisation"
sidebar_name = "Modélisation"

def run():

    st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/2.gif")
    st.title(title)

    st.markdown("---")
    
    st.write("### Problématique")
    
    st.markdown('Notre jeu de données porte sur la vision du bonheur ressenti par un échantillon de la population de 166 pays. \
            Pour rappel, le classement est établi à partir de **8 critères principaux** qui contribuent à former l’indice dit de ***Life Ladder*** \
            ou échelle de qualité de vie / satisfaction plutôt que du bonheur.')
    st.markdown('Nous nous sommes donc fixés pour objectif de mettre en place un modèle qui nous permettrait d’estimer le niveau de la variable ***Life \
            Ladder*** à partir des autres critères pour les années postérieures à 2021. Ainsi, nous avons retenu 2 types de modèles : **régression** et \
            **classification**. Ces approches nous permettent respectivement de :')
            
    st.markdown( 
        """
        - Tenter de **prédire la valeur de *Life Ladder*** pour un pays en particulier.
        - Tenter de **classer un pays** parmi différents groupes de valeur de ***Life Ladder***.""")
        
    st.write("Nous présentons ci-dessous les résultats obtenus en fonction des deux types d'approches. À noter que pour chacune des approches, il s'agit de modèle normalisé car les résultats de la standardisation n'ont pas présentés de résultats bien différents.")
    
    # Affichage de deux types de modélisation
    selected_chart = st.radio('Souhaitez-vous traiter le problème en tant que problème de **régression** ou de **classification** ?',('Régression','Classification'))
    
    # Import des jeux de données
    dir_path = os.path.dirname(os.path.realpath(__file__))
    csv_path = os.path.join(dir_path, "../../data/X_train.csv")
    X_train = pd.read_csv(csv_path)
    csv_path = os.path.join(dir_path, "../../data/X_test.csv")
    X_test = pd.read_csv(csv_path)
    csv_path = os.path.join(dir_path, "../../data/y_train.csv")
    y_train = pd.read_csv(csv_path)
    csv_path = os.path.join(dir_path, "../../data/y_test.csv")
    y_test = pd.read_csv(csv_path)

    if selected_chart == 'Régression': 
        st.write("### Modélisation : Problème de Régression")
        
        #normalisation 
        scaler=MinMaxScaler()
        cols=['Log GDP per capita','Social support','Healthy life expectancy at birth','Freedom to make life choices','Generosity',
            'Perceptions of corruption','Positive affect','Negative affect']
        X_train[cols]=scaler.fit_transform(X_train[cols])
        X_test[cols]=scaler.transform(X_test[cols])
        
        def prediction(regressor):
            if regressor == 'Linear Regressor':
                rg = LinearRegression()
            elif regressor == 'Ridge Regressor':
                rg = Ridge()
            elif regressor == 'Decision Tree Regressor':
                rg = DecisionTreeRegressor()
            elif regressor == 'Random Forest':
                rg = RandomForestRegressor()
            elif regressor == 'KNeighbors Regressor':
                rg = KNeighborsRegressor()
            rg.fit(X_train, y_train)
            return rg

        def scores(rg):
            return rg.score(X_test, y_test)
            
        choix = ['Linear Regressor', 'Ridge Regressor', 'Decision Tree Regressor', 'Random Forest', 'KNeighbors Regressor']
        option = st.selectbox('Choix du modèle', choix)
        st.write('Le modèle choisi est :', option)

        rg = prediction(option) 
        st.write('Score du modèle choisi:', scores(rg)) 
    
    if selected_chart == 'Classification': 
        st.write("### Modélisation : Problème de Classification")
        
        #normalisation 
        scaler=MinMaxScaler()
        cols=['Log GDP per capita','Social support','Healthy life expectancy at birth','Freedom to make life choices','Generosity',
            'Perceptions of corruption','Positive affect','Negative affect']
        X_train[cols]=scaler.fit_transform(X_train[cols])
        X_test[cols]=scaler.transform(X_test[cols])
        
        # On créé une fonction pour déterminer la catégorie

        def categorie(valeur):
            if valeur < 3.5:
                return 'Très bas'
            elif valeur >= 3.5 and valeur <= 4.63:
                return 'Bas'
            elif valeur >= 4.63 and valeur <= 5.76:
                return 'Moyen'
            elif valeur >= 5.76 and valeur <= 6.89:
                return 'Haut'
            else:
                return 'Très Haut'

        y_train['Categorie Life Ladder'] = y_train['Life Ladder'].apply(categorie)
        y_train=y_train.drop('Life Ladder',axis=1)
        
        # On applique la meme chose sur y_test

        y_test['Categorie Life Ladder'] = y_test['Life Ladder'].apply(categorie)
        y_test=y_test.drop('Life Ladder',axis=1) 
        y_train=y_train['Categorie Life Ladder'].values
        y_test=y_test['Categorie Life Ladder'].values

        def prediction(classifier):
            if classifier == 'Logistic Regression':
                clf = LogisticRegression()  
            elif classifier == 'Decision Tree Classifier':
                clf = DecisionTreeClassifier()
            elif classifier == 'Support Vector Classifier':
                clf = SVC()  
            elif classifier == 'Multilayer Perception Classifier':
                clf = MLPClassifier()  
            elif classifier == 'Random Forest Classifier':
                clf = RandomForestClassifier()
            clf.fit(X_train, y_train)
            return clf

        def scores(clf, choice):
            if choice == 'Accuracy':
                return clf.score(X_test, y_test)
            elif choice == 'Matrice de confusion':
                return confusion_matrix(y_test, clf.predict(X_test))

        choix = ['Decision Tree Classifier', 'Logistic Regression', 'Support Vector Classifier', 'Multilayer Perception Classifier', 'Random Forest Classifier']
        option = st.selectbox('Choix du modèle', choix)
        st.write('Le modèle choisi est :', option)
        
        clf = prediction(option)
        display = st.radio('Que souhaitez-vous montrer ?', ('Accuracy', 'Matrice de confusion'))
        if display == 'Accuracy':
            st.write(scores(clf, display))
        elif display == 'Matrice de confusion':
            st.dataframe(scores(clf, display)) 
        st.markdown("Dans les deux types d'approches du problème en régression ou classification, c'est le modèle de ***Random Forest*** qui a été retenu.")
