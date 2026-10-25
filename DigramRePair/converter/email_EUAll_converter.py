from classes import *

def read_email_EUAll():
    edges = []
    with open('Graphs/Email-EuAll.txt', 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            link1, link2 = line.split()
            edges.append(Edge('send email', int(link1), int(link2)))
        return Grammar(Graph(edges),
                       lambda x: x == 'send email',
                       lambda x: 2,
                       lambda x: 3)