// JavaScript to generate a scatter plot (eventually)
// Define some data
var xyData = [{x: 0.5, y: 5}, {x: 1, y: 4.5}, {x: 1.25, y: 4}, {x: 1.5, y: 3}, {x: 1.75, y: 2}, {x: 2, y: 1}, {x: 2.5, y: 0.5}, {x: 3, y: 0.25}, {x: 3.5, y: 0.5}, {x: 4, y: 1}, {x: 4.25, y: 2}, {x: 4.5, y: 3}, {x: 4.75, y: 4}, {x: 5, y: 4.5}];

var xyData2 = [{x: 0.5, y: 1}, {x: 1, y: 1.5}, {x: 1.25, y: 2}, {x: 1.5, y: 3}, {x: 1.75, y: 4}, {x: 2, y: 4.5}, {x: 2.5, y: 4.75}, {x: 3, y: 5}, {x: 3.5, y: 4.75}, {x: 4, y: 4.5}, {x: 4.25, y: 4}, {x: 4.5, y: 3}, {x: 4.75, y: 2}, {x: 5, y: 1.5}];

// Set up the data set colours:
var dataColours = ['#FF6766', '#66FFAA'];
var data = [xyData, xyData2];
var onColours = ['#66FFAA', '#FF6766'];
var offColours = ['#FF6766', '#66FFAA'];
var legendPositions = [true, false];

// Set up the canvas parameters

var canvasMargin = {top: 50, right: 20, bottom: 50, left: 50};
var outerWidth = 500;
var outerHeight = 500;
var innerWidth = outerWidth - canvasMargin["left"] - canvasMargin["right"];
var innerHeight = outerHeight - canvasMargin["top"] - canvasMargin["bottom"];
var axisHeight = innerHeight - canvasMargin["bottom"] - canvasMargin["top"]

// Set up legend parameters

// Function to create legend object

var createLegend = function(legendPosition) {
    // Set up line properties for each legend line
    var legendColours = ['#67FF66', '#FF6766', '#6766FF']
    var legendText = ['Selected data', 'Not selected data', 'Line']
    var legendLineOpacity = [1.0, 1.0, 0.5];
    var legendLineThickness = [4, 4, 2];
    var legendLineLength = 25; // this is the same for all
    // Set up spacing and element height
    var legendElementSizeY = 18;
    var legendSpacingY = 2;
    var legendSpacingX = 4;
    // Initialise the legend
    var legend = canvas.selectAll('.legend')
	.data(legendColours) // colours (I think)
	.enter()
	.append('g')
	.attr('class', 'legend')
	.attr('transform', function(d, i) {
	/* The coordinates of the top left of the legend are encoded here as:
	   horiz (x) and offset (y)
	   Each element is moved apart from the last using height and i.
	*/
	    var height = legendElementSizeY + legendSpacingY;
	    if (legendPosition == true) {
		var offset = innerHeight / 30 + canvasMargin["top"];
	    } else {
		var offset = canvasMargin["top"] + 5 * innerHeight / 9;
	    }
	    var horz = innerWidth - canvasMargin["right"] - innerWidth / 5.5;
	    var vert = i * height + offset;
	    return 'translate(' + horz + ',' + vert + ')';
	});

    // Append lines (although cheat and make them using rectangles):
    legend.append('rect')
    // Position each line vertically centred varying on line thickness
	.attr('y', function(d, i) {
	    return (legendSpacingY + legendElementSizeY - legendLineThickness[i]) / 2;
	})
	.attr('width', legendLineLength)
	.attr('height', function(d, i) {return legendLineThickness[i]; })
	.style('fill', function(d, i) {return legendColours[i]; })
	.style('stroke', "none")
	.attr('opacity', function(d, i) {return legendLineOpacity[i]; });

    // Add legend text
    legend.append('text')
	.attr('x', legendLineLength + legendSpacingX)
	.attr('y', legendElementSizeY - legendSpacingY)
	.attr('font-size', 14)
	.text(function(d, i) {return legendText[i];} );
};

// Function to remove legend on mouseout:
var destroyLegend = function() {
    d3.selectAll('.legend').remove();
};

// Set up the axes scales

var xScale = d3.scale.linear()
    .domain([0, 5])
    .range([0, innerWidth]);

var yScale = d3.scale.linear()
    .domain([5, 0])
    .range([0, axisHeight]);

var xAxis = d3.svg.axis()
    .scale(xScale)
    .ticks(5)
    .orient('bottom');

var yAxis = d3.svg.axis()
    .scale(yScale)
    .ticks(5)
    .orient('left');

// Select chart container - using class selector
var canvas = d3.select('.chart')
    .append('svg')
    .attr('width', outerWidth)
    .attr('height', outerHeight);

