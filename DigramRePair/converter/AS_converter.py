from classes import *

def read_AS():
    edges = []
    with open('Graphs/as20000102.txt', 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            link1, link2 = line.split()
            edges.append(Edge('communicate', int(link1), int(link2)))
        return Grammar(Graph(edges),
                       lambda x: x == 'communicate',
                       lambda x: 2,
                       lambda x: 3)