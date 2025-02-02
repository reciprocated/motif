#!/usr/bin/env python3
import numpy as np
import time
import sys
import csv
import os

from CandidateMarkerFinder import CandidateMarkerFinder
from MarkersSet import MarkersSet
from Marker import Marker
from Genome import Genome
from DataConnector import DataConnector
from DataController import DataController

def run(sources_file, markers_file, output_file):

    prefix = "/".join(sources_file.split('/')[:-1])
    with open(sources_file) as file:
        sourcefiles = [prefix + '/' + line.rstrip('\n') for line in file]

    if len(sourcefiles) < 1:
        print("sources_file must have at least one source filepath")
        exit(1)

    with open(markers_file) as file:
        markers = [line[1] for line in csv.reader(file)]

    genome_names = [sourcefile.split("/")[-1] for sourcefile in sourcefiles]

    candidate_marker_finder = CandidateMarkerFinder("test")
    candidate_marker_finder.marker_set = MarkersSet(
        [Marker(i, 'phenotype', sequence=marker) for i, marker in enumerate(markers)]
    )

    genome_list = [None for _ in range(len(genome_names))]

    for i, genome_name in enumerate(genome_names):
        genome_list[i] = Genome(name=genome_name)
        genome_list[i].add_string_data_connector(
            DataConnector(file=sourcefiles[i])
        )

    candidate_marker_finder.data_controller = DataController("data_type", genome_list)

    candidate_marker_finder.run()

    output = candidate_marker_finder._presence_matrix._presence_matrix

    if int(os.environ['SAVE_RESULT_TO_FILE']):
        with open(output_file, "w") as f:
            for i, res in enumerate(output):
                f.write(genome_names[i])
                f.write(' ')
                f.write(''.join("0" if val == 0 else "1" for val in res))
                f.write('\n')
    else:
        return output

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(f"usage: {sys.argv[0]} <sources_file> <markers_file> <output_file>")
        exit(1)

    run(*sys.argv[1:])
