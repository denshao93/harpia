# Configurando o ambiente

___________________________________________________

## Instalar gdal

```sudo add-apt-repository -y ppa:ubuntugis/ppa
sudo apt update
sudo apt upgrade
sudo apt install gdal-bin python-gdal python3-gdal
```

___________________________________________________

## Instalar OpenCV

```
sudo apt-get install build-essential
sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev

mkdir src
cd src
git clone https://github.com/opencv/opencv.git
git checkout 3.3.1
git clone https://github.com/opencv/opencv_contrib.git
git checkout 3.3.1
cd opencv
mkdir build
cd build
cmake CMAKE_VERBOSE=1 -DOPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules -DCMAKE_SKIP_RPATH=ON ../
make -j4
sudo make install
```

___________________________________________________

## Instalar o gdal-segment

```
cd src
git clone https://github.com/cbalint13/gdal-segment.git
cd gdal-segment
mkdir build
cd build
cmake -DCMAKE_CXX_FLAGS="-std=c++11 -fopenmp" ../
sudo make
```





mkdir src
git clone https://github.com/opencv/opencv.git
cd opencv
git checkout 3.3.1

git clone https://github.com/opencv/opencv_contrib.git
git checkout 3.3.1
cd opencv_contrib

cd opencv/ 
mkdir build 
cd build 
cmake CMAKE_VERBOSE=1 -DOPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules -DCMAKE_SKIP_RPATH=ON ../
make -j4
sudo make install

cd src/gdal-segment && mkdir build && cd build &&\
        cmake -DCMAKE_CXX_FLAGS="-std=c++11 -fopenmp" ../ &&\
        sudo make &&\
        cp ../bin/gdal-segment /usr/local/bin/