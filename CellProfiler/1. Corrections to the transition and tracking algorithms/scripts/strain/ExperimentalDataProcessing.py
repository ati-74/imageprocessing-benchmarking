import math
import statistics
from collections import Counter
import numpy as np
import pandas as pd
import sys
from sklearn.linear_model import LinearRegression



def lineageBacteriaAfterThisTimeStep (dataFrame,Bacteria):
    dataFrameOfLineage = dataFrame.loc[(dataFrame["TrackObjects_Label_50"]==Bacteria["TrackObjects_Label_50"]) &
                                  (dataFrame["ImageNumber"] >= Bacteria["ImageNumber"])]
    return dataFrameOfLineage
                                  

def divisionOccurrence(dataFrameOfLineage,Bacteria,Bacid):
    Parent_time_step_of_cell=Bacteria["ImageNumber"]
    Parent_index_of_cell=Bacteria["ObjectNumber"]
    division_occ=False
    lifehistoryIndex=[]
    
    Bacteriaindex=Bacid
    lifehistoryIndex.append(Bacteriaindex)
    incorrectBacteriumIndex=0
    LastTimeStep=dataFrameOfLineage["ImageNumber"].iloc[-1]
    
    while (division_occ==False) and (LastTimeStep != Parent_time_step_of_cell):
        reletive_Bacteria_in_next_timestep=dataFrameOfLineage.loc[(dataFrameOfLineage["TrackObjects_ParentImageNumber_50"]==Parent_time_step_of_cell) & (dataFrameOfLineage["TrackObjects_ParentObjectNumber_50"]==Parent_index_of_cell)]

        Number_of_reletive_bacteria=reletive_Bacteria_in_next_timestep.shape[0]

        if  Number_of_reletive_bacteria==1 :
                       Parent_index_of_cell=reletive_Bacteria_in_next_timestep.iloc[0]["ObjectNumber"]
                       Parent_time_step_of_cell=reletive_Bacteria_in_next_timestep.iloc[0]["ImageNumber"]
                       Bacteriaindex=reletive_Bacteria_in_next_timestep.index.tolist()[0]
                       lifehistoryIndex.append(Bacteriaindex)
        elif Number_of_reletive_bacteria==2:
                   division_occ=True
                   last_timestep_before_division=Parent_time_step_of_cell
                   
        elif Number_of_reletive_bacteria==0: #interupt
                   last_timestep_before_division=Parent_time_step_of_cell
                   break
        else:
            Length=reletive_Bacteria_in_next_timestep["AreaShape_MajorAxisLength"].values
            minLength=min(reletive_Bacteria_in_next_timestep["AreaShape_MajorAxisLength"].values)
            incorrectBacterium=np.where(Length == minLength)
            incorrectBacteriumIndex=reletive_Bacteria_in_next_timestep.index.values[incorrectBacterium][0]
            division_occ=True
            last_timestep_before_division=Parent_time_step_of_cell
            print("Warning: Three cells are produced from a single cell!")
            print("Lable:" + str(dataFrameOfLineage["TrackObjects_Label_50"].iloc[0]))

    if division_occ==False and LastTimeStep == Parent_time_step_of_cell:
               last_timestep_before_division=dataFrameOfLineage["ImageNumber"].iloc[-1]

    division_status={"division_occ":division_occ,"last_timestep_before_division":last_timestep_before_division,"lifeHistoryIndex":lifehistoryIndex,"incorrectBacteriumIndex":incorrectBacteriumIndex}

    return division_status


def LifeHistory (dataFrameOfLineage,lifehistoryIndex):
    dfLifehistory=dataFrameOfLineage.loc[lifehistoryIndex]

    return dfLifehistory
    

def AverageGrowthRate(divisionLength,birthLength,t):
    elongation_rate=round((math.log(divisionLength)-math.log(birthLength))/t,3)
    return elongation_rate


def LinearRegressionGrowthRate(time,length):
    linear_regressor = LinearRegression()  # create object for the class
    linear_regressor.fit(np.array(time).reshape(-1, 1),np.log(np.array(length).reshape(-1, 1)))  # perform linear regression
    elongation_rate=round(linear_regressor.coef_[0][0],3)
    return elongation_rate


