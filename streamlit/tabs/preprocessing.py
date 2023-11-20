import streamlit as st
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

title = "Préprocessing"
sidebar_name = "Préprocessing"

def run():

    # Import des jeux de données
    dir_path = os.path.dirname(os.path.realpath(__file__))

    csv_path = os.path.join(dir_path, "../../data/world-happiness-report.csv")
    df1 = pd.read_csv(csv_path)
    df1.index = df1.index + 1

    csv_path = os.path.join(dir_path, "../../data/world-happiness-report-2021.csv")
    df2_full = pd.read_csv(csv_path)
    df2_full.index = df2_full.index + 1

    csv_path = os.path.join(dir_path, "../../data/pays&continents.csv")
    df_continents = pd.read_csv(csv_path, sep=';')
    df_continents.index = df_continents.index + 1

    st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/2.gif")
    st.title(title)

    st.markdown("---")
    
    st.markdown("Dans cette partie, nous allons voir quels sont les traitements que nous avons effectués sur le jeu de données afin de le préparer pour la partie ** visualisation des données**. Comme expliqué dans la description des données, nous avons extrait de ***Kaggle*** deux bases de données :")
    
    st.markdown(
                """
                - World_hapiness_report.csv
                - World_hapiness_report_2021.csv""")

    st.write("### Concaténation") 

    st.write("Dès l'import des données, la table « World_hapiness_report_2021» est adaptée au format de la table « world_hapiness_report» et on y ajoute la colonne 'year' non présente. Les variables sont ensuite renommées pour permettre la fusion des deux jeux. La concaténation entre les deux tables est alors réalisable et est effectuée.")
    
    # Harmonisation par suppression des colonnes n'existant que dans le rapport 2021.
    df2=df2_full.drop(['Regional indicator','Standard error of ladder score','upperwhisker',
                    'lowerwhisker','Ladder score in Dystopia','Explained by: Log GDP per capita',
                    'Explained by: Social support','Explained by: Healthy life expectancy',
                    'Explained by: Freedom to make life choices','Explained by: Generosity',
                    'Explained by: Perceptions of corruption','Dystopia + residual'],axis=1)

    # Ajout de la colonne "year" sur le df2021 pour pouvoir le concatener avec le df1
    df2.insert(loc=1,column='year',value=2021)
    
    # Renommage des colonnes du df2021
    df2=df2.rename(columns={'Ladder score':'Life Ladder','Logged GDP per capita':'Log GDP per capita',
                            'Healthy life expectancy':'Healthy life expectancy at birth'})

    # Réindexation du df2021 par rapport au df1
    df2.index=df2.index+1950

    # Concaténation des deux jeux de données en un trosième jeu global.
    df_global=pd.concat([df1,df2],axis=0)
    
    agree = st.checkbox('Afficher le jeu de données concaténées contenant tous les données de 2005 à 2021, **df_global**')
    if agree:
        df_global['year'] = df_global['year'].astype(float).map('{:.0f}'.format)
        st.write(df_global.head(5))
        st.write(df_global.shape)
    
    st.write("### Ajout de la variable 'Regional indicator'")
    
    st.markdown("Dans la table « World_hapiness_report_2021», il existe une colonne « Regional indicator » avec les continents pour chaque pays. Cette variable peut être pertinente si on l’ajoute à notre jeu de données concaténé (**df_global**). Pour créer cette colonne dans notre **df_global**, nous fusionons la colonne « Regional indicator » avec notre **df_global**. Suite à cette étape, il reste encore des valeurs manquantes dans « Regional indicator ».")
            
    # Apurement du df2021 pour ne conserver que les noms de pays et de continent.
    df_continents_only=df2_full[['Country name','Regional indicator']] # Ajout de la colonne "Regional Indicator" pour indexer rattacher les pays à leur continent respectif indiqué dans le df2021.

    # Fusion fusion du df_global avec celui des continents.
    df_global2=df_global.merge(right=df_continents_only,on='Country name',how='outer')
    
    st.markdown("Pour y remédier, nous introduisons alors une nouvelle source de données '***pays&continents.csv***' qui permet, suite à une nouvelle fusion, de compléter les continents manquants de la variable « Regional indicator ».")
            
    # Déplacement de la colonne continent en 2e position.
    df_global2.insert(1,'Regional indicator',df_global2.pop('Regional indicator'))

    # Import du fichier contenant l'ensemble des pays et de leur continent de rattachement.
    agree = st.checkbox('Afficher le jeu de données contenant les continents')
    if agree:
        st.write(df_continents_only.head(5))
        st.write(df_continents_only.shape)
    
    # Fusion du dataset des continent avec notre dataset principal.
    df_global2=df_global.merge(right=df_continents,on='Country name',how='outer')
    
    # Déplacement de la colonne régional indicator en 2e position.
    df_global2.insert(1,'Regional indicator',df_global2.pop('Regional indicator'))

    agree = st.checkbox('Afficher le jeu de données sans continent manquant')
    if agree:
        df_global2.index = df_global2.index + 1
        st.write(df_global2.head(5)) 
        st.write(df_global2.shape)
    
    st.write("### Doublons et fautes d'orthographes")
    
    # Analyse des doublons : visiblement il n'y a pas de doublon.
    print(f'Il y a {df_global2.duplicated().sum()} doublons dans le jeu de données.')
    
    # Analyse de cohérence visuelle des données (orthographe, casse, etc.).
    #df_global2['Country name'].unique()
    
    st.write("L'analyse des doublons montre que le jeu de données n'en contient pas. En outre, l'orthographe des variables catégorielles est sans faute.")
        
    st.write("### Gestion des valeurs manquantes")
    
    st.write("Pour la gestion des valeurs manquantes, nous avons remarqué qu’il manquait généralement des modalités sur certaines variables selon \
            les années mais que les pays avaient toujours quelques années remplies pour chaque variable. Ainsi, nous avons décidé de remplacer les \
            valeurs manquantes par la médiane des valeurs groupées par pays.")
    
    size = df_global2.shape
    nan_values = df_global2.isna().sum().sort_values(ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(nan_values.index, nan_values)
    plt.xlabel('Nombre de valeurs manquantes')
    plt.ylabel('Colonnes')
    plt.title('Nombre de valeurs manquantes par colonne avant imputation')
    plt.legend().remove()  # Supprimer la légende
    st.pyplot(plt)

    st.write("Nous avons décidé de remplacer les valeurs manquantes par la médiane des valeurs groupées par pays pour poursuivre l'exploration.")
    
    # Calcul de la médiane en fonction des variables de pays groupés.
    test=df_global2.groupby('Country name')['Perceptions of corruption'].agg('median')
    
    # Exploration des differentes variables afin d'analyser les valeurs manquantes.
    df_global2.sort_values('Perceptions of corruption').tail(10)
    
    # Regroupement par pays pour poursuivre l'exploration des données.
    agree = st.checkbox('Afficher le jeu de données regroupées par pays')
    if agree:
        # On convertit l'index pour enlever la virgule
        df_global2.reset_index(inplace=True)
        df_global2['index'] = df_global2['index'].map('{:.0f}'.format)
        df_global2.set_index('index', inplace=True)
        df_global2['year'] = df_global2['year'].astype(float).map('{:.0f}'.format)
        st.write(df_global2[df_global2['Country name']=='Somalia'].head(5)) 
        st.write(df_global2[df_global2['Country name']=='Somalia'].shape)
    
    # Séparation des variables catégorielles et des variables numériques et obtention des titres des colonnes.
    cat_data_col = df_global2.select_dtypes(include=[object]).columns.tolist()
    num_data_col = df_global2.select_dtypes(include=[np.number]).columns.tolist()
    
    st.write("On impute ensuite la médiane à la place des valeurs manquantes par pays et par colonne et on vérifie l'action réalisée:")
    # Imputation de la médiane à la place des valeurs manquantes par pays et par colonne.
    for c in num_data_col:
        if c != 'year':
            df_global2[c]=df_global2.groupby('Country name')[c].transform(lambda x : x.fillna(x.median()))
    
    # Vérification des valeurs manquantes.
    
    size = df_global2.shape
    nan_values = df_global2.isna().sum().sort_values(ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(nan_values.index, nan_values)
    plt.xlabel('Nombre de valeurs manquantes')
    plt.ylabel('Colonnes')
    plt.title('Nombre de valeurs manquantes par colonne après la 1re imputation')
    plt.legend().remove()  # Supprimer la légende
    st.pyplot(plt)
    
    st.write("Le nombre de valeurs manquantes a bien diminué mais n'atteint pas zéro : on comprend ici que certaines valeurs manquantes n'ont pas pu etre remplies par manque de données et une impossibilité de calculer la médiane avec une absence de donnée. Ainsi, on émet l'hypothèse que ces pays sont à des scores du **quartile Q1** (premier quartile) par rapport au continent auxquel ils appartiennt.")

    # On comprend ici que certaines valeurs manquantes n'ont pas pu etre remplies par manque de données et impossibilité de calculer la mediane avec rien   
    
    # Exploration des lignes qui contiennent encore des valeurs manquantes.
    agree = st.checkbox('Afficher les lignes de **df_global** contenant encore des valeurs manquantes')
    if agree:
        st.write(df_global2[df_global2.isna().any(axis=1)].head(20)) 
        st.write(df_global2[df_global2.isna().any(axis=1)].shape)
    
    # Par manque de données, on émet l'hypothèse que ces pays sont à des scores de q1 par rapport au continent auxquel ils appartiennt

    # Imputation de la valeur du premier quartile de la zone continentale de rattachement à la place des valeurs manquantes par pays et par colonne.
    for c in num_data_col:
        df_global2[c]=df_global2.groupby('Regional indicator')[c].transform(lambda x : x.fillna(x.quantile(q=0.25)))
    
    # Vérification des valeurs manquantes.
    st.write(f'Le nombre de valeurs manquantes par colonne après imputation est de : {df_global2.isna().sum().sum()} valeur manquante.')

    st.markdown("Ainsi, après la 2e imputation via les scores du quartile Q1, il n'y a plus de valeurs manquantes dans le jeu de données.")
    
    # Vérification des valeurs manquantes. # le graphe est vide confirmant l'absence de valeurs manquantes
    
    size = df_global2.shape
    nan_values = df_global2.isna().sum().sort_values(ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(nan_values.index, nan_values)
    plt.xlabel('Nombre de valeurs manquantes')
    plt.ylabel('Colonnes')
    plt.title('Nombre de valeurs manquantes par colonne après la 2nde imputation')
    plt.legend().remove()  # Supprimer la légende
    st.pyplot(plt)
    
    # On constate qu'il n'y a plus de valeur manquante.  
    
    st.markdown("On a maintenant un jeu de données complet, entier, sans valeurs manquantes ; sans faute, ni doublon.")
    # Affichage du jeu de données complet et sans valeur manquante.
    st.write(df_global2.head(5))
    st.write(df_global2.shape)