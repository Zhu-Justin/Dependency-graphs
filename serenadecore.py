#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Justin Zhu

import os
from tree_sitter import Language, Parser
from stdlib_list import stdlib_list

PY_LANGUAGE = Language('build/my-languages.so', 'python')
LINEIDX = 0
CHARIDX = 1

libraries = {}
# graph = []
packages = []
# DICT Contains all the function inherited from that module
# i.e. DICT[module] == [func1, func2, func3]
# module.func1, module.func2, module.func3 have been called
# in the file or any of its dependencies


DICT = {}
alias = {}

DEBUG = False

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

def getalias(node, lines, filename):
    if node.type == "import_statement":
        # print(node)
        # print(node.children)
        for c in node.children:
            if c.type == "dotted_name":
                cs, ce = c.start_point, c.end_point
                assert cs[0] == ce[0]
                cf = (lines[cs[0]][cs[1]:ce[1]])
                # packages.append(cf)
                if filename not in libraries:
                    libraries[filename] = []
                if cf not in libraries[filename]:
                    libraries[filename].append(cf)
            if c.type == "aliased_import":
                for c1 in c.children:
                    if c1.type == "dotted_name":
                        # print(c)
                        # print(c.children)
                        cs, ce = c1.start_point, c1.end_point
                        assert cs[0] == ce[0]
                        cf = (lines[cs[0]][cs[1]:ce[1]])
                        p = cf
                        if filename not in libraries:
                            libraries[filename] = []
                        if cf not in libraries[filename]:
                            libraries[filename].append(cf)
                        # if cf not in packages:
                        #     packages.append(cf)
                    if c1.type == "identifier":
                        cs, ce = c1.start_point, c1.end_point
                        assert cs[0] == ce[0]
                        cf = (lines[cs[0]][cs[1]:ce[1]])
                        alias[cf] = p

    if node.type == "import_from_statement":
        # print(node)
        # print(node.children)
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
                    if filename not in libraries:
                        libraries[filename] = []
                    if cf not in libraries[filename]:
                        libraries[filename].append(cf)
                    # packages.append(cf)
                    # print("Packages")
                    # print(packages)
                else:
                    if p1 not in DICT:
                        DICT[p1] = []
                    if cf not in DICT[p1]:
                        # print("ADDING " + cf +" in "+p1)
                        # print(DICT)
                        DICT[p1].append(cf)
    if node.type == "module" or node.type == "expression_statement":
        # print("expression")
        # print(node.children)
        for c in node.children:
            getalias(c, lines, filename)
    return alias

def getlibraries(filename):
    code = getcode(filename)
    lines = code.split('\n')
    tree = gettree(filename)
    root_node = tree.root_node
    getalias(root_node, lines, filename)

    # if DEBUG:
    #     print(root_node.sexp())
    #     dir(root_node)
    #     dir(tree)
    #     root_node.end_byte
    #     root_node.start_byte
    #     for i in libraries:
    #         print(i)
    #         # print(dir(c))
    #         break

    # root_node.start_point
    # root_node.end_point
    # dir(tree)

    for c in root_node.children:
        if c.type == "import_statement" or c.type == "import_from_statement":
            # print(c.start_point)
            # print(c.end_point)
            sl, sc = c.start_point
            el, ec = c.end_point
            # sl = c.start_point[LINEIDX]
            # sc = c.start_point[CHARIDX]
            # el = c.end_point[LINEIDX]
            # ec = c.end_point[CHARIDX]
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

            if importline not in libraries:
                libraries[filename].append(importline)

    return libraries



def package2file(package):
    library = '/'.join(package.split('.'))
    suffix = '.py'
    path = os.path.join(library + suffix)
    return path


def file2package(file):
    # homedir = '.'.join(file.split('/')[:-1])
    homedir = '.'.join(file.split('/'))
    # package = file.split('.')[0]
    # if '.' in homedir:
    #     package = homedir+'.'+package
    # return package
    return '.'.join(homedir.split('.')[:-1])


def recurse(filename, directory, identifier):
    path = os.path.join(directory, filename)
    libraries = getlibraries(path)
    getfunctions(filename, directory)
    # print("Latest library")
    # print(libraries)
    # print(identifier)
    # print("FN")
    # print(filename)
    key = package2file(identifier)
    # print(key)
    # print("DIR")
    # print(directory)
    # print(filename)
    # library = '/'.join(identifier.split('.'))
    # suffix = '.py'
    # path = os.path.join(directory, library + suffix)
    if key in libraries:
        for l in libraries[key]:
            # print('Loopy')
            # print(l)
            library = '/'.join(l.split('.'))
            suffix = '.py'
            path = os.path.join(directory, library + suffix)
            # print("Path")
            # print(path)
            if os.path.isfile(path):
                # print("path exists")
                # print(path)
                directory, filename = os.path.split(path)
                # print("dir"+directory)
                # print("file"+filename)
                libraries = recurse(filename, directory, l)
    return libraries


