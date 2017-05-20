# Flex
Application that manage torrents downloads

## Requirements
* Python >= 3.5
* Libtorrent

#### Install libtorrent
> reference http://www.libtorrent.org/python_binding.html

> remember to active your virtualenv

```bash
cd /tmp/
wget https://github.com/arvidn/libtorrent/releases/download/libtorrent-1_1_3/libtorrent-rasterbar-1.1.3.tar.gz
tar xzf libtorrent-rasterbar-1.1.3.tar.gz
cd libtorrent-rasterbar-1.1.3/
./configure --enable-debug=yes --with-boost-python=lib --enable-python-binding
python setup.py build
python setup.py install
```


## Installation and Configuration
```bash
$ git clone git@github.com:marcosflp/flex.git
$ cd flex
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```
