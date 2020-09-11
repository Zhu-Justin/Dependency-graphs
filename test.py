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

tree = parser.parse(bytes("""
import bar
bar.hello()
sys.exit(1)
import sys
""", "utf8"))

# tree.sexp()
dir(tree)

root_node = tree.root_node
dir(root_node)
root_node.sexp()
root_node




