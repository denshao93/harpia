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

```sql
-- DROP SCHEMA metadado_img CASCADE;

CREATE SCHEMA metadado_img;

-- DROP SEQUENCE metadado_sentinel_id_seq CASCADE;

CREATE SEQUENCE metadado_sentinel_id_seq;

-- Table: metadado_img.metadado_sentinel

-- DROP TABLE metadado_img.metadado_sentinel;

CREATE TABLE metadado_img.metadado_sentinel
(
    index text,
    title text,
    link text,
    link_alternative text,
    link_icon text,
    summary text,
    datatakesensingstart timestamp without time zone,
    beginposition timestamp without time zone,
    endposition timestamp without time zone,
    ingestiondate timestamp without time zone,
    orbitnumber bigint,
    relativeorbitnumber bigint,
    cloudcoverpercentage double precision,
    sensoroperationalmode text,
    tileid text,
    hv_order_tileid text,
    format text,
    processingbaseline text,
    platformname text,
    filename text,
    instrumentname text,
    instrumentshortname text,
    size text,
    s2datatakeid text,
    producttype text,
    platformidentifier text,
    orbitdirection text,
    platformserialidentifier text,
    processinglevel text,
    identifier text,
    uuid text,
    geom geometry(Polygon,4326),
    id integer NOT NULL DEFAULT nextval('metadado_sentinel_id_seq'::regclass),
    date_download timestamp without time zone,
    level1cpdiidentifier character(250),
    is_download boolean,
    is_processed boolean,
    file_path boolean
);

ALTER TABLE metadado_img.metadado_sentinel
    OWNER to postgres;

-- Index: idx_metadado_sentinel_geom

-- DROP INDEX metadado_img.idx_metadado_sentinel_geom;

CREATE INDEX idx_metadado_sentinel_geom
    ON metadado_img.metadado_sentinel USING gist
    (geom);

-- Index: idx_metadado_sentinel_index

-- DROP INDEX metadado_img.idx_metadado_sentinel_index;

CREATE INDEX idx_metadado_sentinel_index
    ON metadado_img.metadado_sentinel USING btree
    (index, id);
```

