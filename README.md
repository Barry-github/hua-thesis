1)install conda
    a) install anaconda Linux installer --> https://www.anaconda.com/download/#linux
    b) bash Anaconda-latest-Linux-x86_64.sh
    c) in a terminal run "conda update conda" (if needed)
    d) test your installation with command "conda list" *
        * in some cases you must activate first your base environment <source "path to anaconda dir"/bin/source activate base>

2)install requirements and conda environment
-conda env create -f environment.yml

3)activate conda environment
- source "path to anaconda dir"/bin/source activate "name of env" example source ~/anaconda/bin/activate gendis_test

4)run (from activated environment) gendis_test.py for detailed multiple experiments or

5)run jupyter notebook (from activated environment) and open gendis_test.ipynb for one experiment 

