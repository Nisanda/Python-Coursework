#Author: Dangallage Nisanda Vindiya Gunasinha
#Date: 26/11/2024
#Student ID: 20240164

import csv    # Import the CSv module to read CSV flie
import tkinter as tk
from collections import defaultdict

# Task A: Input Validation
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def get_max_days_in_month(month, year):
    # Months with 31 days
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    
    # Months with 30 days
    if month in [4, 6, 9, 11]:
        return 30
    
    # February
    if month == 2:
        return 29 if is_leap_year(year) else 28
    
    return None  # Invalid month

def validate_date_input():
    """
    Prompts the user for a date in DD MM YYYY format, validates the input for:
    - Correct data type
    - Correct range for day, month, and year
    """
    # This loop ensures correct input for the year
    while True:
        try:
            year = int(input("Please enter the year of the survey in the format YYYY: "))
            if 2000 <= year <= 2024:   # Limits the year to the expected range  
                print(year)
            else:
                print("Out of range - values must be in the range 2000 and 2024")
                continue
        except ValueError:
            print("Integer required")   # Handles non-integer inputs
            continue

        # This loop ensures correct input for the month 
        while True:
            try:
                month = int(input("Please enter the month of the survey in the format MM: "))
                if 1 <= month <= 12:    # Ensure the month is valid     
                    print(month)
                else:
                    print("Out of range - values must be in the range 1 and 12")
                    continue
            except ValueError:
                print("Integer required")   # Handles non-integer inputs
                continue

            # This loop ensures correct input for the day                
            while True:
                try:
                    day = int(input("Please enter the day of the survey in the format dd: "))
                    max_days = get_max_days_in_month(month, year)
                    if 1 <= day <= max_days:   # Ensures the day is within the valid range
                        print(day)
                    else:
                        print(f"Out of range - values must be in the range 1 and {max_days}")
                        continue
                except ValueError:
                    print("Integer required")   # Handles non-integer inputs
                    continue
        
                # Return the formatted date if all inputs are valid
                return f"{day:02}{month:02}{year}"

