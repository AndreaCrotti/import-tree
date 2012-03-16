import argparse
import sys

from imp import load_module, find_module
from inspect import stack, getmodulename
from os import path

from pygraphviz import Edge, AGraph


class ImportGraph(object):

    def __init__(self, full):
        self.tree = AGraph(directed=True)
        self.full = full

    def find_module(self, module_name, package=None):
        caller_mod = getmodulename(stack()[1][1])
        if getmodulename(__file__) != caller_mod:
            print("adding {0}".format(str([caller_mod, module_name])))
            self.tree.add_edge(caller_mod, module_name)


    def write_graph(self, output):
        output = output + '.png'
        print("writing to {0}".format(output))
        self.tree.draw(output, format='png', prog='dot')


def parse_arguments():
    parser = argparse.ArgumentParser(description='generate the tree of imports')

    parser.add_argument('module',
                        help='entry point module')

    parser.add_argument('-f', '--full',
                        action='store_true',
                        help='clear sys.modules every time, showing the entire graph')


    return parser.parse_args()

def main():
    ns = parse_arguments()
    sys.path.append(path.dirname(ns.module))

    im = ImportGraph(full=ns.full)
    sys.meta_path.append(im)
    __import__(path.splitext(ns.module)[0])
    sys.meta_path.remove(im)
    im.write_graph(ns.module)
