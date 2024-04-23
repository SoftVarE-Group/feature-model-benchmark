#!/usr/bin/env python3

from tqdm import tqdm
import argparse
import glob
import os
from os import path
import hashlib
import tempfile

import pandas as pd

from pysat.formula import CNF
from pysat.solvers import Solver

def hash_hex(filepath):    
    with open(filepath, "rb") as f:
        h = hashlib.md5()
        while chunk := f.read(8192):
            h.update(chunk)

    return h.hexdigest()


def compute_core_deads(cnf):

    found = set()

    cores = set()
    deads = set()

    with Solver(bootstrap_with = cnf.clauses) as solver:
        for x in range(1, cnf.nv + 1):

            x_found = x in found
            nx_found = -x in found

            if x_found and nx_found:
                continue

            if not x_found:
                if solver.solve(assumptions = [x]):
                    for y in solver.get_model():
                        found.add(y)
                else:
                    solver.add_clause([-x])
                    deads.add(x)

            if not nx_found:
                if solver.solve(assumptions = [-x]):
                    for y in solver.get_model():
                        found.add(y)
                else:
                    solver.add_clause([x])
                    cores.add(x)

    return cores, deads



def discover_dimacs(paths):

	files = []

	for p in paths:
		print(f"Discovering in {p}")
		p = path.abspath(p)

		if not path.exists(p):
			print(f"Directory {p} does not exist, skipping")
			continue

		files.extend(glob.glob(f"{p}/**/*.dimacs", recursive = True))

	print(f"Discovery found {len(files)} dimacs files.")
	print()

	return files


def remove_duplicates(files, no_bars, out):
	files_good = []
	cache = dict()

	if no_bars:
		files_iter = iter(files)
	else:
		files_iter = tqdm(files, desc = "Uniqueness".ljust(20), bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} ")

	for file in files_iter:

		h = hash_hex(file)

		if h in cache:
			cache[h].append(file)
			continue

		files_good.append(file)
		cache[h] = [file]


	files = files_good

	duplicates = []
	for k, ls in cache.items():
		if len(ls) > 1:
			for file in ls:
				duplicates.append((k, file))

	if duplicates:
		fname = save_to_csv(duplicates, path.join(out, "duplicates.csv"), columns = ["Hash", "File"])
	
		print(f"Removed {len(files) - len(files_good)} duplicates --> {fname}")

	print()
	return files_good


def verify_and_filter(files, vmin, vmax, cmin, cmax, no_bars, out):
	files_good = []
	invalids = []
	voids = []
	filtered = []

	if no_bars:
		files_iter = iter(files)
	else:
		files_iter = tqdm(files, desc = "Verifying".ljust(20), bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} ")

	for file in files_iter:
		try:
			cnf = CNF(from_file = file)

			if vmin and cnf.nv < vmin:
				filtered.append((file, f'Has less than {vmin} variables ({cnf.nv})'))
			elif vmax and cnf.nv > vmax:
				filtered.append((file, f'Has more than {vmax} variables ({cnf.nv})'))
			elif cmin and len(cnf.clauses) < cmin:
				filtered.append((file, f'Has less than {cmin} clauses ({len(cnf.clauses)})'))
			elif cmax and len(cnf.clauses) > cmax:
				filtered.append((file, f'Has more than {cmax} clauses ({len(cnf.clauses)})'))


			with Solver(bootstrap_with=cnf) as solver:
				if not solver.solve():
					voids.append(file)

		except ValueError as ve:
			invalids.append((file, ve))

	bad = set()

	print()
	if invalids:

		fname = save_to_csv(invalids, path.join(out, "invalids.csv"), columns = ["file", "reason"])

		print(f"Found {len(invalids)} invalid files --> {fname}")
		for file, reason in invalids:
			bad.add(file)
			# print(f'{file}: {reason}')
		print()

	if voids:

		fname = save_to_csv(voids, path.join(out, "voids.csv"), columns = ["file"])

		print(f"Found {len(voids)} void files -->{fname}")
		for file in voids:
			bad.add(file)
		print()

	if filtered:

		filter_ls = [("vmin", vmin), ("vmax", vmax), ("cmin", cmin), ("cmax", cmax)]
		filter_ls = [f"{x}={y}" for x,y in filter_ls if y]

		fname = save_to_csv(filtered, path.join(out, f'filtered-{"_".join(filter_ls)}.csv'), columns = ["file", "filter"])

		print(f"Filtered {len(filtered)} files --> {fname}")
		for file, reason in filtered:
			bad.add(file)
			# print(f'{file}: {reason}')
		print()

	for file in files:
		if file not in bad:
			files_good.append(file)

	return files_good


