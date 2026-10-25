from classes import *

def read_labelnames():
    labels = {}
    with open('Graphs/walmart-trips/label-names-walmart-trips.txt', 'r') as file:
        counter = 1
        for line in file:
            labels[counter] = line.strip()
            edge_label_dict[line.strip()] = 1
            counter += 1
    return labels

def read_labels(labelnames):
    edges = []
    counter = 1
    with open('Graphs/walmart-trips/node-labels-walmart-trips.txt', 'r') as file:
        for line in file:
            edges.append(Edge(labelnames[int(line)], 'product' + str(counter)))
            counter += 1
    return edges

def read_edges():
    edges = []
    with open('Graphs/walmart-trips/hyperedges-walmart-trips.txt', 'r') as file:
        for line in file:
            products = line.strip().split(',')
            nodes = []
            for i in products:
                nodes.append('product' + i)
            edges.append(Edge('bought_together'+ str(len(nodes)), *nodes))
            edge_label_dict['bought_together'+ str(len(nodes))] = len(nodes)
    return edges

def read_walmart_trips():
    edges = read_labels(read_labelnames())
    edges.extend(read_edges())
    return Grammar(Graph(edges), lambda x: x in edge_label_dict, lambda x: edge_label_dict[x],
                   lambda x: edge_label_dict[x] + 1)

edge_label_dict = {}