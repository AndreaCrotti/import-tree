__metaclass__ = type

import __builtin__

import argparse
import sys

from inspect import stack, getmodulename
from os import path

from pygraphviz import AGraph

def get_caller_mod():
    return getmodulename(stack()[1][1])


class Grapher:
    def __init__(self):
        self.tree = AGraph(directed=True)

    def add_edge(self, a, b):
        self.tree.add_edge(a, b)

    def write(self, output):
        #TODO: pdf seems to handle better big size
        output = output + '.png'
        print("writing to {0}".format(output))
        self.tree.draw(output, format='png', prog='dot')


class ImportGraph:

    def __init__(self, full):
        self.full = full
        self.graph = Grapher()

    def find_module(self, module_name, package=None):
        caller_mod = get_caller_mod()
        if getmodulename(__file__) != caller_mod:
            print("adding {0}".format(str([caller_mod, module_name])))
            self.graph.add_edge(caller_mod, module_name)


    def write_graph(self, output):
        self.graph.write(output)

class ImportMock:

    def __init__(self):
        self.graph = Grapher()

    def _my_import(self, *args, **kwargs):
        self.graph.add_edge(get_caller_mod(), args[0])
        self.orig(*args, **kwargs)

    def __enter__(self):
        self.orig = __builtin__.__import__
        __builtin__.__import__ = self._my_import
        return self

    def __exit__(self, type, value, traceback):
        __builtin__.__import__ = self.orig
        self.graph.write("x.png")


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
    module = path.splitext(ns.module)[0]
    sys.path.append(path.dirname(ns.module))
    
    if ns.full:
        with ImportMock() as i:
            __import__(module)
    else:
        im = ImportGraph(full=ns.full)
        sys.meta_path.append(im)
        __import__(module)
        sys.meta_path.remove(im)
        im.write_graph(ns.module)