def growthRate (dfLifehistory,interval_time,growth_rate_method):
           LifeHistoryLength=dfLifehistory.shape[0]      
           #calculatation of new feature
           divisionLength=dfLifehistory.iloc[[-1]]["AreaShape_MajorAxisLength"].values[0]
           birthLength=dfLifehistory.iloc[[0]]["AreaShape_MajorAxisLength"].values[0] #length of bacteria when they are born
           #this condition checks the life history of bacteria
           #If the bacterium exists only one time step: NaN will be reported.           
           if (LifeHistoryLength>1):
               if(growth_rate_method=="Average"):
                    t=LifeHistoryLength*interval_time
                    elongation_rate=AverageGrowthRate(divisionLength,birthLength,t)
               if (growth_rate_method=="Linear Regression"):
                    #linear regression
                    time=dfLifehistory["ImageNumber"].values*interval_time
                    length=dfLifehistory["AreaShape_MajorAxisLength"].values
                    elongation_rate=LinearRegressionGrowthRate(time,length)
           else:
                elongation_rate="NaN" #shows: bacterium is present for only one timestep.

           return elongation_rate

def SameIdBacteria (dataFrame,id_of_bacteria):
   dataFrameOfSameBacteria = dataFrame.loc[dataFrame["id"]==id_of_bacteria]
   SameBacteriaIndex=dataFrameOfSameBacteria.index.tolist()
   return SameBacteriaIndex 

def dropIndex(dataFrame):
    dataFrame = dataFrame.loc[dataFrame["drop"]==False].reset_index(drop=True)
    return dataFrame


def CompletingParenteId(dataFrame):
        bacteria_id=1
        #dataFrame=dataFrame.loc[(dataFrame['ImageNumber']==1).values]
        for index, row in dataFrame.iterrows():
           if (dataFrame.iloc[index]["lineage"]!='') and (dataFrame.iloc[index]["id"]>=bacteria_id):
               id_of_bacteria=dataFrame.iloc[index]["id"]
               SameBacteriaIndex=SameIdBacteria (dataFrame,id_of_bacteria)
               for idx in SameBacteriaIndex:
                   dataFrame.at[idx,"lineage"]=dataFrame.iloc[index]["lineage"]
               bacteria_id=dataFrame.iloc[index]["id"]+1
        return dataFrame

    
def AssignCellType(fluorescence_df):
    """
    Assigns cell type based on the fluorescence intensity of a cell.
    cell_type number is ascending based on alphabetical order, followed by types based on channel overlap.
        
    @param fluorescence_df  DataFrame   Fluorescence columns for a specific cell (i.e. a single row of CPdata['Intensity_MeanIntensity_...'])
    
    return cell_type        int         cell_type identifier; cell_type = 0 means no fluorescence   
    
    TODO: allow user to select the fluorescence intensity threshold for selection
    """
    
    #Initialize storage variables    
    cell_type = 0
    
    n_channels = len(fluorescence_df)
    
    #TODO: could do this in a loop to make it work for arbitrary n_channels; would need to specify a vector for the threshold value to pass.
    if n_channels == 1:
        if fluorescence_df[0] > 0.1:
            cell_type = 1
            
    if n_channels == 2:
        channel_threshold_passed = [False,False]
        if fluorescence_df[0] > 0.1:
            channel_threshold_passed[0] = True
        if fluorescence_df[1] > 0.1:
            channel_threshold_passed[1] = True
            
        #Identify cell type
        if channel_threshold_passed == [True,False]:
            cell_type = 1
        elif channel_threshold_passed == [False,True]:
            cell_type = 2
        elif channel_threshold_passed == [True,True]:
            cell_type = 3
    
    return cell_type

#elongation rate: tracking each bacterium and calculate its elongation rate based on formuala: (ln(l(last))-ln(l(first))/age
#some odd types in calculating elongation rate: 1) life history =1 ---> I store elongation rate as NaN /// 2) some times CellProfiler reports the length
#of bacteria as zero, so in this case I store elongation rate as zero ///
#Furthermore:
#I find the first time step that the bacterium is born and the last time step that the bacterium exists,  
#also the length of bacteria in first time step of its life history and also the length of bacteria 
#in the last time step of its life history.    

