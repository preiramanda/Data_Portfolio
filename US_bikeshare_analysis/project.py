import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def filters():
    """
    Function to specify filters in order to display analysis. It will require a city, month, and day to analyze it. 
    """
    print('\nHello! \nWe\'ll now explore some US bikeshare data.')

    while True:
        city = input("\nWhich city would you like to analyse? Insert New York, Chicago or Washington?\n")
        city = city.title()
        if city not in ('New York', 'Chicago', 'Washington'):
            print("\nSorry, I didn't quite understand. Please, type again.")
            continue
        else:
            break 

    while True:
      month = input("\nThis dataset contais information from 2017.\nWhich month you'd like to check?\nYou can choose from January to June, or type \'2017' for all months available.\n")
      month = month.title()
      if month not in ('January', 'February', 'March', 'April', 'May', 'June', '2017'):
        print("\nSorry, I didn't catch that. Please, type again.")
        continue
      else:
        break      
      
    while True:
      day = input("\nAre you looking for a particular day? If so, kindly enter the day as follows: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or type 'No' for all data.\n")
      day = day.title()
      if day not in ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', "No"):
        print("Sorry, I didn't catch that. Try again.")
        continue
      else:
        break

    return(city,month,day)


def load_data(city, month,day):

    """
    Loads data for the city by month, if specified.
    """
    df = pd.read_csv(CITY_DATA[city])  #filtering by city here
    df['Start Time'] = pd.to_datetime(df['Start Time']) 
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime('%A')

    
# filter by month if needed
    if month != '2017':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'No':
        #Filter by day of week
        df = df[df['day_of_week'] == day.title()]
    
    return(df) 


def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nTime insights:\n')

    if month == '2017':
        pmonth = df['month'].mode()[0]
        print('The highest number of trips occurred in the month ',pmonth )
    else:
       pass
    
    if day.title() not in('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'):
        pday = df['day_of_week'].mode()[0]
        print("Day with most bike rides: ",pday )
    else:
        pass

    df['hour'] = df['Start Time'].dt.hour
    phour = df['hour'].mode()[0]
    s = str(phour)
    am = ["1","2","3","4","5","6","7","8","9","10","11","12"]

    if s in am:
        print('The rush hour from the period was at: ', phour," AM" )
    else:
        print('The rush hour from the period was at: ', phour," PM" )
    
    print('-'*50)
    #return(phour,pmonth)

def users(df):
    """Statistics on Users."""
    yeart = datetime.datetime.now().year


    print('\nUser insights:\n')

    # checking if the columns exists in df:
    if 'Gender' in df.columns and 'Birth Year' in df.columns and 'User Type' in df.columns:
        # removing nulls:
        df_cleaned = df.dropna(subset=['Gender', 'Birth Year', 'User Type'])

        if not df_cleaned.empty:
            user_type = df_cleaned['User Type'].value_counts().idxmax()
            print('Most popular user types:', user_type)

            gender = df_cleaned['Gender'].value_counts().idxmax()
            print('Most popular gender:', gender)

            byear = df_cleaned['Birth Year'].value_counts().idxmax()
            print('Most of the users are ', yeart - round(byear) , " years old")
        else:
            print('No data available for user types, gender, and birth year.')
    else:
        print('One or more user info is null: No statistics available.')

    print('-'*50)


def station_stats(df):
    """Statistics of stations and trip."""

    print('\nLocation insights:\n')

    starts = df['Start Station'].value_counts().idxmax()
    print('Most popular departure station:', starts)

    ends = df['End Station'].value_counts().idxmax()
    print('\nThe station where the most of trips end is:', ends)

    print('-'*50)


def trip_duration_stats(df):
    """Statistics on trip duration."""

    print('\nTrip Insights:\n')

    total_time = sum(df['Trip Duration'])
    print('Total travel time:', round(total_time/86400), " Days")


    avg_time = df['Trip Duration'].mean()
    print('Average travel time:', round(avg_time/60), " Minutes")

    print('-'*50)


def display_data(df):
    
    start_loc = 0

    while True:
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()

        if view_data == 'yes':
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
        elif view_data == 'no':
            break  
        else:
            print("Please input 'yes' or 'no'.")

        continue_option = input("Do you wish to continue?: ").lower()
        if continue_option != 'yes':
            break


def main():
    while True:
        city, month, day = filters()
        df = load_data(city, month,day)
        time_stats(df, month,day)
        users(df)
        trip_duration_stats(df)
        station_stats(df)
        display_data(df)
        restart = input("\nType\'yes' to restart or \'enter' to finish\n")
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()







