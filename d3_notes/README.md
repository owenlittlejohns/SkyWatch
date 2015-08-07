# Notes on learning D3 (and related Javascript)

Subdirectory containing examples of annotated code and notes on using D3.

#
# d3_example1.html:

An HTML page containing the basic structure to have:

* CSS imported from `main.css` and `plot.css`.
* Plotting JavaScript imported from `d3_example1.js`.

#
# d3_example.js

A JavaScript file containing the script to produce the displayed figure. The primary goal for this is to produce a figure containing:

* A scatter plot.
* Buttons to produce additional lines.
* Text about the data point that appears when the mouse hovers over the point.
* A legend (ultimately that appears upon mouse hover over button).
* Horizontal line, thicker main lines and dimmer others appear on mouse hover over button.

#
# main.css:

A file containing CSS styling for standard HTML tags, such as `<p>` and `<h1>`.

#
# plot.css:

A file containing CSS styling specifically for the d3 plot object.

Structure:

* Define characteristics, such as the bar colours and sizes (```.chart``` must be the name of a type of D3 class - the one you are using).
* Get the D3 Javascript, this file links to an online version, but it can be local.
* Define data in a variable
* Define the range of the x-axis and the physical size of the plot: ```d3.scale.linear()```
* Choose type of D3 class (chart), and add the data to the plot.
