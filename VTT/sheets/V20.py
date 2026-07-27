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