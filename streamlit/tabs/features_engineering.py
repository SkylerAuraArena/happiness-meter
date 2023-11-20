import streamlit as st
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

title = "***Features Engineering***"
sidebar_name = "Features Engineering"

# Configurer le format sans virgules pour les grands nombres
pd.options.display.float_format = '{:.0f}'.format

def run():

    # Import des jeux de données
    dir_path = os.path.dirname(os.path.realpath(__file__))
    csv_path = os.path.join(dir_path, "../../data/df_global.csv")
    df = pd.read_csv(csv_path)

    st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/2.gif")
    st.title(title)

    st.markdown("---")
    
    st.markdown("Le ***feature engineering*** est crucial afin de lancer des modèles de ***machine learning*** car il va permettre aux algorithmes de comprendre les \
            données explicatives et de les exploiter dans des calculs nécessaires aux prédictions. Pour se faire, nous devons commencer par procéder à \
            une réduction de dimensions. Suite au ***préprocessing***, le jeu de données est composé de **10 variables** après le retrait de 'Country name' et  \
            'year', variables qui n'apportent pas d'informations pertinentes au modèle:")
    
    df_forML = df.drop(['Country name','year'],axis=1)
    
    agree = st.checkbox("Afficher le jeu de données traité sans les colonnes 'Country name' et 'year'")
    if agree:
        df_forML.index = df_forML.index + 1
        st.dataframe(df_forML.head(5))
        st.write(df_forML.shape)

    
    df_forML.to_csv('df_ml.csv', index=False)
    params = df_forML.drop('Life Ladder', axis=1)
    target = df_forML['Life Ladder']
    
    st.markdown('Puis nous avons procédé aux étapes suivantes:')
    
    st.markdown("- **Séparation du jeu de données en jeu d'entrainement et jeu de test**")

    # Instanciation des jeux d'entraînement et de test. 
    X_train, X_test, y_train, y_test = train_test_split(params,
                                                        target,
                                                        test_size=0.2,
                                                        random_state=42)
    
    
    st.code('''
    feats = df_global.drop('Life Ladder', axis=1)
    target = df_global['Life Ladder']
            
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(feats,
                                                        target,
                                                        test_size=0.2,
                                                        random_state=42)''', language='python')
    
    st.write("- **Utilisation du** ***OneHotEncoder***")
    
    st.markdown( "Les modèles de ***machine learning*** n’étant pas en mesure d’**interpréter les variables qualitatives**, nous devons encoder le nom des régions afin de rendre ces valeurs exploitables dans **X_train** et **X_test**. Nous utilisons donc la méthode nommée ***One Hot Encoding*** qui créera n-1 colonnes remplies de valeurs booléennes pour savoir si cette ligne appartient à la région indiquée par le nom de la colonne.")
    
    # utilisation du OneHotEncoder
    ohe = OneHotEncoder(drop="first", sparse=False)

    # Adaptation de l'encodeur aux données d'entraînement
    encoded_train = ohe.fit_transform(X_train[['Regional indicator']])

    # Transformation des données de test
    encoded_test = ohe.transform(X_test[['Regional indicator']])
    # Remplacement des colonnes originales par les nouvelles colonnes transformées
    cat_train = pd.DataFrame(encoded_train, columns=ohe.get_feature_names_out(['Regional indicator']), index=X_train.index)
    cat_test = pd.DataFrame(encoded_test, columns=ohe.get_feature_names_out(['Regional indicator']), index=X_test.index)

    # Suppression de la colonne "Regional indicator dans les jeux d'entraînement et de test."
    X_train = X_train.drop('Regional indicator', axis=1)
    X_test = X_test.drop('Regional indicator', axis=1)

    # Concaténation des jeux avec le jeu encodé
    X_train_concat = pd.concat([X_train,cat_train], axis = 1)
    X_test_concat = pd.concat([X_test,cat_test], axis = 1)
    
    st.markdown("On obtient des jeux d'entrainement et de test finaux pour lequels la colonne 'Regional indicator' a bien été encodée.\
                Les jeux contiennent dorénavant **17 variables explicatives**. Le jeu de données est prêt pour l'entraînement de modèles.")

    agree = st.checkbox('Afficher **X_train** encodé')
    if agree:
        X_train_concat.index = X_train_concat.index.astype(int)
        # On convertit l'index pour enlever la virgule
        X_train_concat.reset_index(inplace=True)
        X_train_concat['index'] = X_train_concat['index'].map('{:.0f}'.format)
        X_train_concat.set_index('index', inplace=True)
        st.dataframe(X_train_concat.head())
        
    
    # On obtient un jeu final pour lequel la colonne 'Regional indicator' a bien été encodé
    # Le dataset est prêt pour l'entraînement de modèles.