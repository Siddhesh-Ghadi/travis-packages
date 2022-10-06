import subprocess, os, sys, argparse, time
from pathlib import Path
import pandas as pd

# commandline args
argParser = argparse.ArgumentParser(description='Script to compare 2 csv lists of packages.')
argParser.add_argument('-b', '--baseData', help='csv file path of base data', type=str)
argParser.add_argument('-n', '--newData', help='csv file path of new data', type=str)
argParser.add_argument('-o', '--outputDir', help='directory to store output',  default='data', type=str)

args = argParser.parse_args()

if not args.baseData or not args.newData:
    print("Please provide base data & new data csv file path. Use -h for help")
    sys.exit(1)

if not os.path.isfile(args.baseData):
   print("{} does not exist. Please provide correct path. Use -h for help".format(args.baseData))
   sys.exit(1)

if not os.path.isfile(args.newData):
   print("{} does not exist. Please provide correct path. Use -h for help".format(args.newData))
   sys.exit(1)

dir_path = args.outputDir.rstrip('/')
Path(dir_path).mkdir(parents=True, exist_ok=True)

# import csv data
# csv format: name,version
base_data = pd.read_csv (args.baseData)
new_data = pd.read_csv (args.newData)

# perform set difference operations to find differences 

# missing packages in new data
# since we are interested in missing packages in new data, we will perform 
# base_data(name) - new_data(name) which gives package names missing in new data(extra in old data)
missing_packages = base_data[base_data.name.isin(new_data.name) == False]

print("Missing Packages")
print(missing_packages)

file_path = dir_path + "/missing_packages.csv"
missing_packages.to_csv(file_path, index=False)
print("Data saved to {}".format(file_path))

# version mismatch
# get common packages based on name key: base_data(name) intersection new_data(name) 
# drop rows which have same versions
version_mismatch = base_data.merge(new_data, on="name")
version_mismatch.drop(version_mismatch[version_mismatch["version_x"] == version_mismatch["version_y"]].index, inplace = True)
version_mismatch.rename(columns={'version_x': 'base_data', 'version_y': 'new_data'}, inplace=True)

print("\nMis-matched Version Packages")
print(version_mismatch)

file_path = dir_path + "/version_mismatch.csv"
version_mismatch.to_csv(file_path, index=False)
print("Data saved to {}".format(file_path))
