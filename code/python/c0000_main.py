import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import requests

from c0001_retrieve_meta import retrieve_path
from c0100_retrieve_trials import retrieve_trials

from c0100_chart_clinical import chart_clinical
from c0200_chart_patents import chart_patents
from c0300_chart_trials import chart_trials


def main():
    """
    Objective: Which approach shows more promise for MSC: allogenic or autologous

    1. Build database of clinical trials from NIH Clinical Trials
    2. 

    """

    print("running main")

    tasks = [1]

    if 1 in tasks: retrieve_trials()


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
