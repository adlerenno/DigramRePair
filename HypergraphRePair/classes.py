
class Grammar:

    _slots__ = ('rules',)

    def __init__(self, graph):
        """Initializes a grammar object.
        :param graph: used as the start_rule of this grammar. start_rule has the name 0 implicitly. Should be a graph."""
        self.rules = {0: graph}


    def __str__(self):
        """:returns: a readable representation of this grammar object"""
        return self.rules.__str__()

    def __iter__(self):
        """:returns an iterable over the rules within this grammar. Can be used by: for rule in grammar: ..."""
        return self.rules.__iter__()


    def size_of_grammar(self):
        """:return: the size of the while grammar"""
        return sum((self.rules[g].size_of() for g in self.rules.keys()))

    def get_start_rule(self):
        """:returns: the start_rule by it's implicit id 0."""
        return self.rules[0]

    def get_unused_nonterminal(self):
        """:return the next ID not associated with a rule"""
        i = 1
        while i in self.rules:
            i += 1
        return i

    def add_rule(self, rule_name, rule):
        """Method used for adding a rule. Note that there is no check, if there is a rule with the given Name.
        :param rule_name: name of the new added rule.
        :param rule: the new added rule."""
        self.rules[rule_name] = rule



class Graph:

    __slots__ = ('edges',)

    def __init__(self, edges=None):
        """Inits a Graph object.
        :param edges: initial edges of this graph."""
        self.edges = [] if edges is None else edges

    def __str__(self):
        """:returns: a string representation of the this graph."""
        return "{}".format(self.edges)

    __repr__ = __str__

    def __getitem__(self, id):
        """:returns the edge at a given ID"""
        return self.edges[id]

    def __len__(self):
        """:returns the number of edges within the graph."""
        return len(self.edges)

    def __setitem__(self, id, newEdge):
        """Replaces a new edge at the given ID.
        :param id: id of the edge.
        :param newEdge: the new edge"""
        self.edges[id] = newEdge

    def __delitem__(self, id):
        """Deletes an edge at a given ID.
        :param id: id of the edge, which is going to be deleted."""
        del self.edges[id]

    def size_of(self):
        """:returns: the cumulative size of all rules."""
        return sum((e.size_of() for e in self.edges))

    def get_edges(self):
        """:returns all edges within this graph object."""
        return self.edges

    def __eq__(self, other):
        """:returns: true, if and only if both graphs are equal. The order of the edges is not important."""
        edges = self.get_edges().copy()
        tenth_of_edges = len(edges) // 10
        counter = 1
        for e in other.get_edges():
            if len(edges) % tenth_of_edges == 0:
                print(f'{counter}/10 of the comparison is finished')
                counter += 1
            for f in edges:
                if e == f:
                    edges.remove(f)
                    break
        return len(edges) == 0


class Edge:

    __slots__ = ('label', 'nodes')

    def __init__(self, label, *args):
        """Inits an labeled Hyperedge.
        :param label: label of the new edge.
        :param args: all following arguments are treated as vertices."""
        self.label = label
        self.nodes = args

    def __repr__(self):
        """:returns: a String representation of this edge object."""
        return "('{}', {})".format(self.label, ", ".join((str(n) for n in self.nodes)))

    def __iter__(self):
        """:returns an iterable looping over the attached nodes in order of their connection_types."""
        return self.nodes.__iter__()

    def __getitem__(self, id):
        """:returns the node with connection_type 'id'"""
        return self.nodes[id]

    def size_of(self):
        """returns the size to save this edge. +1 is for the label of the Edge. """
        return self.rank() + 1

    def rank(self):
        """:returns: the rank of this edge"""
        return len(self.nodes)

    def get_label(self):
        """:returns: the label of this edge."""
        return self.label

    def get_nodes(self):
        """:returns a list of the attached nodes ordered after the connection_type."""
        return self.nodes

    def __eq__(self, other):
        """:returns true if and only if self and other represent the same edge."""
        return self.label == other.get_label() and self.nodes == other.get_nodes()


class Digram(tuple):
    """This class is used to represent a Digram. Note, that the order of the IncidenceTypes is important when comparing,
    but it is not important within the graph-repair-algorithm."""
    def __new__(cls, incidence_type_1, incidence_type_2):
        """Fixes a Digram to two IncidenceTypes.
        :param incidence_type_1: first IncidenceType.
        :param incidence_type_2: second IncidenceType."""
        return tuple.__new__(Digram, (incidence_type_1, incidence_type_2))

    def invert(self):
        """:returns a Digram with the IncidenceTypes in inverted order."""
        return Digram(self[1], self[0])

    __slots__ = ()


class IncidenceType(tuple):
    def __new__(cls, label, connection_type):
        """Fixes an IncidenceType to a label and an connection_type

        :param label: Label of the incidence type. Can be anything hashable.
        :param connection_type: A connection type is a natural number (with 0). It must fit to the rank of the label."""
        return tuple.__new__(IncidenceType, (label, connection_type))

    def get_label(self):
        """:returns: the label of this IncidenceType."""
        return self[0]

    def get_connection_type(self):
        """:returns: the connection type of this IncidenceType."""
        return self[1]

    def size_of(self):
        """:returns: the size of this IncidenceType."""
        return 2

    __slots__ = ()

class Rule:

    __slots__ = ('first', 'second', 'name')

    def __init__(self, digram, grammar):
        self.first = digram[0]
        self.second = digram[1]
        self.name = grammar.get_unused_nonterminal()

    def get_name(self):
        """:returns: the name of this rule."""
        return self.name

    def get_rule(self):
        """:returns: the rule of this rule."""
        return self.first, self.second

    def get_first(self):
        """:returns: the first edge of this rule."""
        return self.first

    def get_second(self):
        """:returns: the second edge of this rule."""
        return self.second

    def size_of(self):
        """:returns: the size of this rule."""
        return self.first.size_of() + self.second.size_of()

    def get_new_edge(self, old_edges):
        """:returns: the new edge of this rule."""
        edge1 = old_edges[0]
        edge2 = old_edges[1]

        nodes1 = list(edge1.nodes)
        common_node = nodes1.pop(self.first.get_connection_type())
        nodes1.insert(0, common_node)

        nodes2 = list(edge2.nodes)
        nodes2.pop(self.second.get_connection_type())

        nodes = nodes1 + nodes2 + [len(nodes1)]

        return Edge(self.get_name(), *nodes)

    def __repr__(self):
        """:returns: a string representation of this rule."""
        return "[{}, {}]".format(self.first, self.second)


class PrunedRule:

    __slots__ = ('connection_type', 'first', 'second')

    def __init__(self, connection_type, first, second):
        self.connection_type = connection_type
        self.first = first
        self.second = second

    def __repr__(self):
        """:returns: a string representation of this rule."""
        return "({},[{}, {}])".format(self.connection_type, self.first, self.second)

    def size_of(self):
        """:returns: the size of this rule."""
        return self.first.size_of() + self.second.size_of() + 1

    def get_connection_type(self):
        """:returns: the connection type of this pruned rule."""
        return self.connection_type

    def get_first(self):
        """:returns: the first edge of this pruned rule."""
        return self.first

    def get_second(self):
        """:returns: the second edge of this pruned rule."""
        return self.second