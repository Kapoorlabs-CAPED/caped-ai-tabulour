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

    def get_data(self):

        return self._data

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.ToolTipRole:
                # no tooltips here
                return QtGui.QBrush(QtCore.Qt.magenta)
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

    def headerData(self, col, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                try:
                    return self._data.columns[col]
                except (IndexError):
                    print(
                        f"IndexError for col:{col} len:{len(self._data.columns)}, shape:{self._data.shape}"
                    )
                    # raise
            elif orientation == QtCore.Qt.Vertical:
                # this is to show pandas 'index' column
                return col
        return QtCore.QVariant()

    def rowCount(self, parent=None):
        if self._data is not None:
            return self._data.shape[0]

    def columnCount(self, parnet=None):
        if self._data is not None:
            return self._data.shape[1]
