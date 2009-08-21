# -*- coding: utf-8 -*-


__author__ = 'Justin S Bayer, bayer.justin@googlemail.com'


import collections
import random

import scipy as sp
import networkx as nx

from env import line


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

  def evade(self, pos, goal, visited):
    print "Started evasion..."
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
    visited = set()

    self.path = []

    while True:
      for point in self.approach(pos, goal):
        pos = point
        self.path.append(pos)
        yield pos
      if pos == goal:
        raise StopIteration("Goal reached.") 
      else:
        for point in self.evade(pos, goal, visited):
          pos = point
          self.path.append(pos)
          yield pos
          if pos == goal:
            raise StopIteration("Goal reached.")


class PRM(Pathfinder):

  def __init__(self, configspace):
    super(PRM, self).__init__(configspace)
    self.graph = nx.Graph()
    self.graph.add_node(self.configspace.start)
    self.graph.add_node(self.configspace.goal)

  def sample(self):
    """Return a vector x where to sample next for clearance."""
    x = random.randint(0, self.configspace.space.shape[0])
    y = random.randint(0, self.configspace.space.shape[1])
    return x, y

  def search(self):
    # Phase for building up roadmap.
    while True:
      point = self.sample()
      yield point
      if not self.configspace.clearance(point):
        continue
      # Search for a node that we can connect with.
      for node in self.graph.nodes():
        if self.configspace.link(point, node):
          self.graph.add_edge(point, node, sp.dot(sp.asarray(point),
                                                  sp.asarray(node)))
      path = nx.shortest_path(self.graph, 
                              self.configspace.start, self.configspace.goal)
      if path:
        break

    # Build up path.
    self.path = []
    for a, b in zip(path, path[1:]):
      self.path += line(a, b)
