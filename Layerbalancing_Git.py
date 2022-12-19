# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 09:11:40 2022

@author: Hadis Abarghouyi
"""

'''Phase 1: Read the needed packages'''
# import glob
import os
from ftplib import FTP
import re
# import time
from datetime import datetime
import pandas as pd
# import pysftp
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
# import numpy as np
# import seaborn as sns
import matplotlib.gridspec as gridspec
import shutil
import copy
import numpy as np
# import cx_Oracle
import warnings

warnings.filterwarnings("ignore")

'''Phase1: backup the output of previous report to a folder,
this part is just a backup for further requirments.'''
main_directory = r'F:...\\'  # you can select a root for this project which contains all input and outputs
os.chdir(main_directory)
excel_lists = os.listdir(main_directory)
backup_files = [i for i in excel_lists if ((i.endswith('csv')) or i.endswith('xlsx') or i.endswith('png'))]

dst = "backup"  # the name of backup folder
for src in backup_files:
    shutil.copy(src, dst)

# %%
'''Read the input hourly stats'''
'''connect to FTP server and enter in location of storage
This part will be changed based on your input data / you should read inputs from your required folder '''
# you can find example in input folder
'''Read the input files from your system'''
desired_days=['11' , '10' ,'09' ] # we consider the hourly stats of three consecutive days for example 9-11th
today = datetime.date.today()
tracker = pd.read_excel("tracker.xlsx") #this folder will be the output of previous run - foe the first run just please get the headers with an empty table
pre_output = pd.read_excel("unbalanced_cells.xlsx") #this folder will be the output of previous run - foe the first run just please get the headers with an empty table
closed_tracker = pd.read_excel("tracker-closed.xlsx") #this folder will be the output of previous run - foe the first run just please get the headers with an empty table
Site_priority = pd.read_excel("Site Priority OPT list.xlsx") #this is added to apply a filtering on our data - you can use your desired inputs

excel_lists = os.listdir(main_directory)
cell_hourly_files = [i for i in excel_lists if i.startswith("CELL_HOURLY")] # these are the hourly stats of desired KPIs you should consider all hours which you need for your project

cell_hourly_data = []
for csv_file in cell_hourly_files: # read hourly stats and change them based on your requirements
    loc = main_directory + csv_file
    data_temp = pd.read_csv(loc, header=1, thousands=',')

    if data_temp[
        '4G_Throughput_UE_DL_kbps_IR(Kbps)'].dtype == 'O':  # This part has been added to ignore the cells with negative throughput
        print('note: {0} is object'.format(
            loc))  # ERROR: You may see an error because of negative throughput, please find the location of error in excel and delet the negative throughput rows
        pattern = r'-.*'

        data_temp = data_temp.dropna(subset=['4G_Throughput_UE_DL_kbps_IR(Kbps)'])
        list_thr = data_temp['4G_Throughput_UE_DL_kbps_IR(Kbps)']
        for i in list_thr:
            result = re.search(pattern, str(i))
            if result:
                print(i, result.group())
                data_temp = data_temp[data_temp['4G_Throughput_UE_DL_kbps_IR(Kbps)'] != result.group()]

                continue
        data_temp.to_csv('{0}'.format(loc), index=False)
        data_temp = pd.read_csv('{0}'.format(loc), thousands=',')
    data_temp = data_temp[['Time', '4G LTE CELL',
                           '4G_Throughput_UE_DL_kbps_IR(Kbps)',
                           '4G_PRB_Util_Rate_PDSCH_Avg_IR(#)', '4G_PAYLOAD_TOTAL_MBYTE_IR(MB)']]
    cell_hourly_data.append(data_temp)

    os.remove(loc)  # this part will remove the file after reading it

data = pd.concat([name for name in cell_hourly_data])
data_backup = copy.copy(data)
print(data.dtypes)

data = data.dropna(subset=['4G_Throughput_UE_DL_kbps_IR(Kbps)'])
data = data[data['4G_Throughput_UE_DL_kbps_IR(Kbps)'] >= 0]
data = data.sort_values(by=['4G_Throughput_UE_DL_kbps_IR(Kbps)'], ascending=False)
data = data.drop_duplicates(subset=['Time', '4G LTE CELL'])

'''['Time', '4G LTE CELL', '4G_Throughput_UE_DL_kbps_IR(Kbps)',
       '4G_PRB_Util_Rate_PDSCH_Avg_IR(#)', '4G_PAYLOAD_TOTAL_MBYTE_IR(MB)']'''
# -----

# maps cellcfg-----
loc = r"..." #location of config files 1
data_maps_cellcfg = pd.read_csv(loc,
                                header=1)
os.remove(loc)
data_maps_cellcfg = data_maps_cellcfg[['4G LTE CELL', 'City', 'PROVINCE', 'Region', 'Vendor']]
data_maps_cellcfg = data_maps_cellcfg.rename(columns={'PROVINCE': 'PROVINCE_CFG'})
data_maps_cellcfg = data_maps_cellcfg.drop_duplicates(subset='4G LTE CELL')

# daily cell availability / we use this part to ensure about availability of cells
loc_avail = r".." #location of daily stats of Cell_Daily_ file
data_availability = pd.read_csv(loc_avail, header=1)
os.remove(loc_avail)
data_availability = data_availability[
    ['4G LTE CELL', 'On air', '4G_CELL_AVAIL_MAN_IR(%)', '4G_CELL_AVAIL_SYS_IR(#)', '4G_PAYLOAD_TOTAL_MBYTE_IR(MB)']]
data_availability = data_availability.rename(columns={'4G_CELL_AVAIL_SYS_IR(#)': '4G_CELL_AVAIL_SYS_IR'})
data_availability = data_availability.rename(columns={'4G LTE CELL': 'Cell'})
data_availability = data_availability.dropna(subset=['4G_CELL_AVAIL_MAN_IR(%)'])
data_availability_copy = copy.copy(data_availability)
data_availability = data_availability[data_availability['4G_CELL_AVAIL_MAN_IR(%)'] > 50]

# this part has been used to apply one filtering on the stats of our network
loc =r"...  " #location of config files 2
cra_cellcfg = pd.read_csv(loc, header=1)
cra_cellcfg = cra_cellcfg.dropna(subset=['Province'])[['4G LTE CELL', 'Province']]
cra_cellcfg = cra_cellcfg.dropna(subset=['4G LTE CELL'])
USO_Cells = cra_cellcfg[cra_cellcfg['Province'].str.contains('_USO')]

# %%preprocessing
'''Phase 2: In this part I have used multiple files to recover cellcfg missing'''
data = pd.merge(data, data_maps_cellcfg, on='4G LTE CELL', how='left')
data = data.rename(columns={'4G LTE CELL': 'Cell', 'PROVINCE_CFG': 'Province',
                            '4G_Throughput_UE_DL_kbps_IR(Kbps)': 'THR_DL',
                            '4G_PRB_Util_Rate_PDSCH_Avg_IR(#)': 'PRB_utilization'})

# updating cellcfg----------------------------------
'''['Time', 'Cell', 'THR_DL', 'PRB_utilization', 'City', 'Province',
       'Region', 'Vendor']'''
my_cellcfg = pd.read_csv('atoll_lte_fdd_cells.csv')
data = pd.merge(data, my_cellcfg, on='Cell', how='left', suffixes=('', '_cellcfg'))

data['Province'] = data['Province'].fillna(data['Province_cellcfg'])
del data['Province_cellcfg']

data['Region'] = data['Region'].fillna(data['Region_cellcfg'])
del data['Region_cellcfg']

data['Vendor'] = data['Vendor'].fillna(data['Vendor_cellcfg'])
del data['Vendor_cellcfg']

data['City'] = data['City'].fillna(data['City_cellcfg'])
del data['City_cellcfg']
del data['On-Air']

# checking tracker - this is a tracker of cells status on our periodic report
data = pd.merge(data, tracker[['Cell', 'City', 'Province', 'Region', 'Vendor']], on='Cell', how='left',
                suffixes=('', '_tracker'))
data['Province'] = data['Province'].fillna(data['Province_tracker'])
del data['Province_tracker']

data['Region'] = data['Region'].fillna(data['Region_tracker'])
del data['Region_tracker']

data['Vendor'] = data['Vendor'].fillna(data['Vendor_tracker'])
del data['Vendor_tracker']

data['City'] = data['City'].fillna(data['City_tracker'])
del data['City_tracker']

# -----------------------------------------------------
# To tag old cases which are in the tracker now
data['pre_output'] = 0
data['pre_output'][data['Cell'].isin(tracker['Cell'])] = 1

# %%
'''initial data processing '''
data = data.drop(data[(data.Cell.str[0:4] == 'PLMN') | (data.Cell.str[0:4] == 'MBTS') | (data.Cell.str[0:1] == 'D') \
                      | (data.City.str[::-1].str[0:3] == 'OSU')].index)

data = data[~data['Cell'].isin(USO_Cells['4G LTE CELL'])]
# keep the site pririty P1 and P2
Site_priority = Site_priority[
    (Site_priority['SITE_Priority(based on New)'] == 'P1') | (Site_priority['SITE_Priority(based on New)'] == 'P2')]
data = data.drop(data[(~data.Cell.str[1:6].isin(Site_priority['SITE'])) & (
    data.City.str.contains('ROAD'))].index)  #


data['BAND'] = data['Cell'].str[-1:]
data = data[data['BAND'] != 'A']
data = data[data['BAND'] != 'D']
data['BAND'] = data['BAND'].astype(float)
data['Sec'] = data['Cell'].str[:7] + data['Cell'].str[-2]
data = data.reset_index()
del data['index']
cell_list = data['Cell'].unique()
sec_list = data['Sec'].unique()
#



# %% limitation
'''Changing the name of regions per cell.
 '''
copyy = copy.copy(data)
data['day'] = pd.to_datetime(data['Time']).dt.day
data = data[data['day'].isin([int(d) for d in desired_days])]
df_unique = data[['Cell', 'BAND', 'Sec', 'City', 'Province', 'Region', 'Vendor', 'pre_output']].drop_duplicates()
a = len(df_unique)

df_unique_region = df_unique[['Sec', 'City', 'Province', 'Region']].dropna(subset={'Region'}).drop_duplicates(
    subset='Sec')
df_unique = pd.merge(df_unique, df_unique_region, on='Sec', how='left', suffixes=('', '_sec'))

df_unique['Province'] = df_unique['Province'].fillna(df_unique['Province_sec'])
del df_unique['Province_sec']

df_unique['City'] = df_unique['City'].fillna(df_unique['City_sec'])
del df_unique['City_sec']

df_unique['Region'] = df_unique['Region'].fillna(df_unique['Region_sec'])
del df_unique['Region_sec']


df_unique['Region'][(df_unique['Region'] == 'R1') | (df_unique['Region'] == 'R3')] = 'R1-R3'
df_unique['Region'][(df_unique['Region'] == 'R2') | (df_unique['Region'] == 'R4')] = 'R2-R4'
df_unique['Region'][(df_unique['Region'] == 'R5') | (df_unique['Region'] == 'R10')] = 'R5-R10'
df_unique['Region'][(df_unique['Region'] == 'R6') | (df_unique['Region'] == 'R9')] = 'R6-R9'

# the cells which had not data in all three days are in Missing category
data_Cell_per_day = data[['Cell', 'day']].drop_duplicates().groupby('Cell').count()
data_Cell_per_day_missing = data_Cell_per_day[data_Cell_per_day['day'] < 3]
data_Cell_per_day_nomissing_last2days = data[['Cell', 'day']][
    data['day'] != int(desired_days[2])].drop_duplicates().groupby('Cell').count()
data_Cell_per_day_nomissing_last2days = data_Cell_per_day_nomissing_last2days[
    data_Cell_per_day_nomissing_last2days['day'] == 2]

# put the stats of every day in the elements of a dict
data_dict = {}
count_per_hour = {}

# day=desired_days[1]
for day in desired_days:
    data_dict[day] = data[data['day'] == int(day)]
    del data_dict[day]['day']
    count_per_hour[day] = data_dict[day][['Time', 'THR_DL']].groupby('Time').count()

    if len(data_dict[day]['Time'].unique()) < 24:
        print('missing data in FTP:{}'.format(day))
    # ---hourly missing stats in FTP---------------------
'''This part has been added to check the MAPS missing'''
with pd.ExcelWriter(
        'missed_per_thr.xlsx') as writer:  # CHECK: check the saved 'missed_per_thr.xlsx' to ensure about number of stats per hour for 3 days.
    for day in desired_days:
        count_per_hour[day].to_excel(writer, sheet_name=day)
writer.save

# %% Layer balancing - here is the main method, you can adjust this part based on your required network

'''Phase 3: Applying layer balancing criteria.'''
# thresholds for layer balancing
percentage = 0.70  # to select the percentage of hours that satisfies any criteria to open a case
percentage_out = 0.50  # to select the percentage of hours that satisfies any criteria to close a case (in some criteria)
required_time = 18  # the minimum requred hours to compare two cells, the cell will be added to missed list if its stats are less than 12 hours stats
PRB_free_rate_target_input = 50  # the needed PRB rate for good cell for layer balancing

balancing_lowTHR_input = 10000  # 10000 bps , upper limitation for poor cells
balancing_lowTHR_output = 11500  #  this cause close the case
band_delta_threshold_input = 5000  # 5000 needed throughput difference to open a case
band_delta_threshold_output = 4500  # needed throughput difference to close a case
min_upperthroughput_threshold = 10000  # minimum needed throughput of better cell

# checking the Balancing status for 3 days
for df in data_dict:  # df='19'
    print('starting day {0}: {1}'.format(df, datetime.datetime.now()))
    # select the list of sectors which are supposed to be checked in layer balancing report
    df_LB = data_dict[df][(data_dict[df]['BAND'] == 1) | (data_dict[df]['BAND'] == 2) | (data_dict[df]['BAND'] == 5) | (
                data_dict[df]['BAND'] == 7) | (data_dict[df]['BAND'] == 8)][
        ['Time', 'Cell', 'BAND', 'Sec', 'Region', 'THR_DL', 'PRB_utilization',
         'pre_output']]  # the used cells for layer balancing

    df_LB_unique = df_LB[['Cell', 'Sec']].drop_duplicates()
    df_LB_grouped = df_LB_unique[['Cell', 'Sec']].groupby(['Sec']).count()
    df_LB_grouped = df_LB_grouped[df_LB_grouped['Cell'] > 1]
    df_LB = df_LB[df_LB['Sec'].isin(df_LB_grouped.index)]
    df_LB_cells_list = df_LB['Cell'].unique()

    # finding the cells numbers
    df_LB = pd.merge(df_LB, df_LB_grouped, left_on='Sec', right_on=df_LB_grouped.index, how='left',
                     suffixes=('', 's_#'))
    # selecting the times in which all cells of a sector have data
    df_LB_grouped_Time = df_LB[['Cell', 'Sec', 'Time']].groupby(['Sec', 'Time']).count()
    df_LB_grouped_Time = df_LB_grouped_Time.reset_index()
    df_LB_grouped_Time = df_LB_grouped_Time.rename(columns={'Cell': 'Times_#'})
    df_LB = pd.merge(df_LB, df_LB_grouped_Time, on=['Time', 'Sec'], how='left')  # 2031871  2025339

    # make some changes
    df_LB_nonequal = df_LB[df_LB['Cells_#'] != df_LB['Times_#']]
    df_LB_nonequal_grouped = df_LB_nonequal[['Time', 'Cell']].groupby(['Cell']).count()
    unequal_cells = df_LB_nonequal_grouped[df_LB_nonequal_grouped['Time'] > (24 - required_time)].index
    df_LB = df_LB[~df_LB['Cell'].isin(unequal_cells)]
    # selecting the sectors/cells which have stats for more than required_time per day
    df_LB_grouped_Time_Cell = df_LB[['Cell', 'Time']].groupby(['Cell']).count()
    df_LB_grouped_Time_Cell_missing = df_LB_grouped_Time_Cell[df_LB_grouped_Time_Cell['Time'] <= int(required_time)]


    # remove missings
    df_LB = df_LB[~df_LB['Cell'].isin(df_LB_grouped_Time_Cell_missing.index)]
    # rank --> higher THR higher Rank
    df_LB = df_LB.assign(rank=df_LB.sort_values(['THR_DL'], ascending=True).groupby(['Time', 'Sec']).cumcount())
    df_LB_sum_rank = df_LB[['Cell', 'rank']].groupby('Cell').sum()
    df_LB = df_LB.rename(columns={'rank': 'rank_time'})
    df_LB = pd.merge(df_LB, df_LB_sum_rank, left_on='Cell', right_on=df_LB_sum_rank.index, how='left')
    df_LB = df_LB.assign(Rank_THR=df_LB.sort_values(['rank'], ascending=True).groupby(['Time', 'Sec']).cumcount())
    del df_LB['rank'], df_LB['rank_time'], df_LB['Times_#']
    '''['Time', 'Cell', 'BAND', 'Sec', 'Region', 'THR_DL', 'PRB_utilization',
           'pre_output', 'Cells_#', 'Unbalance_status', 'Rank_THR']'''

    # applying the thresolds by using pivot
    df_LB_grouped_pivot = df_LB.pivot_table(index=['Time', 'Sec'], columns='Rank_THR',
                                            values=['Cell', 'THR_DL', 'PRB_utilization', 'pre_output'],
                                            aggfunc='first')  # [lambda x: ' '.join(x),'mean','mean','mean'])
    df_LB_grouped_pivot = df_LB_grouped_pivot.reset_index()
    df_LB_grouped_pivot.columns = df_LB_grouped_pivot.columns.to_flat_index()
    i = 0
    for col in df_LB_grouped_pivot.columns:
        if i < 2:
            df_LB_grouped_pivot = df_LB_grouped_pivot.rename(columns={col: col[0]})
        else:
            df_LB_grouped_pivot = df_LB_grouped_pivot.rename(columns={col: col[0] + '_' + str(col[1])})
        i = i + 1
    RANKS_numbers = df_LB['Rank_THR'].max()  # from 0 to this number, higher THR higher rank

    '''['Time', 'Sec', 'Cell_0', 'Cell_1', 'Cell_2', 'PRB_utilization_0',
           'PRB_utilization_1', 'PRB_utilization_2', 'THR_DL_0', 'THR_DL_1',
           'THR_DL_2', 'pre_output_0', 'pre_output_1', 'pre_output_2']'''
    for poor in range(RANKS_numbers + 1):
        for good in range(poor + 1, RANKS_numbers + 1):
            df_LB_grouped_pivot['delta_THR_{0}_{1}'.format(good, poor)] = df_LB_grouped_pivot[
                                                                              'THR_DL_{0}'.format(good)] - \
                                                                          df_LB_grouped_pivot['THR_DL_{0}'.format(
                                                                              poor)] > band_delta_threshold_input
            df_LB_grouped_pivot['delta_THR_{0}_{1}'.format(good, poor)][
                df_LB_grouped_pivot['pre_output_{0}'.format(poor)] == 1] = df_LB_grouped_pivot[
                                                                               'THR_DL_{0}'.format(good)] - \
                                                                           df_LB_grouped_pivot['THR_DL_{0}'.format(
                                                                               poor)] > band_delta_threshold_output

            df_LB_grouped_pivot['poor_throughput_{0}_{1}'.format(good, poor)] = df_LB_grouped_pivot['THR_DL_{0}'.format(
                poor)] < balancing_lowTHR_input
            df_LB_grouped_pivot['poor_throughput_{0}_{1}'.format(good, poor)][
                df_LB_grouped_pivot['pre_output_{0}'.format(poor)] == 1] = df_LB_grouped_pivot['THR_DL_{0}'.format(
                poor)] < balancing_lowTHR_output

            df_LB_grouped_pivot['good_PRB_{0}_{1}'.format(good, poor)] = df_LB_grouped_pivot[
                                                                             'PRB_utilization_{0}'.format(
                                                                                 good)] < PRB_free_rate_target_input
            df_LB_grouped_pivot['good_PRB_{0}_{1}'.format(good, poor)][
                df_LB_grouped_pivot['pre_output_{0}'.format(poor)] == 1] = True

            df_LB_grouped_pivot['good_throughput_{0}_{1}'.format(good, poor)] = df_LB_grouped_pivot['THR_DL_{0}'.format(
                good)] > min_upperthroughput_threshold
            df_LB_grouped_pivot['good_throughput_{0}_{1}'.format(good, poor)][
                df_LB_grouped_pivot['pre_output_{0}'.format(poor)] == 1] = True


    df_LB_grouped_pivot_copy = df_LB_grouped_pivot
    '''['Time', 'Sec', 'Cell_0', 'Cell_1', 'Cell_2', 'PRB_utilization_0',
           'PRB_utilization_1', 'PRB_utilization_2', 'THR_DL_0', 'THR_DL_1',
           'THR_DL_2', 'pre_output_0', 'pre_output_1', 'pre_output_2',
           'delta_THR_1_0', 'poor_throughput_1_0', 'good_PRB_1_0',
           'good_throughput_1_0', 'delta_THR_2_0', 'poor_throughput_2_0',
           'good_PRB_2_0', 'good_throughput_2_0', 'delta_THR_2_1',
           'poor_throughput_2_1', 'good_PRB_2_1', 'good_throughput_2_1'  '''

    df_LB_grouped_pivot_comments = pd.concat(
        [df_LB_grouped_pivot[['Time', 'Sec']], df_LB_grouped_pivot.select_dtypes(include='bool')], axis=1).groupby(
        'Sec').mean()
    df_LB_grouped_pivot = df_LB_grouped_pivot[
        ['Time', 'Sec', 'Cell_0', 'Cell_1', 'Cell_2', 'Cell_3', 'Cell_4', 'pre_output_0', 'pre_output_1',
         'pre_output_2', 'pre_output_3', 'pre_output_4']]
    df_LB_grouped_pivot = pd.merge(df_LB_grouped_pivot, df_LB_grouped_pivot_comments, left_on='Sec',
                                   right_on=df_LB_grouped_pivot_comments.index, how='left')

    for poor in range(RANKS_numbers + 1):
        for good in range(poor + 1, RANKS_numbers + 1):
            df_LB_grouped_pivot['delta_THR_{0}_{1}_result'.format(good, poor)] = df_LB_grouped_pivot[
                                                                                     'delta_THR_{0}_{1}'.format(good,
                                                                                                                poor)] > percentage
            df_LB_grouped_pivot['delta_THR_{0}_{1}_result'.format(good, poor)][
                df_LB_grouped_pivot['pre_output_{0}'.format(poor)] == 1] = df_LB_grouped_pivot[
                                                                               'delta_THR_{0}_{1}'.format(good,
                                                                                                          poor)] > percentage_out

            df_LB_grouped_pivot['poor_throughput_{0}_{1}_result'.format(good, poor)] = df_LB_grouped_pivot[
                                                                                           'poor_throughput_{0}_{1}'.format(
                                                                                               good, poor)] > percentage
            df_LB_grouped_pivot['poor_throughput_{0}_{1}_result'.format(good, poor)][
                df_LB_grouped_pivot['pre_output_{0}'.format(poor)] == 1] = df_LB_grouped_pivot[
                                                                               'poor_throughput_{0}_{1}'.format(good,
                                                                                                                poor)] > 0.2

            df_LB_grouped_pivot['good_PRB_{0}_{1}_result'.format(good, poor)] = df_LB_grouped_pivot[
                                                                                    'good_PRB_{0}_{1}'.format(good,
                                                                                                              poor)] > percentage
            df_LB_grouped_pivot['good_PRB_{0}_{1}_result'.format(good, poor)][
                df_LB_grouped_pivot['pre_output_{0}'.format(poor)] == 1] = True

            df_LB_grouped_pivot['good_throughput_{0}_{1}_result'.format(good, poor)] = df_LB_grouped_pivot[
                                                                                           'good_throughput_{0}_{1}'.format(
                                                                                               good, poor)] > percentage
            df_LB_grouped_pivot['good_throughput_{0}_{1}_result'.format(good, poor)][
                df_LB_grouped_pivot['pre_output_{0}'.format(poor)] == 1] = True

    for poor in range(RANKS_numbers + 1):
        for good in range(poor + 1, RANKS_numbers + 1):
            df_LB_grouped_pivot['comment_{0}_{1}'.format(good, poor)] = df_LB_grouped_pivot[
                                                                            'delta_THR_{0}_{1}_result'.format(good,
                                                                                                              poor)] & \
                                                                        df_LB_grouped_pivot[
                                                                            'poor_throughput_{0}_{1}_result'.format(
                                                                                good, poor)] & df_LB_grouped_pivot[
                                                                            'good_PRB_{0}_{1}_result'.format(good,
                                                                                                             poor)] & \
                                                                        df_LB_grouped_pivot[
                                                                            'good_throughput_{0}_{1}_result'.format(
                                                                                good, poor)]

    df_LB_grouped_pivot = df_LB_grouped_pivot[
        ['Time', 'Sec', 'Cell_0', 'Cell_1', 'Cell_2', 'Cell_3', 'Cell_4', 'comment_1_0', 'comment_2_0', 'comment_3_0',
         'comment_4_0',
         'comment_2_1', 'comment_3_1', 'comment_4_1', 'comment_3_2', 'comment_4_2', 'comment_4_3']]

    # prepareing balanicng status
    df_LB_grouped_pivot['unbalance_comment_0'] = 'OK'
    df_LB_grouped_pivot['unbalance_comment_1'] = 'OK'
    df_LB_grouped_pivot['unbalance_comment_2'] = 'OK'
    df_LB_grouped_pivot['unbalance_comment_3'] = 'OK'
    df_LB_grouped_pivot['unbalance_comment_4'] = 'OK'
    for poor in range(RANKS_numbers):
        for good in range(poor + 1, RANKS_numbers + 1):
            df_LB_grouped_pivot['unbalance_comment_{0}'.format(poor)][
                (df_LB_grouped_pivot['comment_{0}_{1}'.format(good, poor)] == True) & (
                            df_LB_grouped_pivot['unbalance_comment_{0}'.format(poor)] != 'OK')] = df_LB_grouped_pivot[
                                                                                                      'unbalance_comment_{0}'.format(
                                                                                                          poor)] + ', ' + \
                                                                                                  df_LB_grouped_pivot[
                                                                                                      'Cell_{0}'.format(
                                                                                                          good)]

            df_LB_grouped_pivot['unbalance_comment_{0}'.format(poor)][
                (df_LB_grouped_pivot['comment_{0}_{1}'.format(good, poor)] == True) & (
                            df_LB_grouped_pivot['unbalance_comment_{0}'.format(poor)] == 'OK')] = 'Candidates: ' + \
                                                                                                  df_LB_grouped_pivot[
                                                                                                      'Cell_{0}'.format(
                                                                                                          good)]


    # creat the list of cells with their comments
    df_LB_Results = pd.DataFrame(np.concatenate((df_LB_grouped_pivot[['Cell_0', 'unbalance_comment_0']].values,
                                                 df_LB_grouped_pivot[['Cell_1', 'unbalance_comment_1']].values,
                                                 df_LB_grouped_pivot[['Cell_2', 'unbalance_comment_2']].values,
                                                 df_LB_grouped_pivot[['Cell_3', 'unbalance_comment_3']].values,
                                                 df_LB_grouped_pivot[['Cell_4', 'unbalance_comment_4']].values),
                                                axis=0))
    df_LB_Results = df_LB_Results.rename(columns={0: 'Cell', 1: 'Unbalance_status_{0}'.format(df)})
    df_LB_Results = df_LB_Results.drop_duplicates()
    df_unique = pd.merge(df_unique, df_LB_Results[['Cell', 'Unbalance_status_{0}'.format(df)]], on='Cell', how='left')
    df_unique['Unbalance_status_{0}'.format(df)][~df_unique['Cell'].isin(df_LB_cells_list)] = 'OK'
    df_unique['Unbalance_status_{0}'.format(df)][
        df_unique['Cell'].isin(df_LB_grouped_Time_Cell_missing.index)] = 'Missing'
    print('end of day {0}: {1}'.format(df, datetime.datetime.now()))

# %% finding the results of analysis of 3 days
'''['Cell', 'BAND', 'Sec', 'City', 'Province', 'Region', 'Vendor',
       'pre_output', 'pre_output_PRB', 'Unbalance_status_01',
       'Unbalance_status_31', 'Unbalance_status_30']'''

df_unique_result = copy.copy(df_unique)
df_unique['Unbalance_status_new'] = 'OK'
# checking the old cases
df_unique['Unbalance_status_new'][(df_unique['pre_output'] == 1) & (
            (df_unique['Unbalance_status_{0}'.format(desired_days[0])] == 'OK') & (
    df_unique['Unbalance_status_{0}'.format(desired_days[1])]) == 'OK')] = 'OK'
df_unique['Unbalance_status_new'][(df_unique['pre_output'] == 1) & (
            (df_unique['Unbalance_status_{0}'.format(desired_days[0])] == 'OK') & (
    df_unique['Unbalance_status_{0}'.format(desired_days[1])]) != 'OK')] = df_unique[
    'Unbalance_status_{0}'.format(desired_days[1])]
df_unique['Unbalance_status_new'][
    (df_unique['pre_output'] == 1) & (df_unique['Unbalance_status_{0}'.format(desired_days[0])] != 'OK')] = df_unique[
    'Unbalance_status_{0}'.format(desired_days[0])]
# checking the new cases status
df_unique['Unbalance_status_new'][
    (df_unique['pre_output'] == 0) & (df_unique['Unbalance_status_{0}'.format(desired_days[0])] != 'OK') & (
                df_unique['Unbalance_status_{0}'.format(desired_days[1])] != 'OK') & (
                df_unique['Unbalance_status_{0}'.format(desired_days[2])] != 'OK')] = df_unique[
    'Unbalance_status_{0}'.format(desired_days[0])]

for day in desired_days:
    df_unique['Unbalance_status_new'][df_unique['Unbalance_status_{0}'.format(day)] == 'Missing'] = 'Missing'
df_unique['Unbalance_status_new'][df_unique['Cell'].isin(data_Cell_per_day_missing.index)] = 'Missing'

# recheck last 2days for OK cases
df_unique['Unbalance_status_new'][(df_unique['pre_output'] == 1) & (
            (df_unique['Unbalance_status_{0}'.format(desired_days[0])] == 'OK') & (
                df_unique['Unbalance_status_{0}'.format(desired_days[1])] == 'OK')) & (
                                      df_unique['Cell'].isin(data_Cell_per_day_nomissing_last2days.index))] = 'OK'


df_unique.to_csv('df_unique_backup_{0}.csv'.format(today))  # 112849
df_unique = df_unique.drop_duplicates(subset='Cell')


nanprovince = df_unique[df_unique['Province'].astype(str) == 'nan']
nanprovince.to_csv('nanprovince.csv')
nanregion = df_unique[df_unique['Region'].astype(str) == 'nan']
nanregion.to_csv('nanregion.csv')
nancity = df_unique[df_unique['City'].astype(str) == 'nan']
nancity.to_csv('nancity.csv')
nanvendor = df_unique[df_unique['Vendor'].astype(str) == 'nan']
nanvendor.to_csv('nanvendor.csv')

# %%   result layer balancing

'''Phase 4: Output: Preparing the results of layer balancing report in excel files.'''
tracker_copy = copy.copy(tracker)  # tracker=tracker_copy
df_unique_unbalanced = df_unique[df_unique['Unbalance_status_new'] != 'Missing']
tracker_temp = tracker[['Cell', 'Delay', 'Unbalance_status']]
tracker_temp = pd.merge(tracker_temp, df_unique_unbalanced[['Cell', 'pre_output', 'Unbalance_status_new']], on='Cell',
                        how='outer')

'''['Cell', 'Sec', 'City', 'Province', 'Region', 'Vendor', 'Delay',
       'Unbalance_status', 'Date', 'pre_output', 'Unbalance_status_new']'''

tracker_temp = tracker_temp.drop_duplicates(subset='Cell', keep='first')

tracker_temp['Unbalance_status_new'] = tracker_temp['Unbalance_status_new'].fillna(tracker_temp['Unbalance_status'])
tracker_temp = tracker_temp[~((tracker_temp['Unbalance_status_new'].isna()) & (tracker_temp['pre_output'] == 0))]


tracker_temp['Unbalance_status'] = tracker_temp['Unbalance_status_new']
tracker_temp = tracker_temp[~ (tracker_temp['Unbalance_status'] == 'OK')]  # remove OK cases

parked = pd.read_excel("Parked_cells.xlsx") # we need to exclude these cells from result
parked = parked.drop_duplicates(subset='cell', keep='last')
trac_unavail = tracker_temp[~tracker_temp['Cell'].isin(data_availability['Cell'])]
trac_unavail.to_csv('trac_unavail.csv')
# %% continue result
trac_park = tracker_temp[tracker_temp['Cell'].isin(parked['cell'])]
tracker_temp['Delay'] = tracker_temp['Delay'].fillna(0)

tracker_temp['Delay'] = tracker_temp['Delay'] + 1
tracker_temp['Delay'][
    (tracker_temp['pre_output'].astype(str) == 'nan') | (tracker_temp['Cell'].isin(parked['cell'])) | (
        ~tracker_temp['Cell'].isin(data_availability['Cell']))] = tracker_temp[
                                                                      'Delay'] - 1  # update by changing the openning days number


tracker_temp_backup = copy.copy(tracker_temp)
tracker = pd.merge(tracker_temp[['Cell', 'Delay', 'Unbalance_status']],
                   tracker[['Cell', 'Sec', 'City', 'Province', 'Region', 'Vendor', 'Date']], on='Cell', how='left')

tracker = pd.merge(tracker, df_unique_unbalanced[['Cell', 'Sec', 'City', 'Province', 'Region', 'Vendor']], on='Cell',
                   how='left', suffixes=('', '_new'))
'''['Cell', 'Delay', 'Sec', 'City', 'Province', 'Region', 'Vendor', 'Date',
       'Sec_new', 'City_new', 'Province_new', 'Region_new', 'Vendor_new']'''
tracker1 = tracker
for col in tracker.columns[3:8]:
    tracker[col] = tracker[col].fillna(tracker['{0}_new'.format(col)])

tracker = tracker[['Cell', 'Sec', 'City', 'Province', 'Region', 'Vendor', 'Delay', 'Unbalance_status', 'Date']]

tracker = tracker.dropna(subset=['Province', 'Region'])
tracker = tracker[tracker['Province'] != 'Others']
tracker = tracker[tracker['Region'] != 'Others']
# a=df_result[df_result['Cell']=='LT5532XA5']
tracker['Date'] = tracker['Date'].fillna(pd.to_datetime(datetime.date.today()))

tracker.to_excel("tracker.xlsx", index=False)

df_result = copy.copy(tracker)
del df_result['Date']


df_result = df_result[df_result['Cell'].isin(data_availability['Cell'])]
df_result_parked = df_result[df_result['Cell'].isin(parked['cell'])]
df_result = df_result[~ df_result['Cell'].isin(parked['cell'])]  # excluded the parked cases
df_result_parked = pd.merge(df_result_parked[['Cell', 'Region']], parked[['cell', 'comment']], left_on='Cell',
                            right_on='cell', how='left')
del df_result_parked['cell']

new_close_cases = pre_output[['Cell', 'Region']][
    ~pre_output['Cell'].isin(df_result['Cell'])]  # Vlook up with prevous report's result to find close cases
new_open_cases = df_result[['Cell', 'Region']][
    ~df_result['Cell'].isin(pre_output['Cell'])]  # Vlook up with prevous report's result to find new open cases
old_open_cases = df_result[['Cell', 'Region']][
    df_result['Cell'].isin(pre_output['Cell'])]  # Vlook up with prevous report's result to find old open cases

closed_cases = new_close_cases[
    (~ new_close_cases['Cell'].isin(parked['cell'])) | (~ new_close_cases['Cell'].isin(trac_unavail['Cell']))]
closed_cases['comment'] = 'closed'
closed_cases = pd.concat([closed_cases, df_result_parked])
closed_cases['Date'] = datetime.date.today()

closed_tracker = pd.concat([closed_tracker, closed_cases])
closed_tracker = closed_tracker.drop_duplicates(subset='Cell', keep='first')

closed_tracker.to_excel("tracker-closed.xlsx", index=False)

# %%output layer balancing
'''Save the outputs of layer balancing list of current report and also plotting the trend plots.'''

with pd.ExcelWriter('unbalanced_cells.xlsx') as writer:  # saving unbalanced_cells.xlsx file
    df_result.to_excel(writer, sheet_name='unbalanced_list', index=False)
    new_close_cases.to_excel(writer, sheet_name='closed_parked', index=False)

    worksheet = writer.sheets['unbalanced_list']  # pull worksheet object
    worksheet.active
    worksheet.set_column('A:A', 10)  # set column width
    # worksheet.set_column('B:B',20)  # set column width
    worksheet.set_column('C:C', 18)  # set column width
    worksheet.set_column('D:D', 18)  # set column width
    worksheet.set_column('E:E', 18)  # set column width
    # worksheet.set_column('F:F',19)  # set column width
    worksheet.set_column('G:G', 10)  # set column width
    worksheet.set_column('H:H', 27)  # set column width
    worksheet.set_column('I:I', 24)  # set column width
    worksheet.set_column('J:J', 40)

    worksheet = writer.sheets['closed_parked']  # pull worksheet object
    worksheet.active
    worksheet.set_column('A:A', 10)  # set column width
    # worksheet.set_column('B:B',20)  # set column width
    worksheet.set_column('C:C', 18)  # set column width
    worksheet.set_column('D:D', 18)  # set column width
    worksheet.set_column('E:E', 18)  # set column width
    # worksheet.set_column('F:F',19)  # set column width
    worksheet.set_column('G:G', 10)  # set column width
    # worksheet.set_column('H:H',23)  # set column width
    worksheet.set_column('H:H', 40)  # set column width
    # worksheet.set_column('J:J',35)

writer.save()

# ------------------------------------plot of total open cases per region ---------------------------
pre_table = pd.read_excel('trend.xlsx') # trend of output numbers for managers to trace the status of network

if len(pre_table['Date'].unique()) > 10:  # select last 20 days
    pre_table = pre_table.drop(pre_table.index[pre_table['Date'] == pre_table['Date'].unique()[0]])
pre_table = pre_table.sort_values(by=['Date', 'Region'])
temp_pd = df_result['Region']
temp_pd_counts = temp_pd.value_counts().T
table1 = pd.DataFrame(temp_pd_counts)
table1 = table1.rename(columns={'Region': '# of cells'})
table1['Region'] = table1.index
table = table1[['Region', '# of cells']]

# -------------error checking
'''ERROR: if you find any error in drawing plots, first find which plot has problem.
          then investigate if any row has been omitted in comparison with previous table?, if yes please add the omitted row with value of zero.
          You can use the below 'search' and 'if' functions to replace the omitted value as a row with zero 
          For example: here the number of cases in 'R5-R10' may be zero, therfore the 'if' function will check it and replace the missed value with zero'''


def search(list, platform):
    for i in range(len(list)):
        if list[i] == platform:
            return True
    return False


Regions = pre_table['Region'].unique()
for region in Regions:
    print(region)
    if search(list(table['Region']), region) == False:
        table.loc[len(table.index)] = [region, 0]

    # -------------end of error cehcking
from datetime import date, timedelta

y = datetime.date.today() - timedelta(days=1)
today = datetime.date.today()
table['Date'] = today
table['Date'] = pd.to_datetime(table['Date'])
table = pd.concat([pre_table, table])

table['X'] = table['Date'].dt.strftime("%m/%d")
fig = plt.figure(1, figsize=(12, 7), dpi=100)

gridspec.GridSpec(2, 2)
# large subplot
plt.subplot2grid((2, 2), (0, 0), colspan=1, rowspan=1)
plt.locator_params(axis='x', nbins=5)
plt.locator_params(axis='y', nbins=8)
sns.set()
sns.set(palette="Set2")
sns.set(font_scale=0.6)
sns.pointplot(x=table['X'],
              y=table['# of cells'], hue=table['Region'], style=table['Region'], marker=True, dashes=False, scale=0.8)

plt.xlabel('')
plt.xticks(rotation=45)
plt.title('Number of total open cases per Region.')
plt.xticks(labels=None, rotation=30)

# repeat the plot
plt.subplot2grid((2, 2), (0, 0), colspan=1, rowspan=1)
plt.locator_params(axis='x', nbins=5)
plt.locator_params(axis='y', nbins=8)
sns.set()
sns.set(palette="Set2")
sns.set(font_scale=0.6)
sns.pointplot(x=table['X'],
              y=table['# of cells'], hue=table['Region'], style=table['Region'], marker=True, dashes=False, scale=0.8)

plt.xlabel('')
plt.xticks(rotation=45)
plt.title('Number of total open cases per Region.')
plt.xticks(labels=None, rotation=30)
plt.tight_layout()



# save trend
del table['X']
table.to_excel("trend.xlsx", index=False)
# -------------------------end

# -------------------------------------------plot of old open cases per region
# pre_table_open_old=pd.read_excel('trend -old-open.xlsx')
#
# if len(pre_table_open_old['Date'].unique())>10: #select last 10 days
#    pre_table_open_old=pre_table_open_old.drop(pre_table_open_old.index[pre_table_open_old['Date'] == pre_table_open_old['Date'].unique()[0]])


temp_pd = old_open_cases['Region']
temp_pd_counts = temp_pd.value_counts().T
table1 = pd.DataFrame(temp_pd_counts)
table1 = table1.rename(columns={'Region': '# of cells'})
table1['Region'] = table1.index
table = table1.sort_values(by='Region')
table = table[['Region', '# of cells']]

for region in Regions:
    # print(region)
    if search(list(table['Region']), region) == False:
        table.loc[len(table.index)] = [region, 0]

table = table.sort_values(by='Region')
# today = datetime.date.today()
table['Date'] = today
table['Date'] = pd.to_datetime(table['Date'])
# table=pd.concat([pre_table_open_old,table])

table['X'] = table['Date'].dt.strftime("%m/%d")

plt.subplot2grid((2, 2), (0, 1), colspan=1, rowspan=1)
plt.locator_params(axis='x', nbins=5)
plt.locator_params(axis='y', nbins=8)
sns.set()
sns.set(palette="Set2")
sns.set(font_scale=0.6)
# sns.pointplot(x=table['X'],
#                  y=table['# of cells'], hue=table['Region'], style=table['Region'], marker=True, dashes=False,scale=0.8)
sns.barplot(x=table['Region'], y=table['# of cells'])

plt.xlabel('')
plt.ylabel('')
plt.xticks(labels=None, rotation=30)
plt.title('Number of old open cases per Region.')

plt.tight_layout()

# repeat plot
plt.subplot2grid((2, 2), (0, 1), colspan=1, rowspan=1)
plt.locator_params(axis='x', nbins=5)
plt.locator_params(axis='y', nbins=8)
sns.set()
sns.set(palette="Set2")
sns.set(font_scale=0.6)
# sns.pointplot(x=table['X'],
#                  y=table['# of cells'], hue=table['Region'], style=table['Region'], marker=True, dashes=False,scale=0.8)
sns.barplot(x=table['Region'], y=table['# of cells'])
plt.xlabel('')
plt.ylabel('')
plt.xticks(labels=None, rotation=30)
plt.title('Number of old open cases per Region.')

plt.tight_layout()



temp_pd = new_open_cases['Region']
temp_pd_counts = temp_pd.value_counts().T
table1 = pd.DataFrame(temp_pd_counts)
table1 = table1.rename(columns={'Region': '# of cells'})
table1['Region'] = table1.index
table = table1.sort_values(by='Region')
table = table[['Region', '# of cells']]

for region in Regions:
    # print(region)
    if search(list(table['Region']), region) == False:
        table.loc[len(table.index)] = [region, 0]

table = table.sort_values(by='Region')
table['Date'] = today
table['Date'] = pd.to_datetime(table['Date'])

table['X'] = table['Date'].dt.strftime("%m/%d")

plt.subplot2grid((2, 2), (1, 1), colspan=1, rowspan=1)
plt.locator_params(axis='x', nbins=5)
plt.locator_params(axis='y', nbins=8)
sns.set()
sns.set(palette="Set2")
sns.set(font_scale=0.6)
sns.barplot(x=table['Region'], y=table['# of cells'])

plt.xlabel('Region')
plt.ylabel('')
plt.xticks(labels=None, rotation=30)
plt.title('Number of new open cases per Region.')

plt.tight_layout()

# repeat plot
plt.subplot2grid((2, 2), (1, 1), colspan=1, rowspan=1)
plt.locator_params(axis='x', nbins=5)
plt.locator_params(axis='y', nbins=8)
sns.set()
sns.set(palette="Set2")
sns.set(font_scale=0.6)
sns.barplot(x=table['Region'], y=table['# of cells'])

plt.xlabel('Region')
plt.ylabel('')
plt.xticks(labels=None, rotation=30)
plt.title('Number of new open cases per Region.')

plt.tight_layout()

# --------------------end


# --------------------plot of new close cases per region
pre_table_close = pd.read_excel("trend -new-close.xlsx")

if len(pre_table_close['Date'].unique()) > 10:  # select last 10 days
    pre_table_close = pre_table_close.drop(
        pre_table_close.index[pre_table_close['Date'] == pre_table_close['Date'].unique()[0]])

temp_pd = new_close_cases['Region']
temp_pd_counts = temp_pd.value_counts().T
table1 = pd.DataFrame(temp_pd_counts)
table1 = table1.rename(columns={'Region': '# of cells'})
table1['Region'] = table1.index
table = table1[['Region', '# of cells']]

for region in Regions:
    # print(region)
    if search(list(table['Region']), region) == False:
        table.loc[len(table.index)] = [region, 0]

table = table.sort_values(by='Region')

table['Date'] = today
table['Date'] = pd.to_datetime(table['Date'])
table = pd.concat([pre_table_close, table])

table['X'] = table['Date'].dt.strftime("%m/%d")

plt.subplot2grid((2, 2), (1, 0), colspan=1, rowspan=1)
plt.locator_params(axis='x', nbins=5)
plt.locator_params(axis='y', nbins=8)
sns.set()
sns.set(palette="Set2")
sns.set(font_scale=0.6)
sns.pointplot(x=table['X'],
              y=table['# of cells'], hue=table['Region'], style=table['Region'], marker=True, dashes=False, scale=0.8)

plt.xlabel('Date')
plt.ylabel('')
plt.xticks(labels=None, rotation=30)
plt.title('Number of new close cases per Region.')

plt.tight_layout()

# repeat plot
plt.subplot2grid((2, 2), (1, 0), colspan=1, rowspan=1)
plt.locator_params(axis='x', nbins=5)
plt.locator_params(axis='y', nbins=8)
sns.set()
sns.set(palette="Set2")
sns.set(font_scale=0.6)
sns.pointplot(x=table['X'],
              y=table['# of cells'], hue=table['Region'], style=table['Region'], marker=True, dashes=False, scale=0.8)

plt.xlabel('Date')
plt.ylabel('')
plt.xticks(labels=None, rotation=30)
plt.title('Number of new close cases per Region.')

plt.tight_layout()

# save trend
del table['X']
table.to_excel("trend -new-close.xlsx", index=False)
# save total fig of layer balancing

plt.savefig('picture.png', bbox_inches='tight')

