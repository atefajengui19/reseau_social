import requests
import re
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, XSD

FUSEKI_DATA_URL = "http://localhost:3030/master_social/data"
g = Graph()
EX = Namespace("http://www.semanticweb.org/dhouh/ontologies/2026/4/reseau_social#")
g.bind("ex", EX)

def nettoyer_html(texte_brut):
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', str(texte_brut))

print("🐘 Lancement de l'ETL Mastodon...")

try:
    url_mastodon = "https://mastodon.social/api/v1/timelines/tag/Tech?limit=20"
    rep_mastodon = requests.get(url_mastodon).json()
    
    for post in rep_mastodon:
        if 'account' in post:
            auteur_nom = post['account']['username'].replace(" ", "_")
            post_uri = EX[f"Mastodon_{post['id']}"]
            auteur_uri = EX[f"Mastodon_User_{auteur_nom}"]
            
            g.add((auteur_uri, RDF.type, EX.UtilisateurStandard))
            g.add((post_uri, RDF.type, EX.Texte))
            g.add((auteur_uri, EX.aPublie, post_uri))
            
            message_propre = nettoyer_html(post.get('content', ''))
            g.add((post_uri, RDFS.label, Literal(message_propre)))
            g.add((post_uri, EX.nombreLikes, Literal(int(post.get('favourites_count', 0)), datatype=XSD.integer)))
            g.add((post_uri, EX.nombrePartages, Literal(int(post.get('reblogs_count', 0)), datatype=XSD.integer)))

    # INJECTION DIRECTE DANS FUSEKI
    donnees_ttl = g.serialize(format="turtle")
    headers = {'Content-Type': 'text/turtle'}
    res = requests.post(FUSEKI_DATA_URL, data=donnees_ttl.encode('utf-8'), headers=headers)
    
    if res.status_code in [200, 201, 204]:
        print(f"✅ Succès ! {len(g)} triplets Mastodon injectés directement dans Fuseki.")
    else:
        print(f"❌ Erreur d'injection Fuseki : {res.status_code} - {res.text}")
except Exception as e:
    print(f"⚠️ Erreur Mastodon : {e}")
