
import random
import networkx as nx
import matplotlib.pyplot as plt
import json

''''''


class TernarySearchTree:
    root_node = None

    class TSTNode:
        def __init__(self, value):
            self.value = value
            self.right_node = None
            self.left_node = None
            self.middle_node = None
            self.is_terminal = False

    def __init__(self):
        self.root_node = None

    def create_node(self, value):
        # Create a new node with the given value
        node = self.TSTNode(value)
        return node

    def insert(self, string):
        # Start the recursive insertion from the root node
        self.root_node = self._insert_recursive(self.root_node, string, 0)

    def _insert_recursive(self, node, string, position):
        # If current node is None, create a new node with the current character
        if node is None:
            node = self.create_node(string[position])

        # If the current character is smaller than the node's value,
        # go to the left subtree
        if string[position] < node.value:
            node.left_node = self._insert_recursive(
                node.left_node, string, position)

        # If the current character is greater than the node's value,
        # go to the right subtree
        elif string[position] > node.value:
            node.right_node = self._insert_recursive(
                node.right_node, string, position)

        # If last character of string is reached set the is_terminal flag
        # to True for the last character of the string
        elif position == len(string) - 1:
            node.is_terminal = True

        # If the current character is equal to the node's value, go to middle subtree
        else:
            node.middle_node = self._insert_recursive(
                node.middle_node, string, position + 1)

        # Return modified node
        return node

    def search(self, string, exact=False):
        # If exact is True, perform an exact search starting from the root node
        if exact:
            return self._search(self.root_node, string, 0)
         # If exact is False, perform a prefix search starting from the root node
        else:
            return self._prefix_search(self.root_node, string, 0)

    def _search(self, node, string, position):
        # If the current node is None, the string does not exist in the tree, return False
        # If current position does not exist in string, return False
        if node is None or position > len(string) - 1:
            return False

        # If the current character is smaller than the node's value, search in
        # the left subtree
        if string[position] < node.value:
            return self._search(node.left_node, string, position)
        # If the current character is greater than the node's value, search in
        #  the right subtree
        if string[position] > node.value:
            return self._search(node.right_node, string, position)
        # If we reach the last character of the string and the node is marked
        # as terminal and same as current node value, the string is found
        if position == len(string) - 1 and node.is_terminal and node.value == string[position]:
            return True
        # Otherwise, current character is equal to the node's value,
        # continue searching in the middle subtree for the next character
        return self._search(node.middle_node, string, position + 1)

    def _prefix_search(self, node, prefix, position):
        # If the current node is None, the prefix string does not exist in the tree
        if node is None:
            return False
        # print(node.value,prefix[position])

        # If the prefix string is an empty string, return all the strings in
        # the tree
        if prefix == "":
            return self.get_all_strings()

        # If the current character is smaller than the node's value, search in
        # the left subtree
        if prefix[position] < node.value:
            return self._prefix_search(node.left_node, prefix, position)

        # If the current character is greater than the node's value, search in
        # the right subtree
        elif prefix[position] > node.value:
            return self._prefix_search(node.right_node, prefix, position)

        # If we reach the last character of the prefix string and it matches
        # the node's value, the prefix string is found
        elif position == len(prefix) - 1 and node.value == prefix[position]:
            return True

        # Otherwise, the current character of the prefix string and it matches
        # the node's current value match but has not reached the last character,
        # continue searching in the middle subtree for the next character
        else:
            return self._prefix_search(node.middle_node, prefix, position + 1)

    def all_strings(self):
        return self._all_strings(self.root_node)

    def _all_strings(self, node, prefix="", strings=None):
        # If strings is not provided, initialize an empty list
        if strings is None:
            strings = []

        # If the current node is None, return the collected strings
        if node is None:
            return strings

        # If the current node is a terminal node (end of a word), append
        # the prefix together with the node value to the strings list
        if node.is_terminal:
            strings.append(prefix + node.value)

        # Recursively traverse the left subtree, keeping the prefix unchanged
        strings = self._all_strings(node.left_node, prefix, strings)
        # Recursively traverse the middle subtree, updating the prefix by
        # adding the current node value
        strings = self._all_strings(
            node.middle_node, prefix + node.value, strings)
        # Recursively traverse the right subtree, keeping the prefix unchanged
        strings = self._all_strings(node.right_node, prefix, strings)

        return strings

    def __len__(self):
        return self.count_strings()

    def count_strings(self):
        return self._count_strings(self.root_node)

    def _count_strings(self, node):
        # If the current node is None, there are no node to find terminal,
        # so return 0
        if node is None:
            return 0

        count = 0

        # If the current node is a terminal node (end of a string),
        # increment the count by 1
        if node.is_terminal:
            count += 1

        # Recursively count the number of terminal nodes in the left subtree
        count += self._count_strings(node.left_node)
        # Recursively count the number of terminal nodes in the middle subtree
        count += self._count_strings(node.middle_node)
        # Recursively count the number of terminal nodes in the right subtree
        count += self._count_strings(node.right_node)

        return count

    def __str__(self):
        return self.print_tree()

    def print_tree(self):
        return self._print_tree(self.root_node, "")

    def _print_tree(self, node, parent=None, prefix=""):
        # If the current node is None, return an empty string
        if node is None:
            return ""

        result = ""

        # Add indentation based on the prefix and show a visual
        # representation of the tree structure
        result += " " * len(prefix)
        if parent is not None:
            result += "└─"

        # Add the current node's value and terminating status to the
        # result string
        result += f"char: {node.value}, terminates: {node.is_terminal}\n"

        # Recursively call _print_tree on the left, middle, and right subtrees,
        # updating the prefix to create the tree structure representation
        result += self._print_tree(node.left_node, node, prefix + "  │")
        result += self._print_tree(node.middle_node, node, prefix + "  ├─")
        result += self._print_tree(node.right_node, node, prefix + "  └─")

        return result

    def plot_tree(self):
        G = nx.Graph()
        labels = {}
        visited = set()
        self._plot_tree(self.root_node, G, labels, visited=visited)

        # Adjust the width and height as needed
        fig, ax = plt.subplots(figsize=(8, 6))
        pos = nx.nx_pydot.graphviz_layout(G, prog='dot')
        nx.draw_networkx(G, pos, with_labels=True, labels=labels, node_size=500, node_color='lightblue',
                         font_weight='bold', font_size=12, edge_color='gray', ax=ax)

        plt.show()

    def _plot_tree(self, node, G, labels, visited):
        # If the current node is None, return to escape recursive call
        if node is None:
            return

        # Get the unique ID of the node
        node_id = id(node)

        # If the node has already been visited, return to escape recursive call
        if node_id in visited:
            return

        # Add the node to the graph and provide its label as the node's value
        visited.add(node_id)
        G.add_node(node_id)
        labels[node_id] = node.value

        # Recursively process and plot the left, middle, and right subtrees
        if node.left_node is not None:
            left_id = id(node.left_node)
            G.add_edge(node_id, left_id)
            self._plot_tree(node.left_node, G, labels, visited)

        if node.middle_node is not None:
            middle_id = id(node.middle_node)
            G.add_edge(node_id, middle_id)
            self._plot_tree(node.middle_node, G, labels, visited)

        if node.right_node is not None:
            right_id = id(node.right_node)
            G.add_edge(node_id, right_id)
            self._plot_tree(node.right_node, G, labels, visited)

    def visualize_tree(self):
        # Use the plot_tree method to generate and display the tree visualization
        self.plot_tree()