def BacteriaAnalysis(dataFrame,interval_time,growth_rate_method):
    #same Bacteria features
    dataFrame ["id"]=''
    dataFrame ["divideFlag"]=False
    dataFrame ["cellAge"]=''    
    dataFrame ["growthRate"]=''
    dataFrame ["LifeHistory"]=''
    dataFrame ["startVol"]=''
    dataFrame ["targetVol"]=''
    dataFrame ["lineage"]=''
    dataFrame ["drop"]=False

    #single cell Features
    dataFrame["pos"] = ''
    dataFrame["time"] = ''    
    dataFrame["radius"] = ''
    dataFrame["cellType"] = '' 
    
    #fluorescence intensity columns
    fluorescence_intensities = [col for col in dataFrame if col.startswith('Intensity_MeanIntensity')]

    id_of_bacteria = 1    
    for index, row in dataFrame.iterrows():
           if not dataFrame.iloc[index]["growthRate"]:

               dataFrameOfLineage = lineageBacteriaAfterThisTimeStep (dataFrame,row)

               division_status = divisionOccurrence(dataFrameOfLineage,row,index)
               
               if division_status["incorrectBacteriumIndex"]!=0:
                   drop_index=division_status["incorrectBacteriumIndex"]
                   dataFrame.at[drop_index,"drop"]=True   
               
               dfLifehistory=LifeHistory(dataFrameOfLineage,division_status["lifeHistoryIndex"])
               elongation_rate=growthRate(dfLifehistory,interval_time,growth_rate_method)

               LifehistoryIndex=dfLifehistory.index.tolist()
               LifeHistoryLength=dfLifehistory.shape[0]
               divisionLength=dfLifehistory.iloc[[-1]]["AreaShape_MajorAxisLength"].values[0]
               birthLength=dfLifehistory.iloc[[0]]["AreaShape_MajorAxisLength"].values[0] #length of bacteria when they are born
               Cell_Age=1

               
               if dataFrame.iloc[index]["drop"]==True:
                   for idx in LifehistoryIndex:
                           dataFrame.at[idx,"drop"]=True
                           dataFrame.at[idx,"growthRate"]=elongation_rate
               else:
                   for idx in LifehistoryIndex:
                           dataFrame.at[idx,"id"]=id_of_bacteria
                           dataFrame.at[idx,"cellAge"]=Cell_Age
                           dataFrame.at[idx,"growthRate"]=elongation_rate
                           dataFrame.at[idx,"LifeHistory"]=LifeHistoryLength
                           dataFrame.at[idx,"startVol"]=birthLength
                           dataFrame.at[idx,"targetVol"]=divisionLength
                           Cell_Age+=1
                   id_of_bacteria+=1

               if division_status["division_occ"]:
                   lastTimeStepOfBacteria=LifehistoryIndex[-1]
                   dataFrame.at[lastTimeStepOfBacteria,"divideFlag"]=True
                   
               #duaghters
                   divisionTime=division_status["last_timestep_before_division"]+1
                   dataFrameOfdaughters = dataFrameOfLineage.loc[(dataFrameOfLineage["ImageNumber"] == divisionTime)]
                   daughterIndex=dataFrameOfdaughters.index.tolist()

                   parent_id=id_of_bacteria
                   
                   for daughetridx in daughterIndex:
                       dataFrame.at[daughetridx,"lineage"]=parent_id
                       if dataFrame.iloc[index]["drop"]==True:
                           dataFrame.at[daughetridx,"drop"]=True                     

           #SingleCellFeatures
           try:
               dataFrame.at[index,"pos"]=[row["Location_Center_X"],row["Location_Center_Y"]]
           except:
               dataFrame.at[index,"pos"]=[row["AreaShape_Center_X"],row["AreaShape_Center_Y"]]
           dataFrame.at[index,"time"]=row["ImageNumber"]*interval_time
           dataFrame.at[index,"radius"]=row["AreaShape_MinorAxisLength"]/2
           # modification of bacterium orientation
           # -(angle + 90) * np.pi / 180
           dataFrame.at[index,"AreaShape_Orientation"] = (-1 * dataFrame.iloc[index]["AreaShape_Orientation"] + 90) * np.pi / 180
            
       #For fluorescence readings; maybe this would be cleaner if placed in different function?
           if fluorescence_intensities:
                dataFrame.at[index,"cellType"] = AssignCellType(row[fluorescence_intensities])            

    dataFrame=dropIndex(dataFrame)
    dataFrame=CompletingParenteId(dataFrame)
    #rename some columns
    FinaldataFrame = dataFrame.rename(columns={'AreaShape_MajorAxisLength': 'length','AreaShape_Orientation':'orientation'})
    FinaldataFrame = FinaldataFrame[['ImageNumber','id','divideFlag','cellAge','growthRate','LifeHistory','startVol','targetVol','lineage','pos','time','radius','length','orientation','cellType']]
    return FinaldataFrame






