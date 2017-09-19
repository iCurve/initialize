#!/bin/bash
# @Author: minorcong
# @Date:   2017-08-23 14:35:07
# @Last Modified by:   licong08
# @Last Modified time: 2017-09-18 20:40:50

brew install python
pip install -r requirements.txt
swagger_py_codegen --swagger-doc interface.yaml . --ui --spec
pip install -r requirements.txt
sed -i -e "s%debug=True)%debug=True,host='0.0.0.0',port=8081)%" "__init__.py"

# linux

bash -c "$( curl http://jumbo.baidu.com/install_jumbo.sh )"; source ~/.bashrc
jumbo install unzip python python-pip
pip install virtualenv
wget -O iCurve.zip https://github.com/minorcong/initialize/archive/master.zip
rm -rf initialize-master
unzip iCurve.zip && rm iCurve.zip
cd initialize-master
virtualenv --no-site-packages env
source ./env/bin/activate
pip install -r requirements.txt
cd icurve
python
