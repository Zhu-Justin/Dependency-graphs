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

print
(root_node.child_by_field_name('dotted_name'))

# for c in root_node.children:
#     if c.type == "expression" or c.type == "import_from_statement":

# help(root_node.child_by_field_name)
# ()


print(root_node.sexp())
type(root_node)


def traverse():
    for c in root_node.children:
        if c.type == "expression_statement":
            # print(c)
            # print(c.child_by_field_id(1))
            # print(dir(c))
            # print(c.is_named)
            # print(c.children)
            q = c.children[0]
            if q.type == "call":
                # q.child_by_file_name('')
                # print(q)
                # print(q.children)
                attribute = q.children[0]
                assert attribute.type == "attribute"
                print(attribute)
                # print(dir(attribute))
                print(attribute.child_by_field_name('object'))
                obj = (attribute.child_by_field_name('object'))
                function = (attribute.child_by_field_name('attribute'))
                print(attribute.child_by_field_name('attribute'))

            # q = c.walk()
            # print(dir(q))
            # print(q.)


print("===============")
traverse()

