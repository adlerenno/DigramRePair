from classes import *

def read_departments():
    with open('Graphs/Email_EU_core/email-Eu-core-department-labels.txt', 'r') as file:
        edges = []
        for line in file:
            member, department = line.split()
            edges.append(Edge('department', int(member), 'Department' + department))
    return edges

def read_members():
    with open('Graphs/Email_EU_core/email-Eu-core.txt', 'r') as file:
        edges = []
        for line in file:
            member1, member2 = line.split()
            edges.append(Edge('send email', int(member1), int(member2)))
    return edges

def read_email_eu_core():
    edges = read_departments()
    edges.extend(read_members())
    edge_label_dict = {'department': 2, 'send email': 2}
    return Grammar(Graph(edges),
                   lambda x: x in edge_label_dict,
                   lambda x: edge_label_dict[x],
                   lambda x: edge_label_dict[x] + 1,)