def traverse(node, lines, directory, filename):
    global DICT
    # print("Great")
    # print(lines)
    if node.type == "call":
        # print(node)
        # print("callchildren")
        # print(node.children)

        attribute, argument_list = node.child_by_field_name('function'), node.child_by_field_name('arguments')
        # print('---------------')
        # print(attribute.type)
        # print(attribute)
        # print(attribute.children)
        assert argument_list.type == "argument_list"
        if attribute.type == "attribute":
            # print("Good")
            assert attribute.type == "attribute"
            obj = (attribute.child_by_field_name('object'))
            # print(obj)
            fun = (attribute.child_by_field_name('attribute'))
            # print(fun)
            # if attribute.type == "attribute":
            objs, obje = obj.start_point, obj.end_point
            funs, fune = fun.start_point, fun.end_point
            # objs, obje = obj.start_point, obj.end_point
            # funs, fune = fun.start_point, fun.end_point
            # print("great")
            # print(objs, obje)
            # print(funs, fune)
            assert objs[0] == obje[0]
            assert funs[0] == fune[0]
            # print("objs")
            objx = (lines[objs[0]][objs[1]:obje[1]])
            # print(objx)
            # print("funs")
            funx = (lines[funs[0]][funs[1]:fune[1]])
            # print(funx)
            if objx in alias:
                objx = alias[objx]
            if objx not in DICT and objx:
                DICT[objx] = []

            if funx not in DICT[objx]:
                DICT[objx].append(funx)
        else:
            funs, fune = attribute.start_point, attribute.end_point
            # print(funs, fune)
            assert funs[0] == fune[0]
            funx = (lines[funs[0]][funs[1]:fune[1]])
            if 0 not in DICT:
                DICT[0] = []
            if funx not in DICT[0]:
                DICT[0].append(funx)

        if argument_list.children:
            childlist = argument_list.children
            for argchild in childlist:
                # print("HALLELUHAH")
                if argchild.type == "call":
                    DICT = traverse(argchild, lines,
                                    directory, filename)

    if node.type == "function_definition":
        # print("yes!")
        # print(node.children)
        name, parameters, body = node.child_by_field_name('name'), node.child_by_field_name('parameters'), node.children[-1]
        funs, fune = name.start_point, name.end_point
        # print(funs, fune)
        assert funs[0] == fune[0]
        funx = (lines[funs[0]][funs[1]:fune[1]])
        # print("functions")
        # print(parameters)
        # print("Name")
        if funx in DICT[0]:
            key = file2package(filename)
            if directory:
                key = directory + '.' + key
            # print(key)
            if key not in DICT:
                DICT[key] = []
            if funx not in DICT[key]:
                DICT[key].append(funx)

        for c in parameters.children:
            if c.type == "default_parameter":
                for c1 in c.children:
                    traverse(c1, lines, directory, filename)

        # print("body")
        # print(name)
        # print(parameters)
        # print(body)
        # print("children")
        # print(body.children)
        for c in body.children:
            # print("body2")
            # print(c)
            traverse(c, lines, directory, filename)
                # print("children")
                # print(c.children)

        # print(parameters.children)
        # print(parameters.children[0])
        if parameters and parameters.child_by_field_name('values'):
            # print("parameters")
            values = parameters.child_by_field_name('values')
            traverse(values, lines, directory, filename)

    if node.type == "module" or node.type == "expression_statement":
        # print("expression")
        # print(node.children)
        for c in node.children:
            traverse(c, lines, directory, filename)
    return DICT

def getfunctions(filename, directory):

    path = os.path.join(directory, filename)
    code = getcode(path)
    lines = code.split('\n')
    # print(lines)
    tree = gettree(path)
    # print(tree)
    # print(tree.root_node.sexp())
    # alias = []
    getalias(tree.root_node, lines, path)
    x = traverse(tree.root_node, lines, directory, filename)
    # print(x)
    return x

def getgraph(filename, directory, identifier):
    libraries = recurse(filename, directory, identifier)
    path = os.path.join(directory, filename)
    DFS = []
    stack = [path]
    graphs = [[]]
    intermediary = set()
    g = [[]]
    n = [0]
    
    while len(stack) != 0:
        s = stack.pop()
        x = list(graphs[-1])
        x.append(file2package(s))
        # print(x)
        # print("GRAPHS")
        # print(graphs)
        graphs.append(x)
        # print("S")
        # print(s)
        # graphs.append(graphs[-1].append(s))
        # if s in libraries and s not in DFS:
        if s in libraries and s not in stack: 
            # print("ADDED" + file2package(s))
            intermediary.add(file2package(s))
            # oldgraphs = list(graphs)
            # oldso = list(oldgraphs[-1])
            # n.append(len(graphs)-1)
            for c in libraries[s]:
                # so = graphs[-1]
                # print("graphs")
                # print(graphs)
                # print("GO")
                # print(so)
                # print(type(so))
                # so.append(c)
                # graphs.append(so)
                # print(list(so.append(c)))
                # print("source")
                # print(source)
                # print("c")
                # print(c)
                # print("k")
                # print(k)
                # graphs.append(k)
                stack.append(package2file(c))
            # n.pop()
            # graphs.pop()
        else:
            x = graphs.pop()
            # print("GOOD X")
            # print(x)
            # print(intermediary)
            if x[::-1] not in g and x[-1] not in intermediary:
                g.append(x[::-1])
            # if x not in g:
        if s not in DFS:
            DFS.append(s)
        # graphs.pop()
        #     print(graphs)
        #     DFS.pop()
    def prettygraph(g):
        for graph in g:
            # print(graph)
            if not graph:
                continue
            x = graph[0]
            stdlib = stdlib_list("3.8")
            if graph[0] in stdlib:
                graph[0] += " (stdlib)"
            if x in DICT:
                graph[0] = graph[0]+" "+str(DICT[x])
            else:
                graph[0] += " (unused)"
            # for x, i in enumerate(graph):
            #     if x in DICT:
            #         graph[i].add(str(DICT[x]))
                    
            print(' <- '.join(graph))
    prettygraph(g)
    # print(DICT)
    return g


#     for k in libraries:
#         stack.add([k])
#         lib = k
#         while stack:
#             while lib in libraries and lib not in stack[-1]:
#                 for package in libraries[lib]:
#                     # package = libraries[lib]
#                     newpack = stack[-1].add(package)
#                     stack.add(newpack)
#                     lib = package2file(package)
#             graphs.add(stack.pop())
#             # lib
#         # graphs.add(stack)

#     while len(stack) > 0:
#        graphs 





