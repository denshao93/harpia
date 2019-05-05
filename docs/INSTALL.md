### Setting Harpia python 3 enviroment

___________________________________________________

All settings were done in Linux Mint 19.1 with Ubuntu 18.04.

#### Install pyenv
##### It set aside harpia enviroment from system enviroment in order to don't break linux.

For more help to install pyenv, see documentation in:

[GitHub of pyenv](http://github.com/pyenv/pyenv)

Clone pyenv

```bash
git clone https://github.com/pyenv/pyenv.git $HOME/.pyenv
```

Settings of pyenv in order to bash can recognize its commands.
```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
```

Update bashrc to able pyenv commands works in bash
```bash
source $HOME/.bashrc
```

Create python 3 environment with pyenv


```bash
pyenv install 3.7.3
pyenv global 3.7.3
```

Install virtualenv and virtualwrapper

```bash
pip install virtualenv virtualenvwrapper
```

Create dictory to save virtual enviroment of python

```bash
mkdir ~/.ve
mkdir ~/workspac/harpia
mkvirtualenv harpia -a ~/workspace/harpia/app
```

##### Install gdal in VirtualEnvironment

```bash
sudo apt-get install libgdal-dev g++ gdal-bin python-gdal python3-gdal
workon harpia
pip install numpy pygdal==2.2.3.3
```
Obs: Pay attention to pygdal version. It need to be the same as system installed

## Install fmask

```bash
cd ~/Downloads
workon harpia
wget 'https://bitbucket.org/chchrsc/rios/downloads/rios-1.4.8.tar.gz'
wget 'https://bitbucket.org/chchrsc/python-fmask/downloads/python-fmask-0.5.3.tar.gz'
tar -xvzf rios-1.4.8.tar.gz
tar -xvzf python-fmask-0.5.3.tar.gz

workon harpia
cd rios-1.4.8 && python setup.py install
cd ../python-fmask-0.5.3 && python setup.py install
```

#### Install gdal-segment
##### Install OpenCV

Ubuntu 18.04
https://www.pyimagesearch.com/2018/05/28/ubuntu-18-04-how-to-install-opencv/

Ubuntu 18.04
```bash
sudo apt install build-essential cmake unzip pkg-config libjpeg-dev libpng-dev libtiff-dev 
libgtk-3-dev libatlas-base-dev gfortran python3-dev

```

```bash
git clone https://github.com/opencv/opencv_contrib.git
cd ~/opencv_contrib
git checkout 3.4.6

mkdir src && cd src && git clone https://github.com/opencv/opencv.git
cd ~/opencv
git checkout 3.4.6
mkdir build && cd build
```

```bash
cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D INSTALL_C_EXAMPLES=OFF \
	-D OPENCV_ENABLE_NONFREE=ON \
	-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
	-D PYTHON_EXECUTABLE=~/.ve/harpia/bin/python \
	-D BUILD_EXAMPLES=ON ..
make -j6
sudo make install
sudo ldconfig
```

## Compile gdal-segment

```bash
cd ~/
git clone https://github.com/cbalint13/gdal-segment.git
cd gdal-segment && mkdir build && cd build
cmake ../
sudo make
```