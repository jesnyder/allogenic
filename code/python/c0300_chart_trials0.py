import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import requests
from bs4 import BeautifulSoup
import pprint

from c0101_retrieve_clinical import retrieve_clinical
from c0201_query_patents import query_patents

def chart_trials():
    """

    """

    tasks = [2]

    # collect metadata for each clinical trial
    if 1 in tasks: collect_metadata_clinical()
    if 2 in tasks: refine_trials()




def refine_trials():
    """
    Remove Terminated trials
    """

    ref_path = os.path.join( 'data', 'meta')
    ref_file = os.path.join(ref_path, 'clinical' + 'All' + '.csv')
    df = pd.read_csv(ref_file)

    # drop duplicates using url
    df = df.drop_duplicates(subset=['url'])

    # remove terminated trials
    print('len(overall_status) = ' + str(len(list(df['Overall_status']))))
    df =  df[(df['Overall_status'] != "Terminated")]
    df =  df[(df['Overall_status'] != "Withdrawn")]
    df =  df[(df['Overall_status'] != "Suspended")]

    uniqueOveralStatus = np.unique(list(df['Overall_status']))
    print('uniqueOveralStatus = ')
    print(uniqueOveralStatus)

    print('len(overall_status) = ' + str(len(list(df['Overall_status']))))

    ref_file = os.path.join(ref_path, 'clinical' + 'All_withoutTerminated' + '.csv')
    df.to_csv(ref_file)

    Start_date = list(df['Start_date'])
    # print('Start_date = ')
    # print(Start_date)

    dfAll = pd.DataFrame()

    years = ['2021', '2022', '20223']

    for year in years:

        starts = list(df['Start_date'].str.contains(year))
        # print(starts)
        print('len(starts) = ' + str(len(starts)))
        df['starts'] =   starts
        dfnew =  df[(df['starts'] == True)]
        print(dfnew)

        dfAll = dfAll.append(dfnew)

        print(dfAll)


    # df = dfAll
    #print('len(overall_status) = ' + str(len(list(df['Overall_status']))))

    print('dfAll = ')
    print(dfAll)

    searchTerm = list(dfAll['searchTerm'])
    print('len(searchTerm) = ' + str(len(searchTerm)))

    uniqueSearchTerms = np.unique(searchTerm)
    print('uniqueSearchTerms = ')
    print(uniqueSearchTerms)

    for term in uniqueSearchTerms:

        dfTerm =  dfAll[(dfAll['searchTerm'] == term)]
        listTerm = list(dfTerm['searchTerm'])
        print(term + 'listTerm = ' + str(len(listTerm)))


    ref_file = os.path.join(ref_path, 'clinical' + 'All_withoutTerminated' + '_Recent' + '.csv')
    dfAll.to_csv(ref_file)










def collect_metadata_clinical():
    """

    """

    df_allTerms = pd.DataFrame()

    search_terms = []
    search_terms.append('MesenchymalExosome')
    search_terms.append('GeneticEngineering')
    search_terms.append('MesenchymalAllogenic')
    search_terms.append('MesenchymalAutologous')
    search_terms.append('iPSC')
    search_terms.append('Mesenchymal')

    for term in search_terms:

        # retrieve clinical trial data
        ref_path = os.path.join( 'data', 'source')
        ref_file = os.path.join(ref_path, 'clinical' + term + '.csv')
        df = pd.read_csv(ref_file)

        df_all = pd.DataFrame()

        for nctid in list(df['NCT Number']):

            subset, subsubset = define_subset()
            # pprint.pprint(clinicalTrialsGov(nctid))

            tag_dict = clinicalTrialsGov(nctid)
            url = "https://clinicaltrials.gov/ct2/show/" + nctid
            urlXML = "https://clinicaltrials.gov/ct2/show/" + nctid + "?displayxml=true"
            # pprint.pprint(tag_dict)

            df = pd.DataFrame(tag_dict.items())
            df = df.transpose()
            new_header = df.iloc[0]
            df = df[1:]
            df.columns = new_header

            df['Brief_summary'] = linebreak_removal(df['Brief_summary'])
            df['Detailed_description'] = linebreak_removal(df['Detailed_description'])
            df['Eligibility'] = linebreak_removal(df['Eligibility'])
            df['Primary_outcome'] = linebreak_removal(df['Primary_outcome'])
            df['Arm_group'] = linebreak_removal(df['Arm_group'])

            df['source'] = ['https://clinicaltrials.gov/']
            df['searchTerm'] = [term]
            df['NCT'] = [nctid]
            df['url'] = [url]
            df['urlXML'] = [urlXML]

            df['title'] = list(df['Official_title'])

            if '@' in str(list(df['Overall_official'])[0]):
                df['contact'] = list(df['Overall_official'])
            elif '@' in str(list(df['Overall_contact'])[0]):
                df['contact'] = list(df['Overall_contact'])
            elif '@' in str(list(df['Overall_contact_backup'])[0]):
                df['contact'] = list(df['Overall_contact_backup'])
            elif len(str(list(df['Overall_official'])[0])) > 0:
                df['contact'] = list(df['Overall_official'])
            elif len(str(list(df['Overall_contact'])[0])) > 0:
                df['contact'] = list(df['Overall_contact'])
            elif len(str(list(df['Overall_contact_backup'])[0])) > 0:
                df['contact'] = list(df['Overall_contact_backup'])
            else:
                df['contact'] = [' ']



            df['status'] = list(df['Overall_status'])
            # df['date'] = list(df['Start_date'])

            df_all = df_all.append(df)
            print(df_all)

            df_allTerms = df_allTerms.append(df)

            ref_path = os.path.join( 'data', 'meta')
            ref_file = os.path.join(ref_path, 'clinical' + term + '.csv')
            df_all.to_csv(ref_file)

            ref_path = os.path.join( 'data', 'meta')
            ref_file = os.path.join(ref_path, 'clinical' + 'All' + '.csv')
            df_allTerms.to_csv(ref_file)



def linebreak_removal(source_list):
    """
    Remove line breaks from a block of text
    """
    source_str = str(' '.join(source_list))
    source_str = source_str.replace('\n', '')
    single_str = source_str.replace('\r', '').replace('\n', '')
    return(single_str)


def clinicalTrialsGov (nctid):
    """
    Turn the dictionary into a dataframe
    """

    data = BeautifulSoup(requests.get("https://clinicaltrials.gov/ct2/show/" + nctid + "?displayxml=true").text, "xml")
    df = pd.DataFrame(data)

    subset, subsubset = define_subset()
    # tag_matches = data.find_all(subset)
    tag_matches = data.find_all(subsubset)

    for sub in subsubset:
         tag_dict = {'' + current_tag.name.capitalize(): current_tag.text for current_tag in tag_matches}

    # tag_dict = {'' + current_tag.name.capitalize(): current_tag.text for current_tag in tag_matches}

    for sub in subset: tag_dict = multipleFields(data, sub, tag_dict)

    # return removeEmptyKeys(tag_dict)
    return tag_dict



def multipleFields (data, subset, tagDict):
    """

    """
    fields = data.find_all(subset)
    field = [each.text for each in fields]
    # tagDict['ct' + subset.capitalize()] = ", ".join(field)
    tagDict['' + subset.capitalize()] = ", ".join(field)
    return tagDict

def removeEmptyKeys (dict1):
    newDict = {k:v for (k, v) in dict1.items() if v}
    return newDict


def define_subset():
    """

    """

    subset = []
    subset.append('study_type')
    subset.append('brief_title')
    subset.append('official_title')

    # headers
    subset.append('id_info')
    subset.append('sponsors')
    subset.append('lead_sponsor')
    subset.append('oversight_info')
    subset.append('brief_summary')
    subset.append('detailed_description')
    subset.append('why_stopped')
    subset.append('study_design_info')
    subset.append('primary_outcome')
    subset.append('secondary_outcome')
    subset.append('intervention')
    subset.append('eligibility')
    subset.append('location')
    subset.append('location_countries')
    subset.append('responsible_party')
    subset.append('overall_official')
    subset.append('overall_contact')
    subset.append('overall_contact_backup')
    subset.append('responsible_party')

    # point of contact
    subset.append('lead_sponsor')
    subset.append('sponsors_and_collaborators')
    subset.append('investigators')
    subset.append('study_chair')
    subset.append('responsible_party')
    subset.append('contacts')
    subset.append('locations')
    subset.append('sponsored')
    subset.append('collaborator')
    subset.append('information_provided_by')
    subset.append('overall_official')
    subset.append('overall_contact')
    subset.append('overall_contact_email')
    subset.append('overall_contact_backup')
    subset.append('overall_contact_backup_email')
    subset.append('overall_contact')
    subset.append('locations')

    # required info
    subset.append('required_header')
    subset.append('brief_summary')
    subset.append('detailed_description')

    # description
    subset.append('clinicaltrials.gov_identifier')
    subset.append('recruitment_status')
    subset.append('brief_summary')
    subset.append('recruitment_status')
    subset.append('estimated_enrollment')
    subset.append('allocation')
    subset.append('intervention_model')
    subset.append('intervention_model_description')
    subset.append('primary_purpose')
    subset.append('masking')
    subset.append('enrollment')
    subset.append('official_title')
    subset.append('condition')
    subset.append('minimum_age')
    subset.append('maximum_age')
    subset.append('gender')
    subset.append('healthy_volunteers')
    subset.append('phase')
    subset.append('primary_outcome')
    subset.append('secondary_outcome')
    subset.append('arm_group')
    subset.append('number_of_arms')

    # logistics
    subset.append('actual_study_start_date')
    subset.append('estimated_primary_completion_date')
    subset.append('estimated_study_completion_date')
    subset.append('last_verified')
    subset.append('keywords_provided_by')
    subset.append('additional_relevant_mesh_terms')
    subset.append('oversight_info')

    subsubset = []
    subsubset.append('overall_status')
    subsubset.append('brief_title')
    subsubset.append('official_title')
    subsubset.append('study_type')
    subsubset.append('verification_date')
    subsubset.append('start_date')
    subsubset.append('completion_date')
    subsubset.append('primary_completion_date')
    subsubset.append('study_first_submitted')
    subsubset.append('study_first_submitted_qc')
    subsubset.append('last_update_submitted')
    subsubset.append('last_update_submitted_qc')
    subsubset.append('last_update_posted')
    subsubset.append('is_fda_regulated_drug')
    subsubset.append('is_fda_regulated_device')
    subsubset.append('has_dmc')
    subsubset.append('biospec_retention')
    subsubset.append('biospec_descr')

    return (subset, subsubset)
