from classes import *

def read_cit_HepPh():
    edges = []
    with open('Graphs/Cit-HepPh.txt', 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            link1, link2 = line.split()
            edges.append(Edge('citation', int(link1), int(link2)))
        return Grammar(Graph(edges),
                       lambda x: x == 'citation',
                       lambda x: 2,
                       lambda x: 3)