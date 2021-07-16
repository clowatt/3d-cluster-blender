# Read a CSV with stellar data and initialize a star system

#import bpy
import pandas as pd
import os


# Hardcoding the snapshot file. Would be best to have a wrapper to do this
dirname = os.path.dirname(__file__)
dataPath = os.path.join(dirname, './../Data Files/snapshot.csv')

# Get the data into a pandas datafram
starDataFrame = pd.read_csv(dataPath)

print(starDataFrame.to_string()) 