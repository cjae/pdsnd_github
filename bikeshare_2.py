import sys
import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'c': 'chicago.csv',
    'n': 'new_york_city.csv',
    'w': 'washington.csv' 
}

DEFAULT_VALUE = 'all'
DAYS_DATA = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
MONTHS_DATA = [
    'january', 'february', 'march', 'april', 'may', 'june',
    'july', 'august', 'september', 'october', 'november', 'december'
]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    while True:
        print('\nWhich city would you like to see data for?')
        city = input("Enter C for Chicago, N for New york or W for Washington: ").lower().strip()
        if city in CITY_DATA:
            break
        elif city == 'q':
            sys.exit("User quits program")
        else:
            print("Invalid input. Please choose a valid city or Q to quit.")

    while True:
        print('\nWould you like to filter the data by month, day, both or none at all?')
        data_filter = input("Enter M for month, D for day, B for both or \"none\" for no filter: ")
        data_filter = data_filter.lower().strip()
        if data_filter in ['m', 'd', 'b', 'none']:
            break
        elif city == 'q':
            sys.exit("User quits program")
        else:
            print("Invalid input. Please choose a valid filter or Q to quit.")

    if data_filter == 'm':
        month = get_month_input()
        day = DEFAULT_VALUE
    elif data_filter == 'd':
        month = DEFAULT_VALUE
        day = get_day_input()
    elif data_filter == 'b':
        month = get_month_input()
        day = get_day_input()
    else:
        month = DEFAULT_VALUE
        day = DEFAULT_VALUE

    print('-'*40)
    return city, month, day

def get_month_input():
    """
    Asks user to specify month

    Returns:
        (str) month - name of the month to filter by, or "all" to apply no month filter
    """
    # Get user input for month (all, january, february, ... , june)
    while True:
        month_input = input(
            '\nWhich month would you like to filter by? '
            'Enter the full month name or its abbreviation (e.g., "January" or "Jan"): '
        ).lower().strip()
        if month_input in MONTHS_DATA or month_input[:3] in [month[:3] for month in MONTHS_DATA]:
            # Check if the input is either a full month name or its abbreviation
            month = next((m for m in MONTHS_DATA if m.startswith(month_input[:3])), None)
            if month:
                return month
        elif month_input == DEFAULT_VALUE:
            return DEFAULT_VALUE
        elif month_input == 'q':
            sys.exit("User quits program")
        else:
            print(
                'Invalid input. Please enter a valid month '
                'or \'all\' to apply no filter or \'Q\' to quit.'
            )

