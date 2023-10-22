# ArUco-Motion-Detection

Documentation of a process is often cumbersome and time-consuming for the authors. This is also true in the case of [DIY][1] authors and processes. 

This master thesis project aims to support DIY authors in their documentation processes. A tool that automates the collection of information about the tool usage statistics during the DIY processes is proposed. This is done via detecting and tracking the motion of [ArUco markers][2] that can be affixed to tools used during the DIY processes. Details such as the the tool usage order, the usage duration, and time-series visualizations of tool usages are generated. Providing such fundamental information about the tools used, can help in giving the authors a head-start their documentation efforts.

# Instructions
## Building the Project

1. Download/clone the project from the [github repository][3].
2. Download and install the list of packages from the `packages_all.jpeg` ([File][static/imgs/packages_all.jpeg])
3. Print the desired Aruco marker types and sizes from [here][4]. Each tool must have a unique marker affixed to it, for the tools to be differentiated from each other.

[1]: https://en.wikipedia.org/wiki/Do_it_yourself
[2]: https://docs.opencv.org/4.x/d9/d6d/tutorial_table_of_content_aruco.html#:~:text=ArUco%20markers%20are%20binary%20square,pose%20estimation%20and%20camera%20calibration.
[3]: https://github.com/mithilkm8797/ArUco-Motion-Detection
[4]: https://chev.me/arucogen/
