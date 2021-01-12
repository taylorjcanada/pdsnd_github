import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=''
    city_options=['chicago','washington','new_york_city']
    while city not in city_options:
        print("Which city would you like data from? The options are Chicago, New York City, or Washington.")
# The .lower makes all letter lower case, in case the user capitalizes anything
        city=input().lower()
# This replaces the space in 'New York' to an underscore for proper use later on
        city=city.replace(' ','_')
        
        if city not in city_options:
            print('Please enter a valid city.')
        
    # TO DO: get user input for month (all, january, february, ... , june)
    month=''
    month_options=['all','january','february','march','april','may','june','july','august','september','october','november','december']
    while month not in month_options:
        
        print("Which month would you like data for? You can also put 'All' to get data for all months.")
        month=input().lower()
        
        if month not in month_options:
            print("Please enter a valid option.")
            
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day=''
    day_options=['All','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    while day not in day_options:
        print("What day of the week would you like data for? You can also put 'All' to get data for every day of the week.")
        day=input().title()
        
        if day not in day_options:
            print("Please enter a valid option.")

    print('You have chosen: ' + city.title() + ', ' + month.title() + ', ' + day)
    print('-'*40)
    
    #changing month to number to match data in dataframe
    month=month_options.index(month)
    #print(month)
    
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
    #getting data into dataframe
    city_file=city+'.csv'
    df=pd.read_csv(city_file)
    
    #changing start time to date time formart
    df['Start Time']=pd.to_datetime(df['Start Time'])
    
    #adding month column
    df['month']=df['Start Time'].dt.month
    
    #adding day column to filter on
    df['weekday']=df['Start Time'].dt.weekday_name
    
    #adding hour column for later calculation
    df['hour']=df['Start Time'].dt.hour
    
    pd.set_option('display.max_columns', None)
    columns=df.head()
    #print(columns)
    
    #filtering where neccesary
    if month != 0:
        df=df[df['month'] == month]
        
    if day != 'All':
        df=df[df['weekday'] == day]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month=df['month'].mode()
    months=['all','january','february','march','april','may','june','july','august','september','october','november','december']
    print('The most common month is:')
    print(months[common_month[0]].title())

    # TO DO: display the most common day of week
    common_day=df['weekday'].mode()
    print('The most common day of the week is: ')
    print(common_day[0])

    # TO DO: display the most common start hour
    common_hour=df['hour'].mode()
    print('The most common hour is: ')
    if common_hour[0] > 12:
        pm_hour=common_hour[0]-12
        print('{}:00 PM'.format(pm_hour))
        
    else:
        print('{}:00 AM'.format(common_hour[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start=df['Start Station'].mode()
    print('The most common starting station is: ')
    print(common_start[0])

    # TO DO: display most commonly used end station
    common_end=df['End Station'].mode()
    print('The most common ending station is: ')
    print(common_end[0])

    # TO DO: display most frequent combination of start station and end station trip
    df['Start to End']=df['Start Station'] + ' to ' + df['End Station']
    common_startend=df['Start to End'].mode()
    print('The most common start and end combination is: ')
    print(common_startend[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel=df['Trip Duration'].sum()
    days = total_travel // (24*60*60)
    seconds = total_travel % (24*60*60)
    hours = seconds // (60*60)
    seconds = seconds % (60*60)
    minutes = seconds // (60)
    seconds = seconds % (60)
    print('The total travel time is {} days, {} hours, {} minutes, and {} seconds.'.format(days,hours,minutes,seconds))

    # TO DO: display mean travel time
    mean_travel = df['Trip Duration'].mean()
    days = mean_travel // (24*60*60)
    seconds = mean_travel % (24*60*60)
    hours = seconds // (60*60)
    seconds = seconds % (60*60)
    minutes = seconds // (60)
    seconds = seconds % (60)
    print('The average travel time is {} hours, {} minutes, and {} seconds.'.format(hours,minutes,seconds))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_counts=df['User Type'].value_counts()
    print('The count of each user type is:')
    print(user_counts)

    # TO DO: Display counts of gender
    pd.set_option('display.max_columns', None)
    columns=df.columns.tolist()
    if 'Gender' in columns:
        gender_counts=df['Gender'].value_counts()
        print('The count of each gender is:')
        print(gender_counts)
    else:
        print('Gender columns does not exist for this city')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in columns:
        oldest=df['Birth Year'].min()
        youngest=df['Birth Year'].max()
        common_year=df['Birth Year'].mode()
        print('Birth year stats:')
        print('The earliest birth year is: {}'.format(oldest))
        print('The most recent birth year is: {}'.format(youngest))
        print('The most common birth year is: {}'.format(common_year[0]))
    else:
        print('There is no birth year data for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    #Ask user if they want to see raw user data
    display_data='yes'
    while display_data=='yes':
        print("Would you like to see 5 rows of raw data? Please enter 'yes' or 'no'.")
        display_data=input().lower()
        
        if display_data not in ['yes','no']:
            print("Incorrect input entered, please enter 'yes' or 'no'.")
            display_data=input().lower()
        elif display_data=='yes':
            print(df.head())
        else:
            print("You have chosen not to display raw data.")
        #ask if they want to see additional data
        while display_data=='yes':
            print("Would you like to see an additional 5 rows of data?")
            display_data=input().lower()
            count=0
            
            if display_data not in ['yes','no']:
                print("Incorrect input entered, please enter 'yes' or 'no'.")
                display_data=input().lower()
            elif display_data=='yes':
                count+=5
                print(df[count:count+5])
            else:
                print("You have chosen not to display additional raw data.")
            


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
