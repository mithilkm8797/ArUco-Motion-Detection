from flask import Blueprint, render_template, request, redirect, jsonify, Response

import json

import arucoDetection as AD
import processingAndVisualization as PV

import config as config

views = Blueprint(__name__, "views")


@views.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        folder = config.default_folder
        f = request.form

        tools_string = ""
        markers_string = ""
        filename = ""
        # to get tool name and marker ID
        for key in f.keys():
            key = str(key)
            print(key, type(key))
            for value in f.getlist(key):
                value = str(value)
                print(value, type(value))
                if key[0:8] == "filename":
                    filename = value
                elif key[0:4] == "tool":
                    if len(tools_string) == 0:
                        tools_string = value
                    else:
                        tools_string = tools_string + "," + value
                elif key[0:6] == "marker":
                    if len(markers_string) == 0:
                        markers_string = value
                    else:
                        markers_string = markers_string + "," + value

        config.file_exists = AD.check_file(filename)
        config.tool_list = AD.tools_to_list(tools_string)
        config.marker_list = AD.markers_to_list(markers_string)
        config.tool_marker_map_dict = AD.create_tools_marker_map_dict()

        return redirect("/file_creation")
    return render_template("home.html")


@views.route("/file_creation", methods=['GET', 'POST'])
def file_creation():
    if request.method == 'POST':
        return redirect("/detection")
    return render_template("file_creation.html", file_exists=config.file_exists, filename=config.file_name,
                           file_path=config.file_path, dict=config.tool_marker_map_dict)


@views.route("/detection", methods=['GET', 'POST'])
def detection():
    if request.method == 'POST':
        config.append_count += 1  # just to keep track of the appends to the file
        data = request.get_json()
        json_data = json.loads(data)
        if json_data != "":
            AD.detection()
            return render_template("detection.html", file_exists=config.file_exists, filename=config.file_name,
                                   file_path=config.file_path, dict=config.tool_marker_map_dict)
    return render_template("detection.html", file_exists=config.file_exists, filename=config.file_name,
                           file_path=config.file_path, dict=config.tool_marker_map_dict)


@views.route("/visualizations")
def visualizations():
    ordered_df, prev_ordered_df = PV.main()
    print(type(ordered_df))
    return render_template("visualizations.html", file_exists=config.file_exists, filename=config.file_name,
                           file_path=config.file_path, dict=config.tool_marker_map_dict, ordered_data=ordered_df,
                           prev_data=prev_ordered_df)


@views.route("/append_delete", methods=['POST', 'GET'])
def append_delete():
    data = request.get_json()
    json_data = json.loads(data)
    config.choice = AD.file_handling(json_data)
    print("The choice of appending and delete is: ", json_data)
    return jsonify(data)


@views.route("/tips")
def tips():
    return render_template("tips.html")


@views.route("/about")
def about():
    return render_template("about.html")


@views.route("/combined_plot")
def combined_plot():
    return render_template("plot_line_all_combined_cleaned.html")


@views.route("/kde_v1")
def kde_v1():
    return render_template("plot_kde_cleaned_variant1.html")


@views.route("/kde_v2")
def kde_v2():
    return render_template("plot_kde_cleaned_variant2.html")


@views.route("/separated_plot")
def separated_plot():
    return render_template("plot_line_all_separate_cleaned.html")
