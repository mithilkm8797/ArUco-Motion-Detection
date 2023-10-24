from datetime import datetime

import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import mpld3
import itertools

from bokeh.models import DatetimeTickFormatter
from bokeh.palettes import Dark2_5 as palette
from bokeh.plotting import figure, show, output_file

import config as config
import ctypes
import easygui

def split_and_group_data(entire_data):
    """
    :param entire_data: A data frame containing the data read from the csv file generated during the detection process.
    :return: data_list_time_grouped: A list of data frames grouped by time, one for each tool.

    The function splits the entire data into separate data frames one for each tool. The data frames are then
    individually grouped by the time column and mean of x-coordinate and y-coordinate columns is taken and is shortened
    to two decimal places. These data frames are stored in a list and the list is returned.
    """
    if entire_data.empty:
        print("The data sent to split and group was empty.")
        return []

    # splitting data into data frames for each tool
    data_list = []

    for key, value in config.tool_marker_map_dict.items():
        data_list.append(entire_data[entire_data['ID'] == value])

    print("print1\n", data_list)
    # remove empty data frames for cases when a certain tool is not used
    # for each df in data_list if its is not empty then add it to data_list (syntax is called list comprehension)
    data_list = [df for df in data_list if not df.empty]

    # Grouping the columns by time
    data_list_time_grouped = []
    for data in data_list:
        grouped_data = data.groupby(['TimeStamp', 'ID'], as_index=False)[['X-co', 'Y-co']].mean().round(2)
        data_list_time_grouped.append(grouped_data)

    combined_data_for_excel = pd.DataFrame()
    empty_row = {'TimeStamp': "", 'ID': "", 'X-co': "", 'Y-co': ""}

    for data in data_list_time_grouped:
        combined_data_for_excel = combined_data_for_excel._append(data, ignore_index=True)
        combined_data_for_excel = combined_data_for_excel._append(empty_row, ignore_index=True)

    generated_file_path = config.file_path[
                          :-4] + "_split_group.xlsx"  # do not put quotes at the beginning and the end
    generated_file_path = generated_file_path.replace("/", "\\")  # done to fix the path for .to_excel() to work
    combined_data_for_excel.to_excel(generated_file_path, index=False)  # index=False prevent index input in excel

    return data_list_time_grouped


def calculate_tool_usage(data_list_time_grouped, flag):
    """
    :param flag: flag is sent when an override of empty appended data is desired
    :param data_list_time_grouped: A list containing data frames grouped by time, for each tool.
    :return: data_with_tool_used_calc: A data frame with calculated 'used' column.

    In this function we add an entry of 1, if there was a co-ordinate change between current and next entry in the data
    frame (suggesting movement) or 0 if there was no change in the co-ordinates. The co-ordinate is calculated as
    changed if the difference between either the x-coordinates or the y-coordinates or both is greater than 1. The
    entries of 0s and 1s are made in 'used' column of the data frame. The data frames of different tools are combined
    and a new single data frame is returned.

    The flag argument comes into play when the processingAndVisualization.py needs to be run with an empty data append.
    """
    if len(data_list_time_grouped) == 0:
        print("Data in the calculate usage step is empty")
        return

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
        # appending 4 zeros (meaning tool is at rest) after each tool to prevent errors in duration calculations to
        # take of time gap between two appends of data to the same file
        last_index = len(data) - 1
        last_timestamp = data['TimeStamp'].iloc[last_index]
        last_timestamp = datetime.strptime(last_timestamp, '%Y-%m-%d %H:%M:%S')
        counter = 0
        while counter < 4:
            timestamp = last_timestamp + dt.timedelta(seconds=(counter + 1))
            row_to_add_unused_entry = {'TimeStamp': timestamp, 'ID': data['ID'].iloc[last_index], 'X-co': 0,
                                       'Y-co': 0, 'used': int(0)}
            data_with_tool_used_calc = data_with_tool_used_calc._append(row_to_add_unused_entry, ignore_index=True)
            counter += 1

    generated_file_path_xlsx = config.file_path[
                               :-4] + "_with_tool_usage_stats.xlsx"  # do not put quotes at the beginning and the end
    generated_file_path_xlsx = generated_file_path_xlsx.replace("/",
                                                                "\\")  # done to fix the path for .to_excel() to work

    generated_file_path_csv = config.file_path[
                              :-4] + "_with_tool_usage_stats.csv"  # do not put quotes at the beginning and the end
    if flag == 0:
        if os.path.exists(generated_file_path_csv):
            prev_data_with_appened_zeros = pd.read_csv(generated_file_path_csv, sep=',')
            cur_data_with_appened_zeros = prev_data_with_appened_zeros._append(data_with_tool_used_calc,
                                                                               ignore_index=True)
            cur_data_with_appened_zeros = cur_data_with_appened_zeros.reset_index(drop=True)
            data_with_tool_used_calc = cur_data_with_appened_zeros

    data_with_tool_used_calc = data_with_tool_used_calc.reset_index(drop=True)
    data_with_tool_used_calc.to_excel(generated_file_path_xlsx, index=False)
    data_with_tool_used_calc.to_csv(generated_file_path_csv, index=False)  # index=False prevent index input in excel

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
    if data is None:
        print("Data in the suggest order step is empty")
        return pd.DataFrame()  # returning an empty data frame

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
    if tool_usage_duration_filtered.empty:
        print("The tools were not used for long enough to generate an order")
    ordered_data = tool_usage_duration_filtered.sort_values(by=['StartDate'])
    ordered_data = ordered_data.reset_index(drop=True)  # inplace=True

    order_file_path = config.file_path[:-4] + "_tool_order.xlsx"  # do not put quotes at the beginning and the end
    order_file_path = order_file_path.replace("/", "\\")  # done to fix the path for .to_excel() to work
    ordered_data.to_excel(order_file_path)

    print(ordered_data)
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
    if data.empty:
        print("Data in the create clean data step is empty")
        return

    df_start_date = data['StartDate']
    df_end_date = data['EndDate']

    min_of_start_date = min(df_start_date)
    min_of_end_date = min(df_end_date)
    max_of_start_date = max(df_start_date)
    max_of_end_date = max(df_end_date)

    start_date = min(min_of_start_date, min_of_end_date)
    end_date = max(max_of_start_date, max_of_end_date)

    index = start_date

    # Create an empty data frame with continuous time stamps in steps of one second.
    clean_data = pd.DataFrame(columns=['TimeStamp', 'ID', 'used'])
    while index != (end_date + dt.timedelta(seconds=1)):
        row = {'TimeStamp': index, 'ID': '', 'used': int(0)}
        clean_data = clean_data._append(row, ignore_index=True)
        index = index + dt.timedelta(seconds=1)

    # Split data into different data frames for each tool
    data_list = []
    for key, value in config.tool_marker_map_dict.items():
        data_to_append = data[data['ID'] == value]
        data_to_append = data_to_append.reset_index(drop=True)
        data_list.append(data_to_append)

    entire_clean_time_series_data = pd.DataFrame()

    for key, value in config.tool_marker_map_dict.items():
        clean_data['ID'] = value
        entire_clean_time_series_data = entire_clean_time_series_data._append(clean_data, ignore_index=True)

    ectsd = entire_clean_time_series_data  # for convenience

    for df in data_list:
        for index_in_df in df.index:
            tool = str(df['ID'].iloc[index_in_df])
            duration = int(df['Duration'].iloc[index_in_df])
            start_date = df['StartDate'].iloc[index_in_df]
            try:
                start_index_to_fill = ectsd[(ectsd['TimeStamp'] == start_date) & (ectsd['ID'] == tool)].index[0]
            except IndexError:
                break
            for index_clean_data in ectsd.index:
                ectsd.loc[start_index_to_fill + index_clean_data, 'used'] = int(1)
                if index_clean_data > duration - 1:
                    break

    clean_time_series_data_file_path = config.file_path[:-4] + "_filtered_clean.xlsx"
    # done to fix the path for .to_excel() to work
    clean_time_series_data_file_path = clean_time_series_data_file_path.replace("/", "\\")
    ectsd.to_excel(clean_time_series_data_file_path, index=False)

    return ectsd


def plot_line_all_separate(data, flag):
    """
    :param data: A data frame to be plotted
    :param flag: An integer value to differentiate between original and smoothened data
    :return:

    This function plots a graph containing subplots of tool usage of each tool. Creates an image and an HTML page for
    interaction with the graph.
    """
    # fig = plt.figure(figsize=(18, 8), dpi=60)
    fig, ax = plt.subplots(figsize=(15, 7))
    plt.ylabel("Tool usage (1 indicates used, 0 not used")
    plot = sns.relplot(
        data=data, x="TimeStamp", y="used",
        col="ID", hue="ID", style="ID",
        kind="line", col_wrap=1, marker='o', dashes=False, height=1, aspect=10,
    )
    plt.yticks([0, 0.5, 1])
    # plot.set_ylabels("Tool usage (1 indicates used, 0 not used")
    # plot.fig.suptitle("Separated plot of usage statistics of all the each tool over time\n\n", fontname="Times
    # New Roman",fontweight="bold")
    # plot.fig.subplots_adjust(top=1.5)

    html_str = mpld3.fig_to_html(fig)
    if flag == 0:
        plt.savefig('static/imgs/plot_line_all_separate.png', dpi=100)
        html_file = open("templates/plot_line_all_separate.html", "w")
    elif flag == 1:
        plt.savefig('static/imgs/plot_line_all_separate_cleaned.png', dpi=100)
        html_file = open("templates/plot_line_all_separate_cleaned.html", "w")

    html_file.write(html_str)
    html_file.close()


def plot_line_all_combined(data, flag):
    """
    :param data: A data frame to be plotted
    :param flag: An integer value to differentiate between original and smoothened data
    :return:

    This function plots a graph that combines tool usage of all the tools in one. Creates an image and an HTML page for
    interaction with the graph.
    """
    fig, ax = plt.subplots(figsize=(15, 7))
    plt.ylim(-1, 2)
    # ax = plt.gca()  # can access ax this way too
    x_dates = data['TimeStamp'].dt.strftime('%D-%M-%Y %h:%m:%s').sort_values().unique()
    max_date = max(data['TimeStamp'])
    max_date = max_date + dt.timedelta(0, 5)
    min_date = min(data['TimeStamp'])
    min_date = min_date - dt.timedelta(0, 5)
    plt.xlim(min_date, max_date)
    ax.set_xticklabels(labels=x_dates, rotation=10, ha='right')

    ax.set_ylabel("Tool usage (1 indicates used, 0 not used")
    ax.set_title('Plot of usage statistics of all the tools over time', fontname="Times New Roman", size=28,
                 fontweight="bold")
    line_plot_all_combined_plot = sns.pointplot(data=data, x="TimeStamp", y="used", hue="ID")
    line_plot_all_combined_figure = line_plot_all_combined_plot.get_figure()

    number_of_ticks = 0
    for ind, label in enumerate(ax.get_xticklabels()):
        number_of_ticks += 1

    for ind, label in enumerate(ax.get_xticklabels()):
        if ind % 5 == 0:  # every 5th label is kept
            label.set_visible(True)
        else:
            label.set_visible(False)
        if ind == (number_of_ticks - 1):
            label.set_visible(True)

    html_str = mpld3.fig_to_html(fig)
    if flag == 0:
        line_plot_all_combined_figure.savefig('static/imgs/plot_line_all_combined.png')
        html_file = open("templates/plot_line_all_combined.html", "w")
    elif flag == 1:
        line_plot_all_combined_figure.savefig('static/imgs/plot_line_all_combined_cleaned.png')
        html_file = open("templates/plot_line_all_combined_cleaned.html", "w")

    html_file.write(html_str)
    html_file.close()


def plot_kde(data, flag, variant):
    """
    :param data: A data frame to be plotted
    :param flag: An integer value to differentiate between original and smoothened data
    :param variant: An integer value to differentiate between two variants
    :return:

    This function plots a density graph of the usage of all the tools. Creates an image and an HTML page for interaction
    with the graph.
    """
    fig, ax = plt.subplots(figsize=(15, 7))
    # To format the date stamps on the html render
    # x_dates = data['TimeStamp'].dt.strftime('%d-%m-%Y %h:%m:%s').sort_values().unique()
    # ax.set_xticklabels(labels=x_dates, rotation=10, ha='right')
    ax.set_ylabel("Kernel density estimation of tool usage")
    ax.set_title('Kernel density estimation (KDE) plot of tool usage', fontname="Times New Roman", size=28,
                 fontweight="bold")
    if variant == 1:
        kde_plot = sns.kdeplot(data=data, x="TimeStamp", y="used", hue="ID", fill=True, common_norm=False, alpha=.5,
                               linewidth=1)
        kde_plot_figure = kde_plot.get_figure()

        html_str = mpld3.fig_to_html(fig)

        if flag == 0:
            kde_plot_figure.savefig('static/imgs/plot_kde_variant1.png')
            html_file = open("templates/kde_plot_variant1.html", "w")
        elif flag == 1:
            kde_plot_figure.savefig('static/imgs/plot_kde_cleaned_variant1.png')
            html_file = open("templates/plot_kde_cleaned_variant1.html", "w")

        html_file.write(html_str)
        html_file.close()
    else:
        data = data[data['used'] == 1]
        kde_plot = sns.kdeplot(data=data, x="TimeStamp", hue="ID", fill=True, common_norm=False, alpha=.5,
                               linewidth=1)
        kde_plot_figure = kde_plot.get_figure()

        html_str = mpld3.fig_to_html(fig)

        if flag == 0:
            kde_plot_figure.savefig('static/imgs/plot_kde_variant2.png')
            html_file = open("templates/plot_kde_variant2.html", "w")
        elif flag == 1:
            kde_plot_figure.savefig('static/imgs/plot_kde_cleaned_variant2.png')
            html_file = open("templates/plot_kde_cleaned_variant2.html", "w")

        html_file.write(html_str)
        html_file.close()


def plot_bokeh(data, flag, _dict):
    """
    :param data: A data frame to be plotted
    :param flag: An integer value to differentiate between original and smoothened data
    :param _dict: A dictionary containing the tool and marker mapping
    :return:

    This function plots a graph that combines tool usage of all the tools in one using the bokeh package. Creates an
    HTML page for interaction with the graph.
    """
    print(type(data['TimeStamp']))
    colors = itertools.cycle(palette)
    print(colors, type(colors))
    p = figure(width=1400, height=500, x_axis_type="datetime")
    for key, value in _dict.items():
        df = data[data['ID'] == value]
        color_used = next(colors)
        p.line((df['TimeStamp']), df['used'], color=color_used, line_width=2)
        p.circle(df['TimeStamp'], df['used'], fill_color=color_used, size=10)
        p.xaxis.formatter = DatetimeTickFormatter(years="%d/%m/%Y %H:%M:%S",
                                                  months="%d/%m/%Y %H:%M:%S",
                                                  days="%d/%m/%Y %H:%M:%S",
                                                  hours="%d/%m/%Y %H:%M:%S",
                                                  hourmin="%d/%m/%Y %H:%M:%S",
                                                  minutes="%d/%m/%Y %H:%M:%S",
                                                  minsec="%d/%m/%Y %H:%M:%S",
                                                  seconds="%d/%m/%Y %H:%M:%S",
                                                  milliseconds="%d/%m/%Y %H:%M:%S",
                                                  microseconds="%d/%m/%Y %H:%M:%S")

    if flag == 0:
        output_file("templates/bokeh.html")
    elif flag == 1:
        output_file("templates/bokeh_cleaned_data.html")
    show(p)


def plot_data(data, flag):
    """
    :param data: A data frame containing data returned by create_clean_excel().
    :param flag: An integer value to differentiate between original and smoothened data
    :return: plt: A plot to visualize data.

    This function generates different plots to visualize the data
    """

    if data is None:
        print("No data was recorded to be visualized.")
        return

    else:
        # Plot 1
        plot_kde(data, flag, 1)
        # Plot 2
        plot_kde(data, flag, 2)
        # Plot 3
        plot_line_all_combined(data, flag)
        # Plot 4
        plot_line_all_separate(data, flag)


def main():
    print("Starting Data Processing...\n")
    file_path = config.file_path
    entire_data = pd.read_csv(file_path, sep=',')

    # create a copy of the excel
    excel_copy_path = file_path[:-4] + "_copy.csv"

    if os.path.exists(excel_copy_path):
        prev_entire_data = pd.read_csv(excel_copy_path, sep=',')
        appended_data = entire_data[entire_data.index >= len(prev_entire_data)]
        appended_data = appended_data.reset_index(drop=True)
        entire_data = entire_data.reset_index(drop=True)  # drop index and update prev excel
        entire_data.to_csv(excel_copy_path)  # update prev excel
        entire_data = appended_data  # in the new iteration the entire data is only the appended data
    else:
        entire_data.to_csv(excel_copy_path, index=False)

    # add the 'used' column, to see if the tool was used or not
    entire_data['used'] = 'na'

    # Splitting the entire data frame into sub data frames based on tool and then applying grouping on time as there
    # are a lot of readings each second
    print("Starting Split and Group...\n")
    data_list_time_grouped = split_and_group_data(entire_data)

    # code used when processingAndVisualization needs to be used without appending any data
    if len(data_list_time_grouped) == 0:
        easygui.msgbox(
            "\n\n\nEmpty data was sent to the 'Split and Group' step,\n\n No new data was "
            "appended, hence no further steps were attempted.\n\nPlease use the console of your IDE to proceed further.",
            title="The data sent to split and group step was empty")

        print("\nEmpty data in 'Split and Group' step i.e no new data was appended, no further steps were attempted.")
        print("\nThe system is designed to stop if no new data is appended to save computations. Do you wish to "
              "override this and plot the graph of the already existing data from the previous run instead?")
        choice = input("'y' for yes | 'n' for no\n")

        if choice == 'y':
            print(file_path)
            entire_data = pd.read_csv(file_path, sep=',')
            entire_data['used'] = 'na'
            print("Starting Split and Group...\n")
            config.flag_for_empty_data_append_override = 1
            data_list_time_grouped = split_and_group_data(entire_data)

        elif choice == 'n':
            return
        else:
            print("Unexpected input, exiting.")
            return

    #print("print\n", data_list_time_grouped)
    # calculating based on co-ordinate changes if the tool is being used or not
    print("Starting tool usage estimation...\n")
    data_with_tool_used_calc = calculate_tool_usage(data_list_time_grouped, config.flag_for_empty_data_append_override)
    config.flag_for_empty_data_append_override = 0

    # Converting time stamp data to date time format for easier time calculations
    if data_with_tool_used_calc is not None:
        data_with_tool_used_calc['TimeStamp'] = pd.to_datetime(data_with_tool_used_calc['TimeStamp'])

    # Calculations to process and data and suggest thr order of the tool usage
    print("Starting tool order calculations...\n")
    suggested_order_data = suggest_order(data_with_tool_used_calc)

    # Creating clean data
    print("Creating clean data...\n")
    clean_ordered_data = create_clean_data(suggested_order_data)

    print("Order of the Tool usage is: \n")
    print(suggested_order_data)

    # print("\n Visualizing the data...\n")
    # plot_data(data_with_tool_used_calc, 0)
    # plot_bokeh(data_with_tool_used_calc, flag, tool_marker_map_dict)

    print("Plotting smoothened/cleaned data...\n")
    plot_data(clean_ordered_data, 1)
    # plot_bokeh(data_with_tool_used_calc, flag, tool_marker_map_dict)

    # This is done in order to display previous tool order and visualizations (in the visualizations.html page)in case
    # the newly added data (in append mode) is empty.
    tool_order_path = file_path[:-4] + "_tool_order.xlsx"
    try:
        prev_suggested_order_data = pd.read_excel(tool_order_path)
        easygui.msgbox(
            "\n\n\nHold on!\nThis might take a while.\nThe visualizations are being generated in the background.",
            title="Hold on!")
        return suggested_order_data, prev_suggested_order_data

    except FileNotFoundError:
        print("File containing previous data not found, to be plotted")
        #ctypes.windll.user32.MessageBoxW(0, "Your text", "Your title", 1)
        easygui.msgbox("\n\n\n\nNo files containing previous data were found to be plotted.\n\nPlease return to the home page or restart the application to start over again.", title="File not found")



if __name__ == "__main__":
    main()
