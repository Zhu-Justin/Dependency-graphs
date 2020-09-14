#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Justin Zhu
# serenadecore -- core functions for graph dependency cli tool

import os
from tree_sitter import Language, Parser
from stdlib_list import stdlib_list

# Supports python3 for now
PY_LANGUAGE = Language('build/my-languages.so', 'python')

"""
LIBRARIES Contains all the packages imported from a file
i.e. LIBRARIES[file1] == [package1, package2, package3]
The packages can be imported in the following ways
import package1 (singular)
import package1, package2 (many)
from package1 import * (where * is any attribute from
package1)
import package1 as pk1 (aliasing)
"""
LIBRARIES = {}

"""
DICT Contains all the function inherited from that module
i.e. DICT[module] == [func1, func2, func3]
module.func1, module.func2, module.func3 have been called
in the file or any of its dependencies
"""
DICT = {}

"""
ALIAS Contains all the aliased packages mappings
i.e. ALIAS[alias] == [fullname]
ALIAS['np'] == 'numpy'
ALIAS['pandas'] == 'pd'
For now, this code will only work if there's one alias per package
Multiple aliasing will use the most recently alias, i.e. the
alias that is deepest from the root node in the dependency
graph, which may give some undefined behavior
"""
ALIAS = {}


def getcode(filename, DEBUG=False):
    """
    Get the python code as a string from file
    """

    if DEBUG:
        filename = 'samplecode.py'

    with open(filename, "r") as f:
        code = f.read() 
    return code


def gettree(filename, DEBUG=False):
    """
    Get the tree_sitter data from a file
    """
    code = getcode(filename)
    parser = Parser()
    parser.set_language(PY_LANGUAGE)
    tree = parser.parse(bytes(code, "utf8"))

    if DEBUG:
        help(parser.parse)
        print(code)

    return tree


def getalias(node, lines, filename, DEBUG=False):
    """
    Get alias mappings for a file
    """
    if node.type == "import_statement":

        if DEBUG:
            print(node)
            print(node.children)

        for c in node.children:
            if c.type == "dotted_name":
                cs, ce = c.start_point, c.end_point
                assert cs[0] == ce[0]
                cf = (lines[cs[0]][cs[1]:ce[1]])
                if filename not in LIBRARIES:
                    LIBRARIES[filename] = []
                if cf not in LIBRARIES[filename]:
                    LIBRARIES[filename].append(cf)
            if c.type == "aliased_import":
                for c1 in c.children:
                    if c1.type == "dotted_name":
                        cs, ce = c1.start_point, c1.end_point
                        assert cs[0] == ce[0]
                        cf = (lines[cs[0]][cs[1]:ce[1]])
                        p = cf
                        if filename not in LIBRARIES:
                            LIBRARIES[filename] = []
                        if cf not in LIBRARIES[filename]:
                            LIBRARIES[filename].append(cf)
                    if c1.type == "identifier":
                        cs, ce = c1.start_point, c1.end_point
                        assert cs[0] == ce[0]
                        cf = (lines[cs[0]][cs[1]:ce[1]])
                        ALIAS[cf] = p

    if node.type == "import_from_statement":

        if DEBUG:
            print(node)
            print(node.children)

        foundlib = False
        for c in node.children:
            if c.type == "import":
                foundlib = True
            if c.type == "dotted_name":
                cs, ce = c.start_point, c.end_point
                assert cs[0] == ce[0]
                cf = (lines[cs[0]][cs[1]:ce[1]])
                if not foundlib:
                    p1 = cf
                    if filename not in LIBRARIES:
                        LIBRARIES[filename] = []
                    if cf not in LIBRARIES[filename]:
                        LIBRARIES[filename].append(cf)
                else:
                    if p1 not in DICT:
                        DICT[p1] = []
                    if cf not in DICT[p1]:

                        if DEBUG:
                            print("ADDING " + cf + " in "+p1)
                            print(DICT)

                        DICT[p1].append(cf)
    if node.type == "module" or node.type == "expression_statement":
        
        if DEBUG:
            print("expression")
            print(node.children)

        for c in node.children:
            getalias(c, lines, filename)
    return ALIAS


