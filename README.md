1)install conda
    a) install anaconda Linux installer --> https://www.anaconda.com/download/#linux
    b) bash Anaconda-latest-Linux-x86_64.sh
    c) in a terminal run "conda update conda" (if needed)
    d) test your installation with command "conda list" *
        * in some cases you must activate first your base environment <source "path to anaconda dir"/bin/source activate base>

2)install requirements and conda enviroment
- conda create --name generator_trajectories
- conda env update -f environment.yml

3)activate conda enviroment
- source "path to anaconda dir"/bin/source activate "name of env" example source ~/anaconda/bin/activate generator_trajectories

4)run (from activated environment) gendis_test.py

5)run jupyter notebook (from activated environment) and open gendis.ipynb

