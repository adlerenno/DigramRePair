from timetest import *
import time
from converter.email_EU_core_converter import read_email_eu_core
from converter.Gnutella04_converter import read_gnutella04
from converter.Gnutella31_converter import read_gnutella31
from converter.wiki_vote_converter import read_wiki_vote
from converter.cit_HepPh_converter import read_cit_HepPh
from converter.ca_AstroPh_converter import read_ca_AstroPh
from converter.email_EUAll_converter import read_email_EUAll
from converter.facebook_converter import read_facebook
from converter.AS_converter import read_AS

from converter.graph_converter_house_committees import read_US_house
from converter.graph_converter_senate_committees import read_US_senate
from converter.graph_converter_house_bills import read_US_house_bills
from converter.graph_converter_senate_bills import read_US_senate_bills
from converter.graph_converter_cat_cooking import read_cat_cooking
from converter.graph_converter_contact_high_school import read_contact_high_school
from converter.graph_converter_contact_primary_school import read_contact_primary_school
from converter.graph_converter_mathoverflow import read_mathoverflow
from converter.graph_converter_trivago_clicks import read_trivago_clicks
from converter.graph_converter_walmart_trips import read_walmart_trips

from classes import *
import tracemalloc


def create_node_edge_incidence_dict(rule):
    """Returns a dir. At index i, it contains a dict mapping an IncidenceType to its frequency at the node i"""
    # Simply loop over all edges and all nodes an build the mapping of nodes to IncidenceTypes.
    node_edge_incidence_dict = {}
    for edge in rule:
        for connection_type in range(edge.rank()):
            incidence_type = IncidenceType(edge.get_label(), connection_type)
            node = edge[connection_type]
            # Update process. Used to generate objects if they are not available.
            if node in node_edge_incidence_dict:
                incidence_frequency_dir = node_edge_incidence_dict[node]
                if incidence_type in incidence_frequency_dir:
                    incidence_frequency_dir[incidence_type] += 1
                else:
                    incidence_frequency_dir[incidence_type] = 1
            else:
                node_edge_incidence_dict[node] = {incidence_type: 1}
    return node_edge_incidence_dict