def getlibraries(filename, DEBUG=False):
    """
    Get library mappings for a file
    """
    code = getcode(filename)
    lines = code.split('\n')
    tree = gettree(filename)
    root_node = tree.root_node
    getalias(root_node, lines, filename)

    if DEBUG:
        print(root_node.sexp())
        dir(root_node)
        dir(tree)

    for c in root_node.children:
        if c.type == "import_statement" or c.type == "import_from_statement":
            sl, sc = c.start_point
            el, ec = c.end_point
            line = (lines[el][sc:ec])
            line = line.split()
            importline = line[1]

            if DEBUG:
                print(importline)

            if filename not in LIBRARIES:
                LIBRARIES[filename] = []
                homedir = '.'.join(filename.split('/')[:-1])
                if '.' in homedir:
                    importline = homedir+'.'+importline

            if importline not in LIBRARIES:
                LIBRARIES[filename].append(importline)

    return LIBRARIES


def package2file(package, DEBUG=False):
    """
    Convert python package name into UNIX file name
    """
    library = '/'.join(package.split('.'))
    suffix = '.py'
    path = os.path.join(library + suffix)

    if DEBUG:
        print(path)

    return path


def file2package(file, DEBUG=False):
    """
    Convert UNIX file name into python package name
    """
    homedir = '.'.join(file.split('/'))

    if DEBUG:
        homedir = '.'.join(file.split('/')[:-1])
        package = file.split('.')[0]
        if '.' in homedir:
            package = homedir+'.'+package
        print(homedir)
        print(package)

    return '.'.join(homedir.split('.')[:-1])


def recurse(filename, directory, identifier, DEBUG=False):
    """
    Recurse file structure, updating LIBRARIES with dependencies 
    """

    path = os.path.join(directory, filename)
    LIBRARIES = getlibraries(path)
    getfunctions(filename, directory)
    key = package2file(identifier)

    if DEBUG:
        print("Latest library")
        print(LIBRARIES)
        print("Params")
        print(identifier)
        print(directory)
        print(filename)
        print("KEY")
        print(key)

    if key in LIBRARIES:
        for i, l in enumerate(LIBRARIES[key]):
            library = '/'.join(l.split('.'))
            suffix = '.py'
            path = os.path.join(directory, library + suffix)

            if DEBUG:
                print('Loop ' + i)
                print(l)
                print("Path")
                print(path)

            if os.path.isfile(path):
                directory, filename = os.path.split(path)
                LIBRARIES = recurse(filename, directory, l)

                if DEBUG:
                    print("path exists")
                    print(path)
                    print("dir"+directory)
                    print("file"+filename)

    return LIBRARIES


