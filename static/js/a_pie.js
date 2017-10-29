// global D3 variables
var margin = {top: 30, right: 80, bottom: 30, left: 30},
    width = d3.max([200,window.innerWidth/4]) - margin.left - margin.right,
    height = 200 - margin.top - margin.bottom,
    full_width = width + margin.left + margin.right,
    full_height = height + margin.top + margin.bottom;
    
var material = ['#F44336','#E91E63','#9C27B0','#673AB7','#3F51B5','#2196F3','#03A9F4','#00BCD4','#009688','#4CAF50','#8BC34A','#CDDC39','#FFEB3B','#FFC107','#FF9800','#FF5722','#795548','#9E9E9E','#607D8B','#000000'],
    material = ['#d1e4f1', '#13466b', '#f7f00a', '#e01c49', '#facc05'],
    //material = ['#F7F00A', '#EA638C', '#B33C86', '#190E4F', '#00000'],
    //material = ['#d1e4f1', '#FFD23F', '#EE4266', '#540D6E'],
    material = ['#007bff', '#e9ecef', '#212529'],
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
var width = window.innerWidth/6 - margin.left - margin.right,
height = 160 - margin.top - margin.bottom,
full_width = width + margin.left + margin.right,
full_height = height + margin.top + margin.bottom;

// generate random data
function generate() {
  var tags = ['Vitamin A', 'Vitamin C', 'Iron'];
  return tags.map(function(d) {
    return {
      'nutrient': d,
      'count' : d3.randomUniform(0,10)()
    }
  });
}

// d3
var svg = d3.select("#a_pie")
    .attr("width", full_width)
    .attr("height", full_height),
    g = svg.append("g").attr("transform", "translate(" + full_width / 2 + "," + full_height / 2 + ")"),
    radius = height/2,
    data = generate();

var pie = d3.pie()
    .sort(null) // comment out for auto switching
    .value(function(d) { return d.count })

var arc = d3.arc()
    .outerRadius(radius)
    .innerRadius(radius/2);

/*var legend = svg.append("g")
    .style("font-family", "sans-serif")
    .attr("font-size", 10)
    .attr("text-anchor", "end")
    .attr("transform", function(d, i) { return "translate(" + (full_width/2+radius+40) + "," + (full_height/2-40) + ")"; })
    .selectAll("g")
    .data(pie(data))
        .enter().append("g")
        .attr("transform", function(d, i) { return "translate(0," + i*20 + ")"; });

legend.append("rect")
    .attr("x", 5)
    .attr("width", 15)
    .attr("height", 15)
    .attr("fill", function(d, i) { return mat(i); });

legend.append("text")
    .attr("x", radius*2.5-5)
    .attr("y", 7.5)
    .attr("dy", "0.32em")
    .text(function(d) { return d.data.nutrient; });*/

redraw(generate());

d3.interval(function() {
  redraw(generate());
}, 3000);
  
function redraw(data) {
  var arcs = g.selectAll('.arc')
      .data(pie(data), function(d) { return d.data.nutrient; });

  arcs.transition()
      .duration(1000)
      .delay(function(d, i) { return i*250; })
      .attrTween('d', arcTween)

  arcs.enter().append('path')
      .attr('class', 'arc')
      .attr('fill', function(d, i) { return mat(i); })
      .attr('d', arc)
      .each(function(d) { this._current = d; })
}

function arcTween(a) {
  //console.log(this._current);
  var i = d3.interpolate(this._current, a);
  this._current = i(0);
  return function(t) {
    return arc(i(t));
  };
}

})();