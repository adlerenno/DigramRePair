from classes import *

def read_gnutella31():
    edges = []
    with open('Graphs/p2p-Gnutella31.txt', 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            link1, link2 = line.split()
            edges.append(Edge('connect', int(link1), int(link2)))
        return Grammar(Graph(edges),
                       lambda x: x == 'connect',
                       lambda x: 2,
                       lambda x: 3)