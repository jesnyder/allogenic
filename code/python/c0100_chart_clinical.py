import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from c0101_retrieve_clinical import retrieve_clinical

def chart_clinical():
    """

    """

    # clinical_gov_url = 'https://clinicaltrials.gov/ct2/results?cond=&term=&type=&rslt=&age_v=&gndr=&intr=allogenic+AND+msc&titles=&outc=&spons=&lead=&id=&cntry=&state=&city=&dist=&locn=&rsub=&strd_s=&strd_e=&prcd_s=&prcd_e=&sfpd_s=&sfpd_e=&rfpd_s=&rfpd_e=&lupd_s=&lupd_e=&sort='
    # retrieve_clinical(clinical_gov_url)

    ref_path = os.path.join( 'metadata')
    alloFile = 'allogenicANDmesencymalClinicalGov.csv'
    autoFile = 'autologousANDmesencymalClinicalGov.csv'

    fig = plt.figure(figsize=(15, 12))

    ax = plt.subplot(311)

    df_return = count_per_year(alloFile)
    plt.scatter(df_return['year'], df_return['count'], color = [1,0,0], label = 'allogenic')
    plt.plot(df_return['year'], df_return['count'], color = [1,0,0], label = 'allogenic')


    df_return = count_per_year(autoFile)
    plt.scatter(df_return['year'], df_return['count'], color = [0,0,1], label = 'autologous')
    plt.plot(df_return['year'], df_return['count'], color = [0,0,1], label = 'autologous')

    ax.legend(loc = 'center left')
    plt.title('Clinical Trials of MSC - Each Year')

    ax = plt.subplot(312)

    df_return = count_per_year(alloFile)
    plt.scatter(df_return['year'], df_return['cumulative'], color = [1,0,0], label = 'allogenic')
    plt.plot(df_return['year'], df_return['cumulative'], color = [1,0,0], label = 'allogenic')


    df_return = count_per_year(autoFile)
    plt.scatter(df_return['year'], df_return['cumulative'], color = [0,0,1], label = 'autologous')
    plt.plot(df_return['year'], df_return['cumulative'], color = [0,0,1], label = 'autologous')

    ax.legend(loc = 'center left')
    plt.title('Clinical Trials of MSC - Cumulative')

    df_allo = count_per_year(alloFile)
    df_auto = count_per_year(autoFile)

    allo = list(df_allo['count'])
    auto = list(df_auto['count'])

    total, allo_frac, auto_frac = [], [], []
    for i in range(len(list(df_return['year']))):
        total.append(allo[i] + auto[i])

        if total[-1] > 0:
            allo_frac.append(allo[i]/(allo[i]+auto[i]))
            auto_frac.append(1)

        else:
            allo_frac.append(0)
            auto_frac.append(0)

    ax = plt.subplot(313)
    plt.bar(df_return['year'], auto_frac, width=0.8, label = 'autologous', color = [0,0,1])
    plt.bar(df_return['year'], allo_frac, width=0.8, label = 'allogenic', color = [1,0,0])
    ax.legend(loc = 'center left')

    plt.savefig('clincal.png', bbox_inches='tight')

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

    unique_years, unique_counts, cumulative_counts = [], [], []
    for year in np.arange(2002, 2023, 1):
        year = str(year)
        df = dfAllo
        df =  dfAllo[ dfAllo['Start Year']==year]

        unique_years.append(year)
        if len(unique_counts) > 1:
            cumulative = cumulative_counts[-1] + len(list(df['Start Year']))
        else:
            cumulative = len(list(df['Start Year']))

        unique_counts.append(len(list(df['Start Year'])))
        cumulative_counts.append(cumulative)

    df_return = pd.DataFrame()
    df_return['year'] = unique_years
    df_return['count'] = unique_counts
    df_return['cumulative'] = cumulative_counts
    print(df_return)
    return(df_return)
