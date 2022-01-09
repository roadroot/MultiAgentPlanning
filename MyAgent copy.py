
from typing import Tuple
from Treasure import Treasure
from graph import generateFromTreasures
import random

class MyAgent:
    def __init__(self, id, initX, initY, env):
        self.id = id
        self.posX = initX
        self.posY = initY
        self.env = env
        self.mailBox = []

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.getId() == self.getId()
        return False

    def getTreasures(self) -> dict[Tuple[int, int], Treasure]:
        return {(i,j):self.env.grilleTres[i][j] for i in range(self.env.tailleX) for j in range(self.env.tailleY) if self.env.grilleTres[i][j] != None and (not(hasattr(self, 'getType')) or self.getType() == self.env.grilleTres[i][j].getType())}

    def generateChestAffectation(self) -> None:
        self.chestAffectation : dict[Tuple[int, int], list[str]]= {}
        for treasure in self.getTreasures():
            self.chestAffectation[treasure] = []
            for agent in self.getPeers():
                self.chestAffectation[treasure].append(agent)

    def getImpossibleTreasures(self) -> dict[Tuple[int, int], Treasure]:
        impossible = {k:v for k,v in self.getTreasures().items() if hasattr(self, 'backPack') and v.getValue() > self.backPack}
        for k in impossible:
            self.chestAffectation[k].remove(self.id)
            for agent in self.getPeers():
                message = f'declare: impossible {k}'
                self.send(agent, message)
                self.env.log += f'{self.id} -> {agent} => '+ message + '\n'
        return impossible

    def getPossibleChests(self) -> list[Tuple[int, int]]:
        return [t for t in self.chestAffectation if self.id in self.chestAffectation[t] and len(self.chestAffectation[t]) != 1]

    def getMyMustDo(self) -> list[Tuple[int, int]]:
        return [t for t in self.chestAffectation if self.chestAffectation[t] == [self.id]]

    def getPeers(self) -> dict[str, object]:
        return {k:v for k, v in self.env.agentSet.items() if not(hasattr(self, 'getType')) and not(hasattr(v, 'getType')) or hasattr(self, 'getType') and hasattr(v, 'getType') and self.getType() == v.getType()}

    #make the agent moves from (x1,y1) to (x2,y2)
    def move(self,  x1,y1, x2, y2) :
        if x1 == self.posX and y1 == self.posY :
            print("departure position OK")
            if self.env.move(self, x1, y1, x2, y2) :
                self.posX = x2
                self.posY = y2
                print("deplacement OK")
                return 1

        return -1

    #return the id of the agent
    def getId(self):
        return self.id

    #return the position of the agent
    def getPos(self):
        return (self.posX, self.posY)

    # add a message to the agent's mailbox
    def receive(self, idReceiver, textContent):
        self.mailBox.append((idReceiver, textContent))

    def getPlan(self):
        if not hasattr(self, 'bigPlan'):
            self.bigPlan = list(generateFromTreasures(self, self.getMyMustDo())[0])
            if not self.isChest():
                self.bigPlan.append(self.env.posUnload)
            self.bigPlan.append(self.getPos())

    def studyInitialEnvironment(self):
        if not hasattr(self, 'previousAgentPosisions'):
            self.getPlan()
            self.previousAgentPosisions = {}
            self.moves = []
            self.opened = {}
            self.step = 0
            self.lastPosition = self.getPos()
            for name, agent in self.env.agentSet.items():
                self.previousAgentPosisions[name] = agent.getPos()

    def planAMove(self) -> bool:
        if not self.bigPlan:
            return False
        destination = self.bigPlan[0]
        directionX = destination[0] - self.lastPosition[0]
        directionY = destination[1] - self.lastPosition[1]
        treasure = None
        if directionX == 0 and directionY == 0:
            if self.isChest():
                self.moves.append(('open', *destination, None, None))
            elif self.previousAgentPosisions == self.env.posUnload:
                self.moves.append(('unload', None, None, None, None))
            else:
                self.moves.append(('load', None, None, None, None))
            self.bigPlan.pop(0)
            return self.planAMove()
        directionX = 0 if directionX == 0 else (1 if directionX > 0 else -1)
        directionY = 0 if directionY == 0 else (1 if directionY > 0 else -1)
        nextX = self.lastPosition[0] + directionX, self.lastPosition[1]
        nextY = self.lastPosition[0], self.lastPosition[1] + directionY
        s = [(directionX, 0), (0, directionY)]
        for d in s:
        if directionY != 0 and not nextY in self.previousAgentPosisions.values():
            treasure : Treasure= self.env.grilleTres[nextY[0]][nextY[1]]
            if not self.isChest() and nextY == destination and treasure and not treasure.isOpen():
                self.moves.append(('wait', None, None, None, None))
                return True
            self.moves.append(('move', *self.lastPosition, *nextY))
            self.lastPosition = nextY
            for agent in self.env.agentSet:
                mail = f'assert: move {nextY}'
                self.send(agent, mail)
                self.env.log += f'{self.id} -> {agent}: {mail}\n'
        elif directionX != 0 and not nextX in self.previousAgentPosisions.values():
            treasure : Treasure= self.env.grilleTres[nextX[0]][nextX[1]]
            if not self.isChest() and nextX == destination and treasure and not treasure.isOpen():
                self.moves.append(('wait', None, None, None, None))
                return True
            self.moves.append(('move', *self.lastPosition, *nextX))
            self.lastPosition = nextX
            for agent in self.env.agentSet:
                mail = f'assert: move {nextX}'
                self.send(agent, mail)
                self.env.log += f'{self.id} -> {agent}: {mail}\n'
        else:
            s = [-1, 1]
            random.shuffle(s)
            if directionX != 0:
                for d in s:
                    nextY = self.lastPosition[0], d + self.lastPosition[1]
                    if d + self.lastPosition[1] in range(0, self.env.tailleY) and not nextY in self.previousAgentPosisions.values():
                        self.moves.append(('move', *self.lastPosition, *nextY))
                        self.lastPosition = nextY
                        for agent in self.env.agentSet:
                            mail = f'assert: move {nextY}'
                            self.send(agent, mail)
                            self.env.log += f'{self.id} -> {agent}: {mail}\n'
                        return True

            if directionY != 0:
                for d in s:
                    nextX = d + self.lastPosition[0], self.lastPosition[1]
                    if d + self.lastPosition[0] in range(0, self.env.tailleX) and not nextX in self.previousAgentPosisions.values():
                        self.moves.append(('move', *self.lastPosition, *nextX))
                        self.lastPosition = nextX
                        for agent in self.env.agentSet:
                            mail = f'assert: move {nextX}'
                            self.send(agent, mail)
                            self.env.log += f'{self.id} -> {agent}: {mail}\n'
                        return True

            self.moves.append(('wait', None, None, None, None))
        return True

    #the agent reads a message in her mailbox (FIFO mailbox)
    #return a tuple (id of the sender, message  text content)
    def readMail (self):
        idSender, textContent = self.mailBox.pop(0)
        print("{} mail received from {} with content {}".format(self.id,idSender,textContent))
        return (idSender, textContent)

    def getPreferredChest(self) -> Tuple[Tuple[int, int], int]|None:
        all_possibilities = {}
        must = self.getMyMustDo()
        allPosTres = self.getPossibleChests()
        if not allPosTres:
            return None
        for treasure in allPosTres:
            _, cost = generateFromTreasures(self, must + [treasure])
            all_possibilities[treasure] = cost
        min_chest = min(all_possibilities, key=all_possibilities.get)
        return min_chest, all_possibilities[min_chest]

    def askChest(self, tresure_cost:Tuple[Tuple[int, int], int]|None = None) -> bool:
        if not tresure_cost:
            tresure_cost = self.getPreferredChest()
        if tresure_cost:
            chest, cost = tresure_cost
            for agent in self.getPeers():
                self.send(agent, f'discuss: chest {chest}, {cost}')
                self.env.log += f'{self.id} -> {agent} => discuss: chest {chest}, {cost}\n'
            return True
        return False

    def handleMail(self) -> bool:
        if self.mailBox:
            sender, mail = self.readMail()
            mail: str = mail
            mail = mail.replace('(','').replace(')','')
            if mail.startswith('declare: impossible '):
                treasure = tuple(map(lambda x: int(x), mail[20:].split(', ')))
                if treasure in self.chestAffectation and sender in self.chestAffectation[treasure]:
                    self.chestAffectation[treasure].remove(sender)
            elif mail.startswith('assert: move '):
                treasure = tuple(map(lambda x: int(x), mail[13:].split(', ')))
                self.previousAgentPosisions[sender] = treasure
            elif mail.startswith('discuss: chest '):
                treasure = list(map(lambda x: float(x), mail[15:].split(', ')))
                treasure, cost = (int(treasure[0]), int(treasure[1])), float(treasure[2])
                if treasure in self.chestAffectation and self.id in self.chestAffectation[treasure]:
                    nPath = self.getMyMustDo()
                    nPath = nPath if treasure in nPath else nPath + [treasure]
                    _, new_cost = generateFromTreasures(self, nPath)
                    if new_cost < cost:
                        self.chestAffectation[treasure] = [self.id]
                        for agent in self.getPeers():
                            self.send(agent, f'discuss: chest {treasure}, {new_cost}')
                            self.env.log += f'{self.id} -> {agent} => discuss: chest {treasure}, {new_cost}\n'
                    else:
                        self.chestAffectation[treasure] = [sender]
                else:
                    self.chestAffectation[treasure] = [sender]
            return True
        return False

    #send a message to the agent whose id is idReceiver
    # the content of the message is some text
    def send(self, idReceiver, textContent):
        self.env.send(self.id, idReceiver, textContent)

    def isChest(self) -> bool:
        return not hasattr(self, 'getType')

    def isGold(self) -> bool:
        return not self.isChest() and self.getType() == 1

    def isGold(self) -> bool:
        return not self.isChest() and self.getType() == 2

    def __str__(self):
        res = self.id + " ("+ str(self.posX) + " , " + str(self.posY) + ")"
        return res

