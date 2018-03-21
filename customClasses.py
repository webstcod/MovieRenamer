import os
import wx
import wx.xrc
import wx.lib.mixins.listctrl as listmix


###########################################################################
# Class FilesDropTarget
###########################################################################
class CustomCheckListReport(wx.ListCtrl, listmix.CheckListCtrlMixin, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, *args, **kwargs):
        # super(TestListCtrl, self).__init__(*args, **kwargs)
        wx.ListCtrl.__init__(self, *args, **kwargs)
        listmix.CheckListCtrlMixin.__init__(self)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        # self.setResizeColumn(3)

        # For row deletions.
        self.Bind(wx.EVT_LEFT_DOWN, self.OnFindCurrentRow)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

        # ----  "Global attributes"
        self.currRow = None
        self.numCols = -1

        self.entriesList = list()  # Actual dropped file entries; duplicates are avoided.
        self.numEntries = 0  # Dropped file entry count.
        self.haveEntries = False  # Tracks actual dropped file entries, but not help entries.
        self.removed_files = list()

    def GetAllRows(self):
        """ Return a list of all current row data.
        Note that extracting this info directly from the control is insanely complicated.
        This is another reason why the row data list is maintained.
        """

        # SANITY CHECK
        assert (len(self.entriesList) == self.numEntries)

        allRowsList = list()
        for rowIdx in range(self.numEntries):
            rowData = self.entriesList[rowIdx]
            basename = rowData[0]
            foldername = rowData[1]
            fullpath = os.path.join(foldername, basename)
            allRowsList.append(fullpath)

        # end if

        return allRowsList

    def GetAllFiles(self):
        """ Return a list of all current files in the row data.
        Note that extracting this info directly from the control is insanely complicated.
        This is another reason why the row data list is maintained.
        """

        allRowsList = self.GetAllRows()  # Complete file paths list

        # SANITY CHECK
        assert (len(allRowsList) == self.numEntries)

        allFoldersList = list()
        for fullpath in allRowsList:  # len( allRowsList )

            if (not os.path.isdir(fullpath)):  # files and links
                allFoldersList.append(fullpath)

        return allFoldersList

    def GetAllFolders(self):
        """ Return a list of all current folders in the row data.
        Note that extracting this info directly from the control is insanely complicated.
        This is another reason why the row data list is maintained.
        """

        allRowsList = self.GetAllRows()  # Complete file paths list

        # SANITY CHECK
        assert (len(allRowsList) == self.numEntries)

        allFoldersList = list()
        for fullpath in allRowsList:  # len( allRowsList )

            if os.path.isdir(fullpath):  # files and links
                allFoldersList.append(fullpath)

        return allFoldersList

    def WriteTextTuple(self, rowDataTuple):
        """  Write non-duplicate row data to the LstCtrl.
        The text data may be any indexable, 2-text-element data object.
        E.g., a list or tuple [or set ?].
        All row entries written to the ListCtrl are also stored in a list
          for deletion verification purposes.
        """

        # Do some basic data checking.
        assert (len(rowDataTuple) >= self.numCols), 'Given data must have at least %d items.' %(self.numCols)

        for idx in range(self.numCols):  # Need to check only the first two elements.
            assert (isinstance(rowDataTuple[idx], str)), 'One or both data elements are not strings.'

        # -----

        # Write a new row's ietm/text/data.
        rowDataTupleTruncated = tuple(rowDataTuple[:self.numCols])
        # if (rowDataTupleTruncated not in self.entriesList):

        if (not self.haveEntries):  # Clear any help message(s).
            self.DeleteAllItems()

        # Update everything
        self.Append(rowDataTupleTruncated)  # Add row to the ListCtrl.
        self.entriesList.append(rowDataTupleTruncated)  # Store the row data.
        self.numEntries += 1
        self.haveEntries = True

        # Set reasonable column widths.
        self.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        # self.Autosize()

    def Autosize(self):
        """
        Intelligently autosize the first column (the filenames, if any) since the
          control's autosizing method does not include the width of the column labels.
        """

        # Temporarily appending the column headers as a row data item
        #   causes the columns to be resized to min( dropEntryText, headerText ).
        self.Append(self.headerLabelList)
        for colIndex in range(len(self.headerLabelList)):
            self.SetColumnWidth(colIndex, wx.LIST_AUTOSIZE)

        self.DeleteItem(self.GetItemCount() - 1)

        """
        If any one filename is very long the column width was set too long and 
          occupies "too much" width in the control causing little or no display 
          of the folder paths to be shown. 
        Set first row's width to no more than 50% of the control's client width.
        This is a "reasonable" balance which leaves both columns's data 
           at least 50% displayed at all times.
        """
        firstColMaxWid = self.GetClientSize()[0] / 2  # Half the avaiable width.
        firstColIndex = 0  # Avoid the use of "Magic Numbers".
        firstColActualWid = self.GetColumnWidth(firstColIndex)
        reasonableWid = min(firstColMaxWid, firstColActualWid)
        self.SetColumnWidth(firstColIndex, reasonableWid)

    def OnFindCurrentRow(self, event, changeState=True):
        row, _ignoredFlags = self.HitTest(event.GetPosition())
        # print(row)
        self.currRow = row  # Save row index for later use.
        self.Select(row)
        if not row == -1:
            if self.IsChecked(row) and changeState:
                self.CheckItem(row, False)
            elif changeState:
                self.CheckItem(row, True)
            # print("Current Row: {0}\tState: {1}".format(row, self.IsChecked(row)))
        else:
            pass
            # print("Current Row: {0}\tState: {1}".format(row,"Unknown"))

    def OnRightDown(self, event):

        menu = wx.Menu()
        menuItem_delete = menu.Append(-1, 'Delete this entry')

        self.Bind(wx.EVT_MENU, self.OnDeleteRow, menuItem_delete)

        # Select row
        self.OnFindCurrentRow(event, False)

        self.PopupMenu(menu, event.GetPosition())

    def OnDeleteRow(self, event):
        if (self.currRow >= 0):

            # This row data must have been appended to self.entriesList.

            # -----  SANITY CHECK

            # self.GetItemCount() may be greater than self.numEntries due to help messages.
            assert (self.numEntries == len(self.entriesList))

            # -----
            self.removed_files.append(self.GetItemText(self.currRow, 1))

            # Retreive the selected raw-row-data as a list of lists.
            allSelectedRowData = self.GetAllSelectedRowData()

            if (len(allSelectedRowData) >= 1):
                rawRowData = allSelectedRowData[0]  # There can be only a single row selected.
                lineIdx = rawRowData[0]
                unknownData = rawRowData[1]
                textDataTuple = tuple(rawRowData[2:])  # Make same type as in self.entriesList

                if self.numEntries:
                    try:
                        entryListIndex = None
                        entryListIndex = self.entriesList.index(textDataTuple)
                    except ValueError:
                        print('####  ERROR:  textDataTuple NOT FOUND in self.entriesList :')
                        print(' ', textDataTuple)
                        print()
                        return

                    # Delete this row item from [ self.entriesList ].
                    del self.entriesList[entryListIndex]

                    # Update the status vars.
                    self.numEntries -= 1
                    if (self.numEntries < 1):
                        self.haveEntries = False
                        self.Append(self.HelpTextTuple)

                    # Finally, detete the textList row item.
                    self.DeleteItem(self.currRow)

    def GetAllSelectedRowData(self):
        """ A strange algorithm to retrieve all selected row data.
        From "DnD demo with listctrl" @ http ://wiki.wxpython.org/ListControls#List_Controls
        """

        allSelectedRowData = list()
        idx = -1  # Special flag value.
        while True:  # Find all the selected items and put them in a list

            idx = self.GetNextItem(idx, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)

            # ???  If return value is [ -1 ] why predefine it as [ -1 ] before loop entry ?
            if (idx == -1):
                break
            # -----

            allSelectedRowData.append(self.GetItemInfo(idx))

        return allSelectedRowData

    def GetItemInfo(self, idx):
        """ Collects all relevant data of a listitem and puts it in a list
        From "DnD demo with listctrl" @ http ://wiki.wxpython.org/ListControls#List_Controls
        """

        rowItemList = list()
        rowItemList.append(idx)  # We need the original index, so it is easier to eventualy delete it
        rowItemList.append(self.GetItemData(idx))  # Itemdata
        rowItemList.append(self.GetItemText(idx))  # Text first column

        for i in range(1, self.GetColumnCount()):  # Possible extra columns
            rowItemList.append(self.GetItem(idx, i).GetText())

        return rowItemList

    def OnCheckItem(self, index, flag):
        pass
        # print(index, flag)


