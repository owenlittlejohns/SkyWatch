// JavaScript to generate a scatter plot (eventually)
// Define some data
var xyData = [{x: 1, y: 1}, {x: 2, y: 2}, {x: 3, y: 3}, {x: 4, y: 4}];

// Set up the canvas parameters

var canvasMargin = {top: 30, right: 20, bottom: 50, left: 50};
var outerWidth = 500;
var outerHeight = 500;
var innerWidth = outerWidth - canvasMargin["left"] - canvasMargin["right"];
var innerHeight = outerHeight - canvasMargin["top"] - canvasMargin["bottom"];

// Set up the axes scales

var xScale = d3.scale.linear()
    .domain([0, 5])
    .range([0, innerWidth]);

var yScale = d3.scale.linear()
    .domain([5, 0])
    .range([0, innerHeight]);

var xAxis = d3.svg.axis()
    .scale(xScale)
    .ticks(3)
    .orient('bottom');

var yAxis = d3.svg.axis()
    .scale(yScale)
    .ticks(3)
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
    .attr('y', innerHeight - 5)
    .attr('text-anchor', 'middle')
    .attr('stroke', '#000000')
    .attr('stoke-width', 0.25)
    .text('x-axis title (units)');

// y-axis
canvas.append('g')
    .attr('class', 'y axis')
    .attr('transform', 'translate(' + canvasMargin["left"] + ',' + -canvasMargin["bottom"] + ')')
    .call(yAxis);

//y-axis label
/* Note - with the rotation in place, the x and y must be swapped around.
 Also the values are negative what is expected.
*/
canvas.append('text')
    .attr('class', 'axis label')
    .attr('y', -(canvasMargin["top"] + (innerHeight / 2)))
    .attr('x', canvasMargin["left"] - 6)
    .attr('transform', 'rotate(-90)') // make text sideways
    .attr('text-anchor', 'middle')
    .text('y-axis title (units)');

console.log("lalal");
/*

var canvas.append('g')
    .attr('transform', 'translate(' + margin['left'] + ',' + margin['top'] + ')'
);

// Temporary border
 var borderPath = canvas.append('rect')
  .attr('x', 0)
  .attr('y', 0)
  .attr('height', canvasWidth)
  .attr('width', canvasHeight)
  .style('stroke', 'black')
  .style('fill', 'black')
  .style('stroke-width', 5);

// Initiate data - by defining selection to which date will be joined
// This is in the all to select, so imagine it is chart.selectAll("div")
var points = canvas
// Use the empty
    .selectAll('circle')
// Join the data, again imagine chart.date(data)
    .data(xy_data)
// Update the data by using the chart.enter().append() command
    .enter().append("circle")
// Set the position of each new point, using the data, d
    .attr("cx", function(d) { return xScale(d["x"]); })
    .attr("cy", function(d) { return yScale(d["y"]); })
// Make the circle 4 pixels in radius and specify colour:
    .attr("r", 4)
    .attr("fill", "#FF6766");

*/