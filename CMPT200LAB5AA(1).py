# Author: Aaron Alejo
# ID number: 3071852
# Course: CMPT 200 X02L
# Assignment: Lab 5

# Purpose: To create a simulation of a shipping yard management using class
# and linked-list

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

# Shipyard class where the containers and packages are stored
class Shipyard:
    """
    A shipyard object where users could add, remove, search, and ship containers
    containing packages
    Parameters: None
    returns: Container or package contents
    """
    
    # Container class that holds the packages
    class Container:
        """
        A container class that holds the packages assigned to a destination
        Parameters: destination, uniquely generated ID, and next pack
        returns: Package contents and information

        """
        
        # Package class that takes three arguments:
        # an owner, a destination, weight and a unique ID     
        class Package:
            """
            A package class that is assigned to a container based on destination
            and weight.
            Parameters: Owner, weight, ID and next package
            returns: None
            
            """
            # Sets the values of the packages
            def __init__(self, owner, weight, packID, next):
                self._owner = owner
                self._packWeight = weight
                self._nextPack = next
                self._packID = packID         
    
        # Sets the assigned destination to the containers
        def __init__(self, dest, contID, next):
            self._dest = dest
            self._nextDest = next
            self._contWeight = 0
            self._contID = contID
            self._firstPack = None
        
        # Adds the package into the container, with the uniquely generated ID
        def add_pack(self, owner, weight, packID):
              
            # See if the new element will be inserted as _first.
            if self._firstPack == None or weight < self._firstPack._packWeight:
                
                self._contWeight += weight               
                self._firstPack=self.Package(owner,weight,packID,self._firstPack)
                return 
            
            # Otherwise find the insertion point.
            # We will advance until we hit the end of the list or else
            # the next element is strictly greater than the one we want 
            # to insert.
            tmpRef = self._firstPack
            while tmpRef._nextPack != None and\
                  weight >= tmpRef._nextPack._packWeight:
                
                tmpRef = tmpRef._nextPack
                
            tmpRef._nextPack=self.Package(owner,weight,packID,tmpRef._nextPack)
            self._contWeight += weight
            return            
    
    def __init__(self):
        self._headCont = None
        self._size = 0
        self._contID = randID()
        self._packID = randID() 
        
    # Creates and adds a package into a container
    def add(self, owner, dest, weight):
        
        # GENERATE IDs 
        packID = self._packID.genPackID()
        contID = self._contID.genContID()
        
        # Checks if the shipyard is empty or if not checks if the new 
        # container destination alphabetically precedes the first container
        if self._headCont == None or dest < self._headCont._dest:
            
            # add container and package into the container
            self._headCont = self.Container(dest, contID, self._headCont)
            self._headCont.add_pack(owner, weight, packID)
            self._size += 1
            return
        
        # If the yard is not empty:
        # Goes through the list of containers looking for a container
        # that is assigned to the same destination
        cont = self._headCont
        while cont._nextDest != None and dest > cont._dest:
            cont = cont._nextDest
            
        if cont._nextDest == None and dest > cont._dest:
            contID = self._contID.genContID()
            cont._nextDest = self.Container(dest, contID, cont._nextDest)
            cont._nextDest.add_pack(owner, weight, packID)  
            self._size += 1
            return
            
        # If the container to the destination is found
        # Checks if adding the new package will not make the container go over
        # the maximum weight
        if cont._dest == dest and (cont._contWeight +  weight) <= 2000:
            cont.add_pack(owner, weight, packID)
            return
        
        if cont._dest == dest and (cont._contWeight + weight) > 2000:
            contID = self._contID.genContID()
            cont._nextDest = self.Container(dest, contID, cont._nextDest)
            cont._nextDest.add_pack(owner, weight, packID)  
            self._size += 1
            return
        
        # If the next container is not the same as the new destination
        # create and insert the new container
        if cont._nextDest != dest:
            contID = self._contID.genContID()
            cont._nextDest = self.Container(dest, contID, cont._nextDest)
            cont._nextDest.add_pack(owner, weight, packID)  
            self._size += 1
            return             
                
        # Goes through the list of containers again to check if there is a
        # pre-existing container with same destination and enough space for the
        # new package
        while cont._nextDest != None or cont._nextDest._dest >= dest:
            if cont._nextDest._contWeight + weight > 2000 or\
               cont._nextDest._dest != dest:
                cont = cont._nextDest
            else:
                break
        
        # Create a new container otherwise
        cont = self._headCont
        contID = self._contID.genContID()
        cont._nextDest = self.Container(dest, contID, cont._nextDest)        
        cont.add_pack(owner, weight, packID)
        return
    
    # Function that will print the whole system
    # option b(shipyard manifest)
    def printAll(self):
        
        print("\n====== Shipyard Manifest ======\n")
        
        # Traverses through the list of containers
        # And prints container information
        curCont = self._headCont
        while curCont != None:  
            print("Container ID:", curCont._contID)
            print("Destination:",  curCont._dest)
            print("Weight:", str(curCont._contWeight), "lbs", "\n")
            
            # Traverses through the packages in the container
            # And prints package informations
            curPack = curCont._firstPack
            while curPack != None:
                print("\t\t Package ID:", curPack._packID)
                print("\t\t Owner:", curPack._owner)
                print("\t\t Weight:", str(curPack._packWeight),'lbs',"\n")
                
                curPack = curPack._nextPack
            curCont = curCont._nextDest
            
    # Prints the container manifest
    def printContainers(self):
        print("\n====== Container Manifest ======\n")
        
        # Lets the user know if the container is empty
        # Traverses through the list of containers
        # And prints container information
        curCont = self._headCont
        if curCont == None:
            print("The container is empty...")        
        while curCont != None:
            
            # Prints out the contents of the containers
            print("Container ID:", curCont._contID)
            print("Destination:",  curCont._dest)
            print("Weight:", str(curCont._contWeight), "lbs")
            print("Weight left:", str(2000 - curCont._contWeight), "lbs", "\n")
            curCont = curCont._nextDest
            
    # Checks if a container assigned to a destination exists
    def isPresent(self, dest) :
        
        # start at head container
        # traverse list until elem is found or we reach end
        # return true if elem is found and false otherwise
        tmpRef = self._headCont
        while (tmpRef != None):
            if tmpRef._dest == dest:
                return True
            tmpRef = tmpRef._nextDest
        return False     
        
    def printDest(self, dest):
        
        print("\n===== Destination Manifest =====\n")
        # Traverses through the list of containers
        # And prints container information
        curCont = self._headCont
        while curCont != None:
            
            # Prints out the contents of the containers
            if dest == curCont._dest:
                print("Container ID:", curCont._contID)
                print("Destination:",  curCont._dest)
                print("Weight:", str(curCont._contWeight), "lbs", "\n")
                
                # Prints out the contents of the packages
                curPack = curCont._firstPack
                while curPack != None:
                    print("\t\t Package ID:", curPack._packID)
                    print("\t\t Owner:", curPack._owner)
                    print("\t\t Weight:", str(curPack._packWeight), 'lbs',"\n")
                    curPack = curPack._nextPack               
            curCont = curCont._nextDest
    
    # This is a debugging method that assumes two packages belonging to the
    # same destination and owner will have two weights. The remove your system 
    # uses from your menu must go by id #    
    def remove(self, owner, destination, weight):
        
        # Lets the user know if the Shipyard is empty
        if self._headCont == None:
            print("The shipyard is empty...")
            return
        
        # Traverses through the containers and packages looking for the 
        # container and package with the same given parameters
        curCont = self._headCont
        while curCont._nextDest != None and curCont._dest != dest:
            curCont = curCont._nextDest
            
        # if the container is found, search for the right package
        if destination == curCont._dest:
            curPack = curCont._firstPack
            prevPack = None
            # If its the first package, the remove right away
            if curPack._owner == owner and curPack._packWeight == weight:
                self._size -= 1
                curCont._contWeight -= weight
                curCont._firstPack = curCont._firstPack._nextPack
                return
            
            # Keep traversing through the packages
            while curPack._nextPack != None and curPack._owner != owner:
                
                # move to the next pack otherwise
                prevPack = curPack
                curPack = curPack._nextPack                
                
            # if the right owner is found, check if the weight matches then
            # remove it from the container
            # the package should not show up anymore
            if curPack._packWeight == weight:
                self._size -= 1
                curCont._contWeight -= weight
                prevPack._nextPack = curPack._nextPack
                return
            
            if curPack._packWeight != weight:
                curPack = curPack._nextPack
                while curPack._nextPack != None and curPack._owner != owner:
                    # move to the next pack otherwise
                    prevPack = curPack
                    curPack = curPack._nextPack   
                
                if curPack._packWeight == weight:
                    self._size -= 1
                    curCont._contWeight -= weight
                    prevPack._nextPack = curPack._nextPack
                    return                
              
            curCont = curCont._nextDest
    
    # Removes a package given its ID
    def remove_by_id(self, ID):
        print(ID)
        if self._headCont == None:
            print("The shipyard is empty...")
            return  
        
        # Traverses through the containers and packages looking for the 
        # container and package with the same given parameters
        curCont = self._headCont
        while curCont != None:
            
            if curCont._firstPack._packID == ID:
                curCont._contWeight -= curCont._firstPack._packWeight
                curCont._firstPack = curCont._firstPack._nextPack
                return
                       
            curPack = curCont._firstPack
            while curPack._nextPack != None and curPack._packID != ID:
                if curPack._nextPack._packID != ID:
                    curPack = curPack._nextPack
                else:
                    break
            
            if curPack._nextPack != None and curPack._nextPack._packID == ID:
                curCont._contWeight -= curPack._packWeight
                curPack._nextPack = curPack._nextPack._nextPack
                return        
            curCont = curCont._nextDest 
            
    # Searches for a package given its owner, destination, and weight
    def search(self, owner, destination, weight):
        
        curCont = self._headCont
        # Lets the user know if the Shipyard is empty
        if curCont == None:
            print("The shipyard is empty...")
            return
        
        print("=================================\n")
        print("Searching for package...")
        # Traverses through the containers and packages looking for the 
        # container and package with the same given parameters
        while curCont._nextDest != None and curCont._dest != dest:
            curCont = curCont._nextDest
            
        # if the container is found, search for the right package
        if destination == curCont._dest:
            curPack = curCont._firstPack
            
            # If its the first package, confirm that it is found right away
            if curPack._owner == owner and curPack._packWeight == weight:
                print("Package found...\n")
                print("\t\t Package ID:", curPack._packID)
                print("\t\t Owner:", curPack._owner)
                print("\t\t Weight:", str(curPack._packWeight), 'lbs',"\n")                
                return
            
            # Keep traversing through the packages
            while curPack._nextPack != None and curPack._owner != owner:
                # move to the next pack otherwise
                curPack = curPack._nextPack                
                
                # if the right owner is found, check if the weight matches then
                # confirm the package to be found
                if curPack._packWeight == weight:
                    print("\t\t Package ID:", curPack._packID)
                    print("\t\t Owner:", curPack._owner)
                    print("\t\t Weight:", str(curPack._packWeight), 'lbs',"\n")                    
                    print("Package found...")              
                    return
            curCont = curCont._nextDest  
        
        # Otherwise, the package does not exist
        print("Package not found...")
    
    # Searches a package given its ID
    def search_by_id(self):
        
        if self._headCont == None:
            print("The shipyard is empty...")
            return  
        
        # Traverses through the containers and packages looking for the 
        # container and package with the same given parameters
        curCont = self._headCont
        while curCont._nextDest != None:
            curCont = curCont._nextDest       
        
        curPack = curCont._firstPack
        while curPack._nextPack != None and curPack._packID != ID:
            curPack = curPack._nextPack
        
        # If the matching package ID is found, prints out the package 
        # information
        if curPack._packID == ID:
            print("\t\t Package ID:", curPack._packID)
            print("\t\t Owner:", curPack._owner)
            print("\t\t Weight:", str(curPack._packWeight), 'lbs',"\n")            
            return   
        
    # Ships all containers given a destination
    def ship(self, dest):
        
        print("\n=================================\n")
        # Lets the user know if the Shipyard is empty
        if self._headCont == None:
            print("The shipyard is empty...")
            return
        
        while self._headCont != None and dest == self._headCont._dest:
            self._size -= 1
            self._headCont = self._headCont._nextDest
            
        # Traverses through the containers and packages looking for the 
        # container and package with the same given parameters
        curCont = self._headCont
        while curCont._nextDest != None:
            
            if curCont == None:
                print("Error 404: Container not found")
                return
            if curCont._nextDest == dest:
            
                self._size -= 1
                self._nextDest = self._nextDest._nextDest
           
            curCont = curCont._nextDest
                
    
class Empty(Exception):
    pass

# Main function that displays the menu and initiate the call of the shipyard
# object
def main():
    """
    Main function. Lets the user interact with the code
    """
    # Creates the shipyard object
    shipyard = Shipyard()
    
    # Displays the menu
    print("\n=== Shipyard Management Simulation ===\n")
    print("------------------") 
    print("||     Menu     ||")
    print("------------------\n")
    print("(a) add package")
    print("(b) shipyard manifest")
    print("(c) container manifest")
    print("(d) destination manifest")
    print("(e) search for package")
    print("(f) remove package")
    print("(g) ship destination")
    print("(h) exit system\n")
    
    # list of valid menu options
    menu_lst = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    
    # Takes the user input
    user_inpt = input("Choose an option: ")
    
    # Keeps asking the user put input until the user decides to exit 
    while user_inpt != 'h':
        
        if user_inpt not in menu_lst:
            print("Invalid option, please choose again...")
            print("------------------") 
            print("\n||     Menu     ||")
            print("------------------\n")
            print("(a) add package")
            print("(b) shipyard manifest")
            print("(c) container manifest")
            print("(d) destination manifest")
            print("(e) search for package")
            print("(f) remove package")
            print("(g) ship destination")
            print("(h) exit system\n")            
            user_inpt = input("Choose an option: ")
        
        # Option 1: Adding a package into a container
        if user_inpt == 'a':
        
            owner = input("\nOwner: ").title()
            destination = input("Destination: ").title()
            weight = input("Weight: ")
            
            while type(weight) == str or int(weight) > 2000:
                
                try:
                    weight = int(weight)
                    if weight > 2000:
                        print("Weight limit is 2000 lbs, please try again...")
                        weight = input("Weight: ")                        
                    
                except:
                    print("Invalid weight value, please try again...")
                    weight = input("Weight: ")
                
            # Creates a package and assigns it to a new or pre-existing 
            # container that is assigned by the destination
            shipyard.add(owner, destination, weight)          
            
        # Option 2: Shipyard manifest
        # Prints all the information in the shipyard
        elif user_inpt == 'b':
            shipyard.printAll()
               
        # Option 3: Container manifest
        # Prints the manifest of a container
        elif user_inpt == 'c':
            shipyard.printContainers()
        
        # Option 4: Single destination manifest
        # Prints the manifest of containers that is assigned to destination
        elif user_inpt == 'd':
            
            # Asks user for an input, checks if shipyard is empty and if a
            # container going to destination is present
            dest = input("Choose a destination: ").title()
            if shipyard._headCont == None:
                print("The Shipyard is empty...")
            elif shipyard.isPresent(dest) == False:
                print("There are no containers heading to this destination...")
            else:
                shipyard.printDest(dest)
    
        ## Option 5: Search a package given its ID        
        elif user_inpt == 'e':
            
            # Asks the user for an ID input
            ID = input("Enter the package ID: ")
            # Tries to search a package using the given ID
            # If ID is invalid, lets the user know
            shipyard.search_by_id(ID)
        
        # Option 6: Removes a package     
        elif user_inpt == 'f':
            
            # Asks the user for an ID input
            ID = input("Enter the package ID: ")
            # Tries to remove a package using the given ID
            # If ID is invalid, lets the user know
            shipyard.remove_by_id(ID)
                
        # Option 7: Ships all containers given its destination      
        elif user_inpt == 'g':
            dest = input("Enter a destination you want shipped to: ")
            shipyard.ship(dest)

        print("\n------------------")        
        print("||     Menu     ||")
        print("------------------\n")
        print("(a) add package")
        print("(b) shipyard manifest")
        print("(c) container manifest")
        print("(d) destination manifest")
        print("(e) search for package")
        print("(f) remove package")
        print("(g) ship destination")
        print("(h) exit system\n")        
        user_inpt = input("Choose an option: ")
    
 

#Sample test program for Lab 5
def test():
    """
    Test function for error checking
    """
    #initialize the Shipyard object
    testYard=Shipyard()
    
    #adds a new package that is 102 pounds, going to antarctica
    testYard.add("Adrian", "Antarctica", 102)
    
    #adds another new package 
    testYard.add("Peter", "Antarctica", 57)
    #prints manifest of whole system
    testYard.printAll()
    #prints manifest of a single destination
    testYard.printDest("Antarctica")
    #prints container info list
    testYard.printContainers()
    
    #note, you still must write your remove with id number
    #this is a debugging method that assumes two packages belonging to the 
    #same destination and owner will have two weights.  The remove your 
    #system uses from your menu must go by id # 
    testYard.remove("Peter", "Antarctica", 57)
    testYard.printDest("Antarctica")
    #note, you still must write your search with id number
    #this is a debugging method that assumes two packages belonging to the 
    #same destination and owner will have two weights.  The search your 
    #system uses from your menu must go by id .
    #This function should report found or not found, if found, display the 
    #package info (including id #) 
    testYard.search("Adrian", "Antarctica", 102)
    
    #ship out all containers to a given destination
    #testYard.ship("Antarctica")

if __name__ =="__main__":

    main()
    