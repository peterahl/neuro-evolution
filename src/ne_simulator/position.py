# -*- coding: utf-8 -*-
from enum import Enum, unique


@unique
class Direction(Enum):

    NORTH = 0

    EAST = 1

    SOUTH = 2

    WEST = 3


directions = list(Direction)


def turn(direction, right=True):
    """ Turn right or left and return the new direction. """
    new_direction_index = directions.index(direction) + (1 if right else -1)
    return directions[new_direction_index % len(Direction)]


class NoSuchDirectionException(Exception):
    pass


class Position():
    # TODO: reuse Position objects: add meta class with cached objects

    def __init__(self, x, y):
        """
        :type x: int
        :type y: int
        """
        self._x = x
        self._y = y

    def __str__(self):
        return "Position: <{}, {}>".format(self._x, self._y)  # for debug

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def move(self, direction):
        """
        :type direction: Direction
        """
        if direction == Direction.NORTH:
            return Position(self._x, self._y - 1)
        if direction == Direction.EAST:
            return Position(self._x + 1, self._y)
        if direction == Direction.SOUTH:
            return Position(self._x, self._y + 1)
        if direction == Direction.WEST:
            return Position(self._x - 1, self._y)
        raise NoSuchDirectionException(direction)
