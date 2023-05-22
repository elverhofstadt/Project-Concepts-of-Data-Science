
import random
import networkx as nx
import matplotlib.pyplot as plt
import json


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
        node = self.TSTNode(value)
        return node

    def insert(self, string):
        self.root_node = self._insert_recursive(self.root_node, string, 0)

    def _insert_recursive(self, node, string, position):
        if node is None:
            node = self.create_node(string[position])

        if string[position] < node.value:
            node.left_node = self._insert_recursive(node.left_node, string, position)
        elif string[position] > node.value:
            node.right_node = self._insert_recursive(node.right_node, string, position)
        elif position == len(string) - 1:
            node.is_terminal = True
        else:
            node.middle_node = self._insert_recursive(node.middle_node, string, position + 1)

        return node

    def search(self, string, exact=False):
        if exact:
            return self._search(self.root_node, string, 0)
        else:
            return self._prefix_search(self.root_node, string, 0)

    # def search(self,string,exact):
    #     return self._prefix_search(self.root_node, string)

    def _search(self, node, string, position):
        if node is None:
            return False

        if string[position] < node.value:
            return self._search(node.left_node, string, position)
        if string[position] > node.value:
            return self._search(node.right_node, string, position)
        if position == len(string) - 1 and node.is_terminal:
            return True
        return self._search(node.middle_node, string, position + 1)

    def _prefix_search(self, node, prefix, position):
        if node is None:
            return False
        # print(node.value,prefix[position])
        if prefix == "":
            return self.get_all_strings()

        if prefix[position] < node.value:
            return self._prefix_search(node.left_node, prefix, position)

        elif prefix[position] > node.value:

            return self._prefix_search(node.right_node, prefix, position)

        elif position == len(prefix) - 1 and node.value == prefix[position]:
            return True

        else:
            return self._prefix_search(node.middle_node, prefix, position + 1)

    def all_strings(self):
        return self._all_strings(self.root_node)

    def _all_strings(self, node, prefix="", strings=None):
        if strings is None:
            strings = []

        if node is None:
            return strings

        if node.is_terminal:
            strings.append(prefix + node.value)

        strings = self._all_strings(node.left_node, prefix, strings)
        strings = self._all_strings(node.middle_node, prefix + node.value, strings)
        strings = self._all_strings(node.right_node, prefix, strings)

        return strings

    def __len__(self):
        return self.count_strings()

    def count_strings(self):
        return self._count_strings(self.root_node)

    def _count_strings(self, node):
        if node is None:
            return 0

        count = 0

        if node.is_terminal:
            count += 1

        count += self._count_strings(node.left_node)
        count += self._count_strings(node.middle_node)
        count += self._count_strings(node.right_node)

        return count

    def __str__(self):
        return self.print_tree()

    def print_tree(self):
        return self._print_tree(self.root_node, "")

    def _print_tree(self, node, parent=None, prefix=""):
        if node is None:
            return ""

        result = ""

        result += " " * len(prefix)
        if parent is not None:
            result += "└─"

        result += f"char: {node.value}, terminates: {node.is_terminal}\n"

        result += self._print_tree(node.left_node, node, prefix + "  │")
        result += self._print_tree(node.middle_node, node, prefix + "  ├─")
        result += self._print_tree(node.right_node, node, prefix + "  └─")

        return result

    def plot_tree(self):
        G = nx.Graph()
        labels = {}
        visited = set()
        self._plot_tree(self.root_node, G, labels, visited=visited)

        fig, ax = plt.subplots(figsize=(8, 6))  # Adjust the width and height as needed
        pos = nx.nx_pydot.graphviz_layout(G, prog='dot')
        nx.draw_networkx(G, pos, with_labels=True, labels=labels, node_size=500, node_color='lightblue',
                         font_weight='bold', font_size=12, edge_color='gray', ax=ax)

        plt.show()

    def _plot_tree(self, node, G, labels, visited):
        if node is None:
            return

        node_id = id(node)

        if node_id in visited:
            return

        visited.add(node_id)
        G.add_node(node_id)
        labels[node_id] = node.value

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
        self.plot_tree()