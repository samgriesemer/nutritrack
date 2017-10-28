var margin = {top: 30, right: 30, bottom: 30, left: 30},
    width = d3.max([300,window.innerWidth/4]) - margin.left - margin.right,
    height = 200 - margin.top - margin.bottom,
    full_width = width + margin.left + margin.right,
    full_height = height + margin.top + margin.bottom;
    
var material = ['#F44336','#E91E63','#9C27B0','#673AB7','#3F51B5','#2196F3','#03A9F4','#00BCD4','#009688','#4CAF50','#8BC34A','#CDDC39','#FFEB3B','#FFC107','#FF9800','#FF5722','#795548','#9E9E9E','#607D8B','#000000'],
    material = ['#d1e4f1', '#13466b', '#f7f00a', '#e01c49', '#facc05'],
    //material = ['#F7F00A', '#EA638C', '#B33C86', '#190E4F', '#00000'],
    //material = ['#d1e4f1', '#FFD23F', '#EE4266', '#540D6E'],
    material = ['#d1e4f1', '#f7f00a', '#EE4266', '#540D6E'],
    mat = d3.scaleOrdinal(material);

var format = d3.format(',d');

var div = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("display", "none");

function mouseover() {
    div.style("display", "inline");
}

function mouseout() {
    div.style("display", "none");
}

(function() { // wrapper to avoid variable override between files

// generate random data
data = [];
for (var i=0; i<3; i++) {
  sample = [];
  for (var j=0; j<20; j++) {
    sample.push({'x':j, 'y':d3.randomNormal(0,1)()});
  }
  data.push({'id':i, 'values':sample})
}

// d3
var svg_line = d3.select("#calorie")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom),
    g = svg_line.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var x = d3.scaleLinear()
  .domain([
    d3.min(data, function(c) { return d3.min(c.values, function(d) { return d.x; }); }),
    d3.max(data, function(c) { return d3.max(c.values, function(d) { return d.x; }); })
  ])
  .range([0,width]);

var y = d3.scaleLinear()
  .domain([
    d3.min(data, function(c) { return d3.min(c.values, function(d) { return d.y; }); }),
    d3.max(data, function(c) { return d3.max(c.values, function(d) { return d.y; }); })
  ])
  .range([height,0]);

// define line
var line = d3.line()
    .defined(function(d) { return d; })
    .curve(d3.curveBasis)
    .x(function(d) { return x(d.x); })
    .y(function(d) { return y(d.y); });

g.append("g")
  .attr("class", "x-axis")
  .attr("transform", "translate(0," + height + ")")
  .call(d3.axisBottom(x));

g.append("g")
  .attr("class", "y-axis")
  .attr("transform", "translate(0," + 0 + ")")
  .call(d3.axisLeft(y));

series = g.selectAll('.series')
  .data(data)
  .enter().append('g')
    .attr('class', 'series')

series.append('path')
  .attr('class', 'line')
  .attr('fill', 'none')
  .attr('stroke', function(d) { return mat(d.id); })
  .attr('stroke-width', '1.5px')
  .attr('d', function(d) { return line(d.values) });

})();
