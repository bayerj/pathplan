# -*- coding: utf-8 -*-


import scipy


def line(x, y):
  """Return the discrete coordinates of a line between x and y."""
  point = lambda l: (x + l * (y - x)).astype('int')
  # An upper bound for the necessary evaluations is the manhattan distance
  # between x and y. (We could reduce that, but right now I am not interested
  # in this.)
  evals = (x - y).sum()
  step = 1.0 / evals
  points = [x]
  for i in xrange(1, evals):
    point = point(i * step)
    if points[-1] != point:
      points.append(point)
  return points


class ConfigSpace(object):

  def __init__(self, space):
    self.space = space
    self.start = None
    self.goal = None

  def from_png(self, filename):
    a = pylab.imread(filename).mean(2)


  def link(self, x, y):
    """Return whether the direct path from x to y is obstacle free."""

  def clearance(self, x):
    """Return whether the point at x is free."""


def ConfigSpaceDisplay(object):

  def __init__(configspace):
    self.samples = []

  def figure(self):
    """Return a matplotlib figure with the configuration as background."""

  def mark_sample(self, x):
    """Add a sample mark to the figure."""
    self.samples.append(x)

  def mark_route_point(self, x):
    """Add a rout point to the figure."""


def Pathfinder(object):

  def __init__(self, configspace):
    self.configspace = configspace

  def search(self):
    abstractmethod


class Bug1(Pathfinder):

  # Slice is to exclude (0, 0)
  evasions = [(x, y) for x in (-1, 1, 0) for y in (-1, 1, 0)][:-1]

  def search(self):
    route = []
    pos = self.configspace.start
    goal = self.configspace.goal

    while pos != goal:
      route_candidate = line(pos, goal)
      for point in route_candidate:
        obstacle = False
        if not self.configspace.clearance(point):
          # Walk around obstacle.
          obstacle = True
          old_direction = point - pos
          i = self.evasions.find(old_direction)
          other_dirs = self.evasions[:i] + self.evasions[i + 1:]
          for d in other_dirs:
            point = pos + d
            if self.configspace.clearance(point):
              break
        yield point
        if obstacle: 
          break
