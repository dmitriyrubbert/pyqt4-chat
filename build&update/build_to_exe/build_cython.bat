DEL modules\gui\resource_rc.py
python build_release.py
COPY modules\gui\resource_rc.pyc building\modules\gui\
DEL building\modules\logic\base.pyd
COPY modules\logic\base.py building\modules\logic\