import math

import numpy as np
import pandas as pd
from qtpy import QtCore, QtGui


class pandasModel(QtCore.QAbstractTableModel):

    # signalMyDataChanged = QtCore.pyqtSignal(object, object, object)
    signalMyDataChanged = QtCore.Signal(object, object, object)
    """Emit on user editing a cell."""

    def __init__(self, data: pd.DataFrame):
        """Data model for a pandas dataframe.

        Args:
            data (pd.dataframe): pandas dataframe
        """
        QtCore.QAbstractTableModel.__init__(self)

        self._data = data

    def myGetData(self):

        return self._data

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.ToolTipRole:
                # no tooltips here
                pass
            elif role in [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole]:
                columnName = self._data.columns[index.column()]

                realRow = index.row()
                retVal = self._data.loc[realRow, columnName]
                if isinstance(retVal, np.float64):
                    retVal = float(retVal)
                elif isinstance(retVal, np.int64):
                    retVal = int(retVal)
                elif isinstance(retVal, np.bool_):
                    retVal = str(retVal)
                elif isinstance(retVal, list):
                    retVal = str(retVal)
                elif isinstance(retVal, str) and retVal == "nan":
                    retVal = ""

                if isinstance(retVal, float) and math.isnan(retVal):
                    # don't show 'nan' in table
                    retVal = ""
                return retVal

            elif role == QtCore.Qt.FontRole:
                # realRow = self._data.index[index.row()]
                realRow = index.row()
                columnName = self._data.columns[index.column()]
                if columnName == "Symbol":
                    # make symbols larger
                    return QtCore.QVariant(QtGui.QFont("Arial", pointSize=16))
                return QtCore.QVariant()

            elif role == QtCore.Qt.ForegroundRole:
                columnName = self._data.columns[index.column()]
                colorColumns = ["Symbol", "Shape Type"]
                # if columnName == 'Symbol':
                if columnName in colorColumns:
                    # don't get col from index, get from name
                    realRow = self._data.index[index.row()]
                    face_color = self._data.loc[realRow, "Face Color"]  # rgba
                    # TODO: face_color is sometimes a scalar
                    # try:
                    #  _color = (np.array(color.getRgb()) / 255).astype(np.float32)
                    try:
                        # r = int(face_color[0] * 255)
                        # g = int(face_color[1] * 255)
                        # b = int(face_color[2] * 255)
                        # alpha = int(face_color[3] * 255)
                        # theColor = QtCore.QVariant(QtGui.QColor(r, g, b, alpha))
                        # swap AA
                        # napari uses proper order #RRGGBBAA
                        # pyqt uses stange order #AARRGGBB
                        face_color = (
                            face_color[0] + face_color[7:9] + face_color[1:7]
                        )
                        theColor = QtCore.QVariant(QtGui.QColor(face_color))
                        return theColor
                    except (IndexError):
                        print(
                            f'expecting "Face Color"" as list of rgba, got scalar of {face_color}'
                        )
                        return QtCore.QVariant()
                return QtCore.QVariant()

            elif role == QtCore.Qt.BackgroundRole:
                columnName = self._data.columns[index.column()]
                if columnName == "Face Color":
                    realRow = self._data.index[index.row()]
                    face_color = self._data.loc[realRow, "Face Color"]  # rgba
                    face_color = (
                        face_color[0] + face_color[7:9] + face_color[1:7]
                    )
                    theColor = QtCore.QVariant(QtGui.QColor(face_color))
                    return theColor
                elif index.row() % 2 == 0:
                    return QtCore.QVariant(QtGui.QColor("#444444"))
                else:
                    return QtCore.QVariant(QtGui.QColor("#666666"))
        #
        return QtCore.QVariant()

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]
