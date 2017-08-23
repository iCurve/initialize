#!/bin/bash
# @Author: misaka
# @Date:   2017-08-23 14:35:07
# @Last Modified by:   licong08
# @Last Modified time: 2017-08-23 14:39:45

pip install -r requirements.txt
swagger_py_codegen --swagger-doc interface.yaml icurve --ui --spec
pip install -r icurve/requirements.txt
sed -i -e "s%debug=True%debug=True,host='0.0.0.0',port=8081%" "icurve/icurve/__init__.py"
