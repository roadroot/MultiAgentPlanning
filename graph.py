from typing import Tuple
import math

def generateFromTreasures(agent, treasures: list[Tuple[int, int]]) -> Tuple[list[Tuple[int, int]], int]:
    if hasattr(agent, 'getType'):
        saw : dict[list[Tuple[int, int]], Tuple[int, int, int]] = {}
        for treasure in treasures:
            value = agent.env.grilleTres[treasure[0]][treasure[1]].value
            saw[(treasure,)] = (distanceAB(agent.getPos(), treasure), value, min(value, agent.backPack))
        notDone = True
        while notDone:
            newSaw : dict[list[Tuple[int, int]], Tuple[int, int, int]] = {}
            notDone = False
            for path, (distance, backpack, totalEarning) in saw.items():
                path = list(path)
                to_see = [x for x in treasures if x not in path]
                if to_see:
                    notDone = True
                    for treasure in to_see:
                        path = path.copy()
                        value = agent.env.grilleTres[treasure[0]][treasure[1]].value
                        if backpack + value > agent.backPack and backpack != 0:
                            path.append(agent.env.posUnload)
                            newSaw[tuple(path)] = (distance + distanceAB(path[-1], path[-2]), 0, totalEarning)
                        else:
                            path.append(treasure)
                            newSaw[tuple(path)] = (distance + distanceAB(path[-1], path[-2]), backpack + value, totalEarning + min(value, agent.backPack))
                else:
                    newSaw[tuple(path)] = saw[tuple(path)]
            saw = newSaw
        max_earning = -1
        min_distance = 9999999
        min_e = None
        for path, (distance, _, totalEarning) in saw.items():
            if(max_earning < totalEarning):
                min_e = path, distance
                max_earning = totalEarning
                min_distance = distance
            elif distance <= min_distance and max_earning <= totalEarning:
                min_e = path, distance
                max_earning = totalEarning
                min_distance = distance
        return min_e
    else:
        saw : dict[list[Tuple[int, int]], int] = {}
        for treasure in treasures:
            saw[(treasure,)] = distanceAB(agent.getPos(), treasure)
        notDone = True
        while notDone:
            newSaw : dict[list[Tuple[int, int]], int] = {}
            notDone = False
            for path, distance in saw.items():
                path = list(path)
                to_see = [x for x in treasures if x not in path]
                if to_see:
                    notDone = True
                    for treasure in to_see:
                        path = path.copy()
                        path.append(treasure)
                        newSaw[tuple(path)] = distance + distanceAB(path[-1], path[-2])
                else:
                    newSaw[tuple(path)] = saw[tuple(path)]
            saw = newSaw
        min_distance = 9999999
        min_e = None
        for path, distance in saw.items():
            if distance <= min_distance:
                min_distance = distance
                min_e = list(path), distance
        return min_e

def distanceAB(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    # print(a)
    # print(b)
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

