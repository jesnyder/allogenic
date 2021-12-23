import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import requests

from c0001_retrieve_meta import retrieve_path




def create_webpage():
    """
    Objective: Summarize the projects and findings

    Tasks:
        1. Write summary of html

    """

    print("running create_webpage")

    tasks = [1]

    if 1 in tasks: introduction_html()


    print("completed create_webpage")



def introduction_html():
    """

    """


    index_html = retrieve_path('index_html')
    f = open(index_html, "w")
    f.close()
    f = open(index_html, "w")
    f.close()

    f = open(index_html, "w")
    f.write('<!DOCTYPE html>' + '\n' )
    f.write('<html>' + '\n' )
    f.write('<title>Allogenic</title>' + '\n' )
    f.write('</head>' + '\n' )

    f.write('<body>' + '\n')
    f.write('<h1>Introduction</h1>' + '\n')
    f.write('<p>Lets compare the use of allogenic to autologous cells in clinical trials. </p>' + '\n')
    f.write('</body>' + '\n')

    f.write('</html>' + '\n' )
    f.close()


def close_html():
    """

    """
    index_html = retrieve_path('index_html')
    f = open(index_html, "w")
    f.write('</html>' + '\n' )
    f.close()


if __name__ == "__main__":
    main()
