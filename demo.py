#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Justin Zhu

import os
import argparse
from tree_sitter import Language, Parser

DEBUG = False
PY_LANGUAGE = Language('build/my-languages.so', 'python')
LINEIDX = 0
CHARIDX = 1

libraries = {}


def getcode(filename):
    if DEBUG:
        with open('samplecode.py', "r") as f:
            code = f.read() 
    else:
        with open(filename, "r") as f:
            code = f.read() 
    return code


def gettree(filename):
    code = getcode(filename)
    parser = Parser()
    parser.set_language(PY_LANGUAGE)
    tree = parser.parse(bytes(code, "utf8"))
    if DEBUG:
        help(parser.parse)
        print(code)
    return tree


def getlibraries(filename):
    code = getcode(filename)
    tree = gettree(filename)
    root_node = tree.root_node
    if DEBUG:
        print(root_node.sexp())
        dir(root_node)
        dir(tree)
    root_node.end_byte
    root_node.start_byte

    if DEBUG:
        for i in libraries:
            print(i)
            # print(dir(c))
            break

    # root_node.start_point
    # root_node.end_point
    # dir(tree)
    lines = code.split('\n')

    for c in root_node.children:
        if c.type == "import_statement" or c.type == "import_from_statement":
            # print(c.start_point)
            # print(c.end_point)
            sl = c.start_point[LINEIDX]
            sc = c.start_point[CHARIDX]
            el = c.end_point[LINEIDX]
            ec = c.end_point[CHARIDX]
            # print(lines[el][sc:ec])
            line = (lines[el][sc:ec])
            line = line.split()
            importline = line[1]
            # print(importline)
            if filename not in libraries:
                libraries[filename] = []
                homedir = '.'.join(filename.split('/')[:-1])
                if '.' in homedir:
                    importline = homedir+'.'+importline
            libraries[filename].append(importline)

    return libraries


def package2file(directory, package):
    library = '/'.join(package.split('.'))
    suffix = '.py'
    path = os.path.join(library + suffix)
    return path


def file2package(directory, filename):
    homedir = '.'.join(directory.split('/')[:-1])
    package = filename.split('.')[0]
    if '.' in homedir:
        package = homedir+'.'+package
    return package



def recurse(filename, directory, identifier):
    path = os.path.join(directory, filename)
    libraries = getlibraries(path)
    print("Latest library")
    print(libraries)
    print(identifier)
    print("FN")
    print(filename)
    key = package2file(directory, identifier)
    print(key)
    # library = '/'.join(identifier.split('.'))
    # suffix = '.py'
    # path = os.path.join(directory, library + suffix)
    if key in libraries:
        for l in libraries[key]:
            print('Loopy')
            print(l)
            library = '/'.join(l.split('.'))
            suffix = '.py'
            path = os.path.join(directory, library + suffix)
            # print("Path")
            # print(path)
            if os.path.isfile(path):
                print("path exists")
                print(path)
                directory, filename = os.path.split(path)
                # print("dir"+directory)
                # print("file"+filename)
                libraries = recurse(filename, directory, l)
    return libraries


argparser = argparse.ArgumentParser(description='Get Dependency Graphs')
argparser.add_argument('filename')
# os.path.dirname()
args = argparser.parse_args()

homedirectory, filename = os.path.split(args.filename)
if not homedirectory:
    print("DIRECTORY is NONE")
# print('directory')
# print(directory)
# print(args.filename)
# print(type(args.filename))

# libraries = getlibraries(args.filename)
# print("Function works?")
# print(libraries)

package = filename.split('.')[0]
recurse(filename, homedirectory, package)
print("Recurse Function works?")
print(libraries)


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
