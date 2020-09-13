#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Justin Zhu

import os
import argparse
from tree_sitter import Language, Parser
import serenadecore as sc


argparser = argparse.ArgumentParser(description='Get Dependency Graphs')
argparser.add_argument('filename')
args = argparser.parse_args()

homedirectory, filename = os.path.split(args.filename)
# if not homedirectory:
#     print("DIRECTORY is NONE")

# print('directory')
# print(directory)
# print(args.filename)
# print(type(args.filename))

# libraries = getlibraries(args.filename)
# print("Function works?")
# print(libraries)

package = filename.split('.')[0]
libraries = sc.recurse(filename, homedirectory, package)
print("Recurse Function works?")
print(libraries)
functionmaps = sc.getfunctions(filename, homedirectory)
print(functionmaps)

# os.path.dirname()

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
