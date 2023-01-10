
# Library
import praw
import urllib, urllib.request, _collections
import xmltodict
import datetime
from Classes import Document,DocumentFactory
from Classes import Author
from Corpus import Corpus
import pickle
import pandas as pd

# Fonction affichage hierarchie dict
def showDictStruct(d):
    def recursivePrint(d, i):
        for k in d:
            if isinstance(d[k], dict):
                print("-"*i, k)
                recursivePrint(d[k], i+2)
            else:
                print("-"*i, k, ":", d[k])
    recursivePrint(d, 1)

# Identification

reddit= praw.Reddit(client_id='HbrEWdTC5uiwF418u-g-Vw', client_secret='tB5M19gl_AOTOwNxvehY9h5dHP2HRw', user_agent='scarping')   
# Requete
limit = 100
hot_posts = reddit.subreddit('all').hot(limit=limit)#.top("all", limit=limit)#

# Recuperation du texte
# vars :
collection = []
docs_bruts = []
query_terms = ["clustering ", "statistique"]# Parametres
max_results = 100
docs = []
def recup():
   
    
    
    afficher_cles = False
    for i, post in enumerate(hot_posts):
        if i%10==0: print("Reddit:", i, "/", limit)
        if afficher_cles:  # Pour connetre les differentes variables et leur contenu
            for k, v in post.__dict__.items():
                pass
                print(k, ":", v)
    
        if post.selftext != "":  # Osef des posts sans texte
            pass
            #print(post.selftext)
        docs.append(post.selftext.replace("\n", " "))
        docs_bruts.append(("Reddit", post))
    
   
    # =============== 1.2 : ArXiv ===============

                    # Requete
    url = f'http://export.arxiv.org/api/query?search_query=all:{"+".join(query_terms)}&start=0&max_results={max_results}'
    data = urllib.request.urlopen(url)
    
    # Format dict (OrderedDict)
    data = xmltodict.parse(data.read().decode('utf-8'))
    
    
    # Ajout resumes a la liste
    for i, entry in enumerate(data["feed"]["entry"]):
        if i%10==0: print("ArXiv:", i, "/", limit)
        docs.append(entry["summary"].replace("\n", ""))
        docs_bruts.append(("ArXiv", entry))
    
    # print(f"# docs avec doublons : {len(docs)}")
    docs2 = list(set(docs))
    # print(f"# docs sans doublons : {len(docs)}")
    
    for i, doc in enumerate(docs2):
        if len(doc)<100:
            docs2.remove(doc)
    return docs2
                                                                                                                       

def manip():
    for nature, doc in docs_bruts:
        if nature == "ArXiv":  # Les fichiers de ArXiv ou de Reddit sont pas formates de la meme maniere a  ce stade.
    
            titre = doc["title"].replace('\n', '')  # On enleve les retours a  la ligne
            try:
                authors = ", ".join([a["name"] for a in doc["author"]])  # On fait une liste d'auteurs, separes par une virgule
            except:
                authors = doc["author"]["name"]  # Si l'auteur est seul, pas besoin de liste
            summary = doc["summary"].replace("\n", "")  # On enleve les retours a  la ligne
            date = datetime.datetime.strptime(doc["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d")  # Formatage de la date en annee/mois/jour avec librairie datetime
    
            doc_classe = DocumentFactory.factory(titre, authors, date, doc["id"], summary,nature)  # Creation du Document
            collection.append(doc_classe)  # Ajout du Document Ã  la liste.
    
        elif nature == "Reddit":
            titre = doc.title.replace("\n", '')
            auteur = str(doc.author)
            date = datetime.datetime.fromtimestamp(doc.created).strftime("%Y/%m/%d")
            url = "https://www.reddit.com/"+doc.permalink
            texte = doc.selftext.replace("\n", "")
    
            doc_classe = DocumentFactory.factory(titre, auteur, date, url, texte,nature)
    
            collection.append(doc_classe)
    
        # Creation de l'index de documents
        id2doc = {}
        for i, doc in enumerate(collection):
            id2doc[i] = doc.titre
     
# sauvegarde csv 
def save_csv():
    
    df = pd.DataFrame(collection)
    df.to_csv('docs.csv',  sep='\t',index=False)

# load csv
# import csv
# with open('docs.csv') as f:
#     reader = csv.reader(f)
#     data = list(reader)





# Creation de la liste+index des Auteurs
def author():
    authors = {}
    id2doc = {}
    for i, doc in enumerate(collection):
        id2doc[i] = doc.titre
    aut2id = {}
    num_auteurs_vus = 0
    for doc in collection:
        if doc.auteur not in aut2id:
            num_auteurs_vus += 1
            authors[num_auteurs_vus] = Author(doc.auteur)
            aut2id[doc.auteur] = num_auteurs_vus
    
        authors[aut2id[doc.auteur]].add(doc.texte)


# ===============  CORPUS ===============

corpus = Corpus("Mon corpus")

# Construction du corpus a  partir des documents
def create_corpus():
    for doc in collection:
        corpus.add(doc)
# def create_corpus(tri="abc"):
#     corpus.show(tri)
#     print(repr(corpus))
#     #print(repr(corpus))


# ===============  SAUVEGARDE ===============


# Ouverture d'un fichier, puis ecriture avec pickle
with open("corpus.pkl", "wb") as f:
    pickle.dump(corpus, f)

# Supression de la variable "corpus"
del corpus
# Ouverture du fichier, puis lecture avec pickle
with open("corpus.pkl", "rb") as f:
    corpus = pickle.load(f)

# La variable est reapparue
# print(corpus)

# print("\n--------------------------------------------------\n")
# corpus.search("play",longueChaineDeCaracteres)
# print("\n--------------------------------------------------\n")
# print(corpus.concorde(longueChaineDeCaracteres,"play",20))
# print("\n--------------------------------------------------\n")
# corpus.stats(longueChaineDeCaracteres,20)





print("\n------------------== Main ==-----------------------\n")
print ('Veuillez taper votre recherche : ')
keyword_input = input()

print("1")
query_terms = keyword_input.split()

print("2")
recup()

print("3")
manip() 

print("4")
author()

print("5")
create_corpus() #add docs to corpus  


print("6")

# chaine =  corpus.__repr__()
# chaine2 = corpus.nettoyer_texte()

print("7")

print("\n--------------------------------------------------\n")

vocab = corpus.stats2(5)

print("8")
corpus.dictio()

liste_mots = corpus.vocab()
mat = corpus.mat(docs,liste_mots)
print("9")
id_qt = corpus.id_qt(query_terms)



print("10")
docs_result = corpus.score_research(id_qt,mat)
print(docs_result)

print("11")
print("\n---------------------== resultat ==------------------------\n")
corpus.resultat_recherche(docs,docs_result,5)