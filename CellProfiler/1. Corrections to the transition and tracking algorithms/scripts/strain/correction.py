import csv
import pandas as pd
import numpy as np
import pickle
import os
from scipy.spatial import distance_matrix



def find_related_bacteria (df , root_bac_index_in_df, Next_ParentImageNumber, Next_ParentObjectNumber, TimeStep, bac_index_list = None):
        """
            goal:  From the bacteria dataframe, find the row index of bacteria related to a specific bacterium (bacterium without a parent)
            input: root_bac_index_in_df   number   The row index of the corresponding bacterium
            output: bac_index_list   list   row index of related bacteria
            
        """

        if bac_index_list is None:  # create a new result if no intermediate was given
            bac_index_list = []
            bac_index_list.append(root_bac_index_in_df)

        # related bacteri in next timestep
        next_timestep = TimeStep + 1
        #print(df.iloc[-1]['ImageNumber'])
        #print('id: '+ str(root_bac_index_in_df))
        #print('TimeStep'+str(TimeStep))
        #print('ParentImageNumber'+ str(Next_ParentImageNumber))
        #print('ParentObjectNumber'+str(Next_ParentObjectNumber))
        if next_timestep < df.iloc[-1]['ImageNumber']:
            bac_in_next_timestep = df.loc[(df["ImageNumber"] == next_timestep) &
                                          (df["TrackObjects_ParentImageNumber_50"] == Next_ParentImageNumber) &
                                          (df["TrackObjects_ParentObjectNumber_50"] == Next_ParentObjectNumber)]

            if bac_in_next_timestep.shape[0] >0:
                #print(bac_in_next_timestep)
                bac_in_next_timestep_index = bac_in_next_timestep.index.tolist()
                bac_in_next_timestep  = bac_in_next_timestep.reset_index(drop=True)
                #print("yyyyyy")
                #print(bac_index_list)
                bac_index_list.extend(bac_in_next_timestep_index)
                #print(bac_index_list)
                
                for bac_index in range(len(bac_in_next_timestep_index)):
                    root_bac_index_in_df = bac_in_next_timestep_index[bac_index]
                    Next_ParentImageNumber =next_timestep
                    Next_ParentObjectNumber = bac_in_next_timestep.iloc[bac_index]["ObjectNumber"]
                    TimeStep = next_timestep
                    find_related_bacteria (df , root_bac_index_in_df, Next_ParentImageNumber, Next_ParentObjectNumber, TimeStep, bac_index_list )
                
        return bac_index_list


def dropIndex(df):
    """
        goal: remove bacteria that have no parents
        input: df    dataframe   bacteria dataframe
        output: df   dataframe   modified dataframe
        
    """
    
    df = df.loc[df["drop"]==False].reset_index(drop=True)
    return df



def lineageBacteriaAfterThisTimeStep (dataFrame, Bacteria):
    """
        goal: find family tree of corresponding bacterium
        input: dataframe   dataframe   bacteria information dataframe
        input: Bacteria    dataframe   Associated dataframe row with bacterium
        output: dataFrameOfLineage   dataframe   dataframe of related bacteria (family tree) to corresponding bacterium
    """
    dataFrameOfLineage = dataFrame.loc[(dataFrame["TrackObjects_Label_50"]==Bacteria["TrackObjects_Label_50"]) &
                                  (dataFrame["ImageNumber"] >= Bacteria["ImageNumber"])]
    return dataFrameOfLineage



