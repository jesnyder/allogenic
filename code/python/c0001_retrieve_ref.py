import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def retrieve_ref(variableName):

    ref_path = os.path.join( 'metadata')
    ref_file = os.path.join(ref_path, 'ref.csv')
    df = pd.read_csv(ref_file)

    variableNames = list(df['name'])
    variableValues = list(df['value'])

    value = 0
    for i in range(len(variableNames)):
        if variableName == variableNames[i]:
            value = variableValues[i]
            break

    # print('value = ' + str(value))
    return value
