#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Justin Zhu

import os
from tree_sitter import Language, Parser

PY_LANGUAGE = Language('build/my-languages.so', 'python')
LINEIDX = 0
CHARIDX = 1

libraries = {}
graph = []
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


def getlibraries(filename):
    code = getcode(filename)
    lines = code.split('\n')
    tree = gettree(filename)
    root_node = tree.root_node

    if DEBUG:
        print(root_node.sexp())
        dir(root_node)
        dir(tree)
        root_node.end_byte
        root_node.start_byte
        for i in libraries:
            print(i)
            # print(dir(c))
            break

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


def file2package(directory, filename):
    homedir = '.'.join(directory.split('/')[:-1])
    package = filename.split('.')[0]
    if '.' in homedir:
        package = homedir+'.'+package
    return package


def recurse(filename, directory, identifier):
    path = os.path.join(directory, filename)
    libraries = getlibraries(path)
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



def getfunctions(filename, directory):
    def traverse(node):
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
                if objx not in DICT:
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
                        DICT = traverse(argchild)

        if node.type == "function_definition":
            # print("yes!")
            # print(node.children)
            name, parameters, body = node.child_by_field_name('name'), node.child_by_field_name('parameters'), node.children[-1]
            # print("functions")
            # print(parameters)
            for c in parameters.children:
                if c.type == "default_parameter":
                    for c1 in c.children:
                        traverse(c1)

            # print("body")
            # print(name)
            # print(parameters)
            # print(body)
            # print("children")
            # print(body.children)
            for c in body.children:
                # print("body2")
                # print(c)
                traverse(c)
                    # print("children")
                    # print(c.children)

            # print(parameters.children)
            # print(parameters.children[0])
            if parameters and parameters.child_by_field_name('values'):
                # print("parameters")
                values = parameters.child_by_field_name('values')
                traverse(values)

        if node.type == "module" or node.type == "expression_statement":
            # print("expression")
            # print(node.children)
            for c in node.children:
                traverse(c)
        return DICT

    path = os.path.join(directory, filename)
    code = getcode(path)
    lines = code.split('\n')
    # print(lines)
    tree = gettree(path)
    # print(tree)
    # print(tree.root_node.sexp())
    x = traverse(tree.root_node)
    # print(x)
    return x


def getgraph(filename, directory, identifier):
    libraries = recurse(filename, directory, identifier)
    graphs = []
    stack = []
    for k in libraries:
        stack.add([k])
        lib = k
        while lib in libraries and lib not in stack[-1]:
            package = libraries[lib]
            stack[-1].add(package)
            package2file(directory, package)

            # lib

        # graphs.add(stack)

    while len(stack) > 0:
       graphs 





