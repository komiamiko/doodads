#!/usr/bin/env python3

"""
Uses the Kruskal tree library and Graphviz to
play the tree game and output graphical representations of the trees.

Creator note: only works on the command line or the plain Python shell, not IDLE.
As far as I've tested anyway.
"""

import kruskal_tree

import itertools
import os
import subprocess

def ensure_dir(fdir):
    if not os.path.exists(fdir):
        os.makedirs(fdir)

colors = ('a8a8a8', 'd8988e', '80c48e', 'a6a2e2')

def write_tree(node, namer, printer):
	tag = next(namer)
	printer(tag + '[label="",fillcolor="#'+colors[node.color]+'"];')
	for child in node.children:
		ctag = write_tree(child, namer, printer)
		printer(tag + '->' + ctag + ';')
	return tag

def generate_tree(node, numeral):
	fn = f'ktree_{numeral}.txt'
	namer = iter(f'n{k}' for k in itertools.count())
	lines = []
	printer = lines.append
	printer('''digraph{
  graph[fontname=Arial,fontsize=12,splines=spline,overlap=prism]
  node[style=filled,shape=ellipse,fillcolor=white,width=0.1,height=0.1,fontname=Arial,fontsize=12]
  edge[fontname=Arial,fontsize=12,penwidth=2]''')
	write_tree(node, namer, printer)
	printer('}')
	with open(fn,'w') as file:
		file.write('\n'.join(lines))
	with subprocess.Popen(['dot',fn,'-O','-Tpng']):
		pass

def main():
    print('How many trees to make?')
    up_to = int(input())
    ensure_dir('ktrees')
    os.chdir('ktrees')
    for num, tree in zip(range(up_to), kruskal_tree.tree3_friedman()):
        generate_tree(tree, num)

if __name__ == '__main__':
    main()

