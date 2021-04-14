import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
day_data = {'all': 7, 'monday': 0, 'tuesday': 1, 'wednesday': 2,
            'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}
month_data = {'all': 7, 'january': 1, 'february': 2,
              'march': 3, 'april': 4, 'may': 5, 'june': 6}


def get_filters():
    global day
    global month
    global city

    """
        Asks user to specify a city, month, and day to analyze.

        Returns:
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
            """
    print('Hello! Let\'s explore some US bikeshare data!')

    city = ''
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city not in CITY_DATA.keys():
        city = city.lower()
        if city in CITY_DATA.keys():
            break
        if city not in CITY_DATA.keys():
            city_keys = {'1': 'chicago',
                         "2": 'new york city', '3': 'washington'}
            city = city_keys[input(
                'what city you want to explore (enter city number) \n  1.chicago\n  2.new york city\n  3.washington  \n  ')]
    month_data = {'all': 7, 'january': 1, 'february': 2,
                  'march': 3, 'april': 4, 'may': 5, 'june': 6}

    month = ''
    while month not in month_data.keys():
        month = month.lower()
        if month in month_data.keys():
            break
        elif month not in month_data.keys():
            month = input(
                "what month are you intrested in january,february,...,june,for all months type all   ").lower()

    day_data = {'all': 7, 'monday': 0, 'tuesday': 1, 'wednesday': 2,
                'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}
    day = ''

    while day not in day_data.keys():
        day = day.lower()
        if day in day_data.keys():
            break
        elif day not in day_data.keys():
            day = input(
                "what day are you intrested in all, monday, tuesday, ... sunday   ").lower()

        # get user input for day of week (all, monday, tuesday, ... sunday)

    print('-'*80)
    print('calculating data................................')
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    month_data = {'all': 7, 'january': 1, 'february': 2,
                  'march': 3, 'april': 4, 'may': 5, 'june': 6}

    day_data = {'all': 7, 'monday': 0, 'tuesday': 1, 'wednesday': 2,
                'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}

    filename = CITY_DATA[city]
    df = pd.read_csv(filename)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].apply(lambda x: x.hour)
    df['month'] = df['Start Time'].apply(lambda x: x.month)
    df['day'] = df['Start Time'].dt.day_of_week
    if month != 'all':
        # use the index of the months list to get the corresponding int

        # filter by month to create the new dataframe
        df = df[df['month'] == month_data[month]]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day'] == day_data[day]]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        month_list = ['all', 'jan', 'feb', 'march', 'april', 'may', 'june']
        most_common_month = df['month'].mode()[0]
        print(f'The most common month is {month_list[most_common_month]}\n')

    # display the most common day of week
    if day == 'all':
        daylist = ['monday', 'tuesday', 'wednesday',
                   'thursday', 'friday', 'saturday', 'sunday']
        most_common_day = df['day'].mode()[0]
        print(f'The most common day is {daylist[most_common_day]}\n')
    # display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    if most_common_start_hour >= 12:
        most_common_start_hour = most_common_start_hour - 12
        print(f'The most common start hour is {most_common_start_hour} pm \n')
    else:
        print(f'The most common start hour is {most_common_start_hour} am \n')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most common start station is ', most_common_start_station)
    # display most commonly used end station
    most_common_End_station = df['End Station'].mode()[0]
    print('The most common end station is ', most_common_End_station)
    # display most frequent combination of start station and end station trip
    df['combo'] = df['Start Station']+" (to) "+df['End Station']
    most_common_combo = df['combo'].mode()[0]
    print(
        'The most common combinartion of Start and End satation is ', most_common_combo)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    htt, mintt = divmod(total_travel, 60)
    daytt, htt = divmod(htt, 24)
    monthtt, daytt = divmod(daytt, 30)
    yrstt, monthtt = divmod(monthtt, 12)
    print(
        f'The total travel time is {yrstt} year(s) {monthtt} month(s) , {daytt} day(S),{htt} hour(S) and {mintt} mins')
    print(f'{total_travel}in min')
    # display mean travel time
    average_travel = df['Trip Duration'].mean()
    print(f'The average travel time is {average_travel} min \n')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    usertypes = df['User Type'].value_counts()
    print(usertypes)
    # Display counts of gender
    if city == 'washington':
        print('No gender data available')
    else:
        genderstats = df['Gender'].value_counts()
        print(genderstats)

    # Display earliest, most recent, and most common year of birth
    if city == "washington":
        print('No birth year data available')

    else:
        oldest_member = df['Birth Year'].min()
        print(f'The oldest member is born in {oldest_member}\n')
        youngest_member = df['Birth Year'].max()
        print(f'The youngest member is born in {youngest_member}\n')
        common_year_ofbirth = df['Birth Year'].mode()[0]
        print(f'The most common year of birth is {common_year_ofbirth}\n')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
