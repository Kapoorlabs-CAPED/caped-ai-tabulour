import napari
import pandas as pd
from qtpy import QtWidgets

from caped_ai_tabulour._tabulour import Tabulour


def test_table():

    d = {"time": [1, 2], "value": [3, 4]}
    data = pd.DataFrame(data=d)
    viewer = napari.Viewer()
    table_tab = Tabulour(viewer=viewer, data=data, time_key="time")
    _table_tab_layout = QtWidgets.QVBoxLayout()
    table_tab.setLayout(_table_tab_layout)
    _table_tab_layout.addWidget(table_tab)
    viewer.window.add_dock_widget(table_tab)
    napari.run()


if __name__ == "__main__":
    test_table()
