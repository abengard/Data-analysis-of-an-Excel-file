# Data analysis of an Excel file

## What does the code do?

The code analyzes an .xlsx file (Excel) with over 3000 data sets of wind turbines in Schleswig-Holstein (Germany). These data sets are visualized as plots and on the map. 

I recommend using the Python-Code in the Spyder IDE.


## Quick Guide 

When you start the Python-Code "Data_analysis-Tool.py", the following dialog window opens in the background. Select the .xlsx file "Dataset-Wind-turbine".

<img src="https://github.com/abengard/Data-analysis-of-wind-turbines/blob/main/Image/Dialog%20box.jpg" width="400">

Now the program evaluates the complete Excel file in the background. Above the console the plots are visualized (see picture). At the same time the plots are merged into a PDF. Also a map (.html file) with ONE wind turbine is created here. 

The PDF file and the map are then stored in the same folder where the Python code is located.

<img src="https://github.com/abengard/Data-analysis-of-wind-turbines/blob/main/Image/Plots.jpg" width="400">

To visualize all wind turbines on the map, I have separately created a Python code (map_cluster_LayerControl.py). In the upper right corner, different settings that control the visualization can be set. By zooming into the map, the cluster splits in the further. The individual icons are also clickable.

The following result is then ejected:


<img src="https://github.com/abengard/Data-analysis-of-wind-turbines/blob/main/Image/Map.jpg" width="700">


To better understand the Python-Code I have uploaded a program flowchart (PAP_data_analysis-tool.pdf).
