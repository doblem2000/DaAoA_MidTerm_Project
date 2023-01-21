from occurrenceElement import OccurenceElement
from TdP_collections.hash_table.probe_hash_map import ProbeHashMap
from TdP_collections.priority_queue.heap_priority_queue import HeapPriorityQueue
from element import Element
from website import WebSite
import os

class InvertedIndex:
    """
    is a struture that contain word and reference for eache word at her occurrence list
    for store this information we use a ProbeHashMap() where key in word and value is reference to 
    occurrense list implemented by a ProbeHashMap()
    in this occurence list (ProbeHashMap()), the key is URL of the considered page and 
    value is a occurrenceElement(__nOccorrence, __page)
    """
    __slots__="__map" 
    
    def __init__(self): #O(1)
        """it creates a new empty InvertedIndex"""
        self.__map= ProbeHashMap()

    def addWord(self, keyword):     #requestes: O(len(keyword))
                                    #current: O(1), time for add element in ProbeHashMap() amortized
        """ it adds the string keyword into the InvertedIndex"""
        self.__map[keyword]=ProbeHashMap()  #add reference at an occurence list empty

    def addPage(self, page):    #requestes: O(len(word) + log(list(word)) ) for each word into content page,
                                #           where list(word) is the number of page in occurrence list of word
                                #current: O(1 + 1) for eache word into content page: amortized
                                #         adding element to inveted index in time O(1), is a ProbeHashMap()
                                #         adding element into occurence list in time O(1), is a ProbeHashMap()
        """
        it processes the Element page, and for each word in its content,
        this word is inserted in the inverted index if it is not present, and the page is inserted
        in the occurrence list of this word. The occurrence lists also saves the number of
        occurrences of the word in the page
        """
        if not(isinstance(page, Element)):
            raise TypeError("object passed is not a Element")
        if (page.isDir()):
            raise TypeError("object passed is a Dir")
        content=page.getContent().split()
        for word in content:                    #per ogni parola nel contenuto
            try:
                occurenceList=self.__map[word]
            except:
                self.addWord(word)
                occurenceList=self.__map[word]
            #adding element to inveted index in time O(1), is a ProbeHashMap()
            
            try:
                occurenceListElement = occurenceList[page.getUrl()]     # se è present la pagina aggiorno il contatore parola
                occurenceListElement.setnOccurrence(occurenceListElement.getnOccurrence() + 1)
            except KeyError:
                occurenceList[page.getUrl()]=OccurenceElement(page,1)
            
            #adding element into occurence list in time O(1), is a ProbeHashMap()
                

    def getList(self, keyword):     #requestes: O(len(keyword))
                                    #current: O(1), time for access to a element in ProbeHashMap() amortized
        """
        it takes in input the string keyword, and it returns the
        corresponding occurrence list. It throws an Exception if there is no occurrence list
        associated with the string keyword.
        """
        try:    
            return (self.__map[keyword])
        except:
            raise Exception ("keyword not present in inverted index")

class SearchEngine:
    __slots__= "__invertedIndex", "__allWebSite"
    
    def __init__(self, namedir):
        """
        that initializes the SearchEngine, by taking in input a
        directory in which there are multiple files each representing a different webpage.
        Each file contains in the first line the URL (including the hostname) and in the next
        lines the content of the webpage. This function populates the database of the search
        engine, by initializing and inserting values in all the necessary data structures.
        """
        self.__invertedIndex=InvertedIndex()
        self.__allWebSite= ProbeHashMap()
        startDirectory= os.listdir(namedir)
        for file in startDirectory:
            if file.endswith('.txt'):
                fileread= open(namedir + '/' + file, 'r') #namedir + \\ + file è il percorso per accedere al file
                
                firstLine= fileread.readline()[:-1] #evito di prendere \n
                content= fileread.read()
                
                nameSite=firstLine.split('/',1)[0] #prendo solo nome del webSite, 1 indica il numero i parti cui dividere, [0] serve a non creare una lista da split da prendo solo il 1° elemento
                webSite=self.__allWebSite.get(nameSite) #controllo se web site esiste
                if webSite is None:
                    webSite= WebSite(nameSite)          #se website non esiste lo creo
                    self.__allWebSite[nameSite]=webSite
                page=webSite.insertPage(firstLine,content) #aggiungo pagina al web site
                
                self.__invertedIndex.addPage(page)
                fileread.close()

    def search(self, keyword, k):
        """
        it searches the k web pages with the maximum number of
        occurrences of the searched keyword. It returns a string s built as follows: for each
        of these k pages sorted in descending order of occurrences, the site strings (as
        defined above) of the site hosting that page is added to s, unless this site has been
        already inserted.
        """
        
        if not(isinstance(keyword, str)):
            raise TypeError("keyword passed is not a string")
        s=""
        
        occurrenceList= self.__invertedIndex.getList(keyword)
        kelement= HeapPriorityQueue()       #used for store page in order of nOccurrenze
        printing= ProbeHashMap()            #used for do not print the same website 
        
        for elementOccurrenceList in iter(occurrenceList):      #add all element in occurrenze list in a HeapPriorityQueue
            kelement.add(-1 * occurrenceList[elementOccurrenceList].getnOccurrence(),occurrenceList[elementOccurrenceList].getPage())
        
        for i in range(0,k):
            if not (kelement.is_empty()):
                _, value=kelement.remove_min()                  #remove first k element from HeapPriorityQueue that have max nOccurrenze
            
                try:
                    x=printing[value.getSite().getName()]           #return web site at ProbeHashMap(), if this website not exist raise an exception
                                                                    #if web site exist i have already printed
                except:
                    printing[value.getSite().getName()]=None        #if raise an exception the web site does not exist in string
                    s=s+ value.getSite().getSiteString()            #for this reason add the web site at string, and add web site at ProbeHashMap()
        return s.rstrip()   #rstrip() method removes any trailing {finali} characters (characters at the end a string), space is the default trailing character to remove.
    
