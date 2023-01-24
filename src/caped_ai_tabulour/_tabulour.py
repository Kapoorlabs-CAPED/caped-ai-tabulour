from typing import List, Union

import napari
import pandas as pd
from qtpy import QtCore, QtWidgets

from ._data_model import pandasModel


class Tabulour(QtWidgets.QTableView):

    signalSelectionChanged = QtCore.Signal(object, object)
    signalDataChanged = QtCore.Signal(str, set, pd.DataFrame)

    def __init__(
        self,
        parent=None,
        viewer: napari.Viewer = None,
        layer: napari.layers.Layer = None,
        data: pd.DataFrame = None,
        time_key: Union[int, str] = None,
        other_keys: List[Union[int, str]] = None,
    ):

        super().__init__(parent)
        QtCore.QAbstractTableModel.__init__(self)
        self._layer = layer
        self._viewer = viewer
        self._data = pandasModel(data)
        self._time_key = time_key
        self._other_keys = other_keys

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

        # allow discontinuous selections (with command key)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.setSortingEnabled(True)

        self._set_model()
        # to allow click on already selected row
        self.clicked.connect(self._on_user_click)

    def _set_model(self):

        self.proxy = QtCore.QSortFilterProxyModel()
        self.proxy.setSourceModel(self._data)
        self.setModel(self.proxy)
        self._refreshColumns()

    def _refreshColumns(self):

        columns = self._data.myGetData().columns
        for column in columns:
            colIdx = columns.get_loc(column)
            self.setColumnHidden(colIdx, False)

    def _on_user_click(self, item):

        row = self.proxy.mapToSource(item).row()
        # column = self.proxy.mapToSource(item).column()
        if self._time_key in self._data.myGetData():

            self._viewer.dims.set_point(
                0, self._data.myGetData()[self._time_key][row]
            )
            print("time", self._data.myGetData()[self._time_key][row])
