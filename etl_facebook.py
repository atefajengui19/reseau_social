import requests
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, XSD

# --- CONFIGURATION ---
MON_TOKEN_FACEBOOK = "yourToken"
FB_API_URL = f"https://graph.facebook.com/v19.0/me/posts?fields=id,message,full_picture,created_time,reactions.summary(true),comments.summary(true),shares&access_token={MON_TOKEN_FACEBOOK}"
FUSEKI_DATA_URL = "http://localhost:3030/master_social/data"
MON_NOM = "Atef"

g = Graph()
EX = Namespace("http://www.semanticweb.org/dhouh/ontologies/2026/4/reseau_social#")
g.bind("ex", EX)

print("🌐 Lancement de l'ETL Facebook (Textes, Images et Dates)...")

try:
    reponse_fb = requests.get(FB_API_URL)
    if reponse_fb.status_code == 200:
        posts = reponse_fb.json().get("data", [])
        
        for post in posts:
            message = post.get("message", "")
            image_url = post.get("full_picture", "")
            date_fb = post.get("created_time", "")
            
            if message or image_url:
                id_fb = post.get("id").replace('_', '')
                post_uri = EX[f"FB_REEL_{id_fb}"]
                auteur_uri = EX[MON_NOM]
                
                nb_likes = post.get("reactions", {}).get("summary", {}).get("total_count", 0)
                nb_comments = post.get("comments", {}).get("summary", {}).get("total_count", 0)
                nb_shares = post.get("shares", {}).get("count", 0)

                g.add((auteur_uri, RDF.type, EX.UtilisateurStandard))
                g.add((post_uri, RDF.type, EX.Texte))
                g.add((auteur_uri, EX.aPublie, post_uri))
                
                if message:
                    g.add((post_uri, RDFS.label, Literal(message.replace('\n', ' '))))
                else:
                    g.add((post_uri, RDFS.label, Literal("Publication multimédia sans texte")))
                
                if image_url:
                    g.add((post_uri, EX.urlImage, Literal(image_url)))
                
                if date_fb:
                    g.add((post_uri, EX.datePublication, Literal(date_fb, datatype=XSD.dateTime)))
                    
                g.add((post_uri, EX.nombreLikes, Literal(int(nb_likes), datatype=XSD.integer)))
                g.add((post_uri, EX.nombreCommentaires, Literal(int(nb_comments), datatype=XSD.integer)))
                g.add((post_uri, EX.nombrePartages, Literal(int(nb_shares), datatype=XSD.integer)))

        donnees_ttl = g.serialize(format="turtle")
        headers = {'Content-Type': 'text/turtle'}
        res = requests.post(FUSEKI_DATA_URL, data=donnees_ttl.encode('utf-8'), headers=headers)
        
        if res.status_code in [200, 201, 204]:
            print(f"✅ Succès ! {len(g)} triplets Facebook injectés dans Fuseki.")
        else:
            print(f"❌ Erreur d'injection Fuseki : {res.status_code} - {res.text}")
    else:
        print(f"❌ Erreur API Facebook : {reponse_fb.status_code}")
except Exception as e:
    print(f"⚠️ Erreur d'exécution : {e}")
