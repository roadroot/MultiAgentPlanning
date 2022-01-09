from Environment import Environment
from MyAgent import MyAgent
class Discussion:
    def __init__(self, env: Environment) -> None:
        self.env: Environment = env
        env.log = ''
        self.agents_gold: dict[str, MyAgent] = {}
        self.agents_chest: dict[str, MyAgent] = {}
        self.agents_stone: dict[str, MyAgent] = {}
        for name, agent in env.agentSet.items():
            agent.generateChestAffectation()
            if agent.isChest():
                self.agents_chest[name] = agent
            elif agent.isGold():
                self.agents_gold[name] = agent
            else:
                self.agents_stone[name] = agent

    def finishDiscussion(self):
        inDiscussion = True
        while inDiscussion:
            inDiscussion = False
            for agent in self.env.agentSet.values():
                while agent.handleMail():
                    inDiscussion = True

    def divideTask(self):
        for agent in self.env.agentSet.values():
            agent :MyAgent = agent
            agent.getImpossibleTreasures()
        for agent in self.env.agentSet.values():
            while agent.handleMail():
                pass
        notDone = True
        while notDone:
            notDone = False
            for agent in self.env.agentSet.values():
                notDone = agent.askChest() or notDone
                self.finishDiscussion()

    def collectiveTask(self):
        step = 0
        for agent in self.env.agentSet.values():
            agent : MyAgent = agent
            agent.studyInitialEnvironment()
        inPlanning = True
        while inPlanning:
            inPlanning = False
            step += 1
            for agent in self.env.agentSet.values():
                inPlanning = agent.planAMove() or inPlanning
                self.finishDiscussion()
