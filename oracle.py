# Main cli will take an arbitrary number of parameters of tables to roll on

import argparse
import json
import os
import sys

oraclelist = []

# OracleSet is a class that represents a themed set of oracles.
class OracleSet:
    def __init__(self, name, oracle_list):
        self.name = name
        self.oracles = oracle_list

# Oracle is a class that represents a single oracle table.
class Oracle:
    def __init__(self, name, table):
        self.name = name
        self.table = table

    # roll is a method which will select a result from the oracle table
    # at random.
    def roll(self):
        result = 10
        return result

# read_oracles takes a filename to read from where the oracles are kept
# and then parses it into a list of OracleSet objects.
def read_oraclesets(filename):
    filename = os.path.expanduser(filename)
    try:
    	with open(filename, "r") as oracle_file:
            oracle_json = json.load(oracle_file)
    except:
        sys.stderr.write("ERROR: Could not read oracles from file\n")
        sys.exit(1)

    parsed_oraclesets = []

    for raw_oracleset in oracle_json:
        try:
            new_oracleset = OracleSet(raw_oracleset["Name"].lower, parse_oracles(raw_oracleset["Oracles"]))
        except:
            sys.stderr.write("Error parsing oracle set %s\n" % raw_oracleset["Name"]) 

        parsed_oraclesets.append(new_oracleset)

    return parsed_oraclesets

# parse_oracleset takes an oracleset and parses the oracles within
# it into Oracle objects.
def parse_oracles(raw_oracles):
    parsed_oracles = []

    # For each oracle in the set, we want to get its name and the
    # table inside it and add those to a new Oracle object.
    for oracle in raw_oracles:
        try:
            new_oracle = Oracle(oracle["Name"].lower, oracle["Table"])
        except:
            sys.stderr.write("Error parsing oracle %s\n" % oracle["Name"])

        parsed_oracles.append(new_oracle)

    return parsed_oracles

def main():
    parser = argparse.ArgumentParser(description = "Starforged oracle roller")
    parser.add_argument('oracles', metavar='oracle_name', type=str,
                        nargs='+', help='name of an oracle table to roll')
    parser.add_argument('-f', '--file', type=str, nargs=1,
                        metavar='filename',
                        default='~/git-repos/dataforged/oracles.json',
                        help='The location of the oracles.json file.')

    args = parser.parse_args()

    read_oraclesets(args.file)

if __name__ == "__main__":
    main()
