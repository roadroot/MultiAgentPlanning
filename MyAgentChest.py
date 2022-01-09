from MyAgent import MyAgent


#inherits MyAgent

class MyAgentChest(MyAgent) :
    def __init__(self, id, initX, initY, env):
        MyAgent.__init__(self, id, initX, initY, env)


    # open a chest
    def open(self):
        self.env.open(self, self.posX, self.posY)

    # the agent do not hold some treasure
    def getTreasure(self):
        return 0

    # def getTreasures(self):
    #     self.env = self.env
    #     return {(i,j):self.env.grilleTres[i][j] for i in range(self.env.tailleX) for j in range(self.env.tailleY) if self.env.grilleTres[i][j] != None}

    def __str__(self):
        res = "agent Chest "+ self.id + " (" + str(self.posX) + " , " + str(self.posY) + ")"
        return res