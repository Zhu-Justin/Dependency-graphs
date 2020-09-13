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
directory, filename = os.path.split(args.filename)
print('directory')
print(directory)
print(args.filename)
print(type(args.filename))

with open(args.filename, "r") as f:
# with open('samplecode.py', "r") as f:
    code = f.read() 

parser = Parser()
parser.set_language(PY_LANGUAGE)
tree = parser.parse(bytes(code, "utf8"))
root_node = tree.root_node
# help(parser.parse)


# print(code)
# print(root_node.sexp())

dir(root_node)
dir(tree)
root_node.end_byte
root_node.start_byte
libraries = {}
libraries[args.filename] = []
        # for i in line:
        #     print(libraries)


    # print(dir(c))
    # break
    # if c.kind

root_node.start_point
root_node.end_point

dir(tree)
lines = code.split('\n')
LINEIDX=0
CHARIDX=1

for c in root_node.children:
    if c.type == "import_statement" or c.type == "import_from_statement":
        # print(c.start_point)
        # print(c.end_point)
        sl=c.start_point[LINEIDX]
        sc=c.start_point[CHARIDX]
        el=c.end_point[LINEIDX]
        ec=c.end_point[CHARIDX]
        # print(lines[el][sc:ec])
        line = (lines[el][sc:ec])
        line = line.split()
        importline = line[1]
        # print(importline)
        libraries[args.filename].append(importline)

print(libraries)


for l in libraries[args.filename]:
    library = '/'.join(l.split('.'))
    suffix = '.py'
    library = os.path.join(directory, library + suffix)
    if os.path.isfile(library):
        print(library)


# sl=root_node.start_point[LINEIDX]
# sc=root_node.start_point[CHARIDX]
# el=root_node.end_point[LINEIDX]
# ec=root_node.end_point[CHARIDX]

# root_node.walk()
# root_node.start_point[LINEIDX]

# lines[sl:el]
# sc
# ec

# code[root_node.start_point:root_node.end_point]

# cursor = tree.walk()
# dir(cursor)

# assert cursor.node.type == 'module'

# # (module (comment) (comment) (comment) (import_statement name: (aliased_import name: (dotted_name (identifier)) alias: (identifier))) (import_statement name: (aliased_import name: (dotted_name (identifier)) alias: (identifier))) (import_from_statement module_name: (dotted_name (identifier)) name: (dotted_name (identifier))) (expression_statement (binary_operator left: (integer) right: (integer))) (import_statement name: (dotted_name (identifier))) (expression_statement (call function: (identifier) arguments: (argument_list (string)))))
# # (module (comment) (comment) (comment) (import_statement name: (aliased_import name: (dotted_name (identifier)) alias: (identifier))) (import_statement name: (aliased_import name: (dotted_name (identifier)) alias: (identifier))) (import_from_statement module_name: (dotted_name (identifier)) name: (dotted_name (identifier))) (expression_statement (binary_operator left: (integer) right: (integer))) (import_statement name: (dotted_name (identifier))) (expression_statement (call function: (identifier) arguments: (argument_list (string)))))

# (import_statement name: (aliased_import name: (dotted_name (identifier)) alias: (identifier)))

# query = PY_LANGUAGE.query(""" (import_statement name: (aliased_import name: (dotted_name (identifier)) alias: (identifier)))""")

#                           # (import_statement name:
# # (function_definition
#   # name: (identifier) @function.def)

# # (call
#   # function: (identifier) @function.call)
# # """)

# captures = query.captures(tree.root_node)
# assert len(captures) == 2
# assert captures[0][0] == function_name_node
# assert captures[0][1] == "function.def"

# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')


# print(args.accumulate(args.integers))
