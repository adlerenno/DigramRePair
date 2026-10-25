from classes import *

def read_node_labels():
    node_labels = {}
    with open('contact-primary-school/label-names-contact-primary-school.txt', 'r') as file:
        counter = 1
        for line in file:
            node_labels[counter] = line.strip()
            counter += 1
    return  node_labels

def create_labels(dict):
    edges = []
    counter = 1

    with open('contact-primary-school/node-labels-contact-primary-school.txt','r') as file:
        for line in file:
            line = line.strip()
            edges.append(Edge(dict[int(line)], 'student' + str(counter)))
            counter += 1
    return edges

def read_contact_primary_school():
    label_dict = read_node_labels()
    edges = create_labels(label_dict)

    with open('contact-primary-school/hyperedges-contact-primary-school.txt','r') as file:
        for line in file:
            students = line.strip().split(',')
            members = []
            for i in students:
                members.append('student' + i)
            edges.append(Edge('grouped', *members))

    return Grammar(Graph(edges))