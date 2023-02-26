import time
import pandas as pd
import calendar

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def print_raw_data(data):
    '''Displays the RAW Data from dataframe '''
    line_counter = 0
    while True:
        print(data[line_counter: line_counter+5])
        line_counter += 5
        answer = input("Show more lines? yes/no \nDefault: yes: ").lower()
        if answer == "no":
            break


def print_iterative(c_name, df):
    """ Displays content iterative to reduce printing statements and have a clear look
    Args
        c_name: Column name and printing titel
        df: dataframe to sow
    """
    print("Counts of user {}: ".format(c_name))
    data = df[c_name].value_counts()
    if data.index[0] != 0:
        for index, count in enumerate(data):
            print("\t{}: {}".format(data.index[index], count))
    else:
        print("\t0: 0")


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    while True:
        city = input("please insert city name or the first latter of the name"
                     "\n(chicago, nyc for new york city or washington or the first latter): ")
        if city.lower() in ["c", "n", "w", "nyc"]:
            city_short_dict = {'c': 'Chicago',
                               'n': 'New York City',
                               'nyc': 'New York City',
                               'w': 'Washington'}
            city = city_short_dict[city.lower()]

        if city.lower() in CITY_DATA.keys():
            print("you choosed: {}".format(city))
            break
        else:
            print("\ninput not known, please retry\n\n")

    # get user input for month (all, january, february, ... , june)
    month_list = [calendar.month_name[i] for i in range(1, 13)]
    month_list.append("all")
    while True:
        month = input("please input the month you want to view or all to view all month \n{}: ".format(month_list))
        if month.lower() in list(map(lambda x: x.lower(), month_list)):
            print("you choosed: {}".format(month))
            break
        else:
            print("\ninput not known, please retry\n\n")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_list = [calendar.day_name[i] for i in range(0, 7)]
    day_list.append("all")
    while True:
        day = input("please input the day you want to view or typw all to view all days \n{}: ".format(day_list))
        if day.lower() in list(map(lambda x: x.lower(), day_list)):
            print("you choosed: {}".format(day))
            break
        else:
            print("\ninput not known, please retry\n\n")

    print('-' * 40)
    return city, month, day


def filter_data(data_dict, city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (dict) data_dict - dictionary with city data
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print("filtering data")
    df = data_dict[city.lower()]
    if month != "all":
        df = df.loc[df["month_name"] == month]
    if day != "all":
        df = df.loc[df["day_name"] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month_name'].value_counts().idxmax()
    print("The most common month is: {}".format(most_common_month))

    # display the most common day of week
    most_common_day_of_week = df['day_name'].value_counts().idxmax()
    print("The most common day of week is: {}".format(most_common_day_of_week))

    # display the most common start hour
    most_common_start_hour = df['hour'].value_counts().idxmax()
    print("The most common start hour is: {:.0f}".format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station: {}".format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station: {}".format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    most_common_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print("The most commonly used start station and end station : {}, {}" \
          .format(most_common_start_end_station[0], most_common_start_end_station[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    trip_duration = df['Trip Duration']

    # display total travel time
    total_travel = trip_duration.sum()
    print("Total travel time: {}".format(total_travel))

    # display mean travel time
    mean_travel = trip_duration.mean()
    print("Mean travel time: {}".format(mean_travel))

    # display mean travel time
    max_travel = trip_duration.max()
    print("Max travel time: {}".format(max_travel))

    # display the total trip duration for each user type
    print("\nTravel time for each user type:")
    group_by_user_trip = df.groupby(['User Type']).sum(numeric_only=True)['Trip Duration']
    for index, user_trip in enumerate(group_by_user_trip):
        print("\t{}: {}".format(group_by_user_trip.index[index], user_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    c_name = 'User Type'
    print_iterative(c_name, df)

    if 'Gender' in df.columns:
        # Display counts of gender
        c_name = 'Gender'
        print_iterative(c_name, df)

    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        birth_year = df['Birth Year']

        # the most common birth year
        most_common_year = birth_year.value_counts().idxmax()
        print("The most common birth year: {:.0f}".format(most_common_year))

        # the most recent birth year
        most_recent = birth_year.max()
        print("The most recent birth year: {:.0f}".format(most_recent))

        # the most earliest birth year
        earliest_year = birth_year.min()
        print("The most earliest birth year: {:.0f}".format(earliest_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def read_all_csv(data_dict):
    ''' reads input from all CSV files in the dictionary
    this will speedup the process when doing multiple requests, but more memory is needed
    Caution:
        reading all files to the memory could lead to memory problems in bigger environements,
        based on these three sets there should be no problem.
    argument:
        (dict) data_dict - a dirctionary of "citynames" and its correspondig CSV file
    Returns:
        dict of Filenames
    '''
    print("reading data from csv")
    ret_var = {}
    for key in data_dict.keys():
        ret_var[key] = pd.read_csv(data_dict[key])
    return ret_var


def extend_data(data_dict):
    ''' Extend all dataframes with month_name and day_name for faster filtering in later processes

    argument:
        (dict) data_dict - a dirctionary of "citynames" and its correspondig dataframes
    Returns:
        the data_dict with extended columns for faster filtering
    '''
    print("extending data")
    for key in data_dict.keys():
        data_dict[key]["month_name"] = pd.to_datetime(data_dict[key]["Start Time"]).dt.month_name()
        data_dict[key]["day_name"] = pd.to_datetime(data_dict[key]["Start Time"]).dt.day_name()
        data_dict[key]["hour"] = pd.to_datetime(data_dict[key]["Start Time"]).dt.hour
    return data_dict


def main():
    # -> reduce reads in later requests, Could be problematic by big datasets
    print('####################################\nHello! Let\'s explore some US bikeshare data!')
    print("but first let me load and prepare all date... ")
    all_data_dict = read_all_csv(CITY_DATA)
    all_data_dict = extend_data(all_data_dict)
    print("\nData loaded and prepared. Have fun and good luck\n")

    while True:
        city, month, day = get_filters()
        df = filter_data(all_data_dict, city, month, day)
        if df.empty:
            df.loc[0]=[0]*len(df.columns)
        
        try:
            time_stats(df)
        except ValueError as e:
            print("Time State could not be calculated, Missing data for choosen input")
        try:
            station_stats(df)
        except ValueError as e:
            print("Station Stats could not be calculated, Missing data for choosen input")
        try:
            trip_duration_stats(df)
        except ValueError as e:
            print("Time State could not be calculated, Missing data for choosen input")
        try:
            user_stats(df)
        except ValueError as e:
            print("user stats could not be calculated, Missing data for choosen input")

        request = input("do you want to see 5 lines of raw data? yes or no ").lower()
        if request == 'yes':
            print_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
    main()
