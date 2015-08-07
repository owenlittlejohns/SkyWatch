<!-- Define some data in a variable -->
        var data = [4, 8, 15, 16, 23, 42];

<!-- Work out the domain (data range) and the range (physical size) and scaling between the two -->
        var x = d3.scale.linear()
          .domain([0, d3.max(data)])
          .range([0, 420]);

<!-- Select chart container - using class selector -->
        d3.select(".chart")
<!-- Initiate data - by defining selection to which date will be joined -->
<!-- This is in the all to select, so imagine it is chart.selectAll("div") -->
         .selectAll("div")
<!-- Join the data, again imagine chart.date(data) -->
         .data(data)
<!-- Update the data by using the chart.enter().append("div") command -->
         .enter().append("div")
<!-- Set the widths of each new bar, using the data, d -->
         .style("width", function(d) { return x(d) + "px"; })
<!-- Label each bar with the value -->
          .text(function(d) { return d; });
<!--      </div>-->