# Graph Dependency Analyzer
This is a script I wrote that can identify the dependencies for each file in a codebase—using
tree-sitter. It's a command-line utility that takes as an
argument a path to some directory, as well as a file to analyze, and then
outputs what other files are imported for each file in that directory.

A few things to note:
- The analyzer shows the entire chain (run `./demo.py ./tests/foo.py`)
- The analyzer designates unused packages (denoted as `(unused)`)
- The analyzer designates `stdlib` packages (denoted as `(stdlib)`)
- The analyzer is able to handle aliasing and multiple packages imported in one line (run `./demo.py ./tests/importbonanza.py`)
- The analyzer is able to output the specific functions being called in the designated package (functions are bracketed)
- The analyzer supports python3 code

# Getting started

```
git clone https://github.com/Zhu-Justin/Dependency-graphs.git /path/to/repo

cd /path/to/repo
pip3 install -r ./requirements.txt

./demo.py /path/to/pythoncode.py
```


# Getting help
```
./demo.py  -h
```

