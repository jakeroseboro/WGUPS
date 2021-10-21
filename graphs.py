import csv
from hash import HashTable
from package import Package
# This module loads the data from CSVs into the desired data structure

# Specify data file paths and initialize empty hash table object
package_list = "packages.csv"
package_table = HashTable()
distances = "Distances.csv"


# Parse package list, create a package object for each, and store in the hash table
# O(n)
def read_packages():
    with open(package_list, 'r', encoding="utf-8-sig") as infile:
        csvreader = csv.reader(infile)
        for row in csvreader:
            p = Package(row)
            package_table.insert(p.package_id, p)
        return package_table

# Parse distance table into a dictionary O(n^2)
def read_distances():
    with open(distances, 'r', encoding="utf-8-sig") as infile:
        distance_matrix = {}
        csvreader = csv.reader(infile)
        next(csvreader)
        for row in csvreader:
            vals = []
            for i in range(3, len(row)):
               vals.append(row[i])
            distance_matrix[row[1]] = vals
        return distance_matrix