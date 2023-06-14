from datetime import datetime

import cv2
import csv
import os
import numpy as np
import shutil

from cv2 import aruco

import processingAndVisualization as PV
import config as config

#default_folder = "C:/Users/kmmit/Desktop/Aruco Project/"
#folder = ""
#filename = "Data"
#file_path = "C:/Users/kmmit/Desktop/Aruco Project/Data/Data.csv"

#tool_list = ["Hammer", "Chisel", "Screwdriver"]
#marker_list = ["2", "1", "0"]
#tool_marker_map_dict = {"2": "Hammer", "1": "Chisel", "0": "Screwdriver"}

ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
    "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
    "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
    "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
    "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}


def aruco_display(corners, ids, image):
    """
    :param corners: The corners detected and returned by thr function: detectMarkers() from the ArUco Library
    :param ids: The IDs detected and returned by thr function: detectMarkers() from the ArUco Library
    :param image: The image frame returned by the camera
    :return: image: with marked center, edges and text indicating the tool associated with each ArUco marker

    The function builds edges from the received corners and then calculates the center. It then returns an image with
    marked center, edges and text indicating the tool associated with each ArUco marker. All of this information along
    with the x and y co-ordinates are recorded and stored in an Excel sheet.
    """

    if len(corners) > 0:
        ids = ids.flatten()

        for (markerCorner, markerID) in zip(corners, ids):
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners

            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))

            cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)

            centerX = int((topLeft[0] + bottomRight[0]) / 2.0)
            centerY = int((topLeft[1] + bottomRight[1]) / 2.0)
            cv2.circle(image, (centerX, centerY), 4, (0, 0, 255), -1)

            tool_name = config.tool_marker_map_dict.get(str(markerID))

            cv2.putText(image, tool_name, (topLeft[0], topLeft[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            print(" Detected \'" + str(tool_name) + "\' with Aruco Marker ID: " + str(markerID) + " | X Co-ordinate: {}"
                  .format(centerX) + ", Y Co-ordinate: {}".format(centerY))

            headers = ['TimeStamp', 'ID', 'X-co', 'Y-co']
            rows = [
                {
                    'TimeStamp': datetime.now().replace(microsecond=0),
                    'ID': tool_name,
                    'X-co': float(centerX),
                    'Y-co': float(centerY)
                }
            ]
            with open(config.file_path, "a", encoding="UTF8", newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=headers)
                writer = csv.DictWriter(csv_file, fieldnames=headers)
                writer.writerows(rows)

    return image


def augmentAruco(corners, id, img, drawId=True):
    """
    :param corners:
    :param id:
    :param img:
    :param drawId:
    :return:

    This function is aimed at assigning custom images to the ArUco markers. The function is incomplete and may not work
    fully. It was an experiment to test the augmentation functionality. It can be used to further improve this tool.
    """
    imgAug = cv2.imread("static/imgs/axe png.png")
    (topLeft, topRight, bottomRight, bottomLeft) = corners

    topRight = (int(topRight[0]), int(topRight[1]))
    bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
    bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
    topLeft = (int(topLeft[0]), int(topLeft[1]))

    h, w, c = imgAug.shape

    pts1 = np.array([topLeft, topRight, bottomRight, bottomLeft])
    pts2 = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    matrix, _ = cv2.findHomography(pts2, pts1)
    imgOut = cv2.warpPerspective(imgAug, matrix, (img.shape[1], img.shape[0]))

    return imgAug, imgOut


def check_file(filename_received):
    """
    :param filename_received: A string containing the filename given as a input by the user (route @"/" in views.py).
    :return: file_exists: A boolean value telling if the file exists or not.

    The function checks whether the file exits or not, and also updates the file name, folder and file path. It returns
    a boolean value based on the existence of the file.
    """

    default_folder = config.default_folder

    filename = filename_received.strip()  # strip() to remove unwanted leading and trailing spaces
    config.file_name = filename
    folder = default_folder + filename
    config.folder = folder
    file_path = folder + "/" + filename + ".csv"
    config.file_path = file_path
    file_exists = os.path.exists(file_path)
    print(file_path + ": " + str(file_exists))
    return file_exists


def tools_to_list(tools):
    """
    :param tools: A string containing the tools, given as an input by the user (route @"/" in views.py).
    :return: tool_list: A list containing the tools.

    The function converts string of tools to list of tools and returns it.
    """
    stripped_tool_list = []
    tool_list = tools.split(',')
    for tool in tool_list:
        tool = tool.strip()  # strip() to remove unwanted leading and trailing spaces
        stripped_tool_list.append(tool)
    tool_list = stripped_tool_list
    print(tool_list)
    return tool_list


def markers_to_list(markers):
    """
    :param markers: A string containing the markers, given as an input by the user (route @"/file_creation" in views.py)
    :return: marker_list: A list containing the markers.

    The function converts string of markers to list of markers and returns it.
    """

    stripped_marker_list = []
    marker_list = markers.split(',')
    for marker in marker_list:
        marker = marker.strip()  # strip() to remove unwanted leading and trailing spaces
        stripped_marker_list.append(marker)
    marker_list = stripped_marker_list
    print("The Aruco marker list is: ", marker_list)
    return marker_list


def create_tools_marker_map_dict():
    """
    The function takes config variables: marker_list and tool_list,  to create a dictionary: tool_marker_map_dict with
    keys as markers IDs (string) and values as Tool names (string).
    """

    marker_list = config.marker_list
    tool_list = config.tool_list
    tool_marker_map_dict = dict(zip(marker_list, tool_list))
    print("\nCreating marker and tool dictionary...")
    print("The dictionary is: ", tool_marker_map_dict)

    return tool_marker_map_dict


def file_handling(choice):
    """
    :param choice: A string containing the choice, given as an input by the user (route @"/append_delete" in views.py).
    :return: choice: A string.

    This function is responsible for the initial file handling and setup. Based on the user input to create a new file,
    or append or delete, the corresponding respective actions are handled. It returns the choice back.
    """
    folder = config.folder
    filename = config.file_name
    file_path = config.file_path

    headers = ['TimeStamp', 'ID', 'X-co', 'Y-co']
    if choice == "new":
        os.mkdir(folder)
        with open(file_path, "a", encoding="UTF8", newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
    elif choice == "d":
        try:
            shutil.rmtree(folder, ignore_errors=True)
            print("The folder containing the file " + "\'" + filename + ".csv\' with path: " + "\"" + file_path +
                  "\"" + " was deleted.")
        except FileNotFoundError:
            print("File not found!")

        os.mkdir(folder)
        with open(file_path, "a", encoding="UTF8", newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
        print("The file " + "\'" + filename + ".csv\' with path: " + "\"" + file_path + "\"" + " was created.")
    elif choice == "a":
        print("Appending data to " + "\'" + filename + ".csv\' with path: " + "\"" + file_path + "\"" )
    else:
        print("Did not receive the right choice!")

    return choice


def detection():
    """
    This is the primary function for the detection of ArUco markers. Includes importing the ArUco dictionary, creating
    detector parameters, setting up video capture, and the actual detection.
    """

    print("Starting detection...\n")
    aruco_type = "DICT_4X4_50"

    arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[aruco_type])

    arucoParams = cv2.aruco.DetectorParameters_create()

    # The parameters for cv2.VideoCapture() for my system were (changes from system to system):
    # 0: DSLR, 1: IVCam, 2: Iruin Webcam, 3: system (when nothing is connected via USB)
    # 3: IVCam / Phone (when the phone is connected on the left USB port of the PC)

    # File inputs can also be given:
    # Example: 'C:/Users/kmmit/Desktop/Aruco Project/video4k_30fps.mp4'
    # When file is used as an input make sure to divide durations by the video fps for tool usage time calculations
    # as input video and openCV frames rates are different

    # There is also a possibility to use IP Webcams: An app called "IP Webcam" can be found on the playstore for the
    # Android users. The system and the phone must be connected to the same Wi-Fi, and the IP address can be given as
    # the input to cv2.VideoCapture(3) TODO: ip address as input or the below code?? is it true?

    capture = cv2.VideoCapture(1)
    # address = "https://192.168.178.147:8080/video"
    # capture.open(address)

    # Setting frame resolution: 2650 x 1140
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 2650)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1140)
    fps = capture.get(cv2.CAP_PROP_FPS)
    print("Frames per second (fps) of the video: " + str(fps) + "\n")

    # function to map marker IDs to tool names
    # create_tools_marker_map_dict() # use if the web GUI isn't being used

    print("Start Capturing...\n")

    while capture.isOpened():
        ret, img = capture.read()
        h, w, _ = img.shape

        # width = 1000
        # height = int(width * (h / w))
        # img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)

        corners, ids, rejected = cv2.aruco.detectMarkers(img, arucoDict, parameters=arucoParams)
        detected_image = aruco_display(corners, ids, img)

        # Use the below code for augmenting ArUco and assigning custom images to ArUco markers. TODO: future scope
        # if len(corners) != 0:
        #    for (corner, id) in zip(corners[0], ids):
        #        img = augmentAruco(corner, id, img)

        cv2.imshow("Image", detected_image)
        cv2.imshow("Image", img)

        # to make the window automatically pop up
        cv2.setWindowProperty("Image", cv2.WND_PROP_TOPMOST, 1)
        cv2.setWindowTitle("Image", "Aruco Object Detection Video Stream")
        cv2.moveWindow("Image", 120, 50)

        # code enabling close of video stream when X is clicked on the video stream window
        cv2.waitKey(1)
        value = cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE)

        if value == 0:
            break

        # Use the below code to set a keyboard key which on pressing initiates closing of the video stream
        # key = cv2.waitKey(1) & 0xFF
        # if key == ord("q"):
        #    break

    capture.release()
    cv2.destroyAllWindows()

    print("Aruco Marker detection has Ended.\n")


def main():
    detection()
    PV.main()


if __name__ == "__main__":
    main()
