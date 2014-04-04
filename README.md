README
======
Python packages for audio onset detection Evaluation

Structure
---------
* Predict : global package to generate pool and onsets text files
* OnsetNovelty : package grouping multiple onset novelty functions
* Slice : package grouping multiple multidimensionnal "peak-picking" algorithms
* Eval : statistical tools for evaluating onsets prediction vs ground-truth



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
