import csv
import pandas as pd
import numpy as np
import pickle
import os
from ExperimentalDataProcessing import BacteriaAnalysis
from correction import correction_transition


def ProcessData(input_file,output_directory,interval_time=1,growth_rate_method="Average", um_per_pixel = 0.144):
    """
    The main function that processes CellProfiler data.
    .pickle Files are exported to the same directory as input_file.
    
    @param interval_time        float   Time between images
    @param growth_rate_method   str     Method for calculating the growth rate
    @param input_file           .csv    CellProfiler data
    """

    #Parsing CellProfiler output
    dataFrame=pd.read_csv(input_file)
    #remove related rows to bacteria with zero MajorAxisLength
    dataFrame=dataFrame.loc[dataFrame["AreaShape_MajorAxisLength"] != 0].reset_index(drop=True)
    #correction dataframe
    dataFrame = correction_transition (dataFrame)
    # print(dataFrame )

    # Currently, I do not think this command is needed. So, I comment it.
    #remove Nan lables and zero MajorAxisLength
    # dataFrame=dataFrame.loc[dataFrame["TrackObjects_Label_50"].notnull()].reset_index(drop=True)
                                  
    # Convert distances to um (0.144 um/pixel on 63X objective)
    dataFrame["AreaShape_MajorAxisLength"] = dataFrame["AreaShape_MajorAxisLength"]*um_per_pixel
    dataFrame["AreaShape_MinorAxisLength"] = dataFrame["AreaShape_MinorAxisLength"]*um_per_pixel
    try:
        dataFrame["Location_Center_X"] = dataFrame["Location_Center_X"]*um_per_pixel
        dataFrame["Location_Center_Y"] = dataFrame["Location_Center_Y"]*um_per_pixel
    except:
        dataFrame["AreaShape_Center_X"] = dataFrame["AreaShape_Center_X"]*um_per_pixel
        dataFrame["AreaShape_Center_Y"] = dataFrame["AreaShape_Center_Y"]*um_per_pixel

    #process the tracking data
    processed_data=BacteriaAnalysis(dataFrame,interval_time,growth_rate_method)
    output_directory=output_directory+"/"
    
    CreatePickleFiles(processed_data,output_directory)
    processed_data.rename(columns={'ImageNumber': 'stepNum'},inplace=True)

    path=output_directory+input_file.split('/')[-1].split('.')[0]+"-"+growth_rate_method+"-analysis"
    #write to csv
    processed_data.to_csv(path+'.csv', index=False)

def CreatePickleFiles(df,path):
    """
    Saves processed data in a dictionary similar to CellModeller output style and exports as .pickle files
    @param df       data after being processed in ExperimentalDataProcessing.py
    @param path     path where .pickle files are saved
    """    
    lineage={}
    Timesteps=list(set(df['ImageNumber'].values))
    for t in Timesteps:
        lineage_data_frame = df.loc[(df["ImageNumber"] == t) & df["lineage"]]
        lineage.update(dict(zip(lineage_data_frame["id"].values,lineage_data_frame["lineage"].values)))
        data={}
        data_frame_current_time_step = df.loc[df["ImageNumber"] == t]
        data["stepNum"] = t
        data["lineage"] = lineage
        data_frame_current_time_step.index = np.arange(1, len(data_frame_current_time_step) + 1) #start index = 1
        data["cellStates"] = data_frame_current_time_step[['id','cellType','divideFlag','cellAge','growthRate','LifeHistory','startVol','targetVol','pos','time','radius','length','orientation']]
        WrtiteToPickleFile(data,path,t)

def WrtiteToPickleFile(data,path,time_step):
    """
    Writes data to a .pickle file
    
    @param data         *       data to be stored
    @param path         str     path where data will be stored
    @param time_step    float   time between images
    """
    if not os.path.exists(path):
        os.mkdir(path)

    output_file = path + "step-" + str(time_step) + ".pickle"    

    with open(output_file, 'wb') as export:
        pickle.dump(data, export, protocol=-1)


input_file = '../../examples/SingleStrain/InputFile/InputFileForSingleStrainTest.csv'
output_directory = '../../examples/SingleStrain/InputFile'
ProcessData(input_file,output_directory)

    
