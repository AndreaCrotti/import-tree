import argparse
import sys

from inspect import stack, getmodulename
from os import path

from pygraphviz import Edge, AGraph


class ImportGraph(object):
    """
    Loader object
    """

    def __init__(self):
        self.tree = AGraph(directed=True)

    def find_module(self, module_name, package=None):
        caller_mod = getmodulename(stack()[1][1])
        if getmodulename(__file__) != caller_mod:
            print("adding {0}".format(str([caller_mod, module_name])))
            self.tree.add_edge(unicode(caller_mod), unicode(module_name))

    def write_graph(self, output):
        output = output + '.png'
        print("writing to {0}".format(output))
        self.tree.draw(output, format='png', prog='dot')


def parse_arguments():
    parser = argparse.ArgumentParser(description='generate the tree of imports')

    parser.add_argument('module',
                        help='entry point module')

    return parser.parse_args()

def main():
    ns = parse_arguments()
    sys.path.append(path.dirname(ns.module))

    im = ImportGraph()
    sys.meta_path.append(im)
    __import__(path.splitext(ns.module)[0])
    sys.meta_path.remove(im)
    im.write_graph(ns.module)

if __name__ == '__main__':
    main()