import pandas as pd
import numpy as np
from ExperimentalDataProcessing import bacteria_analysis


def lineage_based_analysis(df):
    """
    Conducts lineage-based analysis on the input DataFrame.

    @params df DataFrame DataFrame containing bacteria data.

    Returns:
    - results DataFrame Results of the analysis containing the number of divisions for each label.
    """

    # Get unique labels present in the DataFrame.
    uniq_label = list(set(df["label"].values))
    result_dict = {"label": [], "NumberOfDivision": []}

    # Iterate over each unique label.
    for label in uniq_label:
        # Filter the DataFrame for rows corresponding to the current label.
        df_current_label = df.loc[df["label"] == label]

        # Find rows where division occurred.
        division_df = df_current_label.loc[df_current_label["divideFlag"] == True]

        # Add the number of divisions and the label to the result dictionary.
        if division_df.shape[0] > 1:
            result_dict["NumberOfDivision"].append(division_df.shape[0])
        else:
            # If no division occurred, append 0.
            result_dict["NumberOfDivision"].append(0)
        result_dict["label"].append(label)

    # Convert the results dictionary to a DataFrame.
    results = pd.DataFrame.from_dict(result_dict, orient="index").transpose()

    return results


def find_num_cells_in_each_time_step(df):
    """
    Finds the number of cells present at each time step in the input DataFrame.

    @param df DataFrame DataFrame containing bacteria data.

    Returns:
    - results DataFrame Results of the analysis containing the number of cells for each time step.
    """

    # Get unique time steps present in the DataFrame.
    uniq_time_steps = list(set(df["TimeStep"].values))

    result_dict = {"TimeStep": [], "NumberOfCells": []}

    # Iterate over each unique time step.
    for timestep in uniq_time_steps:
        # Filter the DataFrame for rows corresponding to the current time step.
        df_current_timestep = df.loc[df["TimeStep"] == timestep]

        # Add the time step and the number of cells present to the result dictionary.
        result_dict["TimeStep"].append(timestep)
        result_dict["NumberOfCells"].append(df_current_timestep.shape[0])

    # Convert the results dictionary to a DataFrame.
    results = pd.DataFrame.from_dict(result_dict, orient="index").transpose()

    return results


def process_data(input_file, interval_time, output_directory):
    """
    Processes the data from the input_file and saves the results to various CSV files in the output_directory.

    @param input_file str Path to the input CSV file containing bacteria data (output of Cellprofiler).
    @param interval_time float Interval time between frames.
    @param output_directory str Directory where the processed results will be saved.

    """

    # Read the data from the CSV file into a DataFrame.
    data_frame = pd.read_csv(input_file)

    # Filter out rows where AreaShape_MajorAxisLength is zero and reset index.
    data_frame = data_frame.loc[data_frame["AreaShape_MajorAxisLength"] != 0].reset_index(drop=True)
    data_frame = data_frame.reset_index(drop=True)

    # Process the tracking data using the bacteria_analysis function.
    # Returns a modified DataFrame and a life-history based analysis DataFrame.
    df, life_history_based_analysis = bacteria_analysis(data_frame, interval_time)

    # Perform lineage-based analysis and count the number of cells in each time step.
    lineage_based_analysis_results = lineage_based_analysis(df)
    num_cells_in_each_time_step_results = find_num_cells_in_each_time_step(df)

    # Define paths for saving the results as CSV files.
    path_life_history = output_directory + "CP_LifeHistory_based_Analysis"
    path_lineage = output_directory + "CP_lineage_based_analysis"
    path_bacteria_based_features = output_directory + "CP_bacteria_feature_analysis"
    path_num_cells_in_each_time_step = output_directory + "CP_Num_cells_in_each_timeStep"

    # Save the results to CSV files in the specified output_directory.
    life_history_based_analysis.to_csv(path_life_history + ".csv", index=False)
    lineage_based_analysis_results.to_csv(path_lineage + ".csv", index=False)
    df.to_csv(path_bacteria_based_features + ".csv", index=False)
    num_cells_in_each_time_step_results.to_csv(path_num_cells_in_each_time_step + ".csv", index=False)


if __name__ == "__main__":

    # A dictionary containing paths to output CSV files from CellProfiler and their associated interval times.
    cp_output_path_interval_time = {
        "/CP/IdentifyPrimaryObjects.csv": 5,
    }

    # List of directories where the processed results will be saved.
    output_directory = [
        '/CP/results/',
    ]

    # For each output CSV path from CellProfiler in the dictionary:
    for i, cp_output_path in enumerate(cp_output_path_interval_time.keys()):

        # Retrieve the associated interval time for the current path.
        interval_time_value = cp_output_path_interval_time[cp_output_path]

        # Print the current path and its interval time to the console.
        print("cp output:" + cp_output_path)
        print("interval time: " + str(interval_time_value))

        # Process the data from the current path using the previously defined process_data function.
        process_data(cp_output_path, interval_time_value, output_directory[i])
