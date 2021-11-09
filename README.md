# Cheeky Monkey
> Summary description here.


This file will become your README and also the index of your documentation.

## Install

`pip install cheeky_monkey`

## How to use

Fill me in please! Don't forget code examples:

```
1+1
```




    2



```

source = pd.DataFrame({
    'a': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
    'b': [28, 55, 43, 91, 81, 53, 19, 87, 52]
})

alt.Chart(source).mark_bar().encode(
    x='a',
    y='b'
)
```





<div id="altair-viz-ef2aab06ba6145e2bbeb6e2f3c9d38a3"></div>
<script type="text/javascript">
  (function(spec, embedOpt){
    let outputDiv = document.currentScript.previousElementSibling;
    if (outputDiv.id !== "altair-viz-ef2aab06ba6145e2bbeb6e2f3c9d38a3") {
      outputDiv = document.getElementById("altair-viz-ef2aab06ba6145e2bbeb6e2f3c9d38a3");
    }
    const paths = {
      "vega": "https://cdn.jsdelivr.net/npm//vega@5?noext",
      "vega-lib": "https://cdn.jsdelivr.net/npm//vega-lib?noext",
      "vega-lite": "https://cdn.jsdelivr.net/npm//vega-lite@4.8.1?noext",
      "vega-embed": "https://cdn.jsdelivr.net/npm//vega-embed@6?noext",
    };

    function loadScript(lib) {
      return new Promise(function(resolve, reject) {
        var s = document.createElement('script');
        s.src = paths[lib];
        s.async = true;
        s.onload = () => resolve(paths[lib]);
        s.onerror = () => reject(`Error loading script: ${paths[lib]}`);
        document.getElementsByTagName("head")[0].appendChild(s);
      });
    }

    function showError(err) {
      outputDiv.innerHTML = `<div class="error" style="color:red;">${err}</div>`;
      throw err;
    }

    function displayChart(vegaEmbed) {
      vegaEmbed(outputDiv, spec, embedOpt)
        .catch(err => showError(`Javascript Error: ${err.message}<br>This usually means there's a typo in your chart specification. See the javascript console for the full traceback.`));
    }

    if(typeof define === "function" && define.amd) {
      requirejs.config({paths});
      require(["vega-embed"], displayChart, err => showError(`Error loading script: ${err.message}`));
    } else if (typeof vegaEmbed === "function") {
      displayChart(vegaEmbed);
    } else {
      loadScript("vega")
        .then(() => loadScript("vega-lite"))
        .then(() => loadScript("vega-embed"))
        .catch(showError)
        .then(() => displayChart(vegaEmbed));
    }
  })({"config": {"view": {"continuousWidth": 400, "continuousHeight": 300}}, "data": {"name": "data-c2a3e89ba9d5d1687d5e8c28d630a033"}, "mark": "bar", "encoding": {"x": {"type": "nominal", "field": "a"}, "y": {"type": "quantitative", "field": "b"}}, "$schema": "https://vega.github.io/schema/vega-lite/v4.8.1.json", "datasets": {"data-c2a3e89ba9d5d1687d5e8c28d630a033": [{"a": "A", "b": 28}, {"a": "B", "b": 55}, {"a": "C", "b": 43}, {"a": "D", "b": 91}, {"a": "E", "b": 81}, {"a": "F", "b": 53}, {"a": "G", "b": 19}, {"a": "H", "b": 87}, {"a": "I", "b": 52}]}}, {"mode": "vega-lite"});
</script>


