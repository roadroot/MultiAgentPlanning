import PyQt6.QtCore
import PyQt6.QtGui
import PyQt6.QtWidgets
from typing import Text
from Environment import Environment
from MyAgent import MyAgent
from MyAgentGold import  MyAgentGold
from MyAgentChest import MyAgentChest
from MyAgentStones import MyAgentStones
from Treasure import Treasure
from Discution import Discussion

class Graphics(PyQt6.QtWidgets.QMainWindow):
    def loadFileConfig(self, nameFile):
        self.counter = 0
        file = open(nameFile)
        lines = file.readlines()
        tailleEnv = lines[1].split()
        tailleX = int(tailleEnv[0])
        tailleY = int(tailleEnv[1])
        zoneDepot = lines[3].split()
        cPosDepot =  (int(zoneDepot[0]), int(zoneDepot[1]))
        dictAgent = dict()

        env = Environment(tailleX, tailleY, cPosDepot)
        cpt = 0

        for ligne  in lines[4:] :
            ligneSplit = ligne.split(":")
            if(ligneSplit[0]=="tres"): # new treasure
                if(ligneSplit[1]=="or"):
                    env.addTreasure(Treasure(0, int(ligneSplit[4])), int(ligneSplit[2]), int(ligneSplit[3]))

                elif(ligneSplit[1]=="pierres"):
                    tres = Treasure(1, int(ligneSplit[4]))
                    env.addTreasure(tres, int(ligneSplit[2]), int(ligneSplit[3]))
            elif(ligneSplit[0]=="AG") : #new agent
                if(ligneSplit[1]=="or"):
                    id = "agent" + str(cpt)
                    agent = MyAgentGold(id, int(ligneSplit[2]), int(ligneSplit[3]), env, int(ligneSplit[4]))
                    dictAgent[id] = agent
                    env.addAgent(agent)
                    cpt = cpt +1

                elif(ligneSplit[1]=="pierres"):
                    id = "agent" + str(cpt)
                    agent = MyAgentStones(id, int(ligneSplit[2]), int(ligneSplit[3]), env, int(ligneSplit[4]))
                    dictAgent[id] = agent
                    env.addAgent(agent)
                    cpt = cpt + 1

                elif (ligneSplit[1] == "ouvr"):
                    id = "agent" + str(cpt)
                    agent = MyAgentChest(id, int(ligneSplit[2]), int(ligneSplit[3]), env)
                    dictAgent[id] = agent
                    env.addAgent(agent)
                    cpt = cpt + 1

        file.close()
        env.addAgentSet(dictAgent)

        return (env, dictAgent)

    def loadImages(self):
        self.chest_gold_locked : PyQt6.QtGui.QPixmap = PyQt6.QtGui.QPixmap('ui/money_locked.png').scaled(self.tileWidth, self.tileheight)
        self.chest_gold_unlocked : PyQt6.QtGui.QPixmap = PyQt6.QtGui.QPixmap('ui/money_open.png').scaled(self.tileWidth, self.tileheight)
        self.chest_gold_looted : PyQt6.QtGui.QPixmap = PyQt6.QtGui.QPixmap('ui/money_looted.png').scaled(self.tileWidth, self.tileheight)
        self.chest_gem_locked : PyQt6.QtGui.QPixmap = PyQt6.QtGui.QPixmap('ui/stone_locked.png').scaled(self.tileWidth, self.tileheight)
        self.chest_gem_unlocked : PyQt6.QtGui.QPixmap = PyQt6.QtGui.QPixmap('ui/stone_open.png').scaled(self.tileWidth, self.tileheight)
        self.chest_gem_looted : PyQt6.QtGui.QPixmap = PyQt6.QtGui.QPixmap('ui/stone_looted.png').scaled(self.tileWidth, self.tileheight)
        self.agent_gold : PyQt6.QtGui.QPixmap = PyQt6.QtGui.QPixmap('ui/goldagent.png').scaled(self.tileWidth, self.tileheight)
        self.agent_chest : PyQt6.QtGui.QPixmap= PyQt6.QtGui.QPixmap('ui/moneyagent.png').scaled(self.tileWidth, self.tileheight)
        self.agent_open : PyQt6.QtGui.QPixmap= PyQt6.QtGui.QPixmap('ui/openagent.png').scaled(self.tileWidth, self.tileheight)
        self.empty : PyQt6.QtGui.QPixmap= PyQt6.QtGui.QPixmap('ui/nothing.png').scaled(self.tileWidth, self.tileheight)

    def loadColors(self):
        self.colorLight = '#A0FFA0'
        self.colorDark = '#40ff80'
        self.colorBackground = '#404040'
        self.colorUnload = '#8080C0'

    def __init__(self, file = 'env1.txt') -> None:
        super(Graphics, self).__init__()
        self.sideFrameWidth : int = 250
        self.tileWidth : int = 50
        self.tileheight : int = 50
        self.env, self.lAg = self.loadFileConfig(file)
        self.env : Environment= self.env
        self.lAg : dict[str, MyAgent]= self.lAg
        self.n : int= self.env.tailleX
        self.m : int= self.env.tailleY
        self.width = self.tileWidth * self.n
        self.height = self.tileheight * self.m
        self.setWindowTitle('Agents')
        self.setGeometry(50, 50, self.width + self.sideFrameWidth, self.height)
        self.mainFrame : PyQt6.QtWidgets.QFrame = PyQt6.QtWidgets.QFrame(self)
        self.mainFrame.setGeometry(0, 0, self.width + self.sideFrameWidth, self.height)
        self.edit = PyQt6.QtWidgets.QTextEdit(self.mainFrame)
        self.edit.setGeometry(self.width, 50, self.sideFrameWidth, self.height-100)
        self.edit.setReadOnly(True)
        self.score = PyQt6.QtWidgets.QLabel(self.mainFrame)
        self.score.setGeometry(self.width, 0, self.sideFrameWidth, 50)
        self.loadColors()
        self.loadImages()
        discution = Discussion(self.env)
        discution.divideTask()
        discution.collectiveTask()
        self.createMat()
        self.draw()

    def createMat(self):
        self.mat : dict[(int, int), PyQt6.QtWidgets.QLabel] = {}
        for i in range(self.n):
            for j in range(self.m):
                self.mat[i, j] = PyQt6.QtWidgets.QLabel(self.mainFrame)
                self.mat[i, j].setGeometry(j*self.tileWidth, i*self.tileheight, self.tileWidth, self.tileheight)
                self.mat[i, j].setStyleSheet(f"background-color: {self.colorLight if (i+j)%2 == 0 else self.colorDark}")


    def draw(self):
        for i in range(self.n):
            for j in range(self.m):
                tres = False
                if self.env.grilleTres[i][j] != None and self.env.grilleTres[i][j].getType() == 0:
                    tres = True
                    if self.env.grilleTres[i][j].isOpen() and self.env.grilleTres[i][j].getValue() > 0:
                        self.mat[i, j].setPixmap(self.chest_gold_unlocked)
                    elif self.env.grilleTres[i][j].isOpen():
                        self.mat[i, j].setPixmap(self.chest_gold_looted)
                    else:
                        self.mat[i, j].setPixmap(self.chest_gold_locked)
                if self.env.grilleTres[i][j] != None and self.env.grilleTres[i][j].getType() == 1:
                    if self.env.grilleTres[i][j].isOpen() and self.env.grilleTres[i][j].getValue() > 0:
                        self.mat[i, j].setPixmap(self.chest_gem_unlocked)
                    elif self.env.grilleTres[i][j].isOpen():
                        self.mat[i, j].setPixmap(self.chest_gem_looted)
                    else:
                        self.mat[i, j].setPixmap(self.chest_gem_locked)
                else:
                    if not tres:
                        self.mat[i, j].setPixmap(self.empty)
        self.mat[self.env.posUnload].setStyleSheet(f"background-color: {self.colorUnload}")
        for agent in self.lAg.values():
            print(agent.id + ' ' + str(agent.getPos()))
            if isinstance(agent, MyAgentChest):
                self.mat[agent.posX, agent.posY].setPixmap(self.agent_chest)
            elif isinstance(agent, MyAgentGold):
                self.mat[agent.posX, agent.posY].setPixmap(self.agent_gold)
            else:
                self.mat[agent.posX, agent.posY].setPixmap(self.agent_open)

        self.edit.setText(self.env.log)
        self.score.setText(str(self.env.score))
        button = PyQt6.QtWidgets.QPushButton(self.mainFrame, text='Next')
        button.setGeometry(self.width + 10, self.height-40, self.sideFrameWidth-20, 30)
        button.clicked.connect(self.move)


    def move(self):
        for agent in self.env.agentSet.values():
            agent : MyAgent = agent
            not_yet = True
            while not_yet:
                not_yet = False
                if agent.moves:
                    command, x1, y1, x2, y2 = agent.moves.pop(0)
                    if command == 'unload':
                        self.env.unload(agent)
                        not_yet = True
                    elif command == 'load':
                        self.env.load(agent)
                        not_yet = True
                    elif command == 'open':
                        self.env.open(agent, x1, y1)
                        not_yet = True
                    else:
                        agent.move(x1, y1, x2, y2)
        self.draw()
app = PyQt6.QtWidgets.QApplication([])
window = Graphics()
window.show()
app.exec()