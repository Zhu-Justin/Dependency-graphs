import os

from tree_sitter import Language, Parser
Language.build_library(
  # Store the library in the `build` directory
  'build/my-languages.so',

  # Include one or more languages
  [
    # 'vendor/tree-sitter-go',
    # 'vendor/tree-sitter-javascript',
    # 'vendor/tree-sitter-python'
    'tree-sitter-python'
  ]
)

PY_LANGUAGE = Language('build/my-languages.so', 'python')

parser = Parser()
parser.set_language(PY_LANGUAGE)
tree = parser.parse(bytes("""
print("hello",name)
""", "utf8"))

code = """import bar
bar.hello()
sys.exit(1)
def hello():
    print("Hello")
    bar.hello()
    return
import sys
"""
code.split("\n")

tree = parser.parse(bytes("""
import bar
bar.hello()
sys.exit(1)
def hello():
    print("Hello")
    bar.hello()
    return
import sys
""", "utf8"))

DICT = {}

def getcode(filename, DEBUG=True):
    if DEBUG:
        with open('samplecode.py', "r") as f:
            code = f.read() 
    else:
        with open(filename, "r") as f:
            code = f.read() 
    return code


code = getcode('samplecode.py')
tree = parser.parse(bytes(code, "utf8"))

# tree.sexp()
dir(tree)

root_node = tree.root_node
dir(root_node)
rw = root_node.walk()
dir(rw)
rw.current_field_name()
dir(rw)
rw.node

rw.goto_next_sibling()
rw.node
rw.current_field_name()


x = rw.goto_first_child()
root_node.sexp()
dir(root_node)
root_node.child_by_field_id(1)

print (root_node.child_by_field_name('dotted_name'))

# for c in root_node.children:
#     if c.type == "expression" or c.type == "import_from_statement":

# help(root_node.child_by_field_name)
# ()


print(root_node.sexp())
type(root_node)


code = getcode('samplecode.py')
lines = code.split('\n')


def traverse(node):
    global DICT
    if node.type == "call":
        # print(node)
        # print("callchildren")
        # print(node.children)

        attribute, argument_list = node.child_by_field_name('function'), node.child_by_field_name('arguments')
        print('---------------')
        print(attribute.type)
        print(attribute)
        print(attribute.children)
        assert argument_list.type == "argument_list"
        if attribute.type == "attribute":
            print("Good")
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

    # for c in node.children:
    #     if c.type == "expression_statement":
    #         # print(c)
    #         # print(c.child_by_field_id(1))
    #         # print(dir(c))
    #         # print(c.is_named)
    #         # print(c.children)
    #         q = c.children[0]
    #         if q.type == "call":
    #             # q.child_by_field_name('')
    #             # print(q)
    #             print(q.children)
    #             # attribute = q.children[0]
    #             attribute = q.child_by_field_name('function')
    #             assert attribute.type == "attribute"
    #             print(attribute)
    #             # print(dir(attribute))
    #             # print(attribute.child_by_field_name('object'))
    #             obj = (attribute.child_by_field_name('object'))
    #             print(obj)
    #             fun = (attribute.child_by_field_name('attribute'))
    #             print(fun)
    #             objs, obje = obj.start_point, obj.end_point
    #             funs, fune = fun.start_point, fun.end_point
    #             assert objs[0] == obje[0]
    #             assert funs[0] == fune[0]
    #             print("objs")
    #             objx = (lines[objs[0]][objs[1]:obje[1]])
    #             print(objx)
    #             print("funs")
    #             funx = (lines[funs[0]][funs[1]:fune[1]])
    #             print(funx)
    #             if objx not in DICT:
    #                 DICT[objx] = []
    #             DICT[objx].append(funx)

    #             argument_list = q.child_by_field_name('arguments')
    #             assert argument_list.type == "argument_list"
    #             if argument_list.children:
    #                 childlist = argument_list.children
    #                 for argchild in childlist:
    #                     print("HALLELUHAH")
    #                     if argchild.type == "call":
    #                         traverse(argchild)

    return DICT




                # print(attribute.child_by_field_name('attribute'))

            # q = c.walk()
            # print(dir(q))
            # print(q.)




print("===============")
traverse(root_node)
print(DICT)


