from mpmath import hyper

from classes import *

def create_country_dict():
    dict = {}
    counter = 1
    with open('trivago-clicks/label-names-trivago-clicks.txt','r') as file:
        for line in file:
            country = line.strip()
            dict[counter] = country
            counter += 1
    return dict


def node_labels(dict):
    edges = []
    counter = 1

    with open('trivago-clicks/node-labels-trivago-clicks.txt','r') as file:
        for line in file:
            line = line.strip()
            edges.append(Edge(dict[int(line)], 'accomodation' + str(counter)))
            counter += 1
    return edges

def read_trivago_clicks():
    country_dict = create_country_dict()
    edges = node_labels(country_dict)

    with open('trivago-clicks/hyperedges-trivago-clicks.txt','r') as file:
        for line in file:
            accomodations = line.strip().split(',')
            members = []
            for i in accomodations:
                members.append('accomodation' + i)
            edges.append(Edge('clicked', *members))

    return Grammar(Graph(edges))
