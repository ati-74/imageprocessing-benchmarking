import math
import numpy as np
import pandas as pd


def average_growth_rate(division_length, birth_length, t):
    """
    Compute the average growth rate based on the division length, birth length, and time.

    @param division_length float The length of the bacterium at the last time step before division.
    @param birth_length float The length of the bacterium at birth.
    @param t float Time period for which the growth is observed.

    Returns:
    elongation_rate float Average growth rate, rounded to three decimal places. Returns NaN if the length of bacterium
    is zero
    """
    try:
        elongation_rate = round((division_length - birth_length) / t, 3)
    except:
        elongation_rate = np.nan

    return elongation_rate


def calc_growth_rate(birth_length, division_length, life_history_length, interval_time):
    """
    Calculate the growth rate of a bacterium.

    @param birth_length float The length of the bacterium at birth.
    @param division_length float The length of the bacterium at division.
    @param life_history_length int The duration of the bacterium's life history in number of timesteps.
    @param interval_time float The time interval between each timestep.

    Returns:
    elongation_rate float Growth rate of the bacterium. Returns "NaN" if the bacterium only exists for one timestep.
    """

    # If the bacterium exists for more than one time step, calculate the growth rate.
    if life_history_length > 1:
        t = life_history_length * interval_time
        elongation_rate = average_growth_rate(division_length, birth_length, t)
    else:
        # Bacterium is present for only one timestep.
        elongation_rate = "NaN"

    return elongation_rate


def calc_average_velocity(pos1, pos2, life_history_length, interval_time):
    """
    Calculate the average velocity of a bacterium.

    @param pos1 list Initial position (at the birth time) [x,y] of the bacterium.
    @param pos2 list Final position (last time step of bacterium life) [x,y] of the bacterium.
    @param life_history_length int The duration of the bacterium's life history in number of timesteps.
    @param interval_time float The time interval between each timestep.

    Returns:
    average_velocity float Average velocity of the bacterium, rounded to three decimal places.
    """

    x1 = math.sqrt(pos1[0] ** 2 + pos1[1] ** 2)
    x2 = math.sqrt(pos2[0] ** 2 + pos2[1] ** 2)

    # Compute average velocity
    average_velocity = round((x2 - x1) / (life_history_length * interval_time), 3)

    return average_velocity


def tracking_bacteria_id(cell, last_assigned_delta_id):
    """
    Tracks and maps the IDs of a bacterium's lineage, including its mother and daughters.

    @param cell dict containing data for a single bacterium cell during it's lif history (and also information
    about its family).
    @param last_assigned_delta_id int The last assigned identifier for tracking purposes.

    tracking_this_part_of_family_tree list IDs representing a bacterium's lineage.
    last_assigned_delta_id int The updated last assigned identifier.
    parent_id dict Mapping of daughter bacterium ID to mother bacterium ID.
    daughter1_id dict Mapping of mother bacterium ID to the first daughter bacterium ID.
    daughter2_id dict Mapping of mother bacterium ID to the second daughter bacterium ID.
    bacteria_start_life_points list Sorted list of points in time when a new bacterium begins its life.

    """

    # Extract unique daughter IDs and remove any 'None' entries
    this_bacterium_daughters_id = list(set(cell['daughters']))
    this_bacterium_daughters_id.remove(None)

    # Get the birth points for each daughter
    daughters_birth_point = []
    for indx in this_bacterium_daughters_id:
        daughters_birth_point.append(cell['daughters'].index(indx))

    # Sort daughter IDs by their birth points
    sorted_daughters_id_point = sorted(zip(this_bacterium_daughters_id, daughters_birth_point))
    start_point = 0
    # bacteria life points
    bacteria_start_life_points = [0]

    # Initialize starting IDs and mother ID
    start_id = cell['id']
    mother_id = cell['mother']
    if not mother_id:
        mother_id = 0
    # tracking information
    # daughter: mother
    parent_id = {}
    # mother: daughter
    daughter1_id = {}
    daughter2_id = {}
    tracking_this_part_of_family_tree = []

    # Track and map IDs based on sorted daughter birth points
    for tuple_data in sorted_daughters_id_point:
        end_point = tuple_data[1]
        bacteria_start_life_points.append(end_point)
        tracking_this_part_of_family_tree.extend([start_id] * (end_point - start_point))
        start_point = end_point
        last_assigned_delta_id += 1
        # parent detail
        parent_id[start_id] = mother_id
        daughter1_id[start_id] = last_assigned_delta_id
        daughter2_id[start_id] = tuple_data[0]
        mother_id = start_id
        start_id = last_assigned_delta_id

    # Handle the case for the last end point
    end_point = len(cell['daughters'])
    if end_point - start_point > 0:
        bacteria_start_life_points.append(end_point)
        parent_id[start_id] = mother_id
        daughter1_id[start_id] = None
        daughter2_id[start_id] = None
        tracking_this_part_of_family_tree.extend([start_id] * (end_point - start_point))
    else:
        last_assigned_delta_id -= 1

    return tracking_this_part_of_family_tree, last_assigned_delta_id, parent_id, daughter1_id, daughter2_id, sorted(
        bacteria_start_life_points)


def bacteria_analysis(lin, interval_time):
    """
    Analyzes bacteria data based on their lineage information and other cellular features.

    @param lin object An object containing bacteria lineage data with 'cells' attribute.
    @param interval_time float The time interval between frames.

    Returns:
    cell_info_df DataFrame containing detailed cellular information for each time step.
    life_history_df DataFrame summarizing the life history of each bacterium.

    """

    # Create empty dictionary for individual bacteria features
    single_features = {"TimeStep": [], "CellId": [], "Orientation": [], "label": [], "Center_X": [], "Center_Y": [],
                       "Major_axis": [], "Minor_axis": [], "parent": [], 'daughter1': [], "daughter2": []}
    # Create empty dictionary for results
    result_dict = {"CellId": [], "label": [], "birth_length": [], "AverageLength": [], "AverageVelocity": [],
                   "LifeHistory": [], "GrowthRate": [], "AverageOrientation": []}
    last_label_value = 1
    # Maps id to label for cells
    cell_label = {}

    # Find the maximum id value
    last_assigned_delta_id = max([cell['id'] for cell in lin.cells])

    for cell in lin.cells:
        # Skip cells with all zero length
        if list(set(cell['length'])) != [0.0]:
            # modification of orientations
            modified_orientation = []
            # Assign labels based on mother id or create a new label
            if cell['mother'] in cell_label.keys():
                this_bacterium_label = cell_label[cell['mother']]
            else:
                this_bacterium_label = last_label_value
                last_label_value += 1

            cell_label[cell['id']] = this_bacterium_label

            # Track lineage and update cell ids
            tracking_this_part_of_family_tree, last_assigned_delta_id, parent_id, daughter1_id, daughter2_id, \
                bacteria_start_life_points = tracking_bacteria_id(cell, last_assigned_delta_id)

            # Populate single features dictionary with cell data
            for i, bacteria_id in enumerate(tracking_this_part_of_family_tree):
                    single_features["CellId"].append(bacteria_id)
                    single_features['TimeStep'].append(cell['frames'][i] + 1)
                    single_features['Center_X'].append(cell['x_center'][i])
                    single_features['Center_Y'].append(cell['y_center'][i])
                    single_features['Major_axis'].append(cell['length'][i])
                    single_features['Minor_axis'].append(cell['width'][i])
                    single_features["label"].append(this_bacterium_label)
                    if cell['rectangle_width'][i] > cell['rectangle_height'][i]:
                        angle = (cell['orientation'][i]) * np.pi / 180
                    else:
                        angle = (cell['orientation'][i] + 90) * np.pi / 180

                    modified_orientation.append(angle)
                    single_features['Orientation'].append(angle)

                    # tracking features
                    single_features["parent"].append(parent_id[bacteria_id])
                    single_features['daughter1'].append(daughter1_id[bacteria_id])
                    single_features["daughter2"].append(daughter2_id[bacteria_id])
                    # modify mother id
                    if daughter1_id[bacteria_id] in [cell['id'] for cell in lin.cells]:
                        cell_index = [cell_index for cell_index, cell in enumerate(lin.cells) if cell['id']
                                      == daughter1_id[bacteria_id]][0]
                        lin.cells[cell_index]['mother'] = bacteria_id

                    if daughter2_id[bacteria_id] in [cell['id'] for cell in lin.cells]:
                        cell_index = [cell_index for cell_index, cell in enumerate(lin.cells) if cell['id']
                                      == daughter2_id[bacteria_id]][0]

                        lin.cells[cell_index]['mother'] = bacteria_id

            # Compute and store features based on bacteria's life history
            unique_bacteria_id = sorted(list(set(tracking_this_part_of_family_tree)))
            for index, bacteria_id in enumerate(unique_bacteria_id):
                cell_label[bacteria_id] = this_bacterium_label
                result_dict["CellId"].append(bacteria_id)
                result_dict["label"].append(this_bacterium_label)
                this_bacterium_life_history_length = bacteria_start_life_points[index + 1] - bacteria_start_life_points[
                    index]
                result_dict["LifeHistory"].append(this_bacterium_life_history_length)
                this_bacterium_birth_length = cell["length"][bacteria_start_life_points[index]]
                this_bacterium_last_length = cell["length"][bacteria_start_life_points[index + 1] - 1]
                result_dict["birth_length"].append(this_bacterium_birth_length)
                result_dict["GrowthRate"].append(calc_growth_rate(this_bacterium_birth_length, this_bacterium_last_length,
                                                                  this_bacterium_life_history_length, interval_time))
                first_position = [cell['x_center'][bacteria_start_life_points[index]],
                                  cell['y_center'][bacteria_start_life_points[index]]]
                last_position = [cell['x_center'][bacteria_start_life_points[index + 1] - 1],
                                 cell['y_center'][bacteria_start_life_points[index + 1] - 1]]

                result_dict["AverageVelocity"].append(calc_average_velocity(first_position, last_position,
                                                                            this_bacterium_life_history_length,
                                                                            interval_time))

                result_dict["AverageLength"].append(np.mean(cell['length'][index: (index + 1)]))
                result_dict["AverageOrientation"].append(np.mean(modified_orientation[index: (index + 1)]))

    # convert to dataframes
    cell_info_df = pd.DataFrame.from_dict(single_features, orient="index").transpose().sort_values(["TimeStep", "CellId"])
    life_history_df = pd.DataFrame.from_dict(result_dict, orient="index").transpose().sort_values(["CellId", "label"])

    # Calculate instantaneous growth rate and velocity for each cell
    cell_info_df["InstantaneousGrowthRate"] = ""
    cell_info_df["InstantaneousVelocity"] = ""
    last_time_step = cell_info_df['TimeStep'].unique()[-1]
    for index, row in cell_info_df.iterrows():
        if row['TimeStep'] < last_time_step:
            next_time_step_bacteria = cell_info_df.loc[(cell_info_df['TimeStep'] == row['TimeStep'] + 1)
                                                       & (cell_info_df['CellId'] == row['CellId'])].reset_index(drop=True)
            if next_time_step_bacteria.shape[0] == 1:
                next_time_step_bacteria = next_time_step_bacteria.iloc[0]
                instantaneous_growth_rate = average_growth_rate(next_time_step_bacteria['Major_axis'],
                                                                row['Major_axis'], interval_time)
                # average velocity
                pos1 = row[["Center_X", "Center_Y"]].values.tolist()
                pos2 = next_time_step_bacteria[["Center_X", "Center_Y"]].values.tolist()
                instantaneous_velocity = calc_average_velocity(pos1, pos2, 1, interval_time)
            else:
                instantaneous_growth_rate = np.nan
                instantaneous_velocity = np.nan
        else:
            instantaneous_growth_rate = np.nan
            instantaneous_velocity = np.nan

        cell_info_df.at[index, "InstantaneousGrowthRate"] = instantaneous_growth_rate
        cell_info_df.at[index, "InstantaneousVelocity"] = instantaneous_velocity

    return cell_info_df, life_history_df
