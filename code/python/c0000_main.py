import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import requests

from c0001_retrieve_meta import retrieve_path
from c0100_scrape_trials import scrape_trials
from c1000_create_webpage import create_webpage



def main():
    """
    Objective: Which approach shows more promise for MSC: allogenic or autologous

    1. Build database of clinical trials from NIH Clinical Trials
    2. Create webpage

    """

    print("running main")

    tasks = [2]

    if 1 in tasks: scrape_trials()
    if 2 in tasks:  create_webpage()

    print("completed main")

    """
    # Review the note above
    # Identify which tasks need to be run
    # List the task numbers that need to be run below
    tasks = [3]

    if 1 in tasks: chart_clinical()
    if 2 in tasks: chart_patents()
    if 3 in tasks: chart_trials()
    """

if __name__ == "__main__":
    main()
