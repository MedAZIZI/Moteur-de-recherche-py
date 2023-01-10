import datetime

class Document:
    # Initialisation des variables de la classe
    def __init__(self, titre="", auteur="", date="", url="", texte="" ,_type=""):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        self.type = _type

    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tnature : {self.nature}\tTexte : {self.texte}\t"

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"{self.titre}, par {self.auteur}"
    def getType(self):
        return self.type


class Author:
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = []
    def add(self, production):
        self.ndoc += 1
        self.production.append(production)
    def __str__(self):
        return f"Auteur : {self.name}\t# productions : {self.ndoc}"
    
class ArxivDocument(Document) : 
    
    def __init__(self,t=None,a=None,d=datetime.datetime.now(),u=None,txt=None,co_aut=None,_type=None):
       super().__init__(t,a,d,u,txt,_type)
       self.__co_auteur = co_aut
    
    def  getNbComm(self):
        return self.__co_auteur
    
    def  getTitre(self):
        return super().__titre
    
    def  getAuteur(self):
        return super().__auteur
    
    def  getDate(self):
        return super().__date
    
    def  getUrl(self):
        return super().__url
    
    def  getTexte(self):
        return super().texte 
    
    # def  getType(self):
    #          return super().type
    
    
    
    
    
class RedditDocument(Document) : 
    
    def __init__(self,t=None,a=None,d=datetime.datetime.now(),u=None,txt=None,nbComm=None,_type=None) :
       super().__init__(t,a,d,u,txt,_type)
       self.__nbComm = nbComm
           
        
    def  getNbComm(self):
        return self.__nbComm
    
    def  getTitre(self):
        return super().__titre
    
    def  getAuteur(self):
        return super().__auteur
    
    def  getDate(self):
        return super().__date
    
    def  getUrl(self):
        return super().__url
    
    def  getTexte(self):
        return super().texte
          
class DocumentFactory:
    @staticmethod
    def factory(t,a,d,u,txt,_type):
        if _type=="ArXiv": return ArxivDocument(t,a,d,u,txt,"ArXiv")
        if _type=="Reddit": return RedditDocument(t,a,d,u,txt,"Reddit")
        assert 0 ,"Erreur :" + type
 
        