###########################################################################
# Class FilesDropTarget
###########################################################################
class FilesDropTarget(wx.FileDropTarget):
    def __init__(self, targetControl):
        wx.FileDropTarget.__init__(self)
        self.targetControl = targetControl  # For dropped files are dropped.

    def FilenameDropDict(self):
        """ Defines a succinct dictionary for each given drop file's info. """

        filenameDropDict = dict()
        # Initialize it with dummy values.
        filenameDropDict['coord'] = (-1, -1)  # Real data can never have this value.
        filenameDropDict['pathname'] = ''  # Real data can never be empty.
        filenameDropDict['basenameList'] = list()  # Real data can never be empty.
        filenameDropDict['fullPathList'] = list()  # Real data can never be empty.

        return filenameDropDict

    def OnDropFiles(self, xOrd, yOrd, pathList):
        # Separate the dir path from the basename or leafDirectory name.
        pathname, _ignored = os.path.split(pathList[0])

        # The file's and folders's basenames :
        basenameList = list()
        for aPath in pathList:
            _ignoredDir, aBasename = os.path.split(aPath)
            basenameList.append(aBasename)

        # The target control must know the structure of this dict
        #   in order to use this data about to be stored there.
        filenameDropDict = self.FilenameDropDict()
        filenameDropDict['coord'] = (xOrd, yOrd)
        filenameDropDict['pathList'] = pathList
        filenameDropDict['pathname'] = pathname
        filenameDropDict['basenameList'] = basenameList

        # How the app is to use this data :
        if (hasattr(self.targetControl, 'dropFunc')) and (self.targetControl.dropFunc != None):
            # Call the callback function with the processed drop data.
            self.targetControl.dropFunc(filenameDropDict)

        return True