def get_day_input():
    """
    Asks user to specify day

    Returns:
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_input = input(
            '\nWhich day of the week would you like to filter by? '
            'Enter the full day name or its abbreviation (e.g., "Monday" or "Mon"): '
        ).lower().strip()
        if day_input in DAYS_DATA or day_input[:3] in [day[:3] for day in DAYS_DATA]:
            # Check if the input is either a full day name or its abbreviation
            day = next((d for d in DAYS_DATA if d.startswith(day_input[:3])), None)
            if day:
                return day
        elif day_input == DEFAULT_VALUE:
            return DEFAULT_VALUE
        elif day_input == 'q':
            sys.exit("User quits program")
        else:
            print(
                'Invalid input. Please enter a valid day of the week '
                'or \'all\' to apply no filter or \'Q\' to quit.'
            )

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        data_frame - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    data_frame = pd.read_csv(CITY_DATA[city])

    # Rename the first column
    data_frame = data_frame.rename(columns={'Unnamed: 0': 'Id'})

    # convert the Start Time column to datetime
    data_frame['Start Time'] = pd.to_datetime(data_frame['Start Time'])

    # extract month and day of week from Start Time to create new columns
    data_frame['month'] = data_frame['Start Time'].dt.month
    data_frame['day_of_week'] = data_frame['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != DEFAULT_VALUE:
        # use the index of the months list to get the corresponding int
        month = MONTHS_DATA.index(month) + 1

        # filter by month to create the new dataframe
        data_frame = data_frame[data_frame['month'] == month]

    # filter by day of week if applicable
    if day != DEFAULT_VALUE:
        # filter by day of week to create the new dataframe
        data_frame = data_frame[data_frame['day_of_week'] == day.title()]

    return data_frame

def time_stats(data_frame, month, day):
    """
    Displays statistics on the most frequent times of travel

    Args:
        (DataFrame) - Pandas DataFrame containing city data filtered by month and day
        (str) month - name of the month to use, or "all" to ignore calculation
        (str) day - name of the day of week to use, or "all" to ignore calculation
    """
    print('\nCalculating The Most Frequent Times of Travel...')
    if DEFAULT_VALUE not in {month, day}:
        print(f"For the month of {month.title()} and day of the week: {day.title()}.\n")
    elif month != DEFAULT_VALUE:
        print(f"For the month of {month.title()}.\n")
    elif day != DEFAULT_VALUE:
        print(f"For day of the week: {day.title()}.\n")
    else:
        print()

    start_time = time.time()

    # display the most common month
    if month == DEFAULT_VALUE:
        popular_month = data_frame['month'].mode()[0]
        popular_month_count = data_frame['month'].value_counts().max()
        month_value = MONTHS_DATA[popular_month - 1].title()
        print(f"The most common month is: {month_value}, Count: {popular_month_count}")

    # display the most common day of week
    if day == DEFAULT_VALUE:
        popular_day = data_frame['day_of_week'].mode()[0]
        popular_day_count = data_frame['day_of_week'].value_counts().max()
        print(f"The most common day of week is: {popular_day}, Count: {popular_day_count}")

    # display the most common start hour
    data_frame['hour'] = data_frame['Start Time'].dt.hour
    popular_hour = data_frame['hour'].mode()[0]
    popular_hour_count = data_frame['hour'].value_counts().max()
    print(f"The most common hour is: {popular_hour}, Count: {popular_hour_count}")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*40)

def station_stats(data_frame):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        (DataFrame) - Pandas DataFrame containing city data filtered by month and day
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = data_frame['Start Station'].mode()[0]
    start_station_count = data_frame['Start Station'].value_counts().max()
    print(f"The most used start station is: {popular_start_station}, Count: {start_station_count}")

    # display most commonly used end station
    popular_end_station = data_frame['End Station'].mode()[0]
    end_station_count = data_frame['End Station'].value_counts().max()
    print(f"The most used end station is: {popular_end_station}, Count: {end_station_count}")

    # display most frequent combination of start station and end station trip
    # idxmax() returns a Series with the index of the maximum value for each column
    station_combination = data_frame.groupby(['Start Station', 'End Station']).size().idxmax()
    trip_count = data_frame.groupby(['Start Station', 'End Station']).size().max()
    trip_comb = f"{station_combination[0]} - {station_combination[1]}"
    print(f"The most used start station and end station is: {trip_comb}, Count: {trip_count}")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*40)

def trip_duration_stats(data_frame):
    """
    Displays statistics on the total and average trip duration

    Args:
        (DataFrame) - Pandas DataFrame containing city data filtered by month and day
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = data_frame['Trip Duration'].sum()
    travel_time_count = data_frame['Trip Duration'].value_counts().sum()
    print(f"The total trip duration is: {total_travel_time}, Count: {travel_time_count}")

    # display mean travel time
    avg_travel_time = data_frame['Trip Duration'].mean()
    print(f"The average trip duration is: {avg_travel_time}")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*40)

def user_stats(data_frame):
    """
    Displays statistics on bikeshare users.

    Args:
        (DataFrame) - Pandas DataFrame containing city data filtered by month and day
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = data_frame['User Type'].value_counts()
    print("Available user types and count")
    for user_type, count in user_types.items():
        print(f"{user_type}: {count}")

    # Display counts of gender
    if 'Gender' in data_frame:
        print("\nAvailable genders and count")
        gender_types = data_frame['Gender'].value_counts()
        for gender, count in gender_types.items():
            print(f"{gender}: {count}")
    else:
        print("\nNo gender data to share.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in data_frame:
        earliest_birth_year = int(data_frame['Birth Year'].min())
        print(f"\nEarliest Birth Year: {earliest_birth_year}")

        most_recent_birth_year = int(data_frame['Birth Year'].max())
        print(f"Most Recent Birth Year: {most_recent_birth_year}")

        common_birth_year = int(data_frame['Birth Year'].mode()[0])
        print(f"Most Common Birth Year: {common_birth_year}")
    else:
        print("\nNo birth year data to share.")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*40)

def display_raw_data(data_frame):
    """
    Displays raw data to user in batch of 5 rows

    Args:
        (DataFrame) - Pandas DataFrame containing city data filtered by month and day
    """
    user_input = input(
        '\nWould you like to the first 5 lines of raw data? Enter "yes" or "no": '
    ).strip().lower()

    if user_input == 'yes':
        start_index = 0
        batch_size = 5

        while start_index < len(data_frame):
            display_data = data_frame.iloc[start_index:start_index + batch_size]
            print(display_data.to_string(index=False))

            # Ask the user if they want to see more raw data
            user_input = input(
                '\nPress "Enter" to see more raw data, or enter any other key to quit: '
            ).strip().lower()

            if not user_input:
                start_index += batch_size
            else:
                break

    print('-'*40)

def main():
    """Main method: Program Starts Here"""

    while True:
        city, month, day = get_filters()

        print('\nJust one moment... loading the data')
        data_frame = load_data(city, month, day)
        print('\nData loaded. Now appling filters...')
        print('-'*40)

        time_stats(data_frame, month, day)
        station_stats(data_frame)
        trip_duration_stats(data_frame)
        user_stats(data_frame)
        display_raw_data(data_frame)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