def traverse(node, lines, directory, filename, DEBUG=False):
    """
    Traverse the tree, updating DICT with function mappings
    """

    global DICT
    if node.type == "call":

        if DEBUG:
            print(node)
            print("callchildren")
            print(node.children)

        nc = node.child_by_field_name
        attribute, argument_list = nc('function'), nc('arguments')
        assert argument_list.type == "argument_list"

        if DEBUG:
            print('---------------')
            print(attribute.type)
            print(attribute)
            print(attribute.children)

        if attribute.type == "attribute":
            assert attribute.type == "attribute"
            obj = (attribute.child_by_field_name('object'))
            fun = (attribute.child_by_field_name('attribute'))

            objs, obje = obj.start_point, obj.end_point
            funs, fune = fun.start_point, fun.end_point
            assert objs[0] == obje[0]
            assert funs[0] == fune[0]

            objx = (lines[objs[0]][objs[1]:obje[1]])
            funx = (lines[funs[0]][funs[1]:fune[1]])

            if DEBUG:
                print(obj)
                print(fun)
                print(objs, obje)
                print(funs, fune)
                print(objx)
                print(funx)

            if objx in ALIAS:
                objx = ALIAS[objx]
            if objx not in DICT and objx:
                DICT[objx] = []

            if funx not in DICT[objx]:
                DICT[objx].append(funx)
        else:
            funs, fune = attribute.start_point, attribute.end_point

            if DEBUG:
                print(funs, fune)

            assert funs[0] == fune[0]
            funx = (lines[funs[0]][funs[1]:fune[1]])
            if 0 not in DICT:
                DICT[0] = []
            if funx not in DICT[0]:
                DICT[0].append(funx)

        if argument_list.children:
            childlist = argument_list.children
            for argchild in childlist:
                if argchild.type == "call":
                    DICT = traverse(argchild, lines,
                                    directory, filename)

    if node.type == "function_definition":

        if DEBUG:
            print(node.children)

        nc = node.child_by_field_name
        nchild = node.children
        name, parameters, body = nc('name'), nc('parameters'), nchild[-1]
        funs, fune = name.start_point, name.end_point
        assert funs[0] == fune[0]
        funx = (lines[funs[0]][funs[1]:fune[1]])

        if DEBUG:
            print(funs, fune)
            print("functions")
            print(parameters)
            print("Name")
            print(funx)
            print(DICT)

        if 0 not in DICT:
            DICT[0] = []
        if funx in DICT[0]:
            key = file2package(filename)
            if directory:
                key = directory + '.' + key
            if key not in DICT:
                DICT[key] = []
            if funx not in DICT[key]:
                DICT[key].append(funx)

        for c in parameters.children:
            if c.type == "default_parameter":
                for c1 in c.children:
                    traverse(c1, lines, directory, filename)

        for c in body.children:
            traverse(c, lines, directory, filename)

            if DEBUG:
                print("body2")
                print(c)
                print("children")
                print(c.children)

        if parameters and parameters.child_by_field_name('values'):

            if DEBUG:
                print("parameters")

            values = parameters.child_by_field_name('values')
            traverse(values, lines, directory, filename)

    if node.type == "module" or node.type == "expression_statement":
        if DEBUG:
            print("expression")
            print(node.children)
        for c in node.children:
            traverse(c, lines, directory, filename)
    return DICT


def getfunctions(filename, directory, DEBUG=False):
    """
    Traverse the tree, updating DICT with function mappings
    """

    path = os.path.join(directory, filename)
    code = getcode(path)
    lines = code.split('\n')
    tree = gettree(path)

    if DEBUG:
        print(lines)
        print(tree)
        print(tree.root_node.sexp())

    getalias(tree.root_node, lines, path)
    x = traverse(tree.root_node, lines, directory, filename)
    # print(x)
    return x


def getgraph(filename, directory, identifier, DEBUG=False):
    """
    Get the graph using DICT, LIBRARIES, and ALIAS values
    """
    LIBRARIES = recurse(filename, directory, identifier)
    path = os.path.join(directory, filename)
    DFS = []
    stack = [path]
    graphs = [[]]
    intermediary = set()
    g = [[]]

    while len(stack) != 0:
        s = stack.pop()
        x = list(graphs[-1])
        x.append(file2package(s))

        if DEBUG:
            print(x)
            print("GRAPHS")
            print(graphs)

        graphs.append(x)

        if s in LIBRARIES and s not in stack:
            intermediary.add(file2package(s))
            for c in LIBRARIES[s]:
                stack.append(package2file(c))
        else:
            x = graphs.pop()

            if DEBUG:
                print(x)
                print(intermediary)

            if x not in g and x[-1] not in intermediary:
                g.append(x)

        if s not in DFS:
            DFS.append(s)

    def prettygraph(g, DEBUG=False):
        """
        Prettify the graph according to desired specs
        """
        for graph in g:
            if DEBUG:
                print(graph)
            if not graph:
                continue
            i = -1
            x = graph[i]
            stdlib = stdlib_list("3.8")
            if graph[i] in stdlib:
                graph[i] += " (stdlib)"
            if x in DICT:
                graph[i] = graph[i]+" "+str(DICT[x])
            else:
                graph[i] += " (unused)"

            if DEBUG:
                for i, x in enumerate(graph):
                    if x in DICT:
                        print(str(DICT[x]))

            print(' <- '.join(graph[::-1]))

    prettygraph(g)
    return g
