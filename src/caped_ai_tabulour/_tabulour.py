from typing import Union

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
        other_key: Union[int, str] = None,
        unique_cells: dict() = None,
    ):

        super().__init__(parent)
        self._layer = layer
        self._viewer = viewer
        self._data = pandasModel(data)
        self._time_key = time_key
        self._other_key = other_key
        self._unique_cells = unique_cells

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

        # allow discontinuous selections (with command key)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.setSortingEnabled(True)

        self._set_model()
        self._unique_cell_val = None
        # to allow click on already selected row
        self.clicked.connect(self._on_user_click)

    def _set_model(self):

        self.proxy = QtCore.QSortFilterProxyModel()
        self.proxy.setSourceModel(self._data)
        self.setModel(self.proxy)
        self._refreshColumns()

    def _refreshColumns(self):

        columns = self._data.get_data().columns
        for column in columns:
            colIdx = columns.get_loc(column)
            self.setColumnHidden(colIdx, False)

    def _on_user_click(self, item):

        row = self.proxy.mapToSource(item).row()
        # column = self.proxy.mapToSource(item).column()
        if (
            self._time_key is not None
            and self._time_key in self._data.get_data()
        ):

            self._viewer.dims.set_point(
                0, self._data.get_data()[self._time_key][row]
            )
            self.setStyleSheet(
                """
                QTableView::item:selected:active {
                        background: #013220;
                    }
                """
            )
            if (
                self._other_key is not None
                and self._other_key in self._data.get_data()
            ):

                value_of_interest = self._data.get_data()[self._other_key][row]
                if self._unique_cells is not None:
                    self._unique_cell_val = self._display_unique_cells(
                        value_of_interest=value_of_interest
                    )

    def _display_unique_cells(self, value_of_interest):

        if int(value_of_interest) in self._unique_cells:
            return self._unique_cells[int(value_of_interest)]

    def _get__unique_cell_val(self):

        return self._unique_cell_val
