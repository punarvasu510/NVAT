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

#intermediate_dir = "/home/punarvasu510/Alekhya/FinalYearProject/GIT/NVAT/OpenCV_trials/"
intermediate_dir = sys.argv[1]

cursor = [{"video_id":"example_1","serial_number": 1},{"video_id":"example_2","serial_number": 2}]

for each in cursor:

    text_script = "ffmpeg -i " + str(each["video_id"]) + ".mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts intermediate_" + str(each["serial_number"]) + ".ts"
    #           ffmpeg -i     example_1   .mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts intermediate_          1          .ts

    comm = "echo " + text_script + " >> script_intermediate_test"
    call(comm, shell = True)

    text_input = "file " + intermediate_dir + "intermediate_" + str(each["serial_number"]) + ".ts"
    #             file     /home/..../         intermediate_                 1                .ts

    comm = "echo " + text_input + " >> input_test.txt"
    call(comm, shell = True)

call("chmod 755 script_intermediate_test", shell = True)
call("./script_intermediate_test", shell = True)
call("ffmpeg -f concat -safe 0 -i input_test.txt -c copy output.mp4", shell = True)
call("rm intermediate_*", shell = True)
call("rm *_test*",shell = True)
