---
layout: default
title: Baseline
nav_order: 3
has_children: false
permalink: docs/Baseline
---

Árbol de Decisión

<script src="https://d3js.org/d3.v6.min.js"></script>

<script>
d3.csv("https://gist.githubusercontent.com/d3noob/fa0f16e271cb191ae85f/raw/bf896176236341f56a55b36c8fc40e32c73051ad/treedata.csv", function(data){
    console.log(data);
    var parsedCSV = d3.csvParseRows(data);
});
</script>