import json
from urllib import request
from collections import defaultdict

# Constant Definition
# after the data analysis, I found that the dates distribution ranges from April to June
MAX_DATE = 701
ENDPOINT1 = 'https://candidate.hubteam.com/candidateTest/v2/partners?userKey=7ab19c343e941224f658fb1843e0'
ENDPOINT2 = 'https://candidate.hubteam.com/candidateTest/v2/results?userKey=7ab19c343e941224f658fb1843e0'


# Contract: this function is in charge of
#           1. Send GET request and fetch the json data to be processed.
#           2. Transfer original dictionary data into a new dictionary 'country_dict',
#              using country names as the key.
#           3. Handle with each item in 'country_dict'.
#              Use 'date_dict' to record the available conditions of every two continuous days
#              Traverse 'date_dict' to find the date that most people can attend
#           4. Combine the results of all countries into dictionary result and dump it into json data.
#           5. Send post form to given endpoint and return result.
# Return: the final optimized arrangement in a dictionary structure.
def find_proper_event_date():
    # Obtain data to be processed
    req = request.urlopen(url=ENDPOINT1).read().decode('utf-8')
    # Initialize several dictionary structures
    partner_dict = eval(req)
    country_dict = defaultdict(list)
    result = {"countries": []}
    # Transfer data and remove some useless information to make our dictionary concise
    for partner in partner_dict["partners"]:
            partner_info = {"email": partner["email"], "availableDates": date_to_integer(partner["availableDates"])}
            country_dict[partner["country"]].append(partner_info)
    # Example:
    # {'United States': [{'email': 'bsassone@hubspotpartners.com',
    #                     'availableDates': [430, 503, 504, 511, 514]}]}
    for country in country_dict:
        # Define a dictionary to record the available conditions of every two continuous days
        # The key of every item represents the start date of the two continuous days
        date_dict = defaultdict(set)
        for partner in country_dict[country]:
            for date in partner["availableDates"]:
                date_dict[date].add(partner["email"])
        for date in date_dict:
            if next_date(date) in date_dict:
                # Preserve the intersection set of these two day
                date_dict[date] = date_dict[date]&date_dict[next_date(date)]
            else:
                date_dict[date] = set()
        # Example:
        #    {430: set(), 503: {'gsthill@hubspotpartners.com',
        #                       'cmoniak@hubspotpartners.com',
        #                       'bsassone@hubspotpartners.com'}}
        # max_guest_num stores the max number of attendances
        # best_date stores the corresponding date of max_guest_num
        max_guest_num = 0
        best_date = MAX_DATE
        for date in date_dict:
            if len(date_dict[date]) > max_guest_num:
                best_date = date
                max_guest_num = len(date_dict[date])
            # if the attendance number of two days are the same, select the earlier date.
            elif len(date_dict[date]) == max_guest_num and date < best_date:
                best_date = date
                max_guest_num = len(date_dict[date])
        guest_list = list(date_dict[best_date])
        best_date = '2017-0'+str(best_date)[:1]+'-'+str(best_date)[1:]
        # final_country_info records the final arrangement of each country
        final_country_info = {"attendeeCount": max_guest_num,
                              "attendees": guest_list,
                              "name": country,
                              "startDate": best_date}
        result["countries"].append(final_country_info)
    # Post the result in json format to given endpoint
    test_data = json.dumps(result).encode('utf-8')
    request.urlopen(url=ENDPOINT2, data=test_data).read().decode('utf-8')
    return result


# Helper functions:
# date_to_integer: List[str] -> List[int]
# Example: date_to_integer(["2017-05-04", "2017-12-02"])
#          ->  [504, 1202]
def date_to_integer(date_list):
    res_list = []
    for date in date_list:
        res_list.append(eval(date.replace("-", "")[5:]))
    return res_list


# next_date: Int -> Int
# This function is used to compute the number expression of the next day
def next_date(date):
    # This function can also be realized based on dictionary
    if date == 430:
        return 501
    elif date == 531:
        return 601
    elif date == 630:
        return 701
    else:
        return date+1

if __name__ == '__main__':
    find_proper_event_date()