def validate_continue_input():
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    """
    while True:
        user_input = input("Enter 'Y' to load a new dataset or 'N' to quit: ").strip().upper()
        if user_input in ("Y","N"):
            return user_input      # Accepts only valid inputs
        else:
            print("Invalid input!! Please enter 'Y' for yes or 'N' for no")
            
# Task B: Processed Outcomes
def process_csv_data(file_path):
    """
    Load CSV data from the specified file
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    """
    try:
        with open(file_path, 'r') as file:
            data = csv.DictReader(file)      # Read the CSV file as a dictionary
            outcomes = {
                 
                # Dictionary to store all computed statistics
                'file_name': file_path,
                'total_vehicles': 0,
                'total_trucks': 0,
                'total_electric_vehicles': 0,
                'two_wheeled_vehicles': 0,
                'buses_north_elm_avenue': 0,
                'vehicles_no_turns': 0,
                'truck_percentage': 0,
                'avg_bicycles_per_hour': 0,
                'over_speed_limit_vehicles': 0,
                'vehicles_elm_avenue': 0,
                'vehicles_hanley_highway': 0,
                'scooter_percentage_elm_avenue': 0,
                'peak_vehicles_hanley_highway': 0,
                'peak_hours_hanley_highway': 0,
                'rain_hours': 0

            }
            
            # Variables for intermediate calculation
            total_bicycles = 0
            hanley_total_scooters = 0
            hanley_hour_count = {}
            rain_hour_count = {}
            
            # Iterate through each row in the CSV file
            for row in data:
                outcomes['total_vehicles'] += 1    # Count total vehicles

                if row.get("VehicleType") == "Truck":
                    outcomes['total_trucks'] += 1      # Count trucks

                if row.get("elctricHybrid","").strip().upper() == "TRUE":
                    outcomes['total_electric_vehicles'] += 1     # Count electric vehicles

                if row.get("VehicleType","") in ["Bicycle","Motorcycle","Scooter"]:
                    outcomes['two_wheeled_vehicles'] += 1       # Count two-wheeled vehicles

                if (row.get("JunctionName","") == "Elm Avenue/Rabbit Road" and 
                    row.get("VehicleType","") == "Buss" and
                    row.get("travel_Direction_out","") == "N"  ):
                    outcomes['buses_north_elm_avenue'] += 1       # Count buses going on Elm Avenue

                if row.get("travel_Direction_in") == row.get("travel_Direction_out"):
                    outcomes['vehicles_no_turns'] += 1        # Count vehicles with no turns

                if int(row.get("JunctionSpeedLimit",0)) < int(row.get("VehicleSpeed",0)):
                    outcomes['over_speed_limit_vehicles'] += 1       # Count vehicles over speed limit

                if row.get("JunctionName") == "Elm Avenue/Rabbit Road":
                    outcomes['vehicles_elm_avenue'] += 1      # Count vehicles at Elm Avenue Junction

                if row.get("JunctionName") == "Hanley Highway/Westway":
                    outcomes['vehicles_hanley_highway'] += 1       # Count vehicles at Hanley Highway Junction

                if row.get("JunctionName") == "Elm Avenue/Rabbit Road":
                    if row.get("VehicleType") == "Scooter":
                        hanley_total_scooters += 1        # Count Scooters at Elm Avenue Junction 

                if row.get("JunctionName") == "Hanley Highway/Westway":     # Track vehicle counts per hour at Hanley Highway Junction

                    try:
                        hanley_hour = int(row.get("timeOfDay").split(":")[0])      # Extract hour from time of day
                        hanley_hour_count[hanley_hour] = hanley_hour_count.get(hanley_hour,0) + 1      # Increment count for that hour
                    except (ValueError,TypeError):
                        pass                       

                if row.get("VehicleType") == "Bicycle":
                    total_bicycles += 1        # Count total bicycles

                if row.get("Weather_Conditions") in ["Heavy Rain","Light Rain"] :     # Track hours with rain

                    try:
                        rain_hour = int(row.get("timeOfDay").split(":")[0])       # Extract hour from time of day
                        rain_hour_count[rain_hour] = rain_hour_count.get(rain_hour,0) + 1      # Icrement count for that hour
                    except (ValueError,TypeError):
                        pass      

            if outcomes['vehicles_elm_avenue'] > 0:
                outcomes['scooter_percentage_elm_avenue'] = int((hanley_total_scooters/outcomes['vehicles_elm_avenue'])*100)

            else:
                outcomes['scooter_percentage_elm_avenue'] = 0         # Calculate scooter percentage at Elm Avenue Junction

            outcomes['truck_percentage'] = round((outcomes['total_trucks']/outcomes['total_vehicles'])*100)    # Calculate truck percentage
            outcomes['avg_bicycles_per_hour'] = round(total_bicycles/24)       # Calculate average bicycles per hour

            if hanley_hour_count:    # Find peak hours at Hanley Highway Junction

                max_vehicles_per_hour = max(hanley_hour_count.values())         # Find maximum number of vehicles in an hour
                peak_hour = [hanley_hour for hanley_hour,count in hanley_hour_count.items()     # Find which hour(s) had the maximum vehicles
                                if count == max_vehicles_per_hour ]
                
                # Create hour range descriptions
                peak_hour_range = [f"Between {hanley_hour}:00 and {hanley_hour + 1}:00" for hanley_hour in peak_hour]            
                
                # Store peak vehicle count and hour ranges
                outcomes['peak_vehicles_hanley_highway'] = max_vehicles_per_hour
                outcomes['peak_hours_hanley_highway'] = peak_hour_range
            
            # Count hours with rain
            if rain_hour_count:
                count_hours = list(rain_hour_count.keys())
                count_hours_range = len(count_hours)

                outcomes["rain_hours"] = count_hours_range

            return outcomes

    except FileNotFoundError:
        # Handle case where file is not found
        print("File not found. Please check the file path.")
        return None

def display_outcomes(outcomes):
    """
    Displays the calculated outcomes in a clear and formatted way.
    """
    # Print file name with decorative stars
    print(f"\n{'*' * 25}")
    print(f"The name of the selected CSV file is {outcomes['file_name']}")
    print(f"{'*' * 25}\n")

    # Print out each calculated metric in human-readable format
    print(f"The total number of vehicles passing through all junctions for the selected date is {outcomes['total_vehicles']}") 
    print(f"The total number of trucks passing through all junctions for the selected date is {outcomes['total_trucks']}")  
    print(f"The total number of electric vehicles passing through all junctions for the selected date is {outcomes['total_electric_vehicles']}")  
    print(f"The number of two wheeled vehicles through all junctions for the date (Bicycle, Motorcycle, Scooter) is {outcomes['two_wheeled_vehicles']}")
    print(f"The total number of busses leaving Elm Avenue/Rabbit Road junction heading north is {outcomes['buses_north_elm_avenue']}")
    print(f"The total number of vehicles passing through both junctions without turning left or right is {outcomes['vehicles_no_turns']}")
    print(f"The percentage of all vehicles recorded that are Trucks for the selected date (rounded to an integer) is {outcomes['truck_percentage']}%")
    print(f"The average number Bicycles per hour for the selected date (rounded to an integer) is {outcomes['avg_bicycles_per_hour']}")
    print(f"The total number of vehicles recorded as over the speed limit for the selected date is {outcomes['over_speed_limit_vehicles']}")
    print(f"The total number of vehicles recorded through only Elm Avenue/Rabbit Road junction for the selected date is {outcomes['vehicles_elm_avenue']}")
    print(f"The total number of vehicles recorded through only Hanley Highway/Westway junction for the selected date is {outcomes['vehicles_hanley_highway']}")
    print(f"The percentage of vehicles through Elm Avenue/Rabbit Road that are Scooters (rounded to integer) is {outcomes['scooter_percentage_elm_avenue']}%")
    print(f"The number of vehicles recorded in the peak (busiest) hour on Hanley Highway/Westway is {outcomes['peak_vehicles_hanley_highway']}")
    print(f"The time or times of the peak (busiest) traffic hour (or hours) on Hanley Highway/Westway is {outcomes['peak_hours_hanley_highway']}")
    print(f"The total number of hours of rain on the selected date is {outcomes['rain_hours']}")


# Task C: Save Results to Text File
def save_results_to_file(outcomes, txt_file="results.txt"):
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    # Open file in append mode to add new results each run
    with open(txt_file, 'a') as f:

        # Write each outcome metric to the file
        f.write("\n"+"="*100 +"\n")
        f.write(f"The name of the selected CSV file is {outcomes['file_name']}")
        f.write("\n"+"="*100 +"\n")
        f.write(f"The total number of vehicles passing through all junctions for the selected date is {outcomes['total_vehicles']}\n")
        f.write(f"The total number of trucks passing through all junctions for the selected date is {outcomes['total_trucks']}\n") 
        f.write(f"The total number of electric vehicles passing through all junctions for the selected date is {outcomes['total_electric_vehicles']}\n") 
        f.write(f"The number of two wheeled vehicles through all junctions for the date (Bicycle, Motorcycle, Scooter) is {outcomes['two_wheeled_vehicles']}\n")
        f.write(f"The total number of busses leaving Elm Avenue/Rabbit Road junction heading north is {outcomes['buses_north_elm_avenue']}\n")
        f.write(f"The total number of vehicles passing through both junctions without turning left or right is {outcomes['vehicles_no_turns']}\n")
        f.write(f"The percentage of all vehicles recorded that are Trucks for the selected date (rounded to an integer) is {outcomes['truck_percentage']}%\n")
        f.write(f"The average number Bicycles per hour for the selected date (rounded to an integer) is {outcomes['avg_bicycles_per_hour']}\n")
        f.write(f"The total number of vehicles recorded as over the speed limit for the selected date is {outcomes['over_speed_limit_vehicles']}\n")
        f.write(f"The total number of vehicles recorded through only Elm Avenue/Rabbit Road junction for the selected date is {outcomes['vehicles_elm_avenue']}\n")
        f.write(f"The total number of vehicles recorded through only Hanley Highway/Westway junction for the selected date is {outcomes['vehicles_hanley_highway']}\n")
        f.write(f"The percentage of vehicles through Elm Avenue/Rabbit Road that are Scooters (rounded to integer) is {outcomes['scooter_percentage_elm_avenue']}%\n")
        f.write(f"The number of vehicles recorded in the peak (busiest) hour on Hanley Highway/Westway is {outcomes['peak_vehicles_hanley_highway']}\n")
        f.write(f"The time or times of the peak (busiest) traffic hour (or hours) on Hanley Highway/Westway is {outcomes['peak_hours_hanley_highway']}\n")
        f.write(f"The total number of hours of rain on the selected date is {outcomes['rain_hours']}\n")
        f.write("\n"+"="*100 +"\n")    # Add closing seperator 


