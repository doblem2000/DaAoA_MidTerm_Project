from element import Element

class WebSite:
    """
    web site is a class used for represent a website is composed by the name of host of this website 
    and the element host, the element host will have all hierarchy of the web site by his child
    """
    
    __slots__='__name', '__homeDirectory','__homePage'

    def __init__(self, host:str):
        self.__name=host
        self.__homeDirectory=Element(host,True,None)
        self.__homeDirectory.setSite(self)
        self.__homePage=None

    def __isDir(self, elem:Element):    #O(1)
        """
         if the object Element referenced is a directory returns True,
        otherwise it returns False. The format of elem is not constrained.
        """
        if not(self.__homeDirectory.validate(elem)):
            raise Exception("incorrect validate")
        return (elem.isDir())
        
    def __isPage(self, elem):   #O(1)
        """
        if the object Element referenced is a web page returns
        True, otherwise it returns False. The format of elem is not constrained.
        """
        if not(self.__homeDirectory.validate(elem)):
            raise Exception("incorrect validate")
        return not(elem.isDir())

    def __hasDir(self, ndir, cdir):     #requestes: O(log(K)), k number of direcotry or web page in cdir, searche element in a rbthree
        """
        if in the current directory cdir there is a directory whose name
        is ndir, then it returns a reference to this directory, otherwise it throws an exception.
        An exception must be thrown even if the cdir is not a directory. Here ndir is a string,
        while cdir and the return value are objects of the class Element;
        """
        if not(isinstance(cdir,Element)):
            raise TypeError(" cdir is not a Element")
        if not(isinstance(ndir,str)):
            raise TypeError(" ndir is not a string")
        return cdir.getChild(ndir)

    def __newDir(self, ndir, cdir):     #request: O(k), k number of direcotry or web page in cdir
                                        #actual: O(log(K))=O(log(k)) + O(log(k)), k number of direcotry or web page in cdir,time for search a child in a rbthree and time for addChild() in orderedChild [RedBlackTreeMap]
        """
        if in the current directory cdir there is a directory whose name
        is ndir, then it returns a reference to this directory, otherwise it creates such a
        directory and returns a reference to it. An exception must be thrown even if the cdir
        is not a directory. Here ndir is a string, while cdir and the return value are objects of
        the class Element;
        """
        if not(isinstance(cdir,Element)):
            raise TypeError(" cdir is not a Element")
        if not(isinstance(ndir,str)):
            raise TypeError(" ndir is not a string")
        try:
            return self.__hasDir(ndir,cdir)         #O(log(k))
        except KeyError:
            return cdir.addChild(Element(ndir,True))    #O(log(k))
        except TypeError:
            raise TypeError(" typer error from ___hasdir")
            
    def __hasPage(self, npag, cdir):    #requestes: O(log(K)), k number of direcotry or web page in cdir, searche element in a rbthree
        """
        if in the current directory cdir there is a webpage whose
        name is npage, then it returns a reference to this page, otherwise it throws an
        exception. An exception must be thrown even if the cdir is not a directory. Here
        npage is a string, while cdir and the return value are objects of the class Element;
        """
        if not(isinstance(cdir,Element)):
            raise TypeError(" cdir is not a Element")
        if not(isinstance(npag,str)):
            raise TypeError(" npag is not a string")
        return cdir.getChild(npag)


    def __newPage(self, npag, cdir):    #request: O(k), k number of direcotry or web page in cdir
                                        #actual: O(log(K))=O(log(k)) + O(log(k)), k number of direcotry or web page in cdir,time for search a child in a rbthree and time for addChild() in orderedChild [RedBlackTreeMap]
        """
        if in the current directory cdir there is a webpage whose
        name is npage, then it returns a reference to this page, otherwise it creates such a
        page and returns a reference to it. An exception must be thrown even if the cdir is
        not a directory. Here ndir is a string, while cdir and the return value are objects of the
        class Element
        """
        if not(isinstance(cdir,Element)):
            raise TypeError(" cdir is not a Element")
        if not(isinstance(npag,str)):
            raise TypeError(" npag is not a string")
        try:
            return self.__hasPage(npag,cdir)
        except KeyError:
            return cdir.addChild(Element(npag,False))
        except TypeError:
            raise TypeError(" typer error from ___hasdir")

    def getHomePage(self):      #O(1)
        """
        it returns the home page of the website at which the current object
        refers or it throws an exception if an home page does not exist;
        """
        if(self.__homeDirectory is None):
            raise Exception ("home page does not exist")         
        return self.__homePage

    def getSiteString(self):    #O(N), time used for stringAllOrderedChild()
        """
        it returns a string showing the structure of the website. The string
        must be formatted as follows: in the first line there must be the hostname at which
        the site is hosted; each page or directory contained in the root directory will appear in
        a new line preceded by “--- “ (three dashes and a space) in alphabetical order (with
        numbers preceding lowercase letters preceding uppercase letters). For each
        directory the files and directories contained therein will appear just after the name of
        the directory in a new line preceded by a number of dashes = 3 x the number of
        parent directories, and a space
        """
        return(self.__homeDirectory.stringAllOrderedChild(0).lstrip()) #lstrip() method removes any leading {prima} characters (space is the default leading character to remove)

    def insertPage(self, url, content): #request: O(l * k), k number of element in final directory, l is number of parent directory
                                        #actual: O(l*log(k)), l for arriving into directory where we want to add the page (for cycle) 
                                        #        (condidering that directory exist) and log(k) for add page with __newPage()
        """
        it saves and returns a new page of the website, where url
        is a string representing the URL of the page, and content is a string representing the
        text contained in the page.
        """
        if not(isinstance(url,str)):
            raise TypeError(" url is not a string")
        listParentDirectory = url.split("/",-1) #lista di tutte le parent directory
        if not(listParentDirectory[0] == self.__name):
            raise Exception("web page to add have different web site that web site where you want to add")
        dir=self.__homeDirectory                #direcotry di partenza
        name=listParentDirectory[len(listParentDirectory) -1]   #nome della web page da aggiungere (ultimo elemento url)
        
        for i in listParentDirectory[1:len(listParentDirectory) -1]:    #scorro tutte le directory fino tranne quella di destinazione(-1)
                                                                        #se non esistono directory con quel nome le creo
            dir=self.__newDir(i,dir)            #dir è un element
        page= self.__newPage(name, dir)            #creo element page in quella directory
        page.setContent(content)                   #ne setto il contenuto
        page.setUrl(url)                           #ne setto l'url
        if(page.getName()=="index.html"):
            self.__homePage=page
        return page

    def getSiteFromPage(page): #O(1)
        """that given an Element page returns the WebSite object at which that page belongs"""
        return page.getSite()
    
    def getName(self): #O(1)
        """return the name (host) of website"""
        return self.__name
    