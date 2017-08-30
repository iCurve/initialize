#!/bin/bash
# @Author: misaka
# @Date:   2017-08-23 14:35:07
# @Last Modified by:   licong
# @Last Modified time: 2017-08-25 14:44:00

brew install python
pip install -r requirements.txt
swagger_py_codegen --swagger-doc interface.yaml . --ui --spec
pip install -r requirements.txt
sed -i -e "s%debug=True)%debug=True,host='0.0.0.0',port=8081)%" "__init__.py"