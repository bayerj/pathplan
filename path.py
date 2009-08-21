# -*- coding: utf-8 -*-


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


class Pathfinder(object):

  def __init__(self, configspace):
    self.configspace = configspace

  def search(self):
    abstractmethod


class Bug1(Pathfinder):

  evasions = [(-1, +1), 
              (0, +1),
              (+1, +1),
              (+1, 0),
              (+1, -1),
              (0, -1),
              (-1, -1),
              (-1, 0)]

  def __init__(self, configspace):
    super(Bug1, self).__init__(configspace)
    self._buildneighbourhoodgraph()

  def _buildneighbourhoodgraph(self):
    neighbours = collections.defaultdict(lambda: [])
    for x in xrange(self.configspace.space.shape[0]):
      for y in xrange(self.configspace.space.shape[1]):
        for xd, yd in self.evasions:
          neighbours[(x, y)].append((x + xd, y + yd))

    self.neighbours = neighbours

  def dfs(self, pos, visited):
    """Return a depth first traversal from the current position. 
    
    Steps in the direction of the goal are favored (around the clock).""" 
    shift = lambda l, i: l[i:] + l[:i]
    to_visit = list(self.neighbours[pos])
    while to_visit:
      try:
        direc = line(pos, self.configspace.goal)[1] - pos
      except IndexError:
        # We are right before the goal.
        yield self.configspace.goal

      ind = self.evasions.index(tuple(direc))
      pos = to_visit.pop()
      if pos in visited or not self.configspace.clearance(pos):
        continue
      visited.add(pos)
      yield pos
      to_visit += shift([i for i in self.neighbours[pos] if i not in visited],
                        ind)

  def approach(self, pos, goal):
    route = line(pos, goal)[1:]
    for point in route:
      if not self.configspace.clearance(point):
        break
      yield tuple(point)

  def evade(self, pos, goal):
    print "Started evasion..."
    visited = set([pos])
    for candpos in self.dfs(pos, visited):
      if not self.configspace.clearance(candpos):
        continue
      yield candpos
      try:
        nextpoint = tuple(line(candpos, goal)[1])
      except IndexError:
        # We are right before the goal.
        break
      if self.configspace.clearance(nextpoint) and nextpoint not in visited:
        break
    else:
      raise Exception("I got stuck.")
    print "evaded."

  def search(self):
    pos = self.configspace.start
    goal = self.configspace.goal

    while True:
      for point in self.approach(pos, goal):
        pos = point
        yield pos
      if pos == goal:
        raise StopIteration("Goal reached.") 
      else:
        for point in self.evade(pos, goal):
          pos = point
          yield pos
          if pos == goal:
            raise StopIteration("Goal reached.")
