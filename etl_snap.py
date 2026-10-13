import pandas as pd
import requests
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF

# Configuration
FUSEKI_DATA_URL = "http://localhost:3030/master_social/data"
g = Graph()
EX = Namespace("http://www.semanticweb.org/dhouh/ontologies/2026/4/reseau_social#")
g.bind("ex", EX)

print("🎓 Lancement de l'ETL SNAP (Stanford Dataset)...")

try:
   
    df_snap = pd.read_csv("facebook_combined.txt", sep=" ", names=["source", "target"], nrows=2000)
    
    for index, row in df_snap.iterrows():
        noeud_source = EX[f"SNAP_User_{row['source']}"]
        noeud_cible = EX[f"SNAP_User_{row['target']}"]
        
        g.add((noeud_source, RDF.type, EX.UtilisateurStandard))
        g.add((noeud_cible, RDF.type, EX.UtilisateurStandard))
        
       
        g.add((noeud_cible, EX.influence, noeud_source))

    donnees_ttl = g.serialize(format="turtle")
    headers = {'Content-Type': 'text/turtle'}
    res = requests.post(FUSEKI_DATA_URL, data=donnees_ttl.encode('utf-8'), headers=headers)
    
    if res.status_code in [200, 201, 204]:
        print(f"✅ Succès ! {len(g)} triplets SNAP injectés dans Fuseki.")
    else:
        print(f"❌ Erreur d'injection Fuseki : {res.status_code} - {res.text}")

except FileNotFoundError:
    print("⚠️ Fichier 'facebook_combined.txt' introuvable. Veuillez le télécharger sur http://snap.stanford.edu/data/")
except Exception as e:
    print(f"⚠️ Erreur lors de l'exécution : {e}")
