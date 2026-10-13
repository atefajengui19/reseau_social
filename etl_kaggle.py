import pandas as pd
import requests
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, XSD

FUSEKI_DATA_URL = "http://localhost:3030/master_social/data"
g = Graph()
EX = Namespace("http://www.semanticweb.org/dhouh/ontologies/2026/4/reseau_social#")
g.bind("ex", EX)

print("📊 Lancement de l'ETL Kaggle...")

try:
    df_kaggle = pd.read_csv("reseau_social.csv", delimiter=';') 
    
    for index, row in df_kaggle.head(100).iterrows():
        post_uri = EX[f"Kaggle_Post_{index}"]
        auteur_uri = EX[f"Kaggle_User_Anonyme_{index % 5}"]
        
        g.add((auteur_uri, RDF.type, EX.UtilisateurStandard))
        g.add((post_uri, RDF.type, EX.Texte))
        g.add((auteur_uri, EX.aPublie, post_uri))
        
        if 'message' in row and pd.notna(row['message']):
            g.add((post_uri, RDFS.label, Literal(str(row['message']))))
        else:
            g.add((post_uri, RDFS.label, Literal("Contenu partagé (Kaggle)")))
            
        if 'like' in row and pd.notna(row['like']):
            g.add((post_uri, EX.nombreLikes, Literal(int(row['like']), datatype=XSD.integer)))
        if 'comment' in row and pd.notna(row['comment']):
            g.add((post_uri, EX.nombreCommentaires, Literal(int(row['comment']), datatype=XSD.integer)))
        if 'share' in row and pd.notna(row['share']):
            g.add((post_uri, EX.nombrePartages, Literal(int(row['share']), datatype=XSD.integer)))

    # INJECTION DIRECTE DANS FUSEKI
    donnees_ttl = g.serialize(format="turtle")
    headers = {'Content-Type': 'text/turtle'}
    res = requests.post(FUSEKI_DATA_URL, data=donnees_ttl.encode('utf-8'), headers=headers)
    
    if res.status_code in [200, 201, 204]:
        print(f"✅ Succès ! {len(g)} triplets Kaggle injectés directement dans Fuseki.")
    else:
        print(f"❌ Erreur d'injection Fuseki : {res.status_code} - {res.text}")
except Exception as e:
    print(f"⚠️ Erreur lors de la lecture Kaggle : {e}")
