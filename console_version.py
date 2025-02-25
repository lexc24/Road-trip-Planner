import csv
import os

from model.Objects.Trip import *
from model.APIs.yelp import *
import email, smtplib, ssl
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def set_up_email():
    sender_email = "lex.castaneda.24@gmail.com"
    password = "wvpd bxin ewwm osjk"


def send_email():
    sender_email = "lex.castaneda.24@gmail.com"
    password = "wvpd bxin ewwm osjk"
    reciever_addr = input("Please enter your email address so we can send you your itinerary\n")
    subject = "Your itinerary from VacationPlanner"
    body = "This is an email with attachment of your itinerary in the form of a PDF:)"
    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = reciever_addr
    em['Subject'] = subject
    em.set_content(body)


def write_roadtrip_csv(restaurants_data, travel_data, output_filename="roadtrip.csv"):
    """
    Writes restaurants and travel segments to a CSV file with separate sections.

    The CSV file will have two parts:
      1. [Restaurants] section with columns: City, Cuisine, Restaurant Name, Address.
      2. [Travel] section with columns: Start City, Destination City, Distance/Time.

    Parameters:
      restaurants_data (dict): Nested dictionary where each city maps to cuisines,
                               each cuisine maps to restaurant names and their addresses.
      travel_data (list): List of travel segments. Each segment is a dict with keys
                          "Start City", "Destination City", and "Distance/Time".
      output_filename (str): The name of the output CSV file.
    """
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write the Restaurants section
        writer.writerow(["[Restaurants]"])
        writer.writerow(["City", "Cuisine", "Restaurant Name", "Address"])
        for city, cuisines in restaurants_data.items():
            for cuisine, restaurants in cuisines.items():
                for restaurant, address_lines in restaurants.items():
                    # Join multiple address lines with a separator (e.g., " | ")
                    address = " | ".join(address_lines)
                    writer.writerow([city, cuisine, restaurant, address])

        # Blank line to separate sections
        writer.writerow([])

        # Write the Travel section
        writer.writerow(["[Travel]"])
        writer.writerow(["Start City", "Destination City", "Distance/Time"])
        for segment in travel_data:
            # Expecting segment to be a dictionary.
            writer.writerow([
                segment.get("Start City", ""),
                segment.get("Destination City", ""),
                segment.get("Distance/Time", "")
            ])

    print(f"CSV file successfully written to {output_filename}")


def new_vacation():
    start = input("Please enter your starting location\n")
    # Expecting comma-separated destinations
    dest_input = input("Please enter the location(s) you would like to visit (comma separated)\n")
    # Create a list of trimmed destination strings.
    destinations = [d.strip() for d in dest_input.split(",")]
    trip_obj = Trip(start, destinations)
    trip_obj.build_obj()
    rest = input("Would you like to find restaurants for the trip? [y/n]\n")
    if rest.lower() == 'y':
        food = input("What types of food do you like?\n")
        food_arr = food.split()
        food_obj = Food(trip_obj.destinations, food_arr)
        write_roadtrip_csv(food_obj.dict, trip_obj.get_travel_data())
    # Uncomment to send email once you're ready
    # send_email()


def openingScreen():
    print("Hello, welcome to MyRoadTrip Planner\n")
    print("Please enter which option you would like to explore:\n")
    print("1. Create new vacation")
    print("2. Look at previous vacations")
    option = input()
    if option.strip() == "1":
        new_vacation()
    # elif option.strip() == "2":
    #     previous_vacations()
    else:
        while option.strip() not in ["1", "2"]:
            print("Invalid Input. Please select one of the following choices:\n")
            print("1. Create new vacation")
            print("2. Look at previous vacations")
            option = input()
        if option.strip() == "1":
            new_vacation()
        # else:
        #     previous_vacations()


def main():
    openingScreen()


if __name__ == "__main__":
    main()
