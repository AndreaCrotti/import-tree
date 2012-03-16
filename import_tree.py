import argparse
from sys import meta_path

from pygraphviz import Edge, Node, AGraph


class ImportGraph(object):
    """
    Loader object
    """

    def __init__(self):
        self.tree = AGraph(directed=True)

    def find_module(self, module_name, package=None):
        print("requesting %s" % module_name)
        self.tree.add_node(ns.module_name)

    def write_graph(self, output):
        self.tree.draw(output+'.png', format='png')


def parse_arguments():
    parser = argparse.ArgumentParser(description='generate the tree of imports')

    parser.add_argument('module',
                        help='entry point module')

    return parser.parse_args()

def main():
    ns = parse_arguments()
    im = ImportGraph()
    meta_path.append(im)

    __import__(ns.module)
    meta_path.remove(im)
    im.write_graph(ns.module)

if __name__ == '__main__':
    main()