def incorrectDaughter(dataFrameOfLineage,Bacteria,Bacid):

    """
        goal: find index row of incorrect daughter in dataframe
        input: dataFrameOfLineage   dataframe   dataframe of related bacteria (family tree) to corresponding bacterium
        input: Bacteria    dataframe   Associated dataframe row with bacterium
        output incorrect_daughter_row_index   number row index of incorrect daughter bacterium in bacteria dataframe
    """
    
    Parent_time_step_of_cell=Bacteria["ImageNumber"]
    Parent_index_of_cell=Bacteria["ObjectNumber"]
    division_occ=False
    LastTimeStep = dataFrameOfLineage["ImageNumber"].iloc[-1]

    incorrect_daughter_row_index = 0
    
    while (division_occ==False) and (LastTimeStep != Parent_time_step_of_cell):
        
        reletive_Bacteria_in_next_timestep = dataFrameOfLineage.loc[(dataFrameOfLineage["TrackObjects_ParentImageNumber_50"]==Parent_time_step_of_cell) &
                                                                  (dataFrameOfLineage["TrackObjects_ParentObjectNumber_50"]==Parent_index_of_cell)]

        Number_of_reletive_bacteria = reletive_Bacteria_in_next_timestep.shape[0]

        if  Number_of_reletive_bacteria == 1 :
                       Parent_index_of_cell=reletive_Bacteria_in_next_timestep.iloc[0]["ObjectNumber"]
                       Parent_time_step_of_cell=reletive_Bacteria_in_next_timestep.iloc[0]["ImageNumber"]
                       
        elif Number_of_reletive_bacteria == 2: # the division has been found
                   division_occ=True

        elif Number_of_reletive_bacteria==0: #interupt (family tree of corresponding bacterium has not been continued)
                   break
        else:
            Length=reletive_Bacteria_in_next_timestep["AreaShape_MajorAxisLength"].values
            minLength=min(reletive_Bacteria_in_next_timestep["AreaShape_MajorAxisLength"].values)
            incorrect_daughter=np.where(Length == minLength)
            incorrect_daughter_row_index = reletive_Bacteria_in_next_timestep.index.values[incorrect_daughter][0]
            division_occ=True

    return incorrect_daughter_row_index


def correction_transition (df):
    """
        goal: For bacteria without parent, assign labels, ParentImageNumber, and ParentObjectNumber
        input: df    dataframe   bacteria dataframe
        output: df   dataframe   modified dataframe (without any transitions)
        
    """
    
    # add new column to dataframe
    # During processing, I need it to find bacteria that have no parents (and remove them at the end)
    df ["drop"] = False
    Timesteps=list(set(df['ImageNumber'].values))
    # remove last time step
    Timesteps.pop()
    for t in Timesteps:
        # filter current time step bacteria information
        current_timestep_bac = df.loc[(df["ImageNumber"] == t) & (df["drop"] == False)]
        current_timestep_bac_index = current_timestep_bac.index
        current_timestep_bac = current_timestep_bac.reset_index(drop=True)

        # filter current time step sudden bacteria information (bacteria without parent)
        #current_timestep_sudden_bac = df.loc[(df["ImageNumber"] == t) &
        #                                     (df["TrackObjects_ParentImageNumber_50"] == 0) &
        #                                     (df["drop"] == False)]
        #current_timestep_sudden_bac_index = current_timestep_sudden_bac.index.tolist()
        #current_timestep_sudden_bac  = current_timestep_sudden_bac.reset_index(drop=True)

        # filter next time step bacteria information
        next_timestep_bac = df.loc[df["ImageNumber"] == (t+1) & (df["drop"] == False)]
        next_timestep_bac_index = next_timestep_bac.index
        next_timestep_bac = next_timestep_bac.reset_index(drop=True)

        # filter next time step sudden bacteria information (bacteria without parent)
        next_timestep_sudden_bac = df.loc[(df["ImageNumber"] == (t+1)) &
                                          (df["TrackObjects_ParentImageNumber_50"] == 0) &
                                          (df["drop"] == False)]
        next_timestep_sudden_bac_index = next_timestep_sudden_bac.index
        next_timestep_sudden_bac = next_timestep_sudden_bac.reset_index(drop=True)
        
        #print(current_timestep_bac.shape[0])
        #print(next_timestep_sudden_bac.shape[0])

        if next_timestep_sudden_bac.shape[0] > 0:
            # create distance matrix (rows: next time step sudden bacteria, columns: current time step bacteria)
            distance_df = pd.DataFrame(distance_matrix(next_timestep_sudden_bac[["AreaShape_Center_X","AreaShape_Center_Y"]].values, current_timestep_bac[["AreaShape_Center_X","AreaShape_Center_Y"]].values),
                                           index = next_timestep_sudden_bac_index, columns = current_timestep_bac_index)
            #print(distance_df)
            # find the parent of sudden bacteri in next time step
            for bac_index in range(len(next_timestep_sudden_bac_index.tolist())):
                correspond_distance_df_row = distance_df.iloc[bac_index].values.tolist()
                sorted_distance = [(distance, current_bac_index) for distance, current_bac_index in sorted(zip(correspond_distance_df_row , current_timestep_bac_index.tolist()))]

                # was the parent found?
                was_parent_found = False
                element_index_in_sorted_distance = 0
                while was_parent_found == False and element_index_in_sorted_distance < len(sorted_distance):
                    sorted_distance_bac_index = sorted_distance[element_index_in_sorted_distance][1]
                    # find number of related bacteria to this bacterium in next time step
                    ParentImageNumber = df.iloc[sorted_distance_bac_index]['ImageNumber']
                    ParentObjectNumber = df.iloc[sorted_distance_bac_index]['ObjectNumber']
                    related_bac_in_next_timestep = next_timestep_bac.loc[(next_timestep_bac["TrackObjects_ParentImageNumber_50"] == ParentImageNumber) &
                                                                         (next_timestep_bac["TrackObjects_ParentObjectNumber_50"] == ParentObjectNumber)]
                    if related_bac_in_next_timestep.shape[0] != 2:
                        was_parent_found = True
                    else:
                        element_index_in_sorted_distance += 1

                # find related bacteria to this bacterium
                root_bac_index_in_df = next_timestep_sudden_bac_index.tolist()[bac_index]
                Next_ParentImageNumber = t+1
                Next_ParentObjectNumber = df.iloc[root_bac_index_in_df]["ObjectNumber"]
                TimeStep = t+1
                #print(root_bac_index_in_df)
                #print(Next_ParentImageNumber)
                #print(Next_ParentObjectNumber)
                related_bacteria = find_related_bacteria (df ,  root_bac_index_in_df, Next_ParentImageNumber, Next_ParentObjectNumber, TimeStep)
                
                if was_parent_found == False:
                    # it means that no parent has been found for this bacterium
                    # remove this bacterium and related bacteria
                    for idx in related_bacteria :
                        # change bacteria lable to parent lable
                        df.at[idx,"drop"] = True
                else:
                    # change parent image number & parent object number of root bacterium
                    df.at[root_bac_index_in_df, 'TrackObjects_ParentImageNumber_50'] = df.iloc[sorted_distance_bac_index]["ImageNumber"]
                    df.at[root_bac_index_in_df, 'TrackObjects_ParentObjectNumber_50'] = df.iloc[sorted_distance_bac_index]["ObjectNumber"]
                    for idx in related_bacteria :
                        # change bacteria lable to parent lable
                        df.at[idx,"TrackObjects_Label_50"] = df.iloc[sorted_distance_bac_index]["TrackObjects_Label_50"]

                #print(sorted_distance)
                #print(len(sorted_distance))

    # remove bacteria that have no parents
    df = dropIndex(df)
    # remove the smallest daughter, and related bacteria
    df = correction_tracking(df)
    return df


