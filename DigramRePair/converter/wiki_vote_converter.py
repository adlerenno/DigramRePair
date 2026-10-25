from classes import *

def read_wiki_vote():
    edges = []
    with open('Graphs/Wiki-Vote.txt', 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            link1, link2 = line.split()
            edges.append(Edge('vote', int(link1), int(link2)))
        return Grammar(Graph(edges),
                       lambda x: x == 'vote',
                       lambda x: 2,
                       lambda x: 3)