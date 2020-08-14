#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable-all
"""
Created on Fri Aug 14 2020

Quick code to extract a number from OEIS
change it to a grid lattice
and "beautifully" plot it

@author: thebooort + code adapted
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from urllib import request
import json


def get_sequence_from_name(name):
    """
    Get a sequence of numbers from OEIS via it code
    adapted from @oeispy
    input: oeis code string
    output: string with sequence, strin with explanation
    """
    # request info via json from oeis
    res = request.urlopen('https://oeis.org/search?q=id:'+name+'&fmt=json')
    # read json data properly
    data = json.loads(res.read().decode())
    # extract relevant info
    raw_sequence = data['results'][0]['data']
    explanation = data['results'][0]['name']
    return raw_sequence, explanation


def grid_conversion(sequence):
    """
    Convert a sequence of numbers to a grid  for plotting
    adapted from @bbengfort
    input: string seq
    output: np array, grid-transformed sequence
    """
    # parse the text string into a numpy array
    sequence = sequence.replace(",", "")
    sequence = np.array([int(digit) for digit in sequence])

    # Find the nearest square to get the width and height
    lenn = len(sequence)
    dims = int(math.ceil(math.sqrt(lenn)))
    sequence = np.pad(sequence, (0, (dims**2) - sequence.shape[0]), mode='constant')
    grid = sequence.reshape((dims, dims))
    return grid


def gridplot(grid, name, sequence, explanation):
    """
    Plots the grid of a sequence.
    adapted from @bbengfort
    input: np array, grid-transformed sequence
            string, seq name
            string, raw seq
            string, seq explanatio
    output: string with sequence, strin with explanation
    """

    # Visualize the grid
    fig, axe = plt.subplots(figsize=(15, 15))
    discrete_cmap = plt.get_cmap('nipy_spectral', np.max(grid)-np.min(grid)+1)
    mat = axe.matshow(grid, cmap=discrete_cmap)

    # Configure the figure
    plt.title("{} visualized to {} digits \n".format(name, len(sequence.replace(",", ""))), fontsize=29, pad=29)
    # title and text
    plt.suptitle(explanation, y=0.92, fontsize=18)
    plt.text(-1, 16, 'Made by @bortizmath', fontsize=17)  # WARNING you may need to adjust y-axis
    plt.text(9, 16, 'Data from OEIS', fontsize=17)  # WARNING you may need to adjust y-axis
    # Add the colorbar under the plot
    plt.colorbar(mat, orientation="horizontal")
    # setting off axis
    axe.axis('off')
    # Show the figure
    plt.show()


if __name__ == "__main__":

    # changin plotting style
    plt.style.use('dark_background')

    # getting the seq, and plotting
    seq_name = 'A050918'
    seq, explanation = get_sequence_from_name(seq_name)
    seq_grid = grid_conversion(seq)
    gridplot(seq_grid, seq_name, seq, explanation)
