# -*- coding: utf-8 -*-
# Python imports


from pathlib import Path
import json

# Third party imports
from PyQt5.QtWidgets import QDialog

# Local imports
from Ui_DeviceTableDialog import Ui_DeviceTableDialog
from PandasTableModel import DataFrameModel

#%%

class DeviceTableDialog(QDialog, Ui_DeviceTableDialog):
    # TODO Create and import inheirited files
    def __init__(self, context):
        super(DeviceTableDialog, self).__init__()

        # Context manager
        self.context = context

        # Set user interface from designer
        self.setupUi(self)
        self.setWindowIcon(self.context.report_icon)

        return None

    def get_device_table(self):
        """Retrieve the next cluster of points from documents stored in the
        clustered_points collection. This function handles getting the next
        document that is missing labels, as well as extracting clustered
        points from each of those documents.
        1) Create a data model (Qt is a model-view architecture. The model
        Controls where the data comes from. Right now teh QTableView is only

        inputs
        -------
        None
        outputs
        -------
        dataframe : (pd.DataFrame) a single cluster of points from a document
        in the clustered_ponts collection"""

        # Create a data model (Qt is a model-view architecture. THe model
        # Controls where the data comes from. Right now teh QTableView is only
        # A View on the models data)

        # Instantiate classes if not already
        if not 'dataframe_generator' in self.__dict__.keys():
            self.dataframe_generator = self.mongoQueryHelper.retrieve_points_dataframe(self.current_document)

        try:
            # Generate the next dataframe and set the model in the table view
            self.index, self.current_dataframe = next(self.dataframe_generator)
            tableModel = DataFrameModel(self.current_dataframe)
            self.tableView.setModel(tableModel)

        except StopIteration:
            # The current document is out of clustered points dataframes
            # First, generate a new document to make a new generator over the
            # documents clustered_points objects
            # Finally, get the next dataframe from the generator
            self.current_document = next(self.document_generator)
            self.dataframe_generator = self.mongoQueryHelper.retrieve_points_dataframe(self.current_document)
            self.index, self.current_dataframe = next(self.dataframe_generator)
            tableModel = DataFrameModel(self.current_dataframe)
            self.tableView.setModel(tableModel)

        # Update the documentName Label with the current database name
        database_tag = self.current_document['database_tag']
        documentLabel = self.rightGroupBox.findChild(QLabel, 'databaseTag')
        documentLabel.setText(database_tag)

        # Update the current index
        self.rightGroupBox.findChild(QLabel, 'currentIndex')
        currentIndex = self.rightGroupBox.findChild(QLabel, 'currentIndex')
        currentIndex.setText(str(self.index))

        return None

    def set_device_table(self):

        return None