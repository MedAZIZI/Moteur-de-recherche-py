
from Classes import Author
from functools import wraps
import re
import pandas as pd
# from scipy import sparse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np

def singleton(cls):
    instances  = {}
    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper

# =============== 2.7 : CLASSE CORPUS ===============
@singleton
class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc
    
        
    # =============== 2.8 : REPRESENTATION ===============
    def show(self, n_docs=-1, tri="abc"):
        docs = list(self.id2doc.values())
        if tri == "abc":  # Tri alphabetique
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":  # Tri temporel
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        print("\n".join(list(map(repr, docs))))

    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))

        return "\n".join(list(map(str, docs)))


    def search(self,keyword,text):
        
        print("les passages des documents contenant le mot-clef -"+keyword+" - \n")
        for i in range(len(text)):
            if text[i:(i+len(keyword))] == keyword:
                start=i
                finish=i
                while text[start] != "." and start != 0:
                    start=start-1
                while text[start] == "." or text[start]==" ":
                    start=start+1
                while text[finish] != "." and finish != len(text)-1:
                    finish=finish+1
                print("\n\n")
                print(text[start:finish])
                
                
    def concorde(self,text,keyword,length):
        context = {
          "pre": "",
          "word": "",
          "post": ""
        }
        listCont = []
        context["word"] = keyword
        for i in range(len(text)):
            if text[i:(i+len(keyword))] == keyword:
                start=max(i-length,0)
                context["pre"] = text[start:i+len(keyword)]
                finish=min(i+len(keyword)+length,len(text))
                context["post"] = text[i+len(keyword):finish]
                # print(context)
                # print("\n")
                listCont.append(context)
             
        return listCont
               
                
    def __reduce__(self):
        return (Corpus, (), self.__dict__)
    
    
        
    
   
    
    
    def nettoyer_texte(self):
        txt = self.__repr__()
        # print("\n\n\nnetoyage...\n\n\n")
        txt=txt.lower()
        txt = re.sub(r'\d', " ", txt)
        txt=txt.replace("\n"," ")                  
        txt = re.sub(r'[^\w\s]', " ", txt)
        txt=txt.split()
        
        # print("\n\n\ndone...")
        return txt
    
    def vocab(self):
        words=self.nettoyer_texte()
        vocab=[]
        # iteration={}
        for i in words:
            if i not in vocab:
                vocab.append(i)
            # else:
            #     vocab[i]=iteration[i]+1
        return vocab.sort()
    
    def stats(self,limit):
        iteration={}
        most_used=[]
        # txt = self.__repr__()
        words=self.nettoyer_texte()
        max_order=[]
        current=0
        for i in words:
            if i not in iteration:
                iteration[i]=1
            else:
                iteration[i]=iteration[i]+1
        print("\nfrequence ds mots : \n")
        print(iteration)
        # max=0
        for i in iteration:
            if iteration[i] not in max_order:
                max_order.append(iteration[i])
        max_order.sort(reverse=True)
        while len(most_used) != limit:
            for i in iteration:
                if iteration[i] == max_order[current] and len(most_used) != limit:
                    most_used.append(i)
            # print(current)
            current=current+1
            
                    
        print(f"\nles {limit} mots les plus utiliser : \n")   
        print(most_used )

    def stats2(self,mfw):
        words=self.nettoyer_texte()
        # print(words)
        series = pd.Series(words)
        freq_table = series.value_counts()
        # print(freq_table)
        most_frequent_words = freq_table.head(mfw)
        # print("most_frequent_words : \n",most_frequent_words)
        return freq_table
    
    def dictio(self):
       
        vocab = sorted(self.stats2(0).keys())
        v2 = self.stats2(0)
        dictio = {} 
        data_vocab = { }
        j = 0 
        for i in vocab:
            
            dictio[i] = {
                'Wid':  j,
                'freq':  v2[i] 
            }
            j=j+1
            
        return dictio
    
    
    def mat(self,docs,vocab):
        # vocab = self.dictio()
        vectorizer = CountVectorizer(vocabulary=vocab)
        tf_matrix = vectorizer.fit_transform(docs)
        print(tf_matrix)
        
        word_counts = tf_matrix.sum(axis=0)
        print(word_counts)
        
                
        # doc_counts = np.count_nonzero(tf_matrix, axis=0)
        # print(doc_counts)
        
        return tf_matrix
        
    def id_qt(self,query_terms):
        dictio = self.dictio() 
        for q in query_terms:
            pass
            # print(dictio[q]['Wid'])
            # query_terms[q] = dictio[q]['Wid']
        return query_terms
        
    def score_research(self,id_query_terms,tf_matrix):
        

        tfidf_transformer = TfidfTransformer()
        tfidf_matrix = tfidf_transformer.fit_transform(tf_matrix)
        # print(tfidf_matrix)
        
        tfidf_array = tfidf_matrix.todense()
        highest_scores = np.amax(tfidf_matrix, axis=1)
        # print("%%%%%%%%\n")
        # print(highest_scores)
        
        sorted_indices = np.argsort(highest_scores)[::-1]
        print(sorted_indices)
        
        return highest_scores.row
    
    def resultat_recherche(self,docs,highest_scores,nb_de_res):
        i = 0
        while nb_de_res > 0:
            
            index = highest_scores[i]
            print(f"resltat {i} \n")
            print(docs[index])
            print("\n")
            i += 1
            nb_de_res -= 1 
        

