import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import datetime
import requests

from c0001_retrieve_meta import retrieve_path


def scrape_trials():
    """
    Objective: Query NIH Clinical Trials repository to database relevant trials
    Query terms taken from a text file saved in user_provided folder

    Tasks:
        (1) Scrape clinicaltrials.gov using terms in a saved file
        (2)
        (3)
        (4)
    """

    print("running retireve_trials")

    tasks = [1]

    if 1 in tasks: scrape_clinical_trials()

    print("completed retireve_trials")







def scrape_clinical_trials():
    """

    """

    # Pull query terms from a clinicalTrials.gov
    # query_terms = retrieve_path('search_terms_nih_clinical_trials')
    df = pd.read_csv(retrieve_path('search_terms_nih_clinical_trials'))
    query_terms = list(df['search_terms'])

    stop_term = '<NStudiesReturned>0</NStudiesReturned>'
    stop_term_json = '"NStudiesReturned":0'

    # select file_extension: either json or xml
    file_type = 'json'

    for term in query_terms:

        print('term = ' + term)

        trials_path = retrieve_path('trials_path')
        trials_path = os.path.join(trials_path, term + '.' + file_type)

        print('trials_path = ' + trials_path)

        f = open(trials_path, "w")
        f.close()
        f = open(trials_path, "w")
        f.write('{')
        f.close()

        for i in range(3000):

            if ' ' in term: term.replace(' ', '+')

            url = 'https://clinicaltrials.gov/api/query/full_studies?expr='
            url = url  + str(term)
            url = url  + str('&min_rnk=') + str(i)
            url = url  + str('&max_rnk=' + str(i+1) + '&fmt=')
            url = url + file_type
            print('url = ' + str(url))

            # request contents from link
            r = requests.get(url)
            # j = r.json()

            text = r.text
            # print(text)

            if stop_term in str(text) or stop_term_json in str(text):
                save_count(term, i)
                print('end found at i = ' + str(i))
                break

            trials_path = retrieve_path('trials_path')
            trials_path = os.path.join(trials_path, term + '.' + file_type)
            f = open(trials_path, "a")
            f.write('"Trial":' )
            f.write('{')
            f.write('"URL":' + url + ',' )
            f.write('"SearchTerm":' + term + ',' )
            f.write('"Rank":' + str(i) + ',' )
            f.write(text)
            f.write('}')
            f.close()

    trials_path = retrieve_path('trials_path')
    trials_path = os.path.join(trials_path, term + '.' + file_type)
    f = open(trials_path, "a")
    f.write('}')
    f.close()



def save_count(description, count):
    """
    Save the number of queries found for the term
    """

    now = datetime.datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)

    trial_count = retrieve_path('trial_count')
    f = open(trial_count, "a")
    f.write("\n")
    f.write(str(dt_string) + ' , ' + description + ' , ' + str(count))
    f.close()


if __name__ == "__main__":
    main()
