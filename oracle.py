# Main cli will take an arbitrary number of parameters of tables to roll on

import argparse
import json
import os
import random
import sys

accepted_oraclesets = ["Core"]
oraclelist = []

class Table:
    def __init__(self, results):
        self.results = results
        self.rolls = harvest_rolls(results)
    def roll(self):
        random.seed()
        rolled = random.randint(1,100)

        # If the rolled result is just a key in the table, then we can
        # just return the result and skip the searching.
        if rolled in self.rolls:
            return rolled, self.results[rolled]
        # Otherwise, we need to find out which result is appropriate.
        else:
            roll_result = 1
            for roll_chance in self.rolls:
                if roll_chance > roll_result:
                    roll_result = roll_chance
                else:
                    break

        return rolled, self.results[roll_result]
        
def harvest_rolls(table_results):
    rolls = []
    for result in table_results:
        rolls.append(result["Chance"])

    rolls.sort()
    return rolls
        

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

    parsed_oraclesets = dict()

    for raw_oracleset in oracle_json:
        if raw_oracleset["Name"] in accepted_oraclesets:
            try:
                parsed_oraclesets[raw_oracleset["Name"].lower()] = parse_oracles(raw_oracleset["Oracles"])
            except:
                sys.stderr.write("Error parsing oracle set %s\n" % raw_oracleset["Name"]) 

    return parsed_oraclesets

def parse_oracles(raw_oracles):
    parsed_oracles = dict()

    # For each oracle in the set, we want to get its name and the
    # table inside it and add those to a new Oracle object.
    for oracle in raw_oracles:
        try:
            parsed_oracles[oracle["Name"].lower()] = Table(oracle["Table"])
        except:
            sys.stderr.write("Error parsing oracle %s\n" % oracle["Name"])

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

    oracles = read_oraclesets(args.file)
    for oracle in args.oracles:
        roll, result = oracles["core"][oracle].roll()     
        print("{} : {}, {}\n".format(oracle, roll, result))
        
if __name__ == "__main__":
    main()
