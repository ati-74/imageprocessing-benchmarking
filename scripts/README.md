# Overview of Each Script:

<b><i>tracking-plotbac.py:</i></b> This script creates visualizations for the tracking output of various tools. You'll find
the resulting tracking plots in the specific folder for each tool under the analyses folder.</n></n></n>

<b><i>reference_BW_img.py:</i></b> This script starts by retrieving the output file from LAbkit. It then identifies each
bacterium's pixels from the LAbkit output and displays them in black and white. This script is primarily
used for IOU (Intersection over Union) calculations.</n></n></n>

<b><i>Jitter_remover.py:</b></i> This scripts minimizes stage jitter effects.</n></n></n>


<b><i>delta_modified.zip:</b></i> The Delta output includes the minor and major lengths of the rectangle fitting
around each bacterium, aiding in determining their orientation. It removes bacteria touching the frame's
border. The segmentation output is saved in both black and white (as a TIFF file) and in color (with each
bacterium in a different color, in TIFF format and as an array in an NPY file). The tracking output is also
stored as a TIFF image.</n></n></n>


<b><i>SuperSegger-o-modified.zip:</b></i> Removes bacteria that touch the page border. The segmentation output is
stored in black and white (BW) as a TIFF file and in color (each bacterium in a unique color) as a .mat file.
Rename files: For image input into DeLTA or SS, a specific pattern is required. These scripts adjust the
file names of raw images to align with the desired pattern for these tools, enabling their use in DeLTA
and SS.</n></n></n>


<b><i>CP-omnipose & CP- post-processing:</b></i> This suite of tools reads and post-processes
output from the CP tool. It assigns a fixed ID to each bacterium for its entire lifespan and labels each
family tree. It calculates metrics like birth_length, AverageLength, LifeHistory, GrowthRate, and
AverageOrientation throughout their life histories, counts divisions in family trees, and reports number
of bacteria at each time step.</n></n></n>


<b><i>Other specific package processing:</b></i> These scripts process output from each tool, conducting postprocessing and gathering data about each bacterium over time lapse. They assign consistent IDs to
bacteria and label family trees. They then calculate parameters such as birth_length, AverageLength,
LifeHistory, GrowthRate, and AverageOrientation over their life histories, alongside counting divisions in
family trees and reporting bacterial counts at each time step.