def simplify_implicit_unit_clauses(cnf):

    truths, falses = compute_core_deads(cnf)

    if truths is None and falses is None:
        return

    truths = truths if truths else set()
    falses = falses if falses else set()

    clauses = []

    for x in truths:
        clauses.append([x])

    for x in falses:
        clauses.append([-x])

    cache = set()
    
    clauses_good = []
    for clause in clauses:
        if (s := str(clause)) not in cache:
            clauses_good.append(clause)
            cache.add(s)

    clauses = clauses_good
    
    for clause in cnf.clauses:

        satisfied = False
        nclause = []

        for x in clause:
            if x > 0 and x in truths:
                # x and (x or ...)
                satisfied = True
                break
            elif x > 0 and x in falses:
                continue
            elif x < 0 and abs(x) in truths:
                continue
            elif x < 0 and abs(x) in falses:
                satisfied = True
                break

            nclause.append(x)

        if not satisfied:
            if (s := str(nclause)) not in cache:
                clauses.append(nclause)
                cache.add(s)

    cnf2 = CNF(from_clauses = clauses)
    cnf2.nv = cnf.nv
    cnf2.comments = cnf.comments

    return cnf2


def simplify_dimacs(files, no_bars, out):

	stats = []

	if no_bars:
		files_iter = iter(files)
	else:
		files_iter = tqdm(files, desc = "Simplifying".ljust(20), bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} ")

	for file in files_iter:
		cnf = CNF(from_file = file)
		cnf2 = simplify_implicit_unit_clauses(cnf)

		file2 = path.join(out, path.basename(file))
		
		with open(file2, "w+") as fw:
			fw.write(cnf2.to_dimacs())

		stats.append((file, len(cnf.clauses), file2, len(cnf2.clauses)))

	save_to_csv(stats, path.join(out, "simplify.csv"), columns = ["In", "#Clauses", "Out", "#Clauses"])

def get_non_implemented_vector(files):
	return ['?'] * len(files)

'''
Gets vector mirroring analyses from feature model batch analysis
Only used for feature models where analysis over feature models does not scale to get as many results as possible
'''
def get_analysis_vectors(files, vector= ['File','NumberOfFeatures','NumberOfLeafFeatures','NumberOfTopFeatures','Number_Constraints','AverageConstraintSize','CtcDensity','FeaturesInConstraintsDensity','TreeDepth','AverageNumberOfChildren','NumberOfAlternatives','NumberOfOrs','NumberOfClauses','NumberOfLiterals','NumberOfUnitClauses','NumberOfTwoClauses','ClauseDensity','NumberOfTautologies','NumberOfRedundantConstraints','ConnectivityDensity','Void','Number_CORE','Number_Dead','RatioOptionalFeatures','NumberOfFalseOptionalFeatures','NumberOfOptionalFeatures','NumberOfValidConfigurationsLog','SimpleCyclomaticComplexity','IndependentCyclomaticComplexity']):
	number_of_features = []
	number_of_constraints = []
	average_constraint_sizes = []
	number_of_unit_clauses = []
	number_of_two_clauses = []
	number_of_cores = []
	number_of_deads = []
	number_of_optionals = []
	ecrs = []
	number_of_literals = []
	average_children = []
	optional_rations = []
	for file in files:
		print(f'Analyzing {file}')
		cnf = CNF(from_file=file)
		number_of_features.append(cnf.nv)
		number_of_literals.append(sum([len(clause) for clause in cnf.clauses]))
		number_of_constraints.append(len(cnf.clauses))
		average_constraint_sizes.append((sum([len(clause) for clause in cnf.clauses])) / len(cnf.clauses))
		number_of_unit_clauses.append(len([clause for clause in cnf.clauses if len(clause) == 1]))
		number_of_two_clauses.append(len([clause for clause in cnf.clauses if len(clause) == 2]))
		# cores, deads = compute_core_deads(cnf)
		# number_of_cores.append(len(cores))
		# number_of_deads.append(len(deads))
		# number_of_optionals.append(cnf.nv - len(cores) - len(deads))
		# optional_rations.append((cnf.nv - len(cores) - len(deads))/ cnf.nv)
		variables_in_clauses = set()
		for clause in cnf.clauses:
			for literal in clause:
				variables_in_clauses.add(abs(literal))
		ecrs.append(len(variables_in_clauses) / cnf.nv)
		average_children.append(cnf.nv - 1)
		

	df = pd.DataFrame()
	df['File'] = files
	df['NumberOfFeatures'] = number_of_features
	df['NumberOfLeafFeatures'] = number_of_features
	df['NumberOfTopFeatures'] = number_of_features
	df['Number_Constraints'] = number_of_constraints
	df['AverageConstraintSize'] = average_constraint_sizes
	df['CtcDensity'] = get_non_implemented_vector(files)
	df['FeaturesInConstraintsDensity'] = ecrs
	df['TreeDepth'] = [2] * len(files)
	df['AverageNumberOfChildren'] = cnf.nv - 1
	df['NumberOfAlternatives'] = [0] * len(files)
	df['NumberOfOrs'] = [0] * len(files)
	df['NumberOfClauses'] = number_of_constraints
	df['NumberOfLiterals'] = number_of_literals
	df['NumberOfUnitClauses'] = get_non_implemented_vector(files)
	df['NumberOfTwoClauses'] = get_non_implemented_vector(files)
	df['ClauseDensity'] = get_non_implemented_vector(files)
	df['NumberOfTautologies'] = get_non_implemented_vector(files)
	df['NumberOfRedundantConstraints'] = get_non_implemented_vector(files)
	df['ConnectivityDensity'] = get_non_implemented_vector(files)
	df['Void'] = get_non_implemented_vector(files)
	df['Number_CORE'] = get_non_implemented_vector(files)
	df['Number_Dead'] = get_non_implemented_vector(files)
	df['RatioOptionalFeatures'] = get_non_implemented_vector(files)
	df['NumberOfFalseOptionalFeatures'] = get_non_implemented_vector(files)
	df['NumberOfOptionalFeatures'] = get_non_implemented_vector(files)
	df['NumberOfValidConfigurationsLog'] = get_non_implemented_vector(files)
	df['SimpleCyclomaticComplexity'] = get_non_implemented_vector(files)
	df['IndependentCyclomaticComplexity'] = get_non_implemented_vector(files)

	df.to_csv('dimacs_analysis.csv', index = False)




