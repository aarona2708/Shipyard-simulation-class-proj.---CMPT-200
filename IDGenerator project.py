# Author: Aaron Alejo
"""
***Refer to Shipyard simulation project to see how to use this code***

    Purpose: Produces a random unique ID for Containers and Packages
"""
from random import *

# A class that will generate unique ID's for both the Packages and Containers
# Takes no parameters
class randID:
    """
    Unique ID generator
    Paramaters: None
    Returns uniquely generated IDs from the nodes
    
    """
    # Node for storing the newly generated container ID
    class contNode:
        def __init__(self, c_ID, next):
            self._ID = c_ID
            self._nextID = next
    
    # Node for storing the newly generated package ID
    class packNode:
        
        def __init__(self, p_ID, next):
            self._ID = p_ID
            self._nextID = next
    
    def __init__(self):
        
        self._contHeadID = None
        self._packHeadID = None

    # Checks if ID exists
    # Returns True if ID does exist, returns False otherwise    
    def isContIDPresent(self, contID):
        
        tmpRef = self._contHeadID
        while tmpRef != None:
            if tmpRef == contID:
                return True
            tmpRef = tmpRef._nextID
        
        return False
    
    # Generates and returns the ID
    # Gets called by the addContID function
    def genContID(self):
        
        contID = "Cont_"
        for i in range(0, 6):
            contID += str(randint(0, 6))

        # Checks if the newly generated ID already exist
        # Generates another one if it already exist
        while self.isContIDPresent(contID) == True:
            contID = "Cont_"
            for i in range(0, 6):
                contID += str(randint(0, 6))            
        
        # returns ID
        return contID
    
    # Adds the new ID to the node for future references
    def addContID(self):
        
        self._contHeadID = self.contNode(self.genContID(), self._contHeadID)
        uniqueContID = self._contHeadID
        # returns ID
        return uniqueContID
    
    # Checks if ID exists
    # Returns True if ID does exist, returns False otherwise      
    def isPackIDPresent(self, packID):  
        
        # Checks if ID exists
        # Returns True if ID does exist, returns False otherwise
        tmpRef = self._packHeadID
        while tmpRef != None:
            if tmpRef == packID:
                return True
            tmpRef = tmpRef._nextID
        
        return False
    
    # Generates and returns the ID
    # Gets called by the addPackID function
    def genPackID(self):  
        
        # Generate new ID
        packID = "Pack_"
        for i in range(0, 6):
            packID += str(randint(0, 6))

        # Checks if the newly generated ID already exist
        # Generates another one if it already exist
        while self.isPackIDPresent(packID) == True:
            packID = "Pack_"
            for i in range(0, 6):
                packID += str(randint(0, 6))            
        
        # returns ID
        return packID
    
    # Adds the generated ID to the node
    # Returns the ID
    def addPackID(self):
    
        self._packHeadID = self.packNode(self.genPackID(), self._packHeadID)
        uniquePackID = self._packHeadID
        # returns ID
        return uniquePackID
