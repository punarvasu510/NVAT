from subprocess import call
import sys

    # Fetch all videos of an intruder from database
    # Order them as per serial number ( which in determined by timestamp )
    # Loop through the result to add ffmpeg command ( which generates the intermediate file ) for each video
    # Loop through the result to add each intermediate file to input file (for concatenation)
    # Concatenate
    # Clear all intermediate files
    # The final tapestry is stored in output.mp4

    # To execute: python generateTapestry.py <absolute-path-to-videos-directory>

def genTape(video_list):

    #video_list = ["Video_1_2018-02-02 01-52-51.mp4","Video_1_2018-02-02 01-53-04.mp4"]
    intermediate_dir = "/home/punarvasu510/Alekhya/FinalYearProject/GIT/NVAT/Flask_trial/flask-env/static/video_clips/"
    i=1

    for video in video_list:

        text_script = "ffmpeg -i " + "'\"" + intermediate_dir + str(video) + "\"'" + " -c copy -bsf:v h264_mp4toannexb -f mpegts " + intermediate_dir + "intermediate_" + str(i) + ".ts"
        #ffmpeg -i "/home/.../Video_1_2018-02-02 01-52-51.mp4" -c copy -bsf:v h264_mp4toannexb -f mpegts /home/.../intermediate_1.ts

        #print "text_script --------------- " + text_script

        comm = "echo " + text_script + " >> script_intermediate_test"
        call(comm, shell = True)

        text_input = "file " + intermediate_dir + "intermediate_" + str(i) + ".ts"
        #             file     /home/..../         intermediate_      1       .ts

        comm = "echo " + text_input + " >> input_test.txt"
        call(comm, shell = True)

        i=i+1

    output_file = intermediate_dir + "output.mp4"

    comm = "rm " + output_file
    call(comm, shell = True)

    call("chmod 755 script_intermediate_test", shell = True)
    call("./script_intermediate_test", shell = True)

    comm = "ffmpeg -f concat -safe 0 -i input_test.txt -c copy " + output_file
    #print "\n\n\nconcat command ------------------ " + comm + "\n\n\n"
    call(comm, shell = True)

    comm = "rm " + intermediate_dir +  "intermediate_*"
    #print "\n\n\nremove command -------------- " + comm + "\n\n\n"
    call(comm, shell = True)

    call("rm *_test*",shell = True)

    return output_file