// Add the grid lines (horizontal)
canvas.selectAll('line.horizontalGrid').data(yScale.ticks(10)).enter()
    .append('line')
    .attr('transform', 'translate(' + canvasMargin["left"] + ',' + canvasMargin["top"] + ')')
    .attr({
	'class': 'horizontalGrid',
	'x1': 0,
	'x2': innerWidth,
	'y1': function(d) { return yScale(d); },
	'y2':function(d) { return yScale(d); },
	'fill': 'none',
	'shape-rendering': 'crispEdges',
	'stroke': 'rgba(180, 180, 180, 0.2)',
	'stroke-width': '1px'
    });

// Add some vertical grid lines (to practice some more)
canvas.selectAll('line.verticalGrid').data(xScale.ticks(10)).enter()
    .append('line')
    .attr('transform', 'translate(' + canvasMargin["left"] + ',' + canvasMargin["top"] + ')')
    .attr({
	'class': 'verticalGrid',
	'x1': function(d) { return xScale(d); },
	'x2':function(d) { return xScale(d); },
	'y1': 0,
	'y2': axisHeight,
	'fill': 'none',
	'shape-rendering': 'crispEdges',
	'stroke': 'rgba(180, 180, 180, 0.2)',
	'stroke-width': '1px'
    });

// x-axis
/* Note - the translate string is really choosey:
   ensure the expression is in parentheses */
canvas.append('g')
    .attr('class', 'x axis')
    .attr('transform', 'translate(' + canvasMargin["left"] + ',' + (innerHeight - canvasMargin["bottom"]) + ')')
    .call(xAxis);

// x-axis title
canvas.append('text')
    .attr('class', 'axis label')
    .attr('x', canvasMargin["left"] + innerWidth - innerWidth / 2)
    .attr('y', innerHeight)
    .attr('fill', 'black')
    .attr('text-anchor', 'middle')
    .text('x-axis title (units)');

// y-axis
canvas.append('g')
    .attr('class', 'y axis')
    .attr('transform', 'translate(' + canvasMargin["left"] + ',' + canvasMargin["top"] + ')')
    .call(yAxis);

//y-axis label
/* Note - with the rotation in place, the x and y must be swapped around.
Also - the shifting of the y axis up and down is counterintuitive*/
canvas.append('text')
    .attr('class', 'axis label')
    .attr('y', canvasMargin["left"] - 30)
    .attr('x', canvasMargin["top"] / 2 - innerHeight / 2)
    .attr('transform', 'rotate(270)') // make text sideways
    .attr('text-anchor', 'middle')
    .text('y-axis title (units)');


// Create the function ready to draw the line:
/* Other interpolation options include 'linear'*/
var lineFunction = d3.svg.line()
    .interpolate('cardinal') // This makes the interpolation curved
    .x(function(d) { return xScale(d.x); })
    .y(function(d) { return yScale(d.y); });

// Plot the line (append to "path")
var lineTrack = canvas.append('path')
    .attr('transform', 'translate(' + canvasMargin["left"] + ',' + canvasMargin["top"] + ')')
    .attr('d', lineFunction(data[0]))
    .attr('stroke', '#6766FF')
    .attr('stroke-width', 2)
    .attr('fill', 'none');

/* Initiate data - by defining selection to which date will be joined
   This is in the all to select, so imagine it is chart.selectAll("div")
   To get data points behind the line, do this before the line things above.
*/

var drawCircles = function(data, index, className) {
    var points = canvas
    // Use the empty
	.selectAll(className)
    // Join the data, again imagine chart.date(data)
	.data(data[index])
    // Update the data by using the chart.enter().append() command
	.enter().append("circle")
    // Account for translation to actual place on SVG canvas:
	.attr('transform', 'translate(' + canvasMargin["left"] + ',' + canvasMargin["top"] + ')')
    // Set the position of each new point, using the data, d
	.attr("cx", function(d) { return xScale(d["x"]); })
	.attr("cy", function(d) { return yScale(d["y"]); })
    // Make the circle 4 pixels in radius and specify colour:
	.attr("r", 4)
	.attr("fill", dataColours[index])
// Add rules for what happens when the mouse hovers over the point (and then leaves)
    points.on("mouseover", function(d) {
	d3.select(this).attr("r", 4).style("fill", onColours[index]);
	createLegend(legendPositions[index]);
    });                  
    points.on("mouseout", function(d) {
	d3.select(this).attr("r", 4).style("fill", offColours[index]);
	destroyLegend();
    });
    return points;
};

var firstDataPoints = drawCircles(data, 0, 'firstDataPoints');
var secondDataPoints = drawCircles(data, 1, 'secondDataPoints');

// Make a box for each set of points