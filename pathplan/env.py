# -*- coding: utf-8 -*-


__author__ = 'Justin S Bayer, bayer.justin@googlemail.com'


import collections

import pylab
import scipy


def line(x, y):
  """Return the discrete coordinates of a line between x and y."""
  point_on_line = lambda l: (x + l * (y - x)).astype('int')
  # An upper bound for the necessary evaluations is the manhattan distance
  # between x and y. (We could reduce that, but right now I am not interested
  # in this.)
  x = scipy.array(x)
  y = scipy.array(y)
  evals = abs((x - y).sum())
  step = 1.0 / evals
  points = [x]
  for i in xrange(1, evals):
    point = point_on_line(i * step)
    if (points[-1] != point).any():
      points.append(point)
  return points


class ConfigSpace(object):

  def __init__(self, space):
    self.space = space
    self.start = None
    self.goal = None

  @classmethod
  def from_png(cls, filename):
    a = (pylab.imread(filename).mean(axis=2) == 1.)
    return cls(a)

  def link(self, x, y):
    """Return whether the direct path from x to y is obstacle free."""

  def clearance(self, x):
    """Return whether the point at x is free."""
    x = scipy.asarray(x)
    if (x < 0).any():
      return False
    if any(i >= j for i, j in zip(x, self.space.shape)):
      return False
    return self.space[tuple(x)]


def ConfigSpaceDisplay(object):

  def __init__(configspace):
    self.samples = []

  def figure(self):
    """Return a matplotlib figure with the configuration as background."""

  def mark_sample(self, x):
    """Add a sample mark to the figure."""

  def mark_route_point(self, x):
    """Add a rout point to the figure."""


