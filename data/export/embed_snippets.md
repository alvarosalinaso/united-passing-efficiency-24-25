# Embed Snippets - Visualizaciones United Passing 24-25

## Datawrapper Benchmark (Métricas de Pase)

```html
<div style="width:100%; max-width:800px; margin:0 auto;">
  <iframe
    title="Manchester United vs PL Average - Passing Metrics"
    aria-label="Bar Chart"
    src="https://datawrapper.dwcdn.net/CHART_ID/"
    loading="lazy"
    style="width:100%; border:none; height:400px;"
  ></iframe>
</div>
<noscript>
  <p>Ver <a href="data/export/dw_benchmark_passing.csv">dw_benchmark_passing.csv</a> para los datos.</p>
</noscript>
```

## Flourish Network Graph (Conexiones entre Jugadores)

```html
<div style="width:100%; max-width:900px; margin:0 auto;">
  <iframe
    title="Red de Pases - Manchester United"
    aria-label="Network Graph"
    src="https://public.flourish.studio/visualisation/CHART_ID/"
    loading="lazy"
    style="width:100%; border:none; height:500px;"
  ></iframe>
</div>
<noscript>
  <p>Ver <a href="data/export/flourish_network_pases.csv">flourish_network_pases.csv</a> para los datos.</p>
</noscript>
```

## Observable Scatter (Centralidad vs Precisión)

```html
<div style="width:100%; max-width:800px; margin:0 auto;">
  <div id="observable-chart"></div>
  <script type="module">
    import {Plot} from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/+esm";
    import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";

    const data = await d3.csv("data/export/observable_centralidad.csv");
    const chart = Plot.plot({
      marks: [
        Plot.dot(data, {
          x: "betweenness",
          y: "pass_accuracy",
          fill: "position",
          r: 4,
          title: d => `${d.Player}\nBetweenness: ${d.betweenness}\nAccuracy: ${d.pass_accuracy}%`
        }),
        Plot.linearRegressionY(data, {x: "betweenness", y: "pass_accuracy", stroke: "red", strokeWidth: 1.5})
      ],
      x: {label: "Betweenness Centrality →", grid: true},
      y: {label: "Pass Accuracy (%) →", grid: true},
      color: {legend: true},
      width: 700,
      height: 450,
      marginBottom: 50,
      marginLeft: 60
    });
    document.getElementById("observable-chart").appendChild(chart);
  </script>
</div>
<noscript>
  <p>Ver <a href="data/export/observable_centralidad.csv">observable_centralidad.csv</a> para los datos.</p>
</noscript>
```
