#! /usr/bin/env python2.6
# -*- coding: utf-8 -*-


import sys
import optparse

import pylab

from path import ConfigSpace, Bug1


def lookup_algorithm(string):
  return Bug1


def make_optparser():
  parser = optparse.OptionParser()
  parser.add_option('-f', type='string', dest='configfile',
                    help='configuration file')
  parser.add_option('-a', type='string', dest='algorithm',
                    help='algorithm to use')
  parser.add_option('-s', type='string', dest='start',
                    help='start of the robot. e.g. "2,3". No spaces.')
  parser.add_option('-g', type='string', dest='goal',
                    help='goal of the robot. e.g. "2,3". No spaces.')
  return parser


def main(options, args):
  pylab.ion()
  cs = ConfigSpace.from_png(options.configfile)
  cs.start = [int(i) for i in options.start.split(',')]
  cs.goal = [int(i) for i in options.goal.split(',')]

  pathfinder = lookup_algorithm(options.algorithm)(cs)

  fig = pylab.figure()
  ax = fig.add_subplot(111)
  ax.imshow(pylab.imread(options.configfile))
  ax.plot(cs.start[0], cs.start[1], 'bo')
  ax.plot(cs.goal[0], cs.goal[1], 'go')

  for pos in pathfinder.search():
    ax.plot(pos[1], pos[0], "rx")
    pylab.gcf().canvas.draw()

  while True: 
    pass


if __name__ == '__main__':
  options, args = make_optparser().parse_args()
  sys.exit(main(options, args))