def count_digrams(node_edge_incidence_dict):
    """Returns a dictionary mapping digrams to their occurrence-frequency (ideally) """
    digram_count = {}
    for node in node_edge_incidence_dict.keys():
        incidence_type_dict = node_edge_incidence_dict[node]
        keys = list(incidence_type_dict.keys())
        incidence_type_count = len(keys)
        # consider each pair of IncidenceTypes at the given node as a digram.
        # Note, that digrams should have no oder of IncidenceTypes.
        for i in range(incidence_type_count):
            for j in range(i+1, incidence_type_count):
                _update_digram_count(digram_count, Digram(keys[i], keys[j]), min(incidence_type_dict[keys[i]], incidence_type_dict[keys[j]]))
            # consider each self-pair as well. Note: it has an other way of counting.
            _update_digram_count(digram_count, Digram(keys[i], keys[i]), incidence_type_dict[keys[i]] // 2)
    return digram_count

def _update_digram_count(digram_count, digram, delta):
    """Updates the entry digram of digram_count by delta. If the entry of digram would be <= 0, the entry is removed."""
    inverted_digram = digram.invert()
    if digram in digram_count:
        digram_count[digram] += delta
        if digram_count[digram] <= 0:
            del digram_count[digram]
    elif inverted_digram in digram_count:
        digram_count[inverted_digram] += delta
        if digram_count[inverted_digram] <= 0:
            del digram_count[inverted_digram]
    elif delta > 0:
        digram_count[digram] = delta

def find_occurrence_of_digram(digram_to_replace, start_rule, last_state=None):
    """Searches the next occurrence of a digram within the start_rule
    Returns 2 indices pointing to the edges in the start_rule. The edges are sorted as they fit to the digram-order

    Note that i is returned as index within the current_state_object.
    We have to continue searching, because we replace two edges with one, so all indices are shifted to the left"""
    if last_state is None:
        current_state, start = {}, 0
    else:
        current_state, start = last_state

    # search loop. Remembers a start point to continue searching.
    for i in range(start, len(start_rule)):
        edge = start_rule[i]
        # Check, which type of digram is searched.
        if digram_to_replace[0] != digram_to_replace[1]:
            # check both types of the digram
            for j in (0, 1):
                if edge.get_label() == digram_to_replace[j].get_label():
                    connection_type = digram_to_replace[j].get_connection_type()
                    if connection_type >= edge.rank():
                        continue
                    node = edge[connection_type]
                    incidence_type = digram_to_replace[j]
                    incidence_type_2 = digram_to_replace[1-j]
                    if node not in current_state:
                        # Case: No edge belonging to this node found for this Digram
                        current_state[node] = {incidence_type: [i]}
                    elif incidence_type in current_state[node] and len(current_state[node].keys()) == 1:
                        # Case: only found an edge matching to the same incidence_type as already found.
                        current_state[node][incidence_type].append(i)
                    elif incidence_type_2 in current_state[node] and len(current_state[node].keys()) == 1 and current_state[node][incidence_type_2] == [i]:
                        # Case: found first matching edge, its a loop, so save it as both options.
                        current_state[node][incidence_type] = [i]
                    else:
                        # Case: found two edges, who form an occurrence of the digram

                        # delete Edge i from both lists of incidence types, because it could be an edge.
                        if incidence_type in current_state[node] and i in current_state[node][incidence_type]:
                            del current_state[node][incidence_type][current_state[node][incidence_type].index(i)]
                        if i in current_state[node][incidence_type_2]:
                            del current_state[node][incidence_type_2][current_state[node][incidence_type_2].index(i)]

                        # get the other edge and removes it from that list
                        edge_1 = current_state[node][incidence_type_2].pop(0)

                        # removes it from this list to prevent loops still be listed.
                        # Should be included within the following lines, so the next two are not needed.
                        # if incidence_type in current_state[node] and edge_1 in current_state[node][incidence_type]:
                        #     del current_state[node][incidence_type][current_state[node][incidence_type].index(edge_1)]

                        # remove both edges from the list of other nodes
                        # cascading if's in the case, higher objects need to be deleted as well.
                        connection_type_2 = incidence_type_2.get_connection_type()
                        if edge.get_label() == incidence_type_2.get_label() and connection_type_2 < edge.rank():
                            other_node = edge[connection_type_2]
                            if other_node in current_state and incidence_type_2 in current_state[other_node] and i in current_state[other_node][incidence_type_2]:
                                del current_state[other_node][incidence_type_2][current_state[other_node][incidence_type_2].index(i)]
                                if len(current_state[other_node][incidence_type_2]) == 0:
                                    del current_state[other_node][incidence_type_2]
                                    if len(current_state[other_node]) == 0:
                                        del current_state[other_node]
                        if start_rule[edge_1].get_label() == incidence_type.get_label() and connection_type < start_rule[edge_1].rank():
                            other_node = start_rule[edge_1][connection_type]
                            if other_node in current_state and edge_1 in current_state[other_node][incidence_type]:
                                del current_state[other_node][incidence_type][current_state[other_node][incidence_type].index(edge_1)]
                                if len(current_state[other_node][incidence_type]) == 0:
                                    del current_state[other_node][incidence_type]
                                    if len(current_state[other_node]) == 0:
                                        del current_state[other_node]

                        # remove dicts, if they are not used anymore
                        if incidence_type in current_state[node] and len(current_state[node][incidence_type]) == 0:
                            del current_state[node][incidence_type]
                        if len(current_state[node][incidence_type_2]) == 0:
                            del current_state[node][incidence_type_2]
                        if len(current_state[node].keys()) == 0:
                            del current_state[node]

                        # Return edges in order of the Digram
                        if j == 0:
                            return (i, edge_1), (current_state, i)
                        else:
                            return (edge_1, i), (current_state, i)
        else:
            if edge.get_label() == digram_to_replace[0].get_label():
                incidence_type = digram_to_replace[0]
                connection_type = incidence_type.get_connection_type()
                node = edge[connection_type]
                if node not in current_state:
                    # Case: No edge belonging to this node found for this Digram
                    current_state[node] = i
                else:
                    # Case: found two edges, who form an occurrence of the digram
                    edge_1 = current_state[node]
                    # remove, edge will be replaced
                    del current_state[node]
                    return (edge_1, i), (current_state, i)
    # No further occurrence found, return None for both, occurrence an current state.
    return None, None

def update_digram_count(old_edges, new_edge, node_edge_incidence_dict, digram_count):
    """Updates node_edge_incidence_dict und digram_count"""
    # Do the update for each edge.
    for edge in old_edges:
        for connection_type in range(edge.rank()):
            incidence_type = IncidenceType(edge.get_label(), connection_type)
            node = edge[connection_type]
            incidence_frequency_dir = node_edge_incidence_dict[node]

            # Update the count of Digrams
            for incidence_type_2 in incidence_frequency_dir:
                if (not incidence_type == incidence_type_2) and incidence_frequency_dir[incidence_type] <= incidence_frequency_dir[incidence_type_2]:
                    _update_digram_count(digram_count, Digram(incidence_type, incidence_type_2), -1)

            if incidence_frequency_dir[incidence_type] % 2 == 0:
                _update_digram_count(digram_count, Digram(incidence_type, incidence_type), -1)

            # Reduce the incidence_type in the dict by 1.
            if incidence_type in incidence_frequency_dir:
                incidence_frequency_dir[incidence_type] -= 1
                if incidence_frequency_dir[incidence_type] == 0:
                    del incidence_frequency_dir[incidence_type]

    # Do it for the new edge as well.
    for connection_type in range(new_edge.rank()):
        incidence_type = IncidenceType(new_edge.get_label(), connection_type)
        node = new_edge[connection_type]
        if node in node_edge_incidence_dict:
            incidence_frequency_dir = node_edge_incidence_dict[node]
        else:
            incidence_frequency_dir = {}

        # Add the incidence_type in the dict by 1 for the new edge.
        if incidence_type not in incidence_frequency_dir:
            incidence_frequency_dir[incidence_type] = 1
        else:
            incidence_frequency_dir[incidence_type] += 1
        node_edge_incidence_dict[node] = incidence_frequency_dir

        # Update the count of digrams
        for incidence_type_2 in incidence_frequency_dir:
            if (not incidence_type == incidence_type_2) and incidence_frequency_dir[incidence_type] <= incidence_frequency_dir[incidence_type_2]:
                _update_digram_count(digram_count, Digram(incidence_type, incidence_type_2), +1)
        if incidence_frequency_dir[incidence_type] % 2 == 0:
            _update_digram_count(digram_count, Digram(incidence_type, incidence_type), +1)




def replace_digrams(grammar, start_rule):
    node_edge_incidence_dict = create_node_edge_incidence_dict(grammar.get_start_rule().edges)
    digram_count = count_digrams(node_edge_incidence_dict)
    digram_to_replace = max(digram_count, key=digram_count.get)

    while digram_count[digram_to_replace] > 2:
        count_real_replacements = 0

        occurrence, cur_state = find_occurrence_of_digram(digram_to_replace, start_rule)
        print(
            'Try to replace ' + str(digram_to_replace) + ' with a frequency of ' + str(digram_count[digram_to_replace]))
        new_rule = Rule(digram_to_replace, grammar)
        while occurrence is not None:
            old_edges = [start_rule[i] for i in occurrence]
            new_edge = new_rule.get_new_edge(old_edges)
            # edge replacement
            # used min(...)/max(...) to keep as much ids of rules where they were.
            start_rule[min(occurrence[0], occurrence[1])] = new_edge
            del start_rule[max(occurrence[0], occurrence[1])]
            count_real_replacements += 1

            update_digram_count(old_edges, new_edge, node_edge_incidence_dict, digram_count)
            occurrence, cur_state = find_occurrence_of_digram(digram_to_replace, start_rule, cur_state)

        if count_real_replacements != 0:
            grammar.add_rule(new_rule.get_name(), new_rule)
        if digram_to_replace in digram_count:
            del digram_count[digram_to_replace]
        digram_to_replace = max(digram_count, key=digram_count.get)

        print('Real Replacements: ' + str(count_real_replacements))
        #current, peak = tracemalloc.get_traced_memory()
        #print(f"Aktuell: {current / 1024 ** 2:.2f} MB; Peak: {peak / 1024 ** 2:.2f} MB")
        print('The total size of the uncompressed grammar is {}'.format(grammar.size_of_grammar()))
        print('---------------------------------------------------------------------')

def count_usage_in_startrule(grammar):
    usage_in_start = {}
    for edge in grammar.get_start_rule():
        if edge.get_label() in usage_in_start:
            usage_in_start[edge.get_label()] += 1
        else:
            usage_in_start[edge.get_label()] = 1
    return usage_in_start

def count_usage_in_rules(grammar, rules):
    usage_in_rules = {}
    for rulename in rules:
        rule = grammar.rules[rulename]
        first_label = rule.first.get_label()
        second_label = rule.second.get_label()
        if first_label in usage_in_rules:
            usage_in_rules[first_label] += 1
        else:
            usage_in_rules[first_label] = 1
        if second_label in usage_in_rules:
            usage_in_rules[second_label] += 1
        else:
            usage_in_rules[second_label] = 1

    return usage_in_rules

def prune_grammar(grammar):
    print('Start pruning the grammar')
    print('---------------------------------------------------------------------')
    # get all rules top-down except the start rule
    rules = list(grammar.rules.keys())[1:]

    # count the usage of each rule in the start rule
    usage_in_start = count_usage_in_startrule(grammar)
    # count the usage of each rule in the other rules
    usage_in_rules = count_usage_in_rules(grammar, rules)

    for rule in rules:
        if (rule not in usage_in_rules or usage_in_rules[rule] == 1) and rule not in usage_in_start:
            old_rule = grammar.rules[rule]

            rulename, place, connection_type = grammar.find_rule_usage(rule, rules)
            del grammar.rules[rule]
            rule_to_change = grammar.rules[rulename]
            pruned_Rule = PrunedRule(connection_type, old_rule)
            if place == 0:
                rule_to_change.first = pruned_Rule
            elif place == 1:
                rule_to_change.second = pruned_Rule
            print('Rule {} was pruned'.format(rule))
            print('The total size of the uncompressed grammar is {}'.format(grammar.size_of_grammar()))
            print('---------------------------------------------------------------------')

    print('The total size is {} of the pruned grammar'.format(grammar.size_of_grammar()))
    print('---------------------------------------------------------------------')


def decompress_grammar(grammar):

    def rearrange_nodes(nodes, position):
        """Rearranges the nodes such that the node at position 0 is the node at position and the node at position is the node at 0."""
        return nodes[1:position + 1] + tuple([nodes[0]]) + nodes[position + 1:]

    def decompress_edge(to_decompress, nodes, grammar):
        if isinstance(to_decompress, PrunedRule):
            first_incidence_type = to_decompress.get_rule().get_first()
            second_incidence_type = to_decompress.get_rule().get_second()
            nodes_of_first = to_decompress.get_rule().get_nodes_for_first()
        else:
            rulelabel = to_decompress.get_label()
            nodes_of_first = grammar.rules[rulelabel].get_nodes_for_first()
            first_incidence_type = grammar.rules[rulelabel].get_first()
            second_incidence_type = grammar.rules[rulelabel].get_second()

        first_nodes = nodes[:nodes_of_first]
        second_nodes = tuple([nodes[0]]) + nodes[nodes_of_first:]

        new_edges = []

        first_nodes = rearrange_nodes(first_nodes, first_incidence_type.get_connection_type())
        second_nodes = rearrange_nodes(second_nodes, second_incidence_type.get_connection_type())

        if isinstance(first_incidence_type, PrunedRule) or first_incidence_type.get_label() in grammar.rules:
            new_edges.extend(decompress_edge(first_incidence_type, first_nodes, grammar))
        else:
            # the incidence type is a normal edge, so create it.
            new_edges.append(Edge(first_incidence_type.get_label(), *first_nodes))

        if isinstance(second_incidence_type, PrunedRule) or second_incidence_type.get_label() in grammar.rules:
            new_edges.extend(decompress_edge(second_incidence_type, second_nodes, grammar))
        else:
            # the incidence type is a normal edge, so create it.
            new_edges.append(Edge(second_incidence_type.get_label(), *second_nodes))

        return new_edges

    graph = Graph()

    for edge in grammar.get_start_rule():
        # Check if the edge is a rule, otherwise skip it.
        if edge.get_label() not in grammar.rules:
            new_edges = [edge]
        else:
            new_edges = decompress_edge(edge, edge.nodes, grammar)

        graph.edges.extend(new_edges)

    print('Decompressing completed')
    print('----------------------------------------------------------------------')
    return graph


def repair(grammar):
    print('The total size of the uncompressed grammar is {}'.format(grammar.size_of_grammar()))
    print('---------------------------------------------------------------------')
    start_rule = grammar.get_start_rule()

    replace_digrams(grammar, start_rule)

    prune_grammar(grammar)

    print('The total size of the compressed grammar is {}'.format(grammar.size_of_grammar()))

    return grammar

#tracemalloc.start()

#grammar = read_email_eu_core()
#grammar = read_wiki_vote()
#grammar = read_gnutella04()
#grammar = read_gnutella31()
#grammar = read_cit_HepPh()
#grammar = read_ca_AstroPh()
#grammar = read_email_EUAll()
#grammar = read_facebook()
grammar = read_AS()

#grammar = read_US_house()
#grammar = read_US_senate()
#grammar = read_US_house_bills()
#grammar = read_US_senate_bills()
#grammar = read_cat_cooking()
#grammar = read_contact_high_school()
#grammar = read_contact_primary_school()
#grammar = read_mathoverflow()
#grammar = read_trivago_clicks()
#grammar = read_walmart_trips()

#start = time.perf_counter()
grammar  = repair(grammar)
#end = time.perf_counter()
#print(f"Dauer: {end - start:.6f} Sekunden")

graph = decompress_grammar(grammar)

print('Was the Decompression successful:', read_AS().get_start_rule() == graph)

#tracemalloc.stop()



