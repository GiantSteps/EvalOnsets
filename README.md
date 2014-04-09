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


Eclipse Instructions
---------------------------
1. Install PyDev
 * http://pydev.org/manual_101_install.html
 * You may need to install Oracle Java (http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
 * Then set Java -> Installed JREs -> to Java SE 8
 * Restart and in Preferences you should now have PyDev appearing
  * Set Interpreters > Python Interpreter to "/usr/local/bin/python" or whatever
2. Go to Eclipse Marketplace
 * Install EGit
3. Pull down code
 * Go to File -> Import 
 * Select "Projects from Git"
 * Clone URI "https://github.com/GiantSteps/EvalOnsets"
 * Import existing project to your workspace destination
 
Make sure to set the "src" directory as the PYTHONPATH to detect the packages.


libraries needed:
------------

* essentia
* signal
* sklearn
* scypi
* matplotlib
* modal (https://github.com/johnglover/modal)


optional
------------
*opencv
