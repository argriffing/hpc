
# define the prefix for the new python
setenv MYPATH /brc_share/brc/argriffi/tmp-install


# download a recent stable version of python
curl -O http://python.org/ftp/python/2.6.5/Python-2.6.5.tar.bz2
# untar (1 minute)
tar xjvf Python-2.6.5.tar.bz2
cd Python-2.6.5
# configure python (1 minute)
./configure --prefix=$MYPATH
# build python (2 minutes)
make
# install python (1 minute)
make install
cd ..


# download the numpy module for numerical
# multidimensional-array-based python features
curl -O -L http://downloads.sourceforge.net/project/numpy/NumPy/1.4.1/numpy-1.4.1.tar.gz
tar xzvf numpy-1.4.1.tar.gz
cd numpy-1.4.1
# build numpy (1 minute)
$MYPATH/bin/python setup.py build
# install numpy to the custom version of python
$MYPATH/bin/python setup.py install
cd ..


# download the scipy module for scientific and statistical python features
curl -O -L http://downloads.sourceforge.net/project/scipy/scipy/0.7.2/scipy-0.7.2.tar.gz
tar xzvf scipy-0.7.2.tar.gz
cd scipy-0.7.2
# build scipy (6 minutes)
$MYPATH/bin/python setup.py build
# install scipy to the custom version of python
$MYPATH/bin/python setup.py install
cd ..


# download the matplotlib module for drawing plots with python
# and for other features related to computational geometry
curl -O -L http://downloads.sourceforge.net/project/matplotlib/matplotlib/matplotlib-0.99.1/matplotlib-0.99.1.2.tar.gz
tar xzvf matplotlib-0.99.1.2.tar.gz
cd matplotlib-0.99.1.1
# build matplotlib (1 minute)
$MYPATH/bin/python setup.py build
# install matplotlib to the custom version of python
$MYPATH/bin/python setup.py install
cd ..


# download the argparse module to facilitate command line argument processing;
# this module will be built into python in future python versions.
curl -O http://pypi.python.org/packages/source/a/argparse/argparse-1.1.zip
unzip argparse-1.1.zip
cd argparse-1.1
$MYPATH/bin/python setup.py install
cd ..

