import flet as ft
import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._listYear = []
        self._listShape = []
        self._grafo = nx.Graph()
        self._idMap = {}
        self._idMapName = {}

    def getYears(self):
        self._listYears = DAO.getAllYears()
        return self._listYears

    def getShape(self):
        self._listShape = DAO.getAllShapes()
        return self._listShape

    def buildGraph(self, anno, shape):
        self._nodi = DAO.getAllStates()

        for s in self._nodi:
            self._idMap[s.id] = s

        for s in self._nodi:
            self._idMapName[s.Name] = s

        self._grafo.add_nodes_from(self._nodi)
        self._archi = DAO.getAllEdges(self._idMap)
        for e in self._archi:
            st1 = e.s1
            st2 = e.s2
            peso = DAO.getPesi(anno, shape, st1.id, st2.id)
            if peso > 0:
                self._grafo.add_edge(st1, st2, weight=peso)
                print(st1.id, st2.id, peso)

    def getAllVicini(self):
        elencoPesiVicini = []
        for s in self._grafo.nodes():
            peso = self.getPesoVicini(s)
            elencoPesiVicini.append((s.id, peso))
        return elencoPesiVicini

    def getPesoVicini(self, v0):
        vicini = self._grafo.neighbors(v0)
        pesoTot = 0
        for v in vicini:
            pesoTot += self.getEdgeWeight(v0, v)
        return pesoTot

    def getEdgeWeight(self, v0, v):
        return self._grafo[v0][v]['weight']

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

