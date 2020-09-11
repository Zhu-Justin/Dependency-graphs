#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Justin Zhu

import os
import argparse
parser = argparse.ArgumentParser(description='Get Dependency Graphs')
parser.add_argument('filename')
# os.path.dirname()

args = parser.parse_args()
print(args.filename)
with open(args.filename, "r") as f:
    code = f.read() 

print(code)

# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')


# print(args.accumulate(args.integers))
