from classes import *

def read_ca_AstroPh():
    edges = []
    with open('Graphs/CA-AstroPh.txt', 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            link1, link2 = line.split()
            edges.append(Edge('collaboration', int(link1), int(link2)))
        return Grammar(Graph(edges),
                       lambda x: x == 'collaboration',
                       lambda x: 2,
                       lambda x: 3)