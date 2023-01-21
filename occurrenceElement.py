class OccurenceElement:
    """
    class created for store the number of occurence that a word appear in page (__nOccorrence)
    and the page refereing to (__page)
    """
    __slots__= "__nOccorrence", "__page"
    
    def __init__(self, page, num = 1):
        self.__nOccorrence = num
        self.__page=page

    def getnOccurrence(self):
        return(self.__nOccorrence)
        
    def setnOccurrence(self, n):
        self.__nOccorrence =n
        
    def getPage(self):
        return(self.__page)
        
    