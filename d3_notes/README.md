# Notes on learning D3 (and related Javascript)

Subdirectory containing examples of annotated code and notes on using D3.

#
# d3_example1.html:

An HTML page containing the basic structure to have:

* CSS imported from `main.css` and `plot.css`.
* Plotting JavaScript imported from `d3_example1.js`.

#
# d3_example.js

A JavaScript file containing the script to produce the displayed figure. This figure currently contains:

* An SVG container.
* Axes, with labels.
* Grid lines.
* x and y data points.
* A line interpolated between the points (`cardinal` to make it smoother).
* Changing colour of points on mouse hover (and changing back when not).

Remaining changes:

* A tooltip containing text on mouse hover.
* Multiple data sets.
* Buttons to control multiple data sets:
* Clicking on the buttons toggles data sets on and off.
* Buttons above the plot area that upon a mouse hover:
** Make other data sets fade.
** Makes specific dataset thicker.
** Plot other lines (temporarily).
** Bring up a legend (with a position dependent on whether there are data in the top right corner).


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
