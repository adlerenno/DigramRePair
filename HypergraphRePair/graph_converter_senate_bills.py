from classes import *

def read_names():
    with open('senate-bills/node-names-senate-bills.txt', 'r') as file_input:
        names = []
        for line in file_input:
            names.append(line.replace('\n',''))
    return names

def read_party(names):
    def mapping_party(name, number):
        if number == '1':
            edge = Edge('Democrat', name)
        else:
            edge = Edge('Republican', name)
        return edge

    with open('senate-bills/node-labels-senate-bills.txt', 'r') as file_input:
        party = []
        for line in file_input:
            party.append(line.replace('\n',''))
    edges = list(map(mapping_party, names, party))
    return edges

def read_committee(names):
    with open('senate-bills/hyperedges-senate-bills.txt', 'r') as file_input:
        edges = []
        for line in file_input:
            committee = line.replace('\n','').split(',')
            members = []
            for i in committee:
                members.append(names[int(i)-1])
            edge = Edge('bill', *members)
            edges.append(edge)
    return edges

def read_US_senate_bills():
    names = read_names()
    edges = read_party(names)
    edges.extend(read_committee(names))
    return Grammar(Graph(edges))
