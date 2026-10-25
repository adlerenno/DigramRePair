from classes import *

def read_node_labels():
    node_labels = {}
    with open('Graphs/contact-primary-school/label-names-contact-primary-school.txt', 'r') as file:
        counter = 1
        for line in file:
            node_labels[counter] = line.strip()
            edge_label_dict[line.strip()] = 1
            counter += 1
    return  node_labels

def create_labels(dict):
    edges = []
    counter = 1

    with open('Graphs/contact-primary-school/node-labels-contact-primary-school.txt','r') as file:
        for line in file:
            line = line.strip()
            edges.append(Edge(dict[int(line)], 'student' + str(counter)))
            counter += 1
    return edges

def read_contact_primary_school():
    label_dict = read_node_labels()
    edges = create_labels(label_dict)

    with open('Graphs/contact-primary-school/hyperedges-contact-primary-school.txt','r') as file:
        for line in file:
            students = line.strip().split(',')
            members = []
            for i in students:
                members.append('student' + i)
            edges.append(Edge('grouped' + str(len(members)), *members))
            edge_label_dict['grouped' + str(len(members))] = len(members)

    return Grammar(Graph(edges), lambda x: x in edge_label_dict, lambda x: edge_label_dict[x],
                   lambda x: edge_label_dict[x] + 1)

edge_label_dict = {}