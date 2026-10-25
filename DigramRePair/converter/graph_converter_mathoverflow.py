from classes import *

def read_labelnames():
    labels = {}
    with open('Graphs/mathoverflow-answers/label-names-mathoverflow-answers.txt', 'r') as file:
        counter = 1
        for line in file:
            labels[counter] = line.strip()
            counter += 1
    return labels

def read_labels(labelnames):
    edges = []
    counter = 1
    with open('Graphs/mathoverflow-answers/node-labels-mathoverflow-answers.txt', 'r') as file:
        for line in file:
            labels = [labelnames[int(i)] for i in line.strip().split(',')]
            edges.append(Edge('labels' + str(len(labels)+1), 'question' + str(counter), *labels))
            edge_label_dict['labels' + str(len(labels)+1)] = len(labels)+1
            counter += 1
    return edges

def read_edges():
    edges = []
    with open('Graphs/mathoverflow-answers/hyperedges-mathoverflow-answers.txt', 'r') as file:
        for line in file:
            questions = line.strip().split(',')
            nodes = []
            for i in questions:
                nodes.append('question' + i)
            edge = Edge('answered' + str(len(nodes)), *nodes)
            edge_label_dict['answered' + str(len(nodes))] = len(nodes)
            edges.append(edge)
    return edges

def read_mathoverflow():
    edges = read_labels(read_labelnames())
    edges.extend(read_edges())
    return Grammar(Graph(edges), lambda x: x in edge_label_dict, lambda x: edge_label_dict[x],
                   lambda x: edge_label_dict[x] + 1)

edge_label_dict = {}
