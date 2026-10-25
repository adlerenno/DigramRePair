from classes import *

def read_node_labels():
    node_labels = {}
    with open('cat-edge-Cooking/node-labels.txt', 'r') as file:
        counter = 1
        for line in file:
            node_labels[counter] = line.strip()
            counter += 1
    return  node_labels

def read_hyperedge_labels_identities():
    hyperedge_labels = {}
    with open('cat-edge-Cooking/hyperedge-label-identities.txt', 'r') as file:
        counter = 1
        for line in file:
            hyperedge_labels[counter] = line.strip()
            counter += 1
    return  hyperedge_labels

def read_hyperedge_labels(identities):
    hyperedge_labels = []
    with open('cat-edge-Cooking/hyperedge-labels.txt', 'r') as file:
        for line in file:
            hyperedge_labels.append(identities[int(line.strip())])
    return hyperedge_labels

def read_hyperedges(hyperedge_labels, node_labels):
    edges = []
    with open('cat-edge-Cooking/hyperedges.txt', 'r') as file:
        counter = 0
        for line in file:
            ingredients = line.strip().split()
            edges.append(Edge(hyperedge_labels[counter], *[node_labels[int(i)] for i in ingredients]))
            counter += 1
    return edges


def read_cat_cooking():
    hyperedge_labels = read_hyperedge_labels(read_hyperedge_labels_identities())
    node_labels = read_node_labels()
    return Grammar(Graph(read_hyperedges(hyperedge_labels, node_labels)))

