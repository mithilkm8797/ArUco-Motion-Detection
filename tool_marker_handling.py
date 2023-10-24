import os

import pandas as pd
import config as config


def handling():
    # To handle multiple application runs and reload tools from previous runs
    path = config.folder + "/tool_marker_map_dict.xlsx"
    print("\nThe path of tool marker map dict file is:   ", path)
    if os.path.exists(path):
        previous_tool_marker_map_dict_df = pd.read_excel(path)
        current_tool_marker_map_dict_df = pd.DataFrame(data=config.tool_marker_map_dict.items(),
                                                       columns=['Aruco ID', 'Tool Name']).reset_index(drop=True)
        new_tool_marker_map_dict_df = previous_tool_marker_map_dict_df._append(current_tool_marker_map_dict_df,
                                                                               ignore_index=True)
        new_tool_marker_map_dict_df.dropna(inplace=True)
        config.tool_marker_map_dict = new_tool_marker_map_dict_df.set_index('Aruco ID')['Tool Name'].to_dict()
        print("New tool marker map dictionary is:    ", config.tool_marker_map_dict)
        os.remove(path)
        writer = pd.ExcelWriter(path, engine='xlsxwriter')
        new_tool_marker_map_dict_df.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.close()
        print("tool_marker_map_dict.xlsx was created at path:   ", path)

    else:
        df = pd.DataFrame(config.tool_marker_map_dict.items(), columns=['Aruco ID', 'Tool Name']).reset_index(drop=True)
        writer = pd.ExcelWriter(path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.close()
        print("tool_marker_map_dict.xlsx was created at path:   ", path)
