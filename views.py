from flask import Blueprint, render_template, request, redirect, jsonify, Response
import json
import arucoDetection as AD

views = Blueprint(__name__, "views")

file_exists = False
filename = "Data"
folder = "C:/Users/kmmit/Desktop/Aruco Project/"
file_path = "C:/Users/kmmit/Desktop/Aruco Project/Data/Data.csv"

tool_list = ["Hammer", "Chisel", "Screwdriver"]
marker_list = ["2", "1", "0"]

choice = "a"


@views.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        global filename, file_path, folder, tool_list, file_exists

        # default values assigned
        file_path = "C:/Users/kmmit/Desktop/Aruco Project/Data/Data.csv"
        folder = "C:/Users/kmmit/Desktop/Aruco Project/"

        filename = request.form.get('filename')
        file_path = folder + filename + "/" + filename + ".csv"
        tools = request.form.get('tools')
        tool_list = AD.tools_to_list(tools)
        file_exists = AD.check_file(filename)
        return redirect("/file_creation")
    return render_template("home.html")


@views.route("/file_creation", methods=['GET', 'POST'])
def file_creation():
    global file_exists, filename, file_path, marker_list
    if request.method == 'POST':
        marker_list = request.form.get('map')
        marker_list = AD.markers_to_list(marker_list)
        AD.create_tools_marker_map_dict()
        return redirect("/detection")
    return render_template("file_creation.html", file_exists=file_exists, filename=filename, file_path=file_path, tools=tool_list)


@views.route("/detection",  methods=['GET', 'POST'])
def detection():
    if request.method == 'POST':
        data = request.get_json()
        json_data = json.loads(data)
        if json_data != "":
            AD.detection()
            return render_template("detection.html")
    return render_template("detection.html")


@views.route("/visualizations")
def visualization():
    AD.main()
    return render_template("visualizations.html")


@views.route("/append_delete", methods=['POST', 'GET'])
def append_delete():
    global choice
    data = request.get_json()
    json_data = json.loads(data)
    choice = AD.file_handling(json_data)
    print("The choice of appending and delete is: ", json_data)
    return jsonify(data)


@views.route("/tips")
def tips():
    return render_template("tips.html")


@views.route("/about")
def about():
    return render_template("about.html")
