#!/usr/bin/env python3
# encoding: utf-8
from collections import defaultdict
from itertools import groupby
from operator import itemgetter
import os
from os.path import join
from subprocess import call
from time import sleep
from sys import exit
from pprint import pprint


# Defaults
input_folder = './out'
default_matrix_columns = 18
map_width = None
map_height = None

files = os.listdir(input_folder)
generations = defaultdict(list)

for filename in files:
    generation_id, _, score = tuple(map(int, filename[:-4].split('-')))
    generations[generation_id].append((score, filename))

star_agents = [
    sorted(generations[generation], key=itemgetter(0), reverse=True)[0][1]
    for generation in sorted(generations.keys())]

star_agents = star_agents[-6 * default_matrix_columns:]

star_agents = [
    [open(join(input_folder, e), "rt") for _, e in g]
    for k, g in groupby(
        enumerate(star_agents), lambda i: i[0] // default_matrix_columns)]

# print(star_agents)

end_of_play = False
while not end_of_play:
    end_of_play = True

    for group in star_agents:
        read_flag = True

        height = 0
        line = "-"
        while read_flag and line.replace(' ', ''):

            found_map = False
            line = ""
            for agent_file in group:

                agent_line = agent_file.readline()
                if agent_line:
                    end_of_play = False

                if map_width is None:
                    map_width = len(agent_line)-1

                read_flag = not agent_line.startswith('-')
                if read_flag and agent_line:
                    line += agent_line[:-1] + "  "
                else:
                    line += ' ' * (map_width + 2)

            height += 1
            print(line)

        if map_height is None:
            map_height = height

        if height == 1:
            for _ in range(map_height - 1):
                print()

    sleep(0.6)
    call(['clear'])
