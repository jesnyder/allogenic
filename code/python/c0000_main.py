import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from c0100_chart_clinical import chart_clinical
from c0200_chart_patents import chart_patents


def main():
    """
    Objective: Which approach shows more promise for MSC: allogenic or autologous

    1. Chart allogenic vs autolous clinical trials

    """

    print("running main")

    # Review the note above
    # Identify which tasks need to be run
    # List the task numbers that need to be run below
    tasks = [1, 2]

    if 1 in tasks: chart_clinical()
    if 2 in tasks: chart_patents()



    print("completed main")

if __name__ == "__main__":
    main()
