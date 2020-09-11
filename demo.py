#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Justin Zhu

import os
import argparse
from tree_sitter import Language, Parser

PY_LANGUAGE = Language('build/my-languages.so', 'python')

argparser = argparse.ArgumentParser(description='Get Dependency Graphs')
argparser.add_argument('filename')
# os.path.dirname()

args = argparser.parse_args()
print(args.filename)
with open(args.filename, "r") as f:
    code = f.read() 

parser = Parser()
parser.set_language(PY_LANGUAGE)
tree = parser.parse(bytes(code, "utf8"))
root_node = tree.root_node

# print(code)
print(root_node.sexp())


# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')


# print(args.accumulate(args.integers))
