
class MyString(str):
    """"this class is created for order element into data structure to have lower case before upper case"""
    
    def __lt__(self, other):
      return self.swapcase() < other.swapcase() 
   
    def __le__(self, other):
        return self.swapcase() <= other.swapcase()
    
    def __gt__(self, other):
        return self.swapcase() > other.swapcase()
    
    def __ge__(self, other):
        return self.swapcase() >= other.swapcase()