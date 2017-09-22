# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .api.data_dataName_label import DataDatanameLabel
from .api.data_dataName_band_bandName import DataDatanameBandBandname
from .api.data_dataName import DataDataname
from .api.datas import Datas
from .api.data_dataName_thumb import DataDatanameThumb
from .api.data_dataName_curves import DataDatanameCurves
from .api.menus import Menus


routes = [
    dict(resource=DataDatanameLabel, urls=['/data/<dataName>/label'], endpoint='data_dataName_label'),
    dict(resource=DataDatanameBandBandname, urls=['/data/<dataName>/band/<bandName>'], endpoint='data_dataName_band_bandName'),
    dict(resource=DataDataname, urls=['/data/<dataName>'], endpoint='data_dataName'),
    dict(resource=Datas, urls=['/datas'], endpoint='datas'),
    dict(resource=DataDatanameThumb, urls=['/data/<dataName>/thumb'], endpoint='data_dataName_thumb'),
    dict(resource=DataDatanameCurves, urls=['/data/<dataName>/curves'], endpoint='data_dataName_curves'),
    dict(resource=Menus, urls=['/menus'], endpoint='menus'),
]