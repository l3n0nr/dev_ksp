#!/usr/bin/env python

import matplotlib.pyplot as plt

def read():
	path = "04 - Landing.csv"
	line = [line for line in open(path)]
	dataset = [line.strip().strip(',') for line in open(path)]

	for x in xrange(0,9):
		print(dataset[x])

def matplot():	
	plt.plot([1, 2, 3, 4])
	plt.ylabel('some numbers')
	plt.show()


def main():
	# read()
	matplot()

main()