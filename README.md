# Elagage2D

This repository show preliminary work on how to detect that there are large vegetation around power lines.
Two type of methods can be used to address this task, One using 2d data and other using 3d data.

The one using 3d data promises to give better results than the first one but need more data and a 3d data whis is difficult to get.

## 2D methods

### First
In this repositories we show some results using the first method (using 2d data).

The main assumption for this method is that the electrical lines are very bright(and are straight lines) and when there are large vegetation around or over them this luminosity decreases.

What we do first is to convert the picture in grayscale picture (this quantifies the luminosity)and try to find a line using OTSU and Hough Line Transform method.

After that if we detect interuption in the line found, we decide that there are a large vegetation around this interuption.

### Second
Do the same thing as before but using a deep neural network to detect the line.

## 3D methods
The 3d method just classify each point of the data as vegetation, line or another class. After if there is a 


Look at:
https://github.com/R3ab/ttpla_dataset
https://github.com/bbenligiray/power-line-recognition
