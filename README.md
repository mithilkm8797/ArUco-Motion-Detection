# ArUco-Motion-Detection

Documentation of a process is often cumbersome and time-consuming for the authors. This is also true in the case of [DIY][1] authors and processes. 

This master thesis project aims to support DIY authors in their documentation processes. A tool that automates the collection of information about the tool usage statistics during the DIY processes is proposed. This is done via detecting and tracking the motion of [ArUco markers][2] that can be affixed to tools used during the DIY processes. Details such as the the tool usage order, the usage duration, and time-series visualizations of tool usages are generated. Providing such fundamental information about the tools used, can help in giving the authors a head-start their documentation efforts.

# Instructions
## Building the Project

1. Download/Clone the project from the [github repository][3].
2. Download and install the list of packages from the `packages_all.jpeg`. ([File](static/imgs/packages_all.jpeg))
      * Please make sure to use the `python` version `3.x` and `opencv-contrib-python` version `3.4.11.45` to avoid compile time errors and versioning conflicts.
3. Print the desired ArUco marker types and sizes from [here][4].
      * Each tool must have a unique marker affixed to it, for the tools to be differentiated from each other.
      * An example can be seen in the image below.<br>
        ![][image-1]
4. Install the `iVCam` application both on the computer used to run the application and on the smartphone device whose camera will be used for detection.
      * This application is required to access the smartphone camera directly from the computer during the application run.
      * `iVCam` can be downloaded from [here][5].
5. Also make sure to set the right folder locations, where you would like the application to save the files generated during the applicaiton run in `config.py` 
6. Run the application by running the `app.py` file.
   
[1]: https://en.wikipedia.org/wiki/Do_it_yourself
[2]: https://docs.opencv.org/4.x/d9/d6d/tutorial_table_of_content_aruco.html#:~:text=ArUco%20markers%20are%20binary%20square,pose%20estimation%20and%20camera%20calibration.
[3]: https://github.com/mithilkm8797/ArUco-Motion-Detection
[4]: https://chev.me/arucogen/
[5]: https://www.e2esoft.com/ivcam/

[image-1]: static/imgs/unique_markers_affixed_to_tools.jpg
