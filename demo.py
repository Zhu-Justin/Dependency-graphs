#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Justin Zhu
# CLI Tool for creating dependency graphs

import os
import argparse
from tree_sitter import Language, Parser
import serenadecore as sc

argparser = argparse.ArgumentParser(description='Get Dependency Graphs')
argparser.add_argument('filename')
args = argparser.parse_args()

homedirectory, filename = os.path.split(args.filename)

package = filename.split('.')[0]

libraries = sc.recurse(filename, homedirectory, package)
functionmaps = sc.getfunctions(filename, homedirectory)

g = sc.getgraph(filename, homedirectory, package)
