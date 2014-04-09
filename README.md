README
======
Python packages for audio onset detection Evaluation

Structure
---------
In the "src" dir the tool is organised into python packages as followed:-

* Eval : statistical tools for evaluating onsets prediction vs ground-truth
* Predict : global package to generate pool and onsets text files
	* OnsetNovelty : package grouping multiple onset novelty functions
	* Slice : package grouping multiple multidimensional "peak-picking" algorithms
* Utils : common routines and functions for dealing with files and the environment.

conf.py at the top level holds environment specific things - customise this for your setup.


How-To
---------
Specify folders in conf.py

for already computed onset textfiles : run Eval/\_\_init\_\_.py

for computing : specify desired methods in OnsetNovelty's and Slice's \_\_init\_\_.py then run Predict's init.py

you can use last computation using pool cache (basicaly set fromFile=true in config.py)

Make sure to set the "src" directory as the PYTHONPATH to detect the packages.


librairies needed:
------------

* essentia
* signal
* sklearn
* scypi
* matplotlib


optional
------------
*opencv