def correction_tracking(df):
        """
            goal:  Find bacteria with three daughters, remove the smallest daughter, and related bacteria
            input: df   dataframe   Bacteria information dataframe without transitions
            output df   dataframe   modified dataframe (without incorrect daughters, and related bacteria to them)

        """
        for index, row in df.iterrows():
           if df.iloc[index]["drop"] == False:

               dataFrameOfLineage = lineageBacteriaAfterThisTimeStep (df,row)

               incorrect_daughter_row_index = incorrectDaughter(dataFrameOfLineage,row,index)
               
               if incorrect_daughter_row_index != 0:
                   # it mean that: incorrect daughter has been found
                   # now, we should find related bacteria to the incorrect daughter
                    root_bac_index_in_df = incorrect_daughter_row_index
                    Next_ParentImageNumber = df.iloc[incorrect_daughter_row_index]["ImageNumber"]
                    Next_ParentObjectNumber = df.iloc[incorrect_daughter_row_index]["ObjectNumber"]
                    TimeStep = Next_ParentImageNumber
                    #print(root_bac_index_in_df)
                    #print(Next_ParentImageNumber)
                    #print(Next_ParentObjectNumber)
                    related_bacteria = find_related_bacteria (df ,  root_bac_index_in_df, Next_ParentImageNumber, Next_ParentObjectNumber, TimeStep)
                    # remove this bacterium and related bacteria
                    for idx in related_bacteria :
                        # change bacteria lable to parent lable
                        df.at[idx,"drop"] = True
                        
        # remove incorrect daughter bacteria , and related bacteria to them
        df = dropIndex(df)
        # remove 'drop' column
        df.drop('drop', axis=1, inplace=True)
        df.to_csv('file.csv', sep='\t', index = False)
        #print('okeit')
        return df

    
