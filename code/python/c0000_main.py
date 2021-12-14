import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from c0100_chart_clinical import chart_clinical
from c0200_chart_patents import chart_patents
from c0300_chart_trials import chart_trials


def main():
    """
    Objective: Which approach shows more promise for MSC: allogenic or autologous

    1. Chart allogenic vs autolous clinical trials

    Before running the code
    Navigate to the following url
    https://clinicaltrials.gov/ct2/search/advanced?cond=&term=&cntry=&state=&city=&dist=
    Search terms and save in data/source folder
 
    """

    print("running main")

    # Review the note above
    # Identify which tasks need to be run
    # List the task numbers that need to be run below
    tasks = [3]

    if 1 in tasks: chart_clinical()
    if 2 in tasks: chart_patents()
    if 3 in tasks: chart_trials()


    print("completed main")

if __name__ == "__main__":
    main()
