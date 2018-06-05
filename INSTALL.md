# Setting enviroment

___________________________________________________

## Install gdal

Gdal needs to support hdf5 format file

```sudo add-apt-repository -y ppa:ubuntugis/ppa
sudo apt update
sudo apt upgrade
sudo apt install gdal-bin python-gdal python3-gdal
Suporte para o formato hdf5
sudo apt-get install libhdf5-dev libhdf5-serial-dev

sudo apt-get install dans-gdal-scripts
```

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