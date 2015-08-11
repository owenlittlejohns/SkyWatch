// JavaScript to generate a scatter plot (eventually)
// Define some data
var xyData = [{x: 0.5, y: 5}, {x: 1, y: 4.5}, {x: 1.25, y: 4}, {x: 1.5, y: 3}, {x: 1.75, y: 2}, {x: 2, y: 1}, {x: 2.5, y: 0.5}, {x: 3, y: 0.25}, {x: 3.5, y: 0.5}, {x: 4, y: 1}, {x: 4.25, y: 2}, {x: 4.5, y: 3}, {x: 4.75, y: 4}, {x: 5, y: 4.5}];

// Set up the canvas parameters

var canvasMargin = {top: 50, right: 20, bottom: 50, left: 50};
var outerWidth = 500;
var outerHeight = 500;
var innerWidth = outerWidth - canvasMargin["left"] - canvasMargin["right"];
var innerHeight = outerHeight - canvasMargin["top"] - canvasMargin["bottom"];
var axisHeight = innerHeight - canvasMargin["bottom"] - canvasMargin["top"]

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

// Add some vertical lines (to practice some more)
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

// Create the function ready to draw the line:
/* Other interpolation options include 'linear'*/
var lineFunction = d3.svg.line()
    .interpolate('cardinal') // This makes the interpolation curved
    .x(function(d) { return xScale(d.x); })
    .y(function(d) { return yScale(d.y); });

// Plot the line (append to "path")
var lineTrack = canvas.append('path')
    .attr('transform', 'translate(' + canvasMargin["left"] + ',' + canvasMargin["top"] + ')')
    .attr('d', lineFunction(xyData))
    .attr('stroke', '#6766FF')
    .attr('stroke-width', 2)
    .attr('fill', 'none');


// Initiate data - by defining selection to which date will be joined
// This is in the all to select, so imagine it is chart.selectAll("div")
var points = canvas
// Use the empty
    .selectAll('circle')
// Join the data, again imagine chart.date(data)
    .data(xyData)
// Update the data by using the chart.enter().append() command
    .enter().append("circle")
// Account for translation to actual place on SVG canvas:
    .attr('transform', 'translate(' + canvasMargin["left"] + ',' + canvasMargin["top"] + ')')
// Set the position of each new point, using the data, d
    .attr("cx", function(d) { return xScale(d["x"]); })
    .attr("cy", function(d) { return yScale(d["y"]); })
// Make the circle 4 pixels in radius and specify colour:
    .attr("r", 4)
    .attr("fill", "#FF6766")
    .on("mouseover", function(d) {
	d3.select(this).attr("r", 4).style("fill", "#67FF66");
    })                  
    .on("mouseout", function(d) {
	d3.select(this).attr("r", 4).style("fill", "#FF6766");
    });



/*
// Include the mouseover behaviour:
    .on("mouseover", function(d) {
	div.transition()
	    .duration(200) // duration for the transition in ms.
	    .style("opacity", 0.9);
	div .html("<strong>x: </strong>" + d.x + "<br><strong>y: </strong>" + d.y)
    })
    .on("mouseout", function(d) {
	div.transition()
	    .duration(500)
	    .style("opacity", 0);
    });
*/

/*
// Get tooltip text to pop up when the mouse hovers over a data point
var tip = d3.select().append("div")
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html( function(d) {
	return "<strong>x: </strong>" + d.x + "\n<strong>y: </strong>" + d.y;
    })

canvas.call(tip);*/