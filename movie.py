# -*- coding: utf-8 -*-

import os
import wx
import wx.xrc
import wx.lib.mixins.listctrl as listmix

###########################################################################
## Class MainFrame
###########################################################################
class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"TheRenamer", pos=wx.DefaultPosition, size=wx.Size(750, 500), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        self.filesAndLinks = dict()

        # ------------------------------------------------------------------
        # Menu Bar
        # ------------------------------------------------------------------
        self.m_menubar1 = wx.MenuBar(0)
        self.fileMenu = wx.Menu()
        self.clearMenu = wx.MenuItem(self.fileMenu, wx.ID_ANY, u"Clear", wx.EmptyString, wx.ITEM_NORMAL)
        self.fileMenu.Append(self.clearMenu)
        self.exitMenu = wx.MenuItem(self.fileMenu, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL)
        self.fileMenu.Append(self.exitMenu)
        self.m_menubar1.Append(self.fileMenu, u"File")
        self.SetMenuBar(self.m_menubar1)

        # ------------------------------------------------------------------
        # Body
        # ------------------------------------------------------------------
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.notebook = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.mainPanel = MainPanel(self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.mainPanel.SetCallbackFunc(self.FilesDropped)

        self.notebook.AddPage(self.mainPanel, u"Movie Renamer", False)
        mainSizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 0)

        self.m_statusBar1 = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)
        self.m_statusBar1.SetStatusText("Ready")

        self.SetSizer(mainSizer)
        self.Layout()
        self.Centre(wx.BOTH)

        # ------------------------------------------------------------------
        # Define actions for events
        # ------------------------------------------------------------------
        self.Bind(wx.EVT_MENU, self.ClearData, id=self.clearMenu.GetId())
        self.Bind(wx.EVT_MENU, self.OnExit, id=self.exitMenu.GetId())
        self.mainPanel.generateBttn.Bind(wx.EVT_BUTTON, self.GenerateButton)
        self.mainPanel.renameBttn.Bind(wx.EVT_BUTTON, self.RenameButton)


    def __del__(self):
        pass


    def FilesDropped(self, filenameDropDict):
        # A convenience alias :
        dropTarget = self.mainPanel.GetDropTarget()  # self.filesDropCtrl.listCtrl

        # Extract the info from the drop data dictionary.
        pathList = filenameDropDict['pathList']
        commonPathname = filenameDropDict['pathname']
        basenameList = filenameDropDict['basenameList']  # Not used in this method.
        dropCoord = filenameDropDict['coord']  # Not used in this method.

        keys2remove = []
        for key in self.filesAndLinks.keys():
            if any(self.filesAndLinks[key]['oldName'] == rem for rem in self.mainPanel.movieListCtrl.removed_files):
                keys2remove.append(key)
        for key in keys2remove:
            self.filesAndLinks.pop(key, None)
        self.mainPanel.movieListCtrl.removed_files = []

        for aPath in sorted(pathList):  # May include folders.
            # Keep just files and link files.
            if not os.path.isdir(aPath):
                if (aPath not in self.filesAndLinks.keys()):
                    self.filesAndLinks[aPath] = dict()

                    longFormParentPath, basename = os.path.split(aPath)
                    self.filesAndLinks[aPath]['ext'] = aPath.split('.')[-1]
                    self.filesAndLinks[aPath]['oldName'] = '.'.join(basename.split('.')[:-1])

                    textTuple = ("", self.filesAndLinks[aPath]['oldName'], "")
                    dropTarget.WriteTextTuple(textTuple)
        self.mainPanel.movieListCtrl.SetColumnWidth(1, wx.LIST_AUTOSIZE)

        for row in range(dropTarget.ItemCount):
            dropTarget.CheckItem(row, True)

        if dropTarget.ItemCount > 0:
            self.mainPanel.generateBttn.Enable(True)


    def OnExit(self, event):
        wx.Exit()  # Exit/break out of App.MainLoop{}.


    def GenerateButton(self, event):
        dropTarget = self.mainPanel.GetDropTarget()
        for row in range(dropTarget.ItemCount):
            if dropTarget.IsChecked(row):
                dropTarget.SetItem(row,2, dropTarget.GetItemText(row, 1))
        self.mainPanel.generateBttn.Enable(False)
        self.mainPanel.renameBttn.Enable(True)


    def RenameButton(self, event):
        self.mainPanel.renameBttn.Enable(False)


    def ClearData(self, event):
        self.mainPanel.movieListCtrl.DeleteAllItems()
        self.mainPanel.movieListCtrl.Append(self.mainPanel.movieListCtrl.HelpTextTuple)
        self.mainPanel.generateBttn.Enable(False)
        self.mainPanel.renameBttn.Enable(False)
        self.mainPanel.movieListCtrl.haveEntries = False
        self.filesAndLinks.clear()


    # ------------------------------------------------------------------
    # Unused functions
    # ------------------------------------------------------------------

