from classes import *

def read_facebook():
    edges = []
    with open('Graphs/facebook_combined.txt', 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            link1, link2 = line.split()
            edges.append(Edge('friends', int(link1), int(link2)))
        return Grammar(Graph(edges),
                       lambda x: x == 'friends',
                       lambda x: 2,
                       lambda x: 3)