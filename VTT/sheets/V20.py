#*===============================================================================================================================
#* LEGEND
#*-------------------------------------------------------------------------------------------------------------------------------
#! Missing or error
#& Missing unimportant
#~ Revision notes
#? Questions
#* Section
#^ Important
# Normal comment
#// Deprecated code
#*===============================================================================================================================

#* IMPORTS
# randint (random)
from random import randint

#* CLASS "basicV20"
class basicV20:
    #& Documentation
    #* METHODS
    # __init__
    def __init__(
        self,
        name:str,player:str,chronicle:str,nature:str,demeanor:str,concept:str,clan:str,generation:int,sire:str,
        attributes:dict[str,int],skills:dict[str,int],
        disciplines:dict[str,int],backgrounds:dict[str,int],virtues:dict[str,int],
        merits:dict[str,int],flaws:dict[str,int],
        path:dict[str,int],willpower:dict[str,int],blood_pool:int,
        health:int,
        weakness:str,
        experience:int
    ):
        # Declare instance attributes for the elements of the basic V20 character sheet
        (
            self.name,self.player,self.chronicle,self.nature,self.demeanor,self.concept,self.clan,self.generation,self.sire,
            self.attributes,self.skills,
            self.disciplines,self.backgrounds,self.virtues,
            self.merits,self.flaws,
            self.path,self.willpower,self.blood,
            self.health,
            self.weakness,
            self.experience
        )=(
            name,player,chronicle,nature,demeanor,concept,clan,generation,sire,
            attributes,skills,
            disciplines,backgrounds,virtues,
            merits,flaws,
            path,willpower,blood_pool,
            health,
            weakness,
            experience
        )
    
    # Import "Biblioteca Oscura" sheets
    @classmethod
    def importSheet(self,sheet):
        """
        Imports the data from a "Biblioteca Oscura" character sheet.
        
        Arguments
        ---------
        sheet
        """
        ...
    
    # Dice rolls #^ with dice pool logic
    def roll(self,aspect:str,difficulty:int=6,specialty:bool=False)->tuple[tuple[int],int]:
        """
        Rolls a given aspect from the character sheet.
        
        Arguments
        ---------
        aspect : `str`
            Character's Aspect to be rolled.
        difficulty : `int`, Optional
            Difficulty for the roll. Defaults to `6`, the standard difficulty.
        specialty : `bool`, Optional
            Whether if the roll involves a character's specialty (`True`), so 10's count as two successes each, or not (`False`).
            Defaults to `False`.
        """
        ...
    
    # Dice rolls
    #? Make it to control the dice pool logic instead of receiving an integer from the GUI
    def roll(self,pool:int,difficulty:int=6,specialty:bool=False)->tuple[tuple[int],int]:
        """
        Rolls a given number of ten faced dice.
        
        Arguments
        ---------
        pool : `int`
            Dice pool for the roll.
        difficulty : `int`, Optional
            Difficulty for the roll. Defaults to 6.
        specialty : `bool`, Optional
            Whether if the roll represents an action included in some specialty, so 10's count as two successes each, or not.
            Defaults to `False`.
        
        Returns
        -------
        tuple[int]
            The resultant numbers from the dice.
        int
            Number of successes of the roll for the given difficulty.
        """
        roll=tuple(randint(1,10) for i in range(pool))
        #// successes=0
        #// for die in roll:
        #//     if die==10 and specialty:
        #//         successes+=2
        #//     elif die>=difficulty:
        #//         successes+=1
        successes=len(tuple(die for die in roll if die>=difficulty))
        if specialty:
            successes+=len(tuple(die for die in roll if die==10))
        return roll,successes