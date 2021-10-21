import csv

package_list = "packages.csv"

# Function to load the trucks with the optimal packages and get the best route to take
# "Correct" packages were first sorted by hand, and I determined what the priorities would be.
# Priority 1: Packages that have to be delivered by 9:00
# Priority 2: Assures that all packages that must be on the same truck arrive together. These packages all have the early deadlines except for one so this specific case is needed
# Priority 3: Packages that have to be delivered by 10:30 and are delayed on flight or have other special notes
# Priority 4: Packages that have to be delivered by 10:30 with no special notes
# Priority 5: Packages that have to be delivered by EOD (17:00) and delayed on flight, truck 2 only, or wrong address
# Priority 6: Packages that are EOD with no special notes, but cannot exceed the load of the trucks (16 packages)
# After all trucks are loaded, the choose_next algorithm changes the route to make it more efficient
# O(N^2)
def sort_trucks():
    truck1=[]
    truck2=[]
    truck3=[]

    with open(package_list, 'r', encoding="utf-8-sig") as infile:
        csvreader = csv.reader(infile)
        for row in csvreader:
            if row[5] == '9:00 AM':
                truck1.append(int(row[0]))

    with open(package_list, 'r', encoding="utf-8-sig") as infile:
        csvreader = csv.reader(infile)
        for row in csvreader:
            if row[7] == 'Must be delivered with 13, 16':
                truck1.append(int(row[0]))

    with open(package_list, 'r', encoding="utf-8-sig") as infile:
        csvreader = csv.reader(infile)
        for row in csvreader:
            if row[5] == '10:30 AM' and row[7] != 'None' and row[7] != 'Can only be on truck 2' and row[7] != 'Wrong address listed' and row[7] != 'Delayed on flight---will not arrive to depot until 9:05 am':
                truck1.append(int(row[0]))
            elif row[5] == '10:30 AM' and row[7] =='Delayed on flight---will not arrive to depot until 9:05 am':
                truck2.append(int(row[0]))

    with open(package_list, 'r', encoding="utf-8-sig") as infile:
        csvreader = csv.reader(infile)
        for row in csvreader:
            if row[5] == "10:30 AM" and row[7] == "None":
                truck1.append(int(row[0]))

    with open(package_list, 'r', encoding="utf-8-sig") as infile:
        csvreader = csv.reader(infile)
        for row in csvreader:
            if row[5] == "EOD" and row[7] == "Delayed on flight---will not arrive to depot until 9:05 am":
                truck3.append(int(row[0]))
            if row[5] == "EOD" and row[7] == "Wrong address listed":
                truck3.append(int(row[0]))
            if row[5] == "EOD" and row[7] == "Can only be on truck 2":
                truck2.append(int(row[0]))

    with open(package_list, 'r', encoding="utf-8-sig") as infile:
        csvreader = csv.reader(infile)
        for row in csvreader:
            if row[5] == "EOD" and row[7] == "None":
                if len(truck1) < 16:
                    truck1.append(int(row[0]))
                elif len(truck2) < 16:
                    truck2.append(int(row[0]))
                elif len(truck3) < 16:
                    truck3.append(int(row[0]))
                else:
                    print("package could not be loaded")
    return truck1, truck2, truck3

# Function used to convert the number of minutes to hh:mm format 
# Would prefer to use datetime objects to keep track of the packages
def time_convert(mins):
    hour = "{:02d}".format(int(mins / 60))
    minute = "{:02d}".format(mins % 60)
    time_string = hour + ':' + minute
    return time_string
