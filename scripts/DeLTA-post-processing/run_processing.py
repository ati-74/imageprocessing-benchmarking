import delta
import pandas as pd
from ExperimentalDataProcessing import bacteria_analysis


def lineage_based_analysis(df):
    """
    Analyze the lineage data from a dataframe to determine the number of divisions
    that occurred for each unique label (each family).

    @param df DataFrame containing lineage data with "label" and "parent" columns.

    Returns:
    results DataFrame containing labels and their corresponding number of divisions.
    """

    uniq_label = list(set(df["label"].values))
    result_dict = {"label": [], "NumberOfDivision": []}

    for label in uniq_label:
        df_current_label = df.loc[df["label"] == label]
        division_df = df_current_label.loc[df_current_label["parent"].notnull()]

        # Count divisions and save results
        if division_df.shape[0] > 1:
            result_dict["NumberOfDivision"].append(len(set(division_df["parent"].values.tolist())))
        else:
            # Zero means no division occurred
            result_dict["NumberOfDivision"].append(0)
        result_dict["label"].append(label)

    # Convert dictionary to DataFrame
    results = pd.DataFrame.from_dict(result_dict, orient="index").transpose()

    return results


def find_num_cells_in_each_time_step(lin):
    """
    Count the number of cells present at each timestep in the lineage.

    @param lin object The lineage object

    Returns:
    results DataFrame with columns "TimeStep" and "NumberOfCells" indicating the
                        timestep and the corresponding number of cells, respectively.
    """

    result_dict = {"TimeStep": [], "NumberOfCells": []}

    for timestep in range(len(lin.cellnumbers)):
        # Record timestep and corresponding number of cells
        result_dict["TimeStep"].append(timestep + 1)
        result_dict["NumberOfCells"].append(len(lin.cellnumbers[timestep]))

    # Convert dictionary to DataFrame
    results = pd.DataFrame.from_dict(result_dict, orient="index").transpose()

    return results


if __name__ == '__main__':
    """
    Main execution block to process data from DeLTA output and analyze lineage, life history, 
    and features of bacteria.

    The script reads from specified input directories, performs various analyses on the data, 
    and writes the results to csv files in the specified output directories.
    """

    # Define input directories and their associated time intervals
    delta_output_path_interval_time = {
        "DeLTA/input/": 5,
    }
    # List of output directories corresponding to the input directories
    output_directory_list = [
        'DeLTA/results/',
    ]

    # Loop over each input directory
    for i, input_directory in enumerate(delta_output_path_interval_time.keys()):
        # Fetch the output directory and time interval value for the current input directory
        output_directory = output_directory_list[i]
        interval_time_value = delta_output_path_interval_time[input_directory]

        # Read and process data using the DeLTA utilities and pipeline
        reader = delta.utilities.xpreader(input_directory)
        processor = delta.pipeline.Pipeline(reader, reload=True)
        lin = processor.positions[0].rois[0].lineage

        # Analyze bacteria features
        cell_info_df, life_history_df = bacteria_analysis(lin, interval_time_value)

        # Analyze lineage
        lineage_based_analysis_results = lineage_based_analysis(cell_info_df)

        # Count number of bacteria in each time step
        num_cells_in_each_time_step_results = find_num_cells_in_each_time_step(lin)

        # Define output paths for csv results
        path_life_history = output_directory + "DeLTA_LifeHistory_based_Analysis"
        path_lineage = output_directory + "DeLTA_lineage_based_analysis"
        path_bacteria_based_features = output_directory + "DeLTA_bacteria_feature_analysis"
        path_num_cells_in_each_time_step = output_directory + "DeLTA_Num_cells_in_each_timeStep"

        # Write results to csv files
        life_history_df.to_csv(path_life_history + ".csv", index=False)
        lineage_based_analysis_results.to_csv(path_lineage + ".csv", index=False)
        cell_info_df.to_csv(path_bacteria_based_features + ".csv", index=False)
        num_cells_in_each_time_step_results.to_csv(path_num_cells_in_each_time_step + ".csv", index=False)
