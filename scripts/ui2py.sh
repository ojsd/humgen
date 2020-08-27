#!/usr/bin/env bash
# ui2py.sh
# Convert Qt5 designer XML files (*.ui) into python files

pyuic5 ../pyqt/mainwindow.ui -o ../src/gui/uimainwindow.py
pyuic5 ../pyqt/pump11elitewindow.ui -o ../src/gui/uipump11elitewindow.py
pyuic5 ../pyqt/electrovalvewindow.ui -o ../src/gui/uielectrovalvewindow.py
pyuic5 ../pyqt/redflowmeterwindow.ui -o ../src/gui/uiredflowmeterwindow.py
pyuic5 ../pyqt/elpresswindow.ui -o ../src/gui/uielpresswindow.py
pyuic5 ../pyqt/valvemxseries2window.ui -o ../src/gui/uivalvemxseries2window.py
pyuic5 ../pyqt/maintenancetoolswindow.ui -o ../src/gui/uimaintenancetoolswindow.py
pyuic5 ../pyqt/temperaturewindow.ui -o ../src/gui/uitemperaturewindow.py
pyuic5 ../pyqt/debuglogwindow.ui -o ../src/gui/uidebuglogwindow.py
pyuic5 ../pyqt/statewindow.ui -o ../src/gui/uistatewindow.py
