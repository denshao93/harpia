# Setting enviroment
___________________________________________________

## Install dependecies to pyenv
```c
sudo apt install curl git-core gcc make zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev libssl-dev
```
## Install pyenv
```c
git clone https://github.com/pyenv/pyenv.git $HOME/.pyenv
```
## pyenv configs
```c
nano $HOME/.bashrc 
```
*Copy and paste at the end of bashrc*

```c
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
if command -v pyenv 1>/dev/null 2>&1; then
eval "$(pyenv init -)"
fi
```
*Save file*

```c
source $HOME/.bashrc
```

## Install pyenv-virtualenv
```c
git clone https://github.com/yyuu/pyenv-virtualenv.git   $HOME/.pyenv/plugins/pyenv-virtualenv
```

# Install python with pyenv
```c
pyenv install 3.6.6
```

```c
pyenv global 3.6.6
```

# Directory architecture:
```c
mkdir ~/.ve
"Project code is in:"
mkdir ~/workspace

export WORKON_HOME=~/.ve
export PROJECT_HOME=~/workspace

# Open terminal
```c
source ~/.bashrc
bash
```

# Install virtualenvwrapper
```c
git clone https://github.com/pyenv/pyenv-virtualenvwrapper.git $(pyenv root)/plugins/pyenv-virtualenvwrapper

"Is necessary to do it?"
pyenv virtualenvwrapper
```

# Connect workspace to virtual environment
```
mkvirtualenv -a ~/workspace/harpia harpia
```

### Install gdal in VirtualEnvironment

*Gdal needs to support hdf5 format file to gdal-segment*

```
sudo apt-get install libgdal-dev g++ gdal-bin python-gdal python3-gdal
workon harpia
pip install pygdal==2.2.3.
```
*Obs: Pay attention to pygdal version. It need to be the same as system installed*
___________________________________________________
## Install OpenCV

```sudo apt-get install build-essential
sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev

mkdir src
cd src
git clone https://github.com/opencv/opencv.git
git checkout 3.3.1
cd src/openvc
git clone https://github.com/opencv/opencv_contrib.git
git checkout 3.3.1
cd opencv
mkdir build
cd build
cmake CMAKE_VERBOSE=1 -DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib/modules -DCMAKE_SKIP_RPATH=ON ../
make -j4
sudo make install
```

___________________________________________________

## Install gdal-segment

```git clone https://github.com/cbalint13/gdal-segment.git
cd gdal-segment
mkdir build
cd build
cmake ../
sudo make
```