####################################################
"""
NOT A PART OF THE MAIN CODE. THIS FILE WAS JUST TO DOCUMENT MY LEARNINGS!!!
"""
##############################################
from datetime import datetime
import time
import pandas as pd
import numpy as np

# ct stores current time
df = pd.DataFrame({'month': [1, 4, 7, 10],
                   'year': [2012, 2014, 2013, 2014],
                   'sale': [55, 40, 84, 31]})
print(df)


value = df['year'].loc[lambda x: x==2013].index.to_list()[0]

print(value)

headers = ['TimeStamp', 'ID', 'X-co', 'Y-co']
    answer = input(
        "A file with data already exists, do you want to process by deleting the file or appending to it? Enter d for "
        "delete, a for append\n")
    if answer == "d":
        try:
            os.remove("C:/Users/kmmit/Desktop/Aruco Project/Data.csv")
            print("Data.xlsx file deleted")
        except FileNotFoundError:
            print("File not found")

        with open("C:/Users/kmmit/Desktop/Aruco Project/Data.csv", "a", encoding="UTF8", newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
    elif answer == "a":
        print("Appending data to the existing file...")
    else:
        print()


$(document).ready(function() {

            $("#next").click(function() {

                if ( {{ file_check }} == "True") {
                    $("#output").text("File exists");
                } else {
                    $("#output").text('File not exists');
                }
            });
        });

if request.method == 'POST':
    result = request.form
    print(result)
    return render_template("home.html", file_check=result)
else:
    return render_template("home.html")

// script to send HTML data to python files
        function send_data(){

            var fileName = document.getElementById("filename").value;
            var tool_list = document.getElementById("tools").value;

            var dict_value = {fileName, tool_list};
            var json_data = JSON.stringify(dict_value);
            console.log(json_data);

            $.ajax({
                url:"/check_file",
                type:"POST",
                contentType: "application/json",
                dataType: "json",
                data: JSON.stringify(json_data)});
        }
        //document.getElementById("next").addEventListener("click", send_data);

//modal display
$(document).ready(function() {
            $('#form').on('submit', function(e){
                $('#modal_info').modal('show');
                $(".modal-backdrop").remove();
                var span = document.getElementsByClassName("close")[0];
                span.onclick = function() {
                    modal.style.display = "none";
                }
                e.preventDefault();
            });
        });

# map tool list to ids
        global tool_list
        ids = ids.sort()
        index = 0
        for tool in tool_list:
            ids[index] = tool
            index += 1
        print(ids)

<div style="background-color: rgb(255, 204, 0, 0.4);">
                    <p style="padding-top:10px;">
                        <p style="background-color: rgb(237, 62, 62, 0.4);">Important NOTE:</p>
                        <i>Please place the Aruco marker such that it has the highest likelihood to stay as <b>entirely</b> visible to the camera as possible during the usage of the tool.</i>
                         <br><br>
                        <i>The <u>minimum requirement</u> for accurate results is that the Aruco marker be detected correctly at <u>all times</u> when the tool is at rest.</i>
                        <div style="padding-bottom:10px;">Click <a href="/tips" target="_blank">here</a> for tips.</div>
                    </p>
                </div>

<p style="background-color: rgb(119, 117, 118, 0.2);padding-top: 10px;padding-bottom: 10px;">
                    Please also make sure that the <i><u>ID order</u></i> of aruco markers placed/stuck onto the tools are the same as the <i><u>tool order</u></i> that was input in the previous step.
                    <br><br>
                    <b><u>Example:</u></b>
                    <br><br>
                    If you decide to print out <span style="font-family:Arial">3</span> aruco markers with IDs <b style="font-family:Arial">5</b>, <b style="font-family:Arial">9</b>, and <b style="font-family:Arial">2</b>, and the input tool order was "<b>Hammer</b>, <b>Chisel</b>, and <b>Pliers</b>."
                    <br><br>
                    Please stick marker with the ID
                    <br>
                    <u style="font-family:Arial">2 to the Hammer</u>,
                    <br>
                    <u style="font-family:Arial">5 to the Chisel</u>,
                    <br>
                    <u style="font-family:Arial">9 to the Pliers</u>.
</p>

// to display video stream in html
<!-- // to display opencv video stream in html
                                        <img id="img" src="{{ url_for('views.video_feed') }}">
                                        <<canvas id="canvas" width="1200px" height="480px"></canvas>-->
# To display the video stream in the html
#@views.route('/video_feed')
#def video_feed():
#    """Video streaming route. Put this in the src attribute of an img tag."""
#    return Response(AD.main(), mimetype='multipart/x-mixed-replace; boundary=frame')

// To display the video stream in the html
        /*var ctx = document.getElementById("canvas").getContext('2d');
        var img = new Image();
        img.src = "{{ url_for('views.video_feed') }}";

        // need only for static image
        //img.onload = function(){
        //    ctx.drawImage(img, 0, 0);
        //};

        // need only for animated image
        function refreshCanvas(){
            ctx.drawImage(img, 0, 0);
        };
        window.setInterval("refreshCanvas()", 50);*/

//modal window X (close) button
< span class ="close topright " > & times; < /span >

$('#agree_chkbx').
$('#to_visuals').show();
$('#start').prop('disabled', true);

for index in data_1.index:
    cur_x = float(data_1['X-co'].iloc[index])
    cur_y = float(data_1['Y-co'].iloc[index])
    try:
        next_x = float(data_1['X-co'].iloc[index + 1])
    except IndexError:
        next_x = float(data_1['X-co'].iloc[index])
    try:
        next_y = float(data_1['Y-co'].iloc[index + 1])
    except IndexError:
        next_y = float(data_1['Y-co'].iloc[index])

    if abs(next_x - cur_x) > 1 or abs(next_y - cur_y) > 1:
        data_1.loc[index, 'used'] = int(1)
    else:
        data_1.loc[index, 'used'] = int(0)

for index in data_2.index:
    cur_x = float(data_2['X-co'].iloc[index])
    cur_y = float(data_2['Y-co'].iloc[index])
    try:
        next_x = float(data_2['X-co'].iloc[index + 1])
    except IndexError:
        next_x = float(data_2['X-co'].iloc[index])
    try:
        next_y = float(data_2['Y-co'].iloc[index + 1])
    except IndexError:
        next_y = float(data_2['Y-co'].iloc[index])

    if abs(next_x - cur_x) > 1 or abs(next_y - cur_y) > 1:
        data_2.loc[index, 'used'] = int(1)
    else:
        data_2.loc[index, 'used'] = int(0)

entire_processed_data = pd.concat([data_0, data_1, data_2], ignore_index=True)

return entire_processed_data

generated_file_path_csv = file_path[
                                      :-4] + "_with_tool_usage_stats.csv"
            data_with_tool_used_calc = pd.read_csv(generated_file_path_csv, sep=',')
            data_with_tool_used_calc['TimeStamp'] = pd.to_datetime(data_with_tool_used_calc['TimeStamp'])
            plot_data(data_with_tool_used_calc)
            return

----------------
#for key, value in tool_marker_map_dict.items():
    #    clean_data['ID'] = value
    #    clean_data_list.append(clean_data[:])  # shallow copy (if you just send clean_data, you are actually just
    # sending a reference to clean_data. Hence, at the end of the loop, clean_data_list will have the all the
    # elements inside it same as the latest value of clean_data.

clean_data_list_new = []
    for (df, clean_df) in zip(data_list, clean_data_list):
        #print("before\n")
        #for data in clean_data_list_new:
            #print(data, "\n")
        for index_in_df in df.index:
            duration = int(df['Duration'].iloc[index_in_df])
            start_date = df['StartDate'].iloc[index_in_df]
            start_index_to_fill = clean_data[clean_data['TimeStamp'] == start_date].index[0]
            for index_in_clean_df in clean_df.index:
                clean_df.loc[start_index_to_fill + index_in_clean_df, 'used'] = int(1)
                if index_in_clean_df > duration - 1:
                    break
        clean_data_list_new.append(clean_df[:])
        #print(id(clean_df))
        #print("After\n")
        #for data in clean_data_list_new:
            #print(data, "\n")

    clean_time_series_data = pd.DataFrame()
    for clean_data in clean_data_list_new:
        print(id(clean_data))
        clean_time_series_data = clean_time_series_data._append(clean_data, ignore_index=True)

    clean_time_series_data_file_path = file_path[:-4] + "_filtered_clean.xlsx"
    # done to fix the path for .to_excel() to work
    clean_time_series_data_file_path = clean_time_series_data_file_path.replace("/", "\\")
    clean_time_series_data.to_excel(clean_time_series_data_file_path, index=False)

    return clean_time_series_data

# to enable button only after all inputs are filled
inputs.forEach((input) => {
            input.addEventListener('input', () => {
                let id = event.target.getAttribute('id');
                if (event.target.value.length > 0) {
                    inputValidator[id] = true;
                }
                else {
                    inputValidator[id] = false;
                };

                let allTrue = Object.keys(inputValidator).every((item) => {
                    return inputValidator[item] === true
                });

                if (allTrue) {
                    buttonSend.disabled = false;
                }
                else {
                    buttonSend.disabled = true;
                }
            })
        })
div_to_append.appendChild(newTool, newMarker);

          formfield.appendChild(div_to_append)

# to get fig
fig = plt.figure(figsize=(20, 10), dpi=70)

#
fig = plt.figure()

p = plt.scatter(IMP, CLS, c='g', marker='o', s=25)
ax1 = plt.gca()
ax1.set_ylim(-1.15, -0.6)
ax1.set_xlim(-0.1, 5.1)

# hover over the graph in html  (not working for me)
labels =['point {0}'.format(i + 1) for i in range(len(data))]
tooltip = mpld3.plugins.PointHTMLTooltip(kde_plot, labels=labels)
mpld3.plugins.connect(fig, tooltip)


################################################
def dist_plot(data, flag, _dict):

    fig, ax = plt.subplots(figsize=(15, 7))
    # To format the date stamps on the html render
    x_dates = data['TimeStamp'].dt.strftime('%d-%m-%Y %h:%m:%s').sort_values().unique()
    ax.set_xticklabels(labels=x_dates, rotation=10, ha='right')
    ax.set_ylabel("dist density estimation of tool usage")
    ax.set_title('dist density estimation (KDE) plot of tool usage', fontname="Times New Roman", size=28,
                 fontweight="bold")
    df_list = []
    tool_names = []
    count_list = []
    #data['used'] = pd.to_numeric(data['used'], errors='coerce').astype('Float64')
    data['used'] = data['used'].astype(float)
    for key, value in _dict.items():
        if value != 'hammer':
            x = data[data['ID']==value]
            df_list.append(x[:])
            tool_names.append(value[:])

    count_list = [df['used'].values for df in df_list]
    print(count_list)
    max_count = max([count_i.max() for count_i in count_list])
    min_count = min([count_i.min() for count_i in count_list])

    xs = np.linspace(min_count - 3, max_count + 3, 200)

    month_kde = [gaussian_kde(count_i, bw_method=0.2) for count_i in count_list]

    max_kde = max([kde_i(xs).max() for kde_i in month_kde])
    overlap_factor = 1.9
    whiten_factor = 0.5
    cmap = plt.cm.get_cmap('Spectral')
    #sns.diverging_palette(230, 20, as_cmap=False)
    fig, ax = plt.subplots(figsize=(12, 8))
    for index, color in zip(range(len(tool_names) - 1, -1, -1), list(sns.color_palette("Set2"))):
        kde = month_kde[index](xs) / max_kde * overlap_factor
        ax.plot(xs, index + kde, lw=2, color=color, zorder=50 - index)
        whitened = np.array(to_rgb(color)) * (1 - whiten_factor) + whiten_factor
        ax.fill_between(xs, index, index + kde, color=whitened, alpha=0.8, zorder=50 - index)
    ax.set_xlim(xs[0], xs[-1])
    ax.set_xlabel('Distribution of Counts')
    ax.set_yticks(np.arange(len(tool_names)))
    ax.set_yticklabels(tool_names)
    for spine in ('top', 'left', 'right'):
        ax.spines[spine].set(visible=False)
    plt.tight_layout()
    plt.show()

    #kde_plot_figure = kde_plot.get_figure()

    #html_str = mpld3.fig_to_html(fig)

    #if flag == 0:
        #kde_plot_figure.savefig('static/imgs/dist_plot.png')
        #html_file = open("templates/visualizations/dist_plot.html", "w")
    #elif flag == 1:
        #kde_plot_figure.savefig('static/imgs/dist_plot_cleaned.png')
        #html_file = open("templates/visualizations/dist_plot_cleaned.html", "w")

    #html_file.write(html_str)
    #html_file.close()
    plt.show()
#########################################
#custom_ticks = range(0, len(data), 10)  # ticks every 5
    #timestamps = [f"{data['TimeStamp'][t].day:02}-{data['TimeStamp'][t].month:02}-{data['TimeStamp'][t].year:04} " \
                  #f"{data['TimeStamp'][t].hour:02}:{data['TimeStamp'][t].minute:02}:{data['TimeStamp'][t].second:02}"
                  #for t in custom_ticks]
    #line_plot_all_combined_plot.axes.set_xticks(custom_ticks)
    #line_plot_all_combined_plot.axes.set_xticklabels(labels=timestamps, rotation=10, ha='right')