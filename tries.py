#L'idea è quella di avere un'hash table di hash table.
#Alludendo agli alberi, è come se avessi un primo nodo vuoto (l'hash table esterna)
#Mentre per ogni altro nodo avrò un'altra hash table. 
#Se ci sono delle parole con prefissi in comune, per queste parole avrò una prima parte
#di hash tables in comune... quando arrivo ai suffissi diversi, le hash table saranno diverse.
#
#

from TdP_collections.hash_table.probe_hash_map import ProbeHashMap

class Trie:
    '''
    Trie data structure implemented using hash table
    
    Attributes
    ----------
    trie : probehashmap
    hash table with nested hash table representing branches of trie. Presence of
    key '/' with value 'REF' represents termination node.
    REF is a referement to a ProbeHashMap
    
    Examples
    --------
    Dictionary containing dad, dab, and pila
    Trie View:
             ()
             /\
            d  p
           /    \
          a      i
         / \      \
        d   b      l
       /     \      \
     '/'     '/'     a      
      |       |       \
     list    list     '/'
      of      of       |
     page    page     list
                       of
                      page

    Dict View: {'d': {'a': {'d': {'/': REF}, 'b': {'/': REF}}}, 'p': {'i': {'l': {'a' : {'/': REF}}}}}  
    '''
    __slots__ = '__trie'

    def __init__(self, cap=11, p=109345121):
        self.__trie = ProbeHashMap(cap,p)

    def insert(self, word:str):
        """ inserisce parola nel trie"""
        current_level = self.__trie
        for letter in word:
            current_level = current_level.setdefault(letter, ProbeHashMap(41))     #set default se esiste valore già lo ritorna in alternativa lo crea
        current_level.setdefault('/',ProbeHashMap(41))

    def search(self, word:str):
        """"cerca parola nel trie e ritorna true o false """
        current_level = self.__trie
        for letter in word:
            try:
                current_level = current_level[letter]
            except KeyError:
                return False
        return '/' in current_level

    def getOccurrenceListFromWord(self, word:str):
        """"restituisce occurence list associata alla word"""
        current_level = self.__trie
        for letter in word:
            try:
                current_level = current_level[letter]
            except KeyError as ex:
                raise ex
        return current_level['/']