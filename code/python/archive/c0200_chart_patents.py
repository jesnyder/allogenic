import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from c0101_retrieve_clinical import retrieve_clinical
from c0201_query_patents import query_patents

def chart_patents():
    """

    """

    query_patents()

    # clinical_gov_url = 'https://clinicaltrials.gov/ct2/results?cond=&term=&type=&rslt=&age_v=&gndr=&intr=allogenic+AND+msc&titles=&outc=&spons=&lead=&id=&cntry=&state=&city=&dist=&locn=&rsub=&strd_s=&strd_e=&prcd_s=&prcd_e=&sfpd_s=&sfpd_e=&rfpd_s=&rfpd_e=&lupd_s=&lupd_e=&sort='
    # retrieve_clinical(clinical_gov_url)

    ref_path = os.path.join( 'metadata')
    alloFile = 'allogenicANDmesencymalClinicalGov.csv'
    autoFile = 'autologousANDmesencymalClinicalGov.csv'

    fig = plt.figure()
    ax = plt.subplot(111)

    df_return = count_per_year(alloFile)
    plt.scatter(df_return['year'], df_return['count'], color = [0,0,1], label = 'allogenic')
    plt.plot(df_return['year'], df_return['count'], color = [1,0,0], label = 'allogenic')

    df_return = count_per_year(autoFile)
    plt.scatter(df_return['year'], df_return['count'], color = [0,0,1], label = 'autologous')
    plt.plot(df_return['year'], df_return['count'], color = [0,0,1], label = 'autologous')

    ax.legend(loc = 'center left')
    plt.title('Clinical Trials of MSC')
    plt.savefig('patents.png', bbox_inches='tight')

def count_per_year(refFile):
    """

    """

    ref_path = os.path.join( 'metadata')
    ref_file = os.path.join(ref_path, refFile)
    dfAllo = pd.read_csv(ref_file)

    startAllo = list(dfAllo["Start Date"])

    years = []
    for start in startAllo:
        start = str(start)
        fullDate = start.split(' ')
        year = fullDate[-1]
        years.append(year)

    dfAllo['Start Year'] = years
    # print(years)

    unique_years, unique_counts = [], []
    for year in np.arange(2000, 2025, 1):
        year = str(year)
        df = dfAllo
        df =  dfAllo[ dfAllo['Start Year']==year]

        unique_years.append(year)
        unique_counts.append(len(list(df['Start Year'])))

    df_return = pd.DataFrame()
    df_return['year'] = unique_years
    df_return['count'] = unique_counts
    print(df_return)
    return(df_return)