###########################################################################
## Class MainPanel
###########################################################################
class MainPanel(wx.Panel):
    def __init__(self, parent, callbackFunc=None, *args, **kwargs):
        super(MainPanel, self).__init__(parent=parent, id=wx.ID_ANY)

        self.callbackFunc = callbackFunc  # For the files drop handler.

        pageSizer_1 = wx.BoxSizer(wx.VERTICAL)

        self.movieListCtrl = TestListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL)
        pageSizer_1.Add(self.movieListCtrl, 1, wx.ALL | wx.EXPAND, 5)

        bttnSizer = wx.BoxSizer(wx.HORIZONTAL)

        bttnSizer.Add((0, 0), 1, wx.EXPAND, 5)

        self.generateBttn = wx.Button(self, wx.ID_ANY, u"Generate", wx.DefaultPosition, wx.DefaultSize, 0)
        self.generateBttn.Enable(False)

        bttnSizer.Add(self.generateBttn, 0, wx.ALL, 5)

        bttnSizer.Add((0, 0), 1, wx.EXPAND, 5)

        self.renameBttn = wx.Button(self, wx.ID_ANY, u"Rename", wx.DefaultPosition, wx.DefaultSize, 0)
        self.renameBttn.Enable(False)

        bttnSizer.Add(self.renameBttn, 0, wx.ALL, 5)

        pageSizer_1.Add(bttnSizer, 0, wx.EXPAND, 5)

        self.SetSizer(pageSizer_1)
        self.Layout()
        pageSizer_1.Fit(self)

        # ------------------------------------------------------------------
        # Add rows and columns to table
        # ------------------------------------------------------------------
        headerList = ["", "Current File Names", "New File Names"]
        self.WriteHeaderLabels(headerList)
        self.WriteHelptext()

        # ------------------------------------------------------------------
        # Define extras
        # ------------------------------------------------------------------


    def WriteHelptext(self, helpText='Drop Files and Folders Here'):
        helpTextTuple = ('', helpText, '')
        self.movieListCtrl.Append(helpTextTuple)

        for col in range(self.numCols):  # Widen the column widths.
            self.movieListCtrl.SetColumnWidth(col, wx.LIST_AUTOSIZE)

        # Save for rewriting if all list entries have been deleted.
        self.movieListCtrl.HelpTextTuple = helpTextTuple


    def WriteHeaderLabels(self, headerLabelList):
        self.headerLabelList = headerLabelList
        self.movieListCtrl.headerLabelList = headerLabelList

        # This sets the "official" number of columns the textCtrl has.
        self.numCols = len(self.headerLabelList)
        self.movieListCtrl.numCols = self.numCols

        for col in range(self.numCols):
            self.movieListCtrl.InsertColumn(col, self.headerLabelList[col])

        for col in range(self.numCols):
            self.movieListCtrl.SetColumnWidth(col, wx.LIST_AUTOSIZE_USEHEADER)


    def SetCallbackFunc(self, dropCallbacFunc=None):
        """ This method is called from the parent container wanting
        its FilesDirsDropCtrl object to gain dropFiles capability.

        The parent provides a dropFiles callback function reference
        that actually processes the dropfiles data (a dictionary)
        whenever files are dropped.
        """

        # Create a dropFiles event association for this control.
        #    [ SetDropTarget ] is a built-in method for (all ?) controls.
        self.movieListCtrl.SetDropTarget(FilesDropTarget(self.movieListCtrl))

        # Install the callback-function for this class's parent-widget dropFiles-event.
        self.movieListCtrl.dropFunc = dropCallbacFunc


    def GetDropTarget(self):
        return self.movieListCtrl


    def OnExit(self, event):
        wx.Exit()  # Exit method wx.App.MainLoop{}.

###########################################################################
## Class TestListCtrl
###########################################################################
class TestListCtrl(wx.ListCtrl, listmix.CheckListCtrlMixin, listmix.ListCtrlAutoWidthMixin):
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
## Class FilesDropTarget
###########################################################################
class FilesDropTarget(wx.FileDropTarget):
    def __init__(self, targetControl):
        self.targetControl = targetControl

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


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame(None).Show()
    app.MainLoop()