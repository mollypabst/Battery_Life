import csv
import pandas as pd
import os
import tkinter
from tkinter import filedialog
from datetime import datetime
import numpy as np

def getNum(inputString):
    number = []
    for char in inputString:
        if (char.isdigit() == True):
            number.append(char)
    return number

def listToString(s):  
    # initialize an empty string 
    str1 = ""  
    # traverse in the string   
    for ele in s:  
        str1 += ele   
    # return string   
    return str1

def resistance(col):
    if 'Channel 1' in col:
        print(df[col].astype('float') >= 3)
        return 714
    if 'Channel 2' in col:
        return 715
    if 'Channel 3' in col:
        return  716
    if 'Channel 4' in col:
        return  717
    if 'Channel 5' in col:
        return  716
    if 'Channel 6' in col:
        return  3572
    if 'Channel 7' in col:
        return  3546
    if 'Channel 8' in col:
        return  3555
    if 'Channel 9' in col:
        return  3554
    if 'Channel 10' in col:
        return  3562

def sumSpecial(x):
    try:
        f = float(x)
        return f
    except Exception as e:
        return 0

root = tkinter.Tk()
root.withdraw()

filename = filedialog.askopenfilename(parent=root,title='Select the csv file containing the data you would like energy calculated for.')

print(filename)

#df = pd.read_csv(filename, sep = "\"")
df = pd.read_csv(filename)

df.iloc [2,0]= 'Timestamp'
print(df)
df.columns = df.iloc[2]
df = df[3:]
# df = pd.read_csv('Test.csv', header=None, sep='\n')
# df = df[0].str.split(',', expand=True)

print(df.index[0])
df.drop(df.index[0], inplace = True)

# convert timestamp to datetime object
df['Timestamp'] = df['Timestamp'].values.astype('float')
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')

for index, col in enumerate(df.columns[1:]):
    if col == None:
        break
    elif 'Channel' in col:
        # get channel number
        tmp = getNum(col)
        num = listToString(tmp)
        loc = df.columns.get_loc(col)
        energy_col = 'Energy ' + num
        time_col = 'Time ' + num

        # make new column for energy values
        df.insert(loc + 1, energy_col, value=['' for i in range(df.shape[0])])
        # make new column for time values
        df.insert(loc + 2, time_col, value=['' for i in range(df.shape[0])])

        # get resistance value depending on which channel it is
        res = resistance(col)
        df[col] = df[col].astype('float')

        # calculate energy
        df.loc[df[col] >= 3, energy_col] = ((df[col]**2)/res) * 600
        df.loc[df[col] < 3, energy_col] = 0


        # print only valid timestamps in this column
        df.loc[df[col] >= 3, time_col] = df['Timestamp'] 
        df.loc[df[col] < 3, time_col] = None

        # find first and last timestamps in column and take the difference
        first = df[time_col].notna().idxmax()
        last = df[time_col].notna()[::-1].idxmax()
        s = df[time_col]
        tdelta = s[last] - s[first]
        tdelta = tdelta.total_seconds()
        print(tdelta)
 

        # add up all energy values and put in new column
        df[energy_col] = df[energy_col].astype('float')
        energy_name = 'Total Energy ' + str(num) + ' (J)'
        df[energy_name] = df[energy_col].sum()

        # put total time of battery life in seconds in new column
        time_name = 'Battery Life ' +   str(num) + ' (s)'
        df[time_name] = tdelta

        # only first row show total energy and battery life
        df.loc[5::, energy_name] = None
        df.loc[5::, time_name] = None


df.to_csv('EnergyCalculation.csv')

print(df)