def save_to_csv(ls, filepath, columns = None):

	if columns:
		df = pd.DataFrame(ls, columns = columns)
	else:
		df = pd.DataFrame(ls)

	df.to_csv(filepath, index = False)

	return filepath


def main(files = None, discover = None, unique = False, verify = False, simplify = None, analysis = False, vmin = None, vmax = None, cmin = None, cmax = None, no_bars = False, out = None):
	
	if out is None:
		out = tempfile.mkdtemp()
	
	out = path.abspath(out)

	if not path.exists(out):
		os.makedirs(out, exist_ok = True)


	print("Saving files to", out)
	print()


	if not files:
		files = []

	if discover:
		files.extend(discover_dimacs(discover))

	if unique:
		files = remove_duplicates(files, no_bars, out)

	if verify or vmin or vmax or cmin or cmax:
		files = verify_and_filter(files, vmin, vmax, cmin, cmax, no_bars, out)

	if simplify:
		simplify_dimacs(files, no_bars, out)

	if analysis:
		get_analysis_vectors(files)


if __name__ == '__main__':

	argparser = argparse.ArgumentParser(
	                    prog='DIMACS tools',
	                    description='Small utilities to handle dimacs files',
	                    epilog='')

	argparser.add_argument("files", nargs = "*", help = "DIMACS files")
	argparser.add_argument("--discover", nargs = "*", help = "Discovers dimacs files in specified paths (default=..)")
	argparser.add_argument("--no_bars", action = "store_true", help = "Disables progress bars")
	argparser.add_argument("--unique", action = "store_true", help = "Enforces uniqueness of input files")
	argparser.add_argument("--verify", action = "store_true", help = "Verify the validity of input files")
	argparser.add_argument("--analysis", action = "store_true", help = "Compute analysis vector for each found dimacs")
	argparser.add_argument("--vmin", type = int, help = "Filters files with more or equal variables than")
	argparser.add_argument("--vmax", type = int, help = "Filters files with less or equal variables than")
	argparser.add_argument("--cmin", type = int, help = "Filters files with more or equal clauses than")
	argparser.add_argument("--cmax", type = int, help = "Filters files with less or equal clauses than")
	argparser.add_argument("--simplify", action = "store_true", help = "Performs an analysis for implicit unit clauses (i.e., core and dead features) and simplifies the clauses, respectively.")
	argparser.add_argument("--out", help = "Directory to store output files into")

	args = argparser.parse_args()

	if not args.files:
		if args.discover is None:
			print("No files selected and --discover not set. Nothing to do.")
			exit()
		elif args.discover == []:
			args.discover = [".."]

	main(**vars(args))
