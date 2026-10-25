from classes import *

def read_labelnames():
    labels = {}
    with open('mathoverflow-answers/label-names-mathoverflow-answers.txt', 'r') as file:
        counter = 1
        for line in file:
            labels[counter] = line.strip()
            counter += 1
    return labels

def read_labels(labelnames):
    edges = []
    counter = 1
    with open('mathoverflow-answers/node-labels-mathoverflow-answers.txt', 'r') as file:
        for line in file:
            labels = [labelnames[int(i)] for i in line.strip().split(',')]
            edges.append(Edge('labels', 'question' + str(counter), *labels))
            counter += 1
    return edges

def read_edges():
    edges = []
    with open('mathoverflow-answers/hyperedges-mathoverflow-answers.txt', 'r') as file:
        for line in file:
            questions = line.strip().split(',')
            nodes = []
            for i in questions:
                nodes.append('question' + i)
            edges.append(Edge('answered', *nodes))
    return edges

def read_mathoverflow():
    edges = read_labels(read_labelnames())
    edges.extend(read_edges())
    return Grammar(Graph(edges))
