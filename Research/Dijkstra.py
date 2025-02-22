from matplotlib import pyplot as plt
import numpy as np
import copy
import time
import statistics as stats


# Een zeer generieke manier om een graaf de implementeren is er
# daarwerkelijk twee sets van te maken op basis van twee classes:
class Vertex:
    def __init__(self, identifier, data_):
        self.id = identifier
        self.data = data_

    def __eq__(self, other):  # nodig om aan een set toe te voegen
        return self.id == other.id

    def __hash__(self):  # nodig om aan een set toe te voegen
        return hash(self.id)

    def __repr__(self):
        return str(self.id) + ":" + str(self.data)


class Edge:
    def __init__(self, vertex1, vertex2, data_):
        if (vertex1.id < vertex2.id):
            self.v1 = vertex1
            self.v2 = vertex2
        else:
            self.v1 = vertex2
            self.v2 = vertex1
        self.data = data_

    def __eq__(self, other):  # nodig om aan een set toe te voegen
        return self.v1.id == other.v1.id and self.v2.id == self.v2.id

    def __hash__(self):  # nodig om aan een set toe te voegen
        return hash(str(self.v1.id) + "," + str(self.v2.id))

    def __repr__(self):
        return "(" + str(self.v1.id) + "," + str(self.v2.id) + "):" + str(self.data)


class CGraph:
    def __init__(self):
        self.V = set()
        self.E = set()

    def __str__(self):
        return "V: " + str(self.V) + "\nE: " + str(self.E)

def findNeighbours(n,graph):
    neighbours = set()
    for group in graph.E:
        if (group.v1 == n) or (group.v2 == n):
            if group.v1 != n:
                neighbours.add(group.v1)
            elif group.v2 != n:
                neighbours.add(group.v2)
    return neighbours



def minDist(N):
    minValue = float('inf')
    minDict = {}
    for i in N:
        if N[i][1]["dist"] < minValue:
            minValue = N[i][1]["dist"]
            minDict[i] = N[i]
    return minDict


def findNeighboursD(n, graph, n_key):
    neighbours = {}
    keys = n[n_key][1].keys()
    for key in keys:
        if key != "dist" and key != "prev" and key != "solved":
            neighbours[key] = graph[key]

    return neighbours


def getPath(node, start, path):
    key = list(node.keys())[0]
    path.append(key)

    if (key == start):
        return path

    getPath(node[key][1]["prev"], start, path)


def DPath(gr2, start, finish):
    graph = copy.deepcopy(gr2)
    for n in graph:
        graph[n][1]["dist"] = float('inf')
        graph[n][1]["prev"] = None
        graph[n][1]["solved"] = False

    graph[start][1]["dist"] = 0
    S = {}
    N = {}
    N[start] = graph[start]

    while (len(N) != 0):
        n = minDist(N)
        n_key = list(n.keys())[0]
        n[n_key][1]["solved"] = True

        S.update(n)
        del N[n_key]

        if n_key == finish:
            break

        neighbours = findNeighboursD(n, graph, n_key)
        for m in neighbours:
            if (neighbours[m][1]["solved"] == False):
                if m not in N:
                    N[m] = graph[m]

                altDistance = n[n_key][1]["dist"] + n[n_key][1][m]
                if (neighbours[m][1]["dist"] > altDistance):
                    neighbours[m][1]["dist"] = altDistance
                    neighbours[m][1]["prev"] = n

    node = {}
    node[finish] = graph[finish]
    path = []
    getPath(node, start, path)
    path.reverse()
    return node[finish][1]["dist"], path


DGraph = dict
gr2 = {1: ("", {2:9}),
       2: ("", {1:9, 3:11}),
       3: ("", {2:11, 8:8.5}),
       4: ("", {5:6, 6:5}),
       5: ("", {4:6}),
       6: ("", {4:5, 7:6, 11:4}),
       7: ("", {6:6, 14:10}),
       8: ("", {3:8.5, 9:6, 10:2}),
       9: ("", {8:6}),
       10: ("", {8:2, 11:13, 12:6}),
       11: ("", {6:4, 10:13, 13:6}),
       12: ("", {10:6, 15:17}),
       13: ("", {11:6, 14:6, 16:16.5}),
       14: ("", {7:10, 13:6}),
       15: ("", {12:17, 20:13.5, 23:19.5}),
       16: ("", {13:16.5, 17:2, 18:3.5, 19:4}),
       17: ("", {16:2, 18:4, 19:3.5}),
       18: ("", {16:3.5, 17:4, 19:2, 20:2.5}),
       19: ("", {16:4, 17:3.5, 18:2}),
       20: ("", {15:13.5, 18:2.5, 21:8}),
       21: ("", {20:8, 22:6, 24:6}),
       22: ("", {21:6, 28:10}),
       23: ("", {15:19.5, 24:13, 26:2}),
       24: ("", {21:6, 23:13, 27:4}),
       25: ("", {26:6}),
       26: ("", {23:2, 25:6, 30:8}),
       27: ("", {24:4, 28:6, 31:6}),
       28: ("", {22:10, 27:6}),
       29: ("", {30:6}),
       30: ("", {26:8, 29:6, 31:13}),
       31: ("", {27:6, 30:13, 32:4.5, 33:2.5}),
       32: ("", {31:4.5, 33:3.5}),
       33: ("", {31:2.5, 32:3.5})
      }

print(DPath(gr2, 21, 28))
