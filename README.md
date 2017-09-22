initialize
---

An initialize project for baseline, eg. falsk demo, plugins, requirements and so on.

## run

```
# python2.7+ is required
# download
wget -O iCurve.zip https://github.com/minorcong/initialize/archive/master.zip
# untar
rm -rf initialize-master
unzip iCurve.zip && rm iCurve.zip
# virtualenv
cd initialize-master
virtualenv --no-site-packages env
source ./env/bin/activate
# dependence
pip install -r requirements.txt
# workdir
cd icurve
# local port config
sed -i -e "s%port=8080%port=8080%" "__main__.py"
# run
python -m icurve
```

## plugin dir

```
icurve/v1/plugins
```

## test

```
# workdir
cd icurve
# pytest
pytest
```