#! /usr/bin/env python2.6
# -*- coding: utf-8 -*-


import optparse

import pylab

from path import ConfigSpace, Bug1


def make_optparser():
  parser = optparse.OptionParser()
  parser.add_option('-i', type='string', dest='configfile'
                    help='configuration file')
  parser.add_option('-a', type='string', dest='algorithm',
                    help='algorithm to use')
  parser.add_option('-s', type='string', dest='start',
                    help='start of the robot. e.g. "2,3". No spaces.')
  parser.add_option('-g', type='string', dest='goal',
                    help='goal of the robot. e.g. "2,3". No spaces.')


def main(options, args):
  cs = ConfigSpace.from_png(options.configfile)
  cs.start = options.start.split(',')
  cs.goal = options.goal.split(',')

  pathfinder = lookup_algorithm(options.algorithm)(cs)
  for pos in pathfinder.search():
    print pos


if __name__ == '__main__':
  options, args = make_optparser().parse_args()
  sys.exit(main(options, args))
