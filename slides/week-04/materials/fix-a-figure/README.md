# Fixing a figure (more practice)

`broken-figure.png` shows the event rate by arm from `figure-source.csv`, drawn by
`plot_figure.py`. It has three problems. Synthetic data.

1. `git init && git add -A && git commit -m start`, then look at the PNG and the CSV.
   Write down what is wrong before asking the agent.
2. `opencode`: "Compare broken-figure.png with figure-source.csv and plot_figure.py.
   List every way the figure misrepresents the data: scale, denominator, labels. Do not
   change anything yet."
3. Compare its list with yours. Then: "Fix plot_figure.py for the problems we agree on.
   Write the plotted values to figure-values.csv, rerun, and open the new PNG."
4. Check every plotted value against the CSV yourself, with a calculator.
