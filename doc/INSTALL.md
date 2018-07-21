# Setting enviroment
___________________________________________________

## Install pyenv and pyenv-virtualenv
```console
curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
```

## Install pyenv-virtualenvwrapper
```console
git clone https://github.com/yyuu/pyenv-virtualenvwrapper.git ~/.pyenv/plugins/pyenv-virtualenvwrapper
```

# Directory architecture:
```console
mkdir ~/.ve
Project code is in:
mkdir ~/workspace

export WORKON_HOME=~/.ve
export PROJECT_HOME=~/workspace
eval "$(pyenv init -)"
#pyenv virtualenvwrapper_lazy

# Open terminal
```console
source ~/.bashrc
bash
```
*Obs: With you use Linux Mint or Ubuntu you should change ~/.zshrc*

## Install dependecies
```console
sudo apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev
```

## Install python set aside of system
```console
pyenv install 3.6.7

# Set python env as global 
pyenv global 3.6.7
```

# Remove # from pyenv virtualenvwrapper_lazy
*Open terminal*
```console
source ~/.
bash
```
*Obs: With you use Linux Mint or Ubuntu you should change ~/.zshrc*

# Connect workspace to virtual environment
```
mkvirtualenv -a ~/workspace/harpia harpia
```

### Install gdal in VirtualEnvironment

*Gdal needs to support hdf5 format file to gdal-segment*

```
sudo apt-get install libgdal-dev
workon harpia
pip install pygdal==2.2.3

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