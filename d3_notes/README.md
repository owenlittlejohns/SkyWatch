# Notes on learning D3 (and related Javascript)

Subdirectory containing examples of annotated code and notes on using D3.

#
# d3_example1.html

Taken directly from the first example on the D3 website. An annotated version of the necassary HTML and Javascript to produce a bar chart.

Structure:

* Define characteristics, such as the bar colours and sizes (```.chart``` must be the name of a type of D3 class - the one you are using).
* Get the D3 Javascript, this file links to an online version, but it can be local.
* Define data in a variable
* Define the range of the x-axis and the physical size of the plot: ```d3.scale.linear()```
* Choose type of D3 class (chart), and add the data to the plot.
