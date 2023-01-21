from TdP_collections.map.red_black_tree import RedBlackTreeMap
from mystring import MyString

class Element:
    '''
    Element is a class that rapresent a Element of a web site: a directory o a webpage
    this strcutre have a data strucure for save the child of an element:
    redblacktreemap for have a better in ordere visit (ordered by using class mystring)
    the attribute of this class are:
    -name: element name
    -directory: boolean value that if is true sign this element as a directory if is false sign this element as a web page
    -child: all child for rapid access
    -orderedChild: alla child for rapid in ordere visiti
    -content: the content of a web page
    -website: is a reference to web page to which that element belongs
    -url: is a url that identy a element(dir or webpage)
    '''
    __slots__='__name','__directory','__orderedChild','__content','__website','__url'
        
    def __init__(self, name:str, directory:bool=True, content: str=None):
        self.__name=MyString(name)
        self.__directory=directory
        self.__website=None
        self.__url=None
        
        if(directory==True):
            self.__orderedChild=RedBlackTreeMap()
            self.__content=None
        else:
            self.__orderedChild=None
            self.__content=content
    
    def getName(self):
        return self.__name
           
    def setUrl(self, url):
        self.__url= url
        
    def getUrl(self):
        return (self.__url)
    
    def setSite(self, site):
        self.__website= site
        
    def getSite(self):
        return (self.__website)
    
    def getChild(self, name):
        return self.__orderedChild[name]
    
    def isDir(self):
        return self.__directory
    
    def isPage(self):
        return not(self.__directory)
    
    def __str__(self):
        return self.__name
    
    def setContent(self,cont):
        if not(self.isPage()):
            raise TypeError("object passed is not a webpage")
        self.__content=cont
        
    def getContent(self):
        if not(self.isPage()):
            raise TypeError("object passed is not a webpage")
        return self.__content

    def stringAllOrderedChild(self, dept): #O(N), time for iterate all element n in structure (in order visit)
        """
        Method that give a string of all descendant of a element in every line,
        for every level down the string is formatted to add --- at start of line,
        according to level hierarchy
        """
        s=dept * "---"
        s= s + " " + self.getName() + "\n"
        iterator= iter(self.__orderedChild)
        
        for i in iterator:
            if(self.__orderedChild[i].isDir()):
                s = s + self.__orderedChild[i].stringAllOrderedChild(dept+1)
            else:
                s=s + (dept+1) * "---"
                s=s + " " + self.__orderedChild[i].getName() + "\n"
        return s

           
    def addChild(self, elem):
        """add a element as child in both the structure child and ordered child"""
        if not(isinstance(elem, Element)):
            raise TypeError("object passed is not a Element")
        elem.setSite(self.__website)
        self.__orderedChild[elem.getName()]=elem
        return elem
        
    def printChild(self):
        """"print child iterate all structure child"""
        if not(self.isDir()):
            raise ValueError("Element is webpage")
        iterator= iter(self.__child)
        for i in iterator:
            print(i)
        
    def printOrderedChild(self):
        """"print ordered child iterate all structure orderedChild"""
        if not(self.isDir()):
            raise ValueError("Element is webpage")
        iterator= iter(self.__orderedChild)
        for i in iterator:
            print(i)
            
    
    def validate(self, elem):
        """method used for verify that two element belong at same"""
        if not(isinstance(elem,Element)):
            raise TypeError("Object passe in not a Element")
        if elem.getSite() is not self.getSite():
            raise ValueError("The element has not of the correct web site")
        return True