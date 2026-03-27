import sys


def parse_nyt_data(file_path=''):
    """
    Parse the NYT covid database and return a list of tuples. Each tuple describes one entry in the source data set.
    Date: the day on which the record was taken in YYYY-MM-DD format
    County: the county name within the State
    State: the US state for the entry
    Cases: the cumulative number of COVID-19 cases reported in that locality
    Deaths: the cumulative number of COVID-19 death in the locality

    :param file_path: Path to data file
    :return: A List of tuples containing (date,county, state, fips, cases, deaths) information
    """
    
    # data point list
    data=[]

    # open the NYT file path
    try:
        fin = open(file_path)
    except FileNotFoundError:
        print('File ', file_path, ' not found. Exiting!')
        sys.exit(-1)

    # get rid of the headers
    fin.readline()

    # while not done parsing file
    done = False

    # loop and read file
    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        # format is date,county,state,fips,cases,deaths
        (date,county, state, fips, cases, deaths) = line.rstrip().split(",")

        # clean up the data to remove empty entries
        if cases=='':
            cases=0
        if deaths=='':
            deaths=0

        # convert elements into ints
        try:
            entry = (date,county,state, fips, int(cases), int(deaths))
        except ValueError:
            print('Invalid parse of ', entry)

        # place entries as tuple into list
        data.append(entry)


    return data

def first_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # When was the first positive COVID case in Rockingham County?
    # When was the first positive COVID case in Harrisonburg?
    :return:
    """

    # your code here
    rockingham_date = []
    harrisonburg_date = []
    for (date, county, state, fips, cases, deaths) in data:
        if county == 'Rockingham' and state == 'Virginia':
            rockingham_date.append((date,cases))
            first_case_rockingham = min(rockingham_date)
        elif county == 'Harrisonburg city' and state == 'Virginia':
            harrisonburg_date.append((date,cases))
            first_case_harrisonburg = min(harrisonburg_date)
    print('The first positive COVID case in Rockingham County was on ', first_case_rockingham)
    print('The first positive COVID case in Harrisonburg City was on ', first_case_harrisonburg)

    return

def second_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # What day was the greatest number of new daily cases recorded in Harrisonburg?
    # What day was the greatest number of new daily cases recorded in Rockingham County?
    :return:
    """

    # your code here
    rockingham_cases = []
    harrisonburg_cases = []
    for (date, county, state, fips, cases, death) in data:
        if county == 'Harrisonburg city' and state == 'Virginia':
            harrisonburg_cases.append((date,cases))
        elif county == 'Rockingham' and state == 'Virginia':
            rockingham_cases.append((date,cases))

    def find_max_cases(rockingham_cases, harrisonburg_cases):
        rockingham_cases = sorted(rockingham_cases, key=lambda x: x[0])
        harrisonburg_cases = sorted(harrisonburg_cases, key=lambda x: x[0])

        max_cases_rockingham = 0
        max_date_rockingham = ""
        max_cases_harrisonburg = 0
        max_date_harrisonburg = ""

        for i in range(1, len(rockingham_cases)):
            diff = int(rockingham_cases[i][1]) - int(rockingham_cases[i-1][1])
            if diff > max_cases_rockingham:
                max_cases_rockingham = diff
                max_date_rockingham = rockingham_cases[i][0]

        for i in range(1, len(harrisonburg_cases)):
            diff = int(harrisonburg_cases[i][1]) - int(harrisonburg_cases[i-1][1])
            if diff > max_cases_harrisonburg:
                max_cases_harrisonburg = diff
                max_date_harrisonburg = harrisonburg_cases[i][0]

        return (max_date_rockingham, max_cases_rockingham), (max_date_harrisonburg, max_cases_harrisonburg)

    (max_date_rockingham, max_cases_rockingham), (max_date_harrisonburg, max_cases_harrisonburg) = find_max_cases(rockingham_cases, harrisonburg_cases)

    print('The greatest number of new daily cases recorded in Harrisonburg City was on ', max_date_harrisonburg, ',', max_cases_harrisonburg)
    print('The greatest number of new daily cases recorded in Rockingham County was on ', max_date_rockingham, ',', max_cases_rockingham)

    return

def third_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # What was the worst 7-day period in either the city and county for new COVID cases?
    # This is the 7-day period where the number of new cases was maximal.
    :return:
    """
    
    # your code here
    rockingham_cases_week = []
    harrisonburg_cases_week = []
    for (date, county, state, fips, cases, death) in data:
        if county == 'Harrisonburg city' and state == 'Virginia':
            harrisonburg_cases_week.append((date,cases))
        elif county == 'Rockingham' and state == 'Virginia':
            rockingham_cases_week.append((date,cases))

    def find_max_cases(rockingham_cases_week, harrisonburg_cases_week):
        rockingham_cases_week = sorted(rockingham_cases_week, key=lambda x: x[0])
        harrisonburg_cases_week = sorted(harrisonburg_cases_week, key=lambda x: x[0])

        max_caseweek_rockingham = 0
        max_dateweek_rockingham = ""
        max_casesweek_harrisonburg = 0
        max_dateweek_harrisonburg = ""

        for i in range(7, len(rockingham_cases_week)):
            diff_week_r = int(rockingham_cases_week[i][1]) - int(rockingham_cases_week[i-7][1])
            if diff_week_r > max_caseweek_rockingham:
                max_caseweek_rockingham = diff_week_r
                max_dateweek_rockingham = (rockingham_cases_week[i][0], rockingham_cases_week[i-7][0])

        for i in range(7, len(harrisonburg_cases_week)):
            diff_week_h = int(harrisonburg_cases_week[i][1]) - int(harrisonburg_cases_week[i-7][1])
            if diff_week_h > max_casesweek_harrisonburg:
                max_casesweek_harrisonburg = diff_week_h
                max_dateweek_harrisonburg = (harrisonburg_cases_week[i][0], harrisonburg_cases_week[i-7][0])

        return (max_dateweek_rockingham, max_caseweek_rockingham), (max_dateweek_harrisonburg, max_casesweek_harrisonburg)

    (max_dateweek_rockingham, max_caseweek_rockingham), (max_dateweek_harrisonburg, max_casesweek_harrisonburg) = find_max_cases(rockingham_cases_week, harrisonburg_cases_week)

    print('The worst week in Harrisonburg City for new cases was from ', max_dateweek_harrisonburg, ',', max_casesweek_harrisonburg)
    print('The worst week in Rockingham County for new cases was from ', max_dateweek_rockingham, ',', max_caseweek_rockingham)

    return

if __name__ == "__main__":
    data = parse_nyt_data('us-counties.csv')

    #for (date,county, state, fips, cases, deaths) in data:
        #print('On ', date, ' in ', county, ' ', state, ' there were ', cases, ' cases and ', deaths, ' deaths')


    # write code to address the following question: Use print() to display your responses.
    # When was the first positive COVID case in Rockingham County?
    # When was the first positive COVID case in Harrisonburg?
    first_question(data)


    # write code to address the following question: Use print() to display your responses.
    # What day was the greatest number of new daily cases recorded in Harrisonburg?
    # What day was the greatest number of new daily cases recorded in Rockingham County?
    second_question(data)

    # write code to address the following question: Use print() to display your responses.
    # What was the worst seven day period in Harrisonburg for new COVID cases (in terms of absolute number of cases)?
    # What was the worst seven day period in Rockingham County for new COVID cases (in terms of absolute number of cases)?
    third_question(data)


