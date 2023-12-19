# Overview of Each Script:

<p align="justify"><b><i><a href="tracking-plotbac.py">tracking-plotbac.py</a>:</i></b> This script creates visualizations for the tracking output of various tools. You'll find
the resulting tracking plots in the specific folder for each tool under the analyses folder.</p></br>

<p align="justify"><b><i><a href="reference_BW_img.py">reference_BW_img.py</a>:</i></b> This script starts by retrieving the output file from LAbkit. It then identifies each
bacterium's pixels from the LAbkit output and displays them in black and white. This script is primarily
used for IOU (Intersection over Union) calculations.</p></br>

<p align="justify"><b><i><a href="jitter_remover.py">Jitter_remover.py</a>:</b></i> This scripts minimizes stage jitter effects.</p></br>


<p align="justify"><b><i><a href="DeLTA and SS-O modified code/delta_modified.zip">delta_modified.zip</a>:</b></i> The Delta output includes the minor and major lengths of the rectangle fitting
around each bacterium, aiding in determining their orientation. It removes bacteria touching the frame's
border. The segmentation output is saved in both black and white (as a TIFF file) and in color (with each
bacterium in a different color, in TIFF format and as an array in an NPY file). The tracking output is also
stored as a TIFF image.</p></br>


<p align="justify"><b><i><a href="https://github.com/Ati-74/supersegger-omnipose">SuperSegger-o-modified</a>:</b></i> Removes bacteria that touch the page border. The segmentation output is
stored in black and white (BW) as a TIFF file and in color (each bacterium in a unique color) as a .mat file.
Rename files: For image input into DeLTA or SS, a specific pattern is required. These scripts adjust the
file names of raw images to align with the desired pattern for these tools, enabling their use in DeLTA
and SS.</p></br>


<p align="justify"><b><i><a href="CP-omnipose & CP- post-processing/CP_Post_Processing">CP-omnipose & CP- post-processing</a>:</b></i> This suite of tools reads and post-processes
output from the CP tool. It assigns a fixed ID to each bacterium for its entire lifespan and labels each
family tree. It calculates metrics like birth_length, AverageLength, LifeHistory, GrowthRate, and
AverageOrientation throughout their life histories, counts divisions in family trees, and reports number
of bacteria at each time step.</p></br>


<p align="justify"><b><i>Other specific package processing:</b></i> These scripts process output from each tool, conducting postprocessing and gathering data about each bacterium over time lapse. They assign consistent IDs to
bacteria and label family trees. They then calculate parameters such as birth_length, AverageLength,
LifeHistory, GrowthRate, and AverageOrientation over their life histories, alongside counting divisions in
family trees and reporting bacterial counts at each time step.</p>
