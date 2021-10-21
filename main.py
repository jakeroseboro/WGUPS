# Jacob Roseboro
# ID: 001307315

from graphs import *
from util import sort_trucks, time_convert

# Initialize the data structures and load CSV data
# Hash table
package_table = read_packages()
# Python dictionary
distance_matrix = read_distances()

travel = []


# Identify the next destination based on current location and truck load
# Nearest neighbor algorithm uses distance matrix to check adresses of
# remaining packages and go to the one closest to the current address
# O(n)
def choose_next(truckload, IsAtHub, *args):
    # If this is true, it finds the package closest to the hub
    at_hub = IsAtHub
    # Arbitrary value that is not worth automating at the current project scale
    # but if this app was built upon it should be automated
    # to be larger than the greatest distance in the distance CSV
    short_route = 40
    next_package = None
    package_num=0
    # Iterate through package IDs on truck and choose shortest route
    # O(n)
    for package_id in truckload:
        if at_hub:
            # Gets the package
            package = package_table.lookup(package_id)
            # Finds the distance from hub based on the index of the address in the dict.
            # For example the hub is index 0 on the dict if it were converted to a list
            # and the 1st value (0 index) of the key WGU is zero which is accurate because
            # the distance from wgu to wgu is 0
            distance = float(distance_matrix['4001 South 700 East'][(list(distance_matrix).index(package.address))])
        else:
            # Gets the potential next package
            package = package_table.lookup(package_id)
            # Gets the package that was just delivered
            current_package = package_table.lookup(int(args[0]))
            # Gets the distance from the current stop
            distance = float(distance_matrix[current_package.address][(list(distance_matrix).index(package.address))])
        # If this route is shorter than the other routes, it becomes the shortest route temporarily
        if distance < short_route:
            short_route = distance
            next_package = package
            package_num = package.package_id
    return package_num, next_package, short_route


# Deliver the chosen package and return to the hub once the truck is empty
# O(n^2) since is calls another for loop from choose_next within a for loop
def run_route(truck, time):
    total_dist = 0
    # The first delivery comes from the hub and will supply different
    # values to the choose_next function
    deliveries = 0
    route_time = 0
    num = 0
    route_time += time
    # This allows the user to view which truck delivered their package
    # and is useful in displaying a status at a specific time
    truck_number = "0"
    if time == 480:
        truck_number = "1"
    elif time == 546:
        truck_number = "2"
    elif time == 620:
        truck_number = "3"
    # Run once for each package on the truck
    # 0(n)
    for j in range(len(truck)):
        # Sets off the first delivery from the hub
        if deliveries == 0:
            # Package ID, Package object, and distance returned
            num, pckg, dist = choose_next(truck, True)
            # Denotes that we are no longer at the hub
            deliveries+=1
            # Updates the total distance
            total_dist += dist
            # Calculates the time based on distance
            route_time += int((dist / 18) * 60)
            # Update delivery time based on minutes
            pckg.delivery_time = time_convert(route_time)
            # Update status
            pckg.delivery_status = "Delivered at " + pckg.delivery_time + " by truck " + truck_number
            truck.remove(num)
        else:
            # Does the same thing as the previous block, but inputs the previous package location
            # instead of starting from the hub
            num, pckg, dist = choose_next(truck, False, num)
            total_dist += dist
            route_time += int((dist / 18) * 60)
            pckg.delivery_time = time_convert(route_time)
            pckg.delivery_status = "Delivered at " + pckg.delivery_time + " by truck " + truck_number
            truck.remove(num)
    if len(truck) == 0:
        # Calculates the total time and distance required to return to the hub from the final package
        package = package_table.lookup(num)
        returnDist = float(distance_matrix['4001 South 700 East'][(list(distance_matrix).index(package.address))])
        total_dist += returnDist
        route_time += int((returnDist/18)*60)
    return total_dist


# Simulate package delivery. Load packages on trucks and run each
# truck's route at the appropriate start time
# O(n^2) complexity due to calling the run_route() function
def run_sim():
    # Get truck loads from package sorter
    t1, t2, t3 = sort_trucks()
    # Currently uses static start times based on package data
    # T1, T2, T3 leave at 8,9:06, and 10:20 AM
    t1_start_mins = 480
    t2_start_mins = 546
    t3_start_mins = 620

    # run each truck route and record the distance traveled
    # Each truck route is O(n^2)
    t1_distance = run_route(t1, t1_start_mins)
    travel.append(t1_distance)
    t2_distance = run_route(t2, t2_start_mins)
    travel.append(t2_distance)

    # It's 10:20, and we have the corrected address for Package ID 9
    package_table.lookup(9).notes = "Address corrected at 10:20AM"
    t3_distance = run_route(t3, t3_start_mins)
    travel.append(t3_distance)
    all_distance = t1_distance + t2_distance + t3_distance
    travel.append(all_distance)


# Main function to kick off the simulation and control the CLI
if __name__ == '__main__':
    prompt_text = '''
        Welcome to the WGUPS package tracking system.
        The time is now 07:59 AM
        ----------------------------------------------
        What would you like to do?
        - [1] Load Trucks (Insert Packages)
        - [2] Lookup Individual Package 
        - [3] View Status of All Packages at 9:00 AM
        - [4] View Status of All Packages at 10:00 AM
        - [5] View Status of All Packages at 12:30 PM
        - ENTER 0 TO EXIT
    '''
    user_input = ''
    # Run the route simulation.
    run_sim()
    # Limited 'CLI' for the program
    # Consider replacing with GUI
    while user_input != '0':
        user_input = input(prompt_text)
        # Exit the program
        if user_input == "0":
            print("You entered 0 or did not enter a valid menu option.")
            print("Goodbye!")
            SystemExit

        # Get the truck distance info O(1)
        if user_input == '1':
            print("Truck 1 distance traveled: %.2f miles" % travel[0])
            print("Truck 2 distance traveled: %.2f miles" % travel[1])
            print("Truck 2 distance traveled: %.2f miles" % travel[2])
            print("Total distance traveled: %.2f miles" % travel[3])

        # Display info for a single package O(n)
        elif user_input == "2":
            package_number = input("Enter Package ID to Search ")
            try:
                package_key = int(package_number)
                if package_key in range(1, package_table.table_size() + 1):
                    package_table.lookup(package_key).print_long()
                else:
                    print("Invalid entry!")
            except Exception:
                print("Invalid entry!")

        # Options 3,4,5 display pacakge status at the required times on the rubric O(n)
        elif user_input == "3":
            delivered = []
            not_delivered = []
            for i in range(1, package_table.table_size()):
                p = package_table.lookup(i)
                if p.delivery_time <= "09:00":
                    delivered.append(p)
                else:
                    not_delivered.append(p)
            print("Packages delivered by 9:00 AM")
            for p in delivered:
                p.print_inline()
            print("\n")
            print("Packages not delivered by 9:00 AM")
            for p in not_delivered:
                if "truck 1" not in p.delivery_status:
                    temp_status = p.delivery_status
                    p.delivery_status = "At Hub"
                    p.print_inline()
                    p.delivery_status = temp_status
                if "truck 1" in p.delivery_status and "9:00" not in p.delivery_status:
                    temp_status = p.delivery_status
                    p.delivery_status = "En Route"
                    p.print_inline()
                    p.delivery_status = temp_status

        elif user_input == "4":
            delivered = []
            not_delivered = []
            for i in range(1, package_table.table_size()):
                p = package_table.lookup(i)
                if p.delivery_time <= "10:00":
                    delivered.append(p)
                else:
                    not_delivered.append(p)
            print("Packages delivered by 10:00 AM")
            for p in delivered:
                p.print_inline()
            print("\n")
            print("Packages not delivered by 10:00 AM")
            for p in not_delivered:
                if "truck 3" in p.delivery_status:
                    temp_status = p.delivery_status
                    p.delivery_status = "At Hub"
                    p.print_inline()
                    p.delivery_status = temp_status
                if "truck 2" in p.delivery_status and "10:00" not in p.delivery_status:
                    temp_status = p.delivery_status
                    p.delivery_status = "En Route"
                    p.print_inline()
                    p.delivery_status = temp_status

        elif user_input == "5":
            delivered = []
            not_delivered = []
            for i in range(1, package_table.table_size()):
                p = package_table.lookup(i)
                if p.delivery_time <= "12:30":
                    delivered.append(p)
                else:
                    not_delivered.append(p)
            print("Packages delivered by 12:30 PM")
            for p in delivered:
                p.print_inline()
            print("\n")
            print("Packages not delivered by 12:30 PM")
            for p in not_delivered:
                if "truck 3" in p.delivery_status and "12:30" not in p.delivery_status:
                    temp_status = p.delivery_status
                    p.delivery_status = "En Route"
                    p.print_inline()
                    p.delivery_status = temp_status
