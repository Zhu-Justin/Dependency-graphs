#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Justin Zhu
import argparse
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()

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
def foo():
    if bar:
        baz()
""", "utf8"))

root_node = tree.root_node
type(root_node)
dir(root_node)
root_node.end_point
root_node.sexp()



assert root_node.type == 'module'
assert root_node.start_point == (1, 0)
assert root_node.end_point == (3, 13)

function_node = root_node.children[0]
assert function_node.type == 'function_definition'
assert function_node.child_by_field_name('name').type == 'identifier'

function_name_node = function_node.children[1]
assert function_name_node.type == 'identifier'
assert function_name_node.start_point == (1, 4)
assert function_name_node.end_point == (1, 7)

assert root_node.sexp() == "(module "
    "(function_definition "
        "name: (identifier) "
        "parameters: (parameters) "
        "body: (block "
            "(if_statement "
                "condition: (identifier) "
                "consequence: (block "
                    "(expression_statement (call "
                        "function: (identifier) "
                        "arguments: (argument_list))))))))"

cursor = tree.walk()

assert cursor.node.type == 'module'

assert cursor.goto_first_child()
assert cursor.node.type == 'function_definition'

assert cursor.goto_first_child()
assert cursor.node.type == 'def'

# Returns `False` because the `def` node has no children
assert not cursor.goto_first_child()

assert cursor.goto_next_sibling()
assert cursor.node.type == 'identifier'

assert cursor.goto_next_sibling()
assert cursor.node.type == 'parameters'

assert cursor.goto_parent()
assert cursor.node.type == 'function_definition'

tree.edit(
    start_byte=5,
    old_end_byte=5,
    new_end_byte=5 + 2,
    start_point=(0, 5),
    old_end_point=(0, 5),
    new_end_point=(0, 5 + 2),
)

new_tree = parser.parse(new_source, tree)


query = PY_LANGUAGE.query("""
(function_definition
  name: (identifier) @function.def)

(call
  function: (identifier) @function.call)
""")

captures = query.captures(tree.root_node)
assert len(captures) == 2
assert captures[0][0] == function_name_node
captures[0][0]
assert captures[0][1] == "function.def"


