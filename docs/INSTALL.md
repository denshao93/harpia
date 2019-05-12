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
exec "$SHELL"
```

Create python 3 environment with pyenv


```bash
pyenv install 3.7.3
pyenv global 3.7.3
```

Install pyenv-virtualenv and pyenv-virtualwrapper

```bash
git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

git clone https://github.com/pyenv/pyenv-virtualenvwrapper.git $(pyenv root)/plugins/pyenv-virtualenvwrapper
export PYENV_VIRTUALENVWRAPPER_PREFER_PYVENV="true"
pyenv virtualenvwrapper_lazy
pyenv virtualenvwrapper
exec "$SHELL"
```

Create dictory to save virtual enviroment of python

```bash
mkdir ~/.ve
mkdir ~/workspace/harpia
mkvirtualenv harpia -a ~/workspace/harpia/app
```

##### Install gdal in VirtualEnvironment
Install gdal grater than 2.4.0 (previous version doesn't work with sentinel level 2A)
```bash
sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
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

## Change const.yaml.dist to const.yaml and setting the parameters

## Install postgres and postgis
```bash
sudo apt install postgresql postgresql-contrib
sudo apt install postgresql-10-postgis-2.4
sudo apt install postgresql-10-postgis-scripts
```
```bash
sudo -u postgres psql
```
```sql
ALTER USER postgres PASSWORD 'newpassword';
CREATE DATABASE harpia;
CREATE EXTENSION postgis;
```

### OBS: Create file that set the area of interest from project tha intersect 
### tiles of sentinel. It will return files that can ben downloaded to projet.
### The file has to be in "app/data/vector/aoi.geojson"

```sql
-- DROP SCHEMA metadado_img CASCADE;

CREATE SCHEMA metadado_img;

-- DROP SEQUENCE metadado_sentinel_id_seq CASCADE;

CREATE SEQUENCE metadado_sentinel_id_seq;

-- Table: metadado_img.metadado_sentinel

-- DROP TABLE metadado_img.metadado_sentinel;

-- Drop table

-- DROP TABLE metadado_img.metadado_sentinel;

CREATE TABLE metadado_img.metadado_sentinel (
	"index" text NULL,
	title text NULL,
	link text NULL,
	link_alternative text NULL,
	link_icon text NULL,
	summary text NULL,
	beginposition timestamp NULL,
	endposition timestamp NULL,
	ingestiondate timestamp NULL,
	orbitnumber int8 NULL,
	relativeorbitnumber int8 NULL,
	cloudcoverpercentage numeric(5, 2) NULL,
	highprobacloudspercentage numeric(5, 2) NULL,
	mediumprobacloudspercentage numeric(5, 2) NULL,
	snowicepercentage numeric(5, 2) NULL,
	vegetationpercentage numeric(5, 2) NULL,
	waterpercentage numeric(5, 2) NULL,
	notvegetatedpercentage numeric(5, 2) NULL,
	unclassifiedpercentage numeric(5, 2) NULL,
	format text NULL,
	instrumentshortname text NULL,
	instrumentname text NULL,
	s2datatakeid text NULL,
	platformidentifier text NULL,
	orbitdirection text NULL,
	platformserialidentifier text NULL,
	processingbaseline text NULL,
	processinglevel text NULL,
	producttype text NULL,
	platformname text NULL,
	"size" text NULL,
	filename text NULL,
	level1cpdiidentifier text NULL,
	identifier text NULL,
	uuid text NULL,
	geom geometry(Geometry,4326),
    id integer NOT NULL DEFAULT nextval('metadado_sentinel_id_seq'::regclass),
    date_download_img timestamp without time zone,
    file_path text

);
CREATE INDEX idx_metadado_sentinel_geom ON metadado_img.metadado_sentinel USING gist (geom);
CREATE INDEX ix_metadado_img_metadado_sentinel_index ON metadado_img.metadado_sentinel USING btree (index);
```

