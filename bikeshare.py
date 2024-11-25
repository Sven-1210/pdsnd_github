# Import necessary python modules
import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

# Creates function which defines the filters
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington).
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington? ").lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print("City does not exist. Please enter either 'Chicago', 'New York City', or 'Washington'.")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month? January, February, March, April, May, June, or 'all' to apply no month filter: ").lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print("Invalid input. Please enter a month from January to June, or 'all'.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which day? Please type a day (e.g., 'Monday', 'Tuesday', etc.) or 'all' to apply no day filter: ").lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print("Invalid input. Please enter a day of the week, or 'all'.")

    print('-'*40)
    return city, month, day
# Creates function load_data with three input parameters (city, month, day)
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1  # +1 because index is 0-based but months are 1-based
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day]
    
    return df

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most Popular Start Month:', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Start Day of Week:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['station_combination'] = df['Start Station'] + " to " + df['End Station']
    popular_station_combination = df['station_combination'].mode()[0]
    print('Most Popular Trip:', popular_station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """
    Displays statistics on bikeshare users.
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_counts = df['User Type'].value_counts()
    print('User Types:\n', user_types_counts)

    # Display counts of gender (if available)
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('\nGender Counts:\n', gender_counts)
    else:
        print("Gender data is not available for this city.")

    # Display earliest, most recent, and most common year of birth (if available)
    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        print('\nEarliest Year of Birth:', earliest_year)
        print('Most Recent Year of Birth:', most_recent_year)
        print('Most Common Year of Birth:', most_common_year)
    else:
        print("Birth Year data is not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_rows(df):
    """
    Displays rows of the dataset based on user preference.
    """
    while True:
        direction = input("Would you like to view the first or bottom 5 rows of the dataset? Enter 'first', 'bottom', or 'no' to skip: ").lower()
        if direction not in ['first', 'bottom', 'no']:
            print("Invalid input. Please enter 'first', 'bottom', or 'no'.")
        elif direction == 'no':
            break
        else:
            start_loc = 0 if direction == 'first' else -5
            while True:
                if direction == 'first':
                    print(df.iloc[start_loc:min(start_loc + 5, len(df))])
                else:  # Handling 'bottom' with negative slicing
                    print(df.iloc[max(len(df) + start_loc, 0):len(df) + start_loc + 5])
                
                start_loc += 5 if direction == 'first' else -5
                if start_loc >= len(df) or len(df) + start_loc <= 0:
                    print("You've reached the end of the dataset.")
                    break
                
                view_display = input("Do you wish to see the next 5 rows? Enter 'yes' or 'no': ").lower()
                if view_display != 'yes':
                    break
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_rows(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()