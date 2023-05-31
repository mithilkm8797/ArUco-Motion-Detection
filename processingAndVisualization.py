from datetime import datetime
import csv
import openpyxl
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "C:/Users/kmmit/Desktop/Aruco Project/Data/Data.csv"
tool_marker_map_dict = {"2": "Hammer", "1": "Chisel", "0": "Screwdriver"}


def split_and_group_data(entire_data):
    """
    :param entire_data: A data frame containing the data read from the csv file generated during the detection process.
    :return: data_list_time_grouped: A list of data frames grouped by time, one for each tool.

    The function splits the entire data into separate data frames one for each tool. The data frames are then
    individually grouped by the time column and mean of x-coordinate and y-coordinate columns is taken and is shortened
    to two decimal places. These data frames are stored in a list and the list is returned.
    """

    # splitting data into data frames for each tool
    global tool_marker_map_dict
    data_list = []
    for key, value in tool_marker_map_dict.items():
        data_list.append(entire_data[entire_data['ID'] == value])

    # Grouping the columns by time
    data_list_time_grouped = []
    for data in data_list:
        data_list_time_grouped.append(data.groupby(['TimeStamp', 'ID'], as_index=False)[['X-co', 'Y-co']].mean().round(2))

    return data_list_time_grouped


def calculate_tool_usage(data_list_time_grouped):
    """
    :param data_list_time_grouped: A list containing data frames grouped by time, for each tool.
    :return: data_with_tool_used_calc: A data frame with calculated 'used' column.

    In this function we add an entry of 1, if there was a co-ordinate change between current and next entry in the data
    frame (suggesting movement) or 0 if there was no change in the co-ordinates. The co-ordinate is calculated as
    changed if the difference between either the x-coordinates or the y-coordinates or both is greater than 1. The
    entries of 0s and 1s are made in 'used' column of the data frame. The data frames of different tools are combined
    and a new single data frame is returned.
    """

    for data in data_list_time_grouped:
        for index in data.index:
            cur_x = float(data['X-co'].iloc[index])
            cur_y = float(data['Y-co'].iloc[index])
            try:
                next_x = float(data['X-co'].iloc[index + 1])
            except IndexError:
                next_x = float(data['X-co'].iloc[index])
            try:
                next_y = float(data['Y-co'].iloc[index + 1])
            except IndexError:
                next_y = float(data['Y-co'].iloc[index])

            if abs(next_x - cur_x) > 1 or abs(next_y - cur_y) > 1:
                data.loc[index, 'used'] = int(1)
            else:
                data.loc[index, 'used'] = int(0)

    data_with_tool_used_calc = pd.DataFrame()
    for data in data_list_time_grouped:
        data_with_tool_used_calc = data_with_tool_used_calc._append(data, ignore_index=True)

    return data_with_tool_used_calc


def suggest_order(data):
    """
    :param data: The data frame returned from the function: calculate_tool_usage(). Data with 'used' column entries.
    :return: tool_usage_duration_filtered: Data frame with tool usage duration in order.

    The function calculates the duration for which each tool was used. The entries of 1 in the 'used' column are
    counted to calculate the duration. The count indicates the number of seconds a particular tool was used. The goal is
    to filter the data and remove the occasional 1's and 0's (errors in the readings due to a lot of factors such as
    fast tool movements resulting in the marker going undetected leading to a 0 between 1's, the camera itself failing
    to record and detect some frames, etc.) that occur in between a series of continuous 0'S and 1's respectively.

    A tool is considered to be at rest when a series of more than 3 continuous zeros are encountered. A series of 4
    continuous zeros (tool has not moved for 4 seconds) is assumed as the tool being at rest/unused. Similarly, a tool
    is considered as being in use if there are 2 or more occurrences of continuous 1's.This is because, from basic user
    testing we found that it takes on an average a minimum of 2 seconds to pick up the tool and place it back down. We
    remove such cases as picking up and immediately putting the tool down to rest is not considered as using the tool
    (might be accidental).

    The continuity of 0's and 1's are monitored using 'next_of_cur_used' and 'next_of_next_of_cur_used'. The function
    returns a data frame with duration of usage of each tool along with the sequence of the tool.
    """

    counter = 0
    tool_usage_duration = pd.DataFrame(columns=['StartDate', 'EndDate', 'ID', 'Duration'])

    for index in data.index:

        cur_used = int(data['used'].iloc[index])  # status of the current tool being used. checking if is it a 1 or 0?
        cur_tool = data['ID'].iloc[index]  # current tool
        if index == 0:
            prev_tool = cur_tool  # previous tool is equal to current tool
        else:
            prev_tool = data['ID'].iloc[index - 1]

        # checking and assigning the 'next' and 'next to next' entries in 'used' column
        try:
            next_of_cur_used = float(data['used'].iloc[index + 1])
        except IndexError:
            next_of_cur_used = cur_used
        try:
            next_of_next_of_cur_used = float(data['used'].iloc[index + 2])
        except IndexError:
            next_of_next_of_cur_used = next_of_cur_used

        # checking all the conditions for 1's
        if cur_used == int(1) and cur_tool == prev_tool:
            counter += 1
        elif cur_used == int(1) and counter > 1 and cur_tool != prev_tool:
            start_time = data['TimeStamp'].iloc[index - counter]
            end_time = data['TimeStamp'].iloc[index - 1]
            duration = end_time.timestamp() - start_time.timestamp()

            counter = 0

            # timestamp() function converts time to seconds
            row = {'StartDate': start_time, 'EndDate': end_time, 'ID': data['ID'].iloc[index - 1],
                   'Duration': duration}
            tool_usage_duration = tool_usage_duration._append(row, ignore_index=True)

        elif cur_used == int(1) and counter <= 1 and cur_tool != prev_tool:
            counter += 1

        # checking all the conditions for 0's
        if cur_used == int(0) and counter > 1 and cur_tool == prev_tool and \
                next_of_cur_used == int(0) and next_of_next_of_cur_used == int(0):

            start_time = data['TimeStamp'].iloc[index - counter]
            end_time = data['TimeStamp'].iloc[index - 1]
            duration = end_time.timestamp() - start_time.timestamp()

            counter = 0

            row = {'StartDate': start_time, 'EndDate': end_time, 'ID': data['ID'].iloc[index - 1],
                   'Duration': duration}
            tool_usage_duration = tool_usage_duration._append(row, ignore_index=True)

        elif cur_used == int(0) and counter > 1 and cur_tool == prev_tool and \
                (
                (next_of_cur_used == int(0) and next_of_next_of_cur_used != int(0)) or
                (next_of_cur_used == int(0) and next_of_next_of_cur_used != int(0)) or
                (next_of_cur_used != int(0) and next_of_next_of_cur_used != int(0))
                ):
            counter += 1

        elif cur_used == int(0) and counter > 1 and cur_tool != prev_tool:

            start_time = data['TimeStamp'].iloc[index - counter]
            end_time = data['TimeStamp'].iloc[index - 1]
            duration = end_time.timestamp() - start_time.timestamp()

            counter = 0

            row = {'StartDate': start_time, 'EndDate': end_time, 'ID': data['ID'].iloc[index - 1],
                   'Duration': duration}

            tool_usage_duration = tool_usage_duration._append(row, ignore_index=True)

    # Discarding tool usage less than 2 seconds
    tool_usage_duration_filtered = tool_usage_duration.query("Duration > 2.0")
    ordered_data = tool_usage_duration_filtered.sort_values(by=['StartDate'])
    ordered_data.reset_index(drop=True, inplace=True)
    # TODO: Write the code for 2 or more tools being used at the same time. suggest: tool 1 and tool 2

    order_file_path = file_path[:-4] + "_tool_order.xlsx"  # do not put quotes at the beginning and the end
    order_file_path = order_file_path.replace("/", "\\")  # done to fix the path for .to_excel() to work
    ordered_data.to_excel(order_file_path)

    return ordered_data


def create_clean_data(data):
    """
    :param data: A data frame containing data from the function: suggest_order().
    :return: clean_time_series_data: A data frame with clean continuous time series data.

    The aim of this function is to create a clean continuous uninterrupted time series data. Due to fast motion of the
    tool being used and sometimes the camera failing to record some frames there are missing values in the timeline.
    Example: Hammer was correctly detected between 10:30:20 and 10:30:30, but due to users fast motions it wasn't
    detected between 10:30:30 and 10:30:35. This will result in 5 seconds of missing data. This is not a problem in
    the overall tool usage duration calculation as, when the tool does get detected again, we simply add these missing
    5 seconds to the duration (the suggest_order() function takes care of this). However, this data with missing values
    is discrete and hence not good when we want to visualize a time series graph/plot of the tool usage which is
    continuous in nature. This function fixes this issue and makes the data continuous by intelligently filling 1's or
    0's accordingly.

    Steps:
    1. An empty data frame (clean_data) with start date of the first entry in the data (ordered data) and the end
    date of the last entry is created. All entries in 'ID' column are set to null and in 'used' column are set to 0.
    2. The data is split into data frames for each tool and create a list of data frames called data_list.
    3. Create a list of clean_data data frames for each tool called clean_data_list.
    4. For each data frame df in data_list and clean_df in clean_df_list a mapping is created.
    5. The start date of df is searched for in clean_df. 1's are filled from that index for a count of the duration.
     This is done for each row in the df.
    6. This is done for each df and clean_df and a concatenated data frame of all data frames in clean_df_list is
    returned.
    """

    start_date = data.loc[0, 'StartDate']
    end_date = data.loc[len(data) - 1, 'EndDate']

    df = pd.DataFrame(columns=['TimeStamp', 'ID', 'used'])

    index = start_date

    # Create an empty data frame with continuous time stamps in steps of one second.

    clean_data = pd.DataFrame(columns=['TimeStamp', 'ID', 'used'])
    while index != (end_date + dt.timedelta(seconds=1)):
        row = {'TimeStamp': index, 'ID': '', 'used': 0}
        clean_data = clean_data._append(row, ignore_index=True)
        index = index + dt.timedelta(seconds=1)

    # Split data into different data frames for each tool
    global tool_marker_map_dict
    data_list = []
    for key, value in tool_marker_map_dict.items():
        data_list.append(data[data['ID'] == value].reset_index())

    # Create a list of clean_data for each tool
    clean_data_list = []
    for key, value in tool_marker_map_dict.items():
        clean_data['ID'] = value
        clean_data_list.append(clean_data)

    for (df, clean_df) in zip(data_list, clean_data_list):
        for index_in_df in df.index:
            duration = int(df['Duration'].iloc[index_in_df])
            start_date = df['StartDate'].iloc[index_in_df]
            start_index_to_fill = clean_data[clean_data['TimeStamp'] == start_date].index[0]
            for index_in_clean_df in clean_df.index:
                clean_data.loc[start_index_to_fill + index_in_clean_df, 'used'] = int(1)
                if index_in_clean_df > duration - 1:
                    break
        clean_data_list.append(clean_data)

    clean_time_series_data = pd.DataFrame()
    for clean_data in clean_data_list:
        clean_time_series_data = clean_time_series_data._append(clean_data, ignore_index=True)

    clean_time_series_data_file_path = file_path[:-4] + "_filtered.xlsx"
    clean_time_series_data_file_path = clean_time_series_data_file_path.replace("/", "\\") # done to fix the path for .to_excel() to work
    clean_time_series_data.to_excel(clean_time_series_data_file_path)

    return clean_time_series_data


def plot_data(data):
    """
    :param data: A data frame containing data returned by create_clean_excel().
    :return: plt: A plot to visualize data.

    This function generates different plots to visualize the data
    """

    if data.empty:
        print("No data was recorded to be visualized.")

    else:
        sns.set_theme(style="darkgrid")
        sns.kdeplot(data=data, x="TimeStamp", hue="ID", fill=True, common_norm=False, alpha=.5, linewidth=0)
        sns.kdeplot(data=data, x="TimeStamp", hue="ID", bw_adjust=.2)
        plt.show()
        plt.close()

        # Load an example dataset with long-form data

        # Plot the responses for different events and regions
        sns.lineplot(x="TimeStamp", y="used",
                     hue="ID",
                     data=data)
        plt.show()


def main(path, map_dict):
    print("Starting Data Processing...\n")
    global file_path, tool_marker_map_dict
    file_path = path
    tool_marker_map_dict = map_dict

    entire_data = pd.read_csv(file_path, sep=',')

    # add the 'used' column, to see if the tool was used or not
    entire_data['used'] = 'na'

    # Splitting the entire data frame into sub data frames based on tool and then applying grouping on time as there
    # are a lot of readings each second
    print("Starting Split and Group...\n")
    data_list_time_grouped = split_and_group_data(entire_data)

    # calculating based on co-ordinate changes if the tool is being used or not
    print("Starting tool usage estimation...\n")
    data_with_tool_used_calc = calculate_tool_usage(data_list_time_grouped)

    # Converting time stamp data to date time format for easier time calculations
    data_with_tool_used_calc['TimeStamp'] = pd.to_datetime(data_with_tool_used_calc['TimeStamp'])

    # Calculations to process and data and suggest thr order of the tool usage
    print("Starting tool order calculations...\n")
    suggested_order_data = suggest_order(data_with_tool_used_calc)
    clean_ordered_data = create_clean_data(suggested_order_data)

    print("Order of the Tool usage is: \n")
    print(suggested_order_data)

    print("\n Visualizing the data...\n")
    plot_data(data_with_tool_used_calc)

    print("Plotting smoothened/cleaned data...\n")
    #plot_data(clean_ordered_data)

    generated_file_path = file_path[:-4] + "_with_tool_usage_stats.xlsx" # do not put quotes at the beginning and the end
    generated_file_path = generated_file_path.replace("/", "\\")  # done to fix the path for .to_excel() to work
    data_with_tool_used_calc.to_excel(generated_file_path)


if __name__ == "__main__":
    main()
