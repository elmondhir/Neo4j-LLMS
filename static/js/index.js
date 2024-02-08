    // JavaScript code for rendering the directed graph using D3.js
    var width = 600;
    var height = 600;

    var nodes = JSON.parse(document.getElementById('mynodes').textContent);
    var links = JSON.parse(document.getElementById('myrels').textContent);
    var labels = JSON.parse(document.getElementById('mylables').textContent);

    // var colorScale = d3.scaleOrdinal()
    // .domain(Array.from(colors))
    // .range(d3.schemeCategory10);
    // console.log(colorScale);

    var svg = d3
  .select("svg")
  .attr("width", width)
  .attr("height", height)
  .call(d3.zoom().on("zoom", function () {
       svg.attr("transform", d3.event.transform)
    }));

    
var linkSelection = svg
  .selectAll("line")
  .data(links)
  .enter()
  .append("line")
  .attr("stroke", "black")
  .attr("stroke-width", 1);

var myColor = d3.scaleSequential().domain([1,10])
  .interpolator(d3.interpolateViridis)

var colorScale = d3.scaleOrdinal(d3.schemeCategory10).domain(labels);

var nodeSelection = svg
  .selectAll("circle")
  .data(nodes)
  .enter()
  .append("circle")
  .attr("r", 15)
  .attr("fill", function(d){
    return colorScale(d.labels[0]) }) // Use the color scale (only works with one node label)
  // .attr("fill", "red")
  .call(
    d3
      .drag()
      .on("start", dragStart)
      .on("drag", drag)
      .on("end", dragEnd)
  );

  var labelSelection = svg
  .selectAll("text")
  .data(nodes)
  .enter()
  .append("text")
  .text(d => { 
    // console.log(d.properties.name);
    return d.properties.name || d.properties.title || d.id})  // Adjust this line based on your node data structure
  .attr("x", d => d.x)
  .attr("y", d => d.y)
  .attr("dy", -15)

// add legend

// Add legend using HTML and CSS for absolute positioning
var legendContainer = d3.select("#graph-container") // Assuming the ID of your graph container is "graph-container"
    .append("div")
    .attr("id", "legend-container")
    .style("position", "absolute")
    .style("top", "10px")
    .style("left", "10px");

legendContainer.selectAll("mylabels")
    .data(labels)
    .enter()
    .append("div")
    .style("display", "flex")
    .style("align-items", "center")
    .html(function (d) {
        return '<svg width="10" height="10" style="margin-right: 5px;"><circle cx="5" cy="5" r="5" fill="' + colorScale(d) + '"/></svg>' + d;
    });

var simulation = d3.forceSimulation(nodes);

function boundForce(width, height) {
  const padding = 10; // Adjust the padding as needed

  function force(alpha) {
    nodes.forEach(d => {
      d.x = Math.max(padding, Math.min(width - padding, d.x));
      d.y = Math.max(padding, Math.min(height - padding, d.y));
    });
  }

  return force;
}

simulation
  .force("center", d3.forceCenter(width / 2, height / 2))
  .force("nodes", d3.forceManyBody())
  .force(
    "links",
    d3
      .forceLink(links)
      .id(d => d.id)
      .distance(d => 100)
  )
  .force("bounds", boundForce(width, height))  // Add bounding force
  .on("tick", ticked);

function ticked() {

  nodeSelection.attr("cx", d => d.x).attr("cy", d => d.y);

  linkSelection
    .attr("x1", d => d.source.x)
    .attr("y1", d => d.source.y)
    .attr("x2", d => d.target.x)
    .attr("y2", d => d.target.y);
    
    labelSelection
        .attr("x", d => d.x + 10)  // Adjust the positioning for better visibility
        .attr("y", d => d.y - 10);  // Adjust the positioning for better visibility
}

function dragStart(d) {

  simulation.alphaTarget(0.5).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function drag(d) {
  // console.log('dragging');
  // simulation.alpha(0.5).restart()
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragEnd(d) {
  // console.log('drag end');
  simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}
