# Main cli will take an arbitrary number of parameters of tables to roll on

import argparse
import json
import os
import sys

# Oracle is a class represents a single oracle table.
class Oracle:
    def __init__(self, name):
        self.name = name

    # roll is a method which will select a result from the oracle table
    # at random.
    def roll(self):
        result = 10
        return result

# read_oracles takes a filename to read from where the oracles are kept
# and then parses it into a series of oracle table objects, then returns
# them.
def read_oracles(filename):
    try:
    	with open(filename, "r") as oracle_file:
            oracle_json = json.load(oracle_file)
    except:
        sys.stderr.write("ERROR: Could not read oracles from file")
        sys.exit(1)

    print(oracle_json)

def main():
    parser = argparse.ArgumentParser(description = "Starforged oracle roller")
    parser.add_argument('-f', '--file', type=str, nargs=1,
                        metavar='filename',
                        default='~/git-repos/dataforged/oracles.json',
                        help='The location of the oracles.json file.')
    parser.add_argument('oracles', metavar='oracle_name', type=str,
                        nargs='+', help='name of an oracle table to roll')

    args = parser.parse_args()

    print(args.oracles)

if __name__ == "__main__":
    main()
