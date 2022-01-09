from MyAgent import MyAgent


#inherits MyAgent

class MyAgentStones(MyAgent):

    def __init__(self, id, initX, initY, env, capacity):
        MyAgent.__init__(self, id, initX, initY, env)
        self.stone = 0
        self.backPack = capacity

    # return quantity of precious stones collected and not unloaded yet
    def getTreasure(self):
        return self.stone

    # unload precious stones in the pack back at the current position
    def unload(self):
        self.env.unload(self)
        self.stone = 0

    #return the agent's type
    def getType(self):
        return 1

    # def getTreasures(self) -> dict[Tuple[int, int], Treasure]:
    #     self.env = self.env
    #     return {(i,j):self.env.grilleTres[i][j] for i in range(self.env.tailleX) for j in range(self.env.tailleY) if self.env.grilleTres[i][j] != None and self.getType() == self.env.grilleTres[i][j].getType()}


    # load the treasure at the current position
    def load(self,env):
        env.load(self)

    # add some precious stones to the backpack of the agent (quantity t)
    # if the quantity exceeds the back pack capacity, the remaining is lost
    def addTreasure(self, t):
        if(self.stone + t <= self.backPack) :
            self.stone = self.stone + t
        else :
            self.stone = self.backPack

    def __str__(self):
        res ="agent Stone "+ self.id + " ("+ str(self.posX) + " , " + str(self.posY) + ")"
        return res

