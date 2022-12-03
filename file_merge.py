#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 15:19:42 2021

@author: m31781
"""

import pandas as pd
import os
#import xlrd

data_path = r'/Users/m31781/Documents/NFL Decision Tree/Second Run/GAME_DATA'

os.chdir(data_path)
file_names = os.listdir(data_path)


df_dict = {}
for file in file_names:
    
    game_df = pd.read_csv(file)
    game_df = game_df[1:18]
    
    column_names = ['Week', 'Day', 'Date', 'Time', 'boxscore', 'result', 'OT', 'Rec', 'home', 'Opp', 'TM_Score', 'Opp_Score',
     'O_1stD', 'O_Tot_Yd', 'O_P_Yd', 'O_R_Yd', 'O_TO', 'D_1stD', 'D_Tot_Yd', 'D_P_Yd', 'D_R_Yd', 'D_TO', 
     'O_EP', 'D_EP', 'SP_TEAMS_EP']
    
    game_df.columns = column_names
    
    f_column_names = ['Week', 'result', 'home', 'Opp', 'TM_Score', 'Opp_Score',
     'O_1stD', 'O_Tot_Yd', 'O_P_Yd', 'O_R_Yd', 'O_TO', 'D_1stD', 'D_Tot_Yd', 'D_P_Yd', 'D_R_Yd', 'D_TO']
    
    game_df = game_df[f_column_names].reset_index(drop = True)
    game_df = game_df[game_df['Opp'] != 'Bye Week']
    
    #Column conversions
    game_df = game_df.assign(Result = [1 if a == 'W' else 0 for a in game_df['result']])
    game_df = game_df.assign(Home = [0 if a == '@' else 1 for a in game_df['home']])
    game_df = game_df.drop(['result', 'home'], axis = 1)
    
    game_df.insert(0, 'Tm', file[0:3])
    
    df_dict[file[0:3]] = game_df
    
#complete data set
com_data = pd.concat(df_dict.values(), ignore_index=True).fillna(0)
    
#read in output from og model
ada_results = pd.read_csv(r'/Users/m31781/Documents/NFL Decision Tree/Second Run/2020_ADA_results.csv')
log_results = pd.read_csv(r'/Users/m31781/Documents/NFL Decision Tree/Second Run/2020_LOG_results.csv')

ada_results['norm'] = (ada_results['pred_mean']-ada_results['pred_mean'].min())/(ada_results['pred_mean'].max()-ada_results['pred_mean'].min())
ada_results = ada_results.sort_values(by=['norm'], ascending = False)
log_results['norm'] = (log_results['Prediction']-log_results['Prediction'].min())/(log_results['Prediction'].max()-log_results['Prediction'].min())
log_results = log_results.sort_values(by=['norm'], ascending = False)


#%%


#Add ADA Results and Log Results
team_names = pd.read_csv(r'/Users/m31781/Documents/NFL Decision Tree/Second Run/team_names.csv')
com_data = com_data.merge(team_names, how = 'left', left_on = 'Tm', right_on = 'ABR')

com_data = com_data.merge(ada_results[['Team', 'pred_mean']], how = 'left', left_on = 'FULL_TEAM_NAME', right_on = 'Team')
com_data = com_data.merge(log_results[['Team', 'Prediction']], how = 'left', left_on = 'FULL_TEAM_NAME', right_on = 'Team')

com_data = com_data[['Tm', 'FULL_TEAM_NAME',  'Week', 'Opp', 'TM_Score', 'Opp_Score', 'O_1stD', 'O_Tot_Yd',
        'O_P_Yd', 'O_R_Yd', 'O_TO', 'D_1stD', 'D_Tot_Yd', 'D_P_Yd', 'D_R_Yd',
        'D_TO', 'Result', 'Home', 'pred_mean', 'Prediction']]

com_data.columns = ['Tm', 'FULL_TEAM_NAME', 'Week', 'Opp', 'TM_Score', 'Opp_Score', 'O_1stD', 'O_Tot_Yd',
        'O_P_Yd', 'O_R_Yd', 'O_TO', 'D_1stD', 'D_Tot_Yd', 'D_P_Yd', 'D_R_Yd',
        'D_TO', 'Result', 'Home', 'ADA_Pred_Mean', 'LOG_Prediction']
        

#%%
# X = np.asarray(test[train_columns])
# y = np.asarray(test['Superbowl'])
# print(X.shape)
# print(y.shape)

# #normalize
# from sklearn import preprocessing
# X = preprocessing.StandardScaler().fit(X).transform(X)
# #X[0:5]
#%%

#write data
os.chdir(r'/Users/m31781/Documents/NFL Decision Tree/Second Run')
#com_data.to_csv('2020_NFL_Game_Data.csv', index = False)
