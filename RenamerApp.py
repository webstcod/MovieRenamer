import os
import wx
import wx.xrc
import RenamerGUI
from customClasses import FilesDropTarget


class MainFrame(RenamerGUI.MainFrame):
    def __init__(self, parent):
        RenamerGUI.MainFrame.__init__(self, parent)
        self.FilesAndDirs = dict()

        self.name = "Main Frame"
        self.movieList.name = "Movie List"
        self.musicReport.name = "Music List"
        self.MovieRenamer.name = "Movie Renamer"
        self.MusicRenamer.name = "Music Renamer"

        movieHeaders = ["", "Old Name", "Generated Name"]
        self.WriteHeaderLabels(self.movieList, movieHeaders)
        self.SetCallbackFunc(self.movieList, self.FilesDropped)
        self.MovieRenamer.dropTarget = self.movieList

        musicHeaders = ["", "Title", "Artists", "Album", "Genre", "Comments"]
        self.WriteHeaderLabels(self.musicReport, musicHeaders)
        self.SetCallbackFunc(self.musicReport, self.FilesDropped)
        self.MusicRenamer.dropTarget = self.musicReport

    def WriteHeaderLabels(self, target, headerLabelList):
        target.headerLabelList = headerLabelList
        target.numCols = len(target.headerLabelList)

        for col in range(target.numCols):
            target.InsertColumn(col, target.headerLabelList[col])

        for col in range(target.numCols):
            target.SetColumnWidth(col, wx.LIST_AUTOSIZE_USEHEADER)

    def FilesDropped(self, filenameDropDict):
        def MovieRenamerTarget(self, target, filesDict):
            pass

        def MusicRenamerTarget(self, target, filesDict):
            pass

        def TVRenamerTarget(self, target, filesDict):
            pass

        def GenreOrgTarget(self, target, filesDict):
            pass

        # A convenience alias :
        dropTarget = self.TheNotebook.CurrentPage.dropTarget  # self.filesDropCtrl.listCtrl
        if dropTarget not in self.FilesAndDirs.keys():
            self.FilesAndDirs[dropTarget] = dict()

        name = dropTarget.name
        if name == "Music List":
            MusicRenamerTarget(self, target=dropTarget ,filesDict=filenameDropDict)
        elif name == "Movie List":
            MovieRenamerTarget(self, target=dropTarget, filesDict=filenameDropDict)
        elif name == "Movie Genre List":
            GenreOrgTarget(self, target=dropTarget, filesDict=filenameDropDict)
        else:
            pass

        # Extract the info from the drop data dictionary.
        pathList = filenameDropDict['pathList']
        commonPathname = filenameDropDict['pathname']
        basenameList = filenameDropDict['basenameList']  # Not used in this method.
        dropCoord = filenameDropDict['coord']  # Not used in this method.

        keys2remove = []
        for key in self.FilesAndDirs[dropTarget].keys():
            if any(self.FilesAndDirs[dropTarget][key]['oldName'] == rem for rem in dropTarget.removed_files):
                keys2remove.append(key)
        for key in keys2remove:
            self.FilesAndDirs[dropTarget].pop(key, None)
            dropTarget.removed_files = []

        for aPath in sorted(pathList):  # May include folders.
            # Keep just files and link files.
            if not os.path.isdir(aPath):
                if (aPath not in self.FilesAndDirs[dropTarget].keys()):
                    self.FilesAndDirs[dropTarget][aPath] = dict()

                    longFormParentPath, basename = os.path.split(aPath)
                    self.FilesAndDirs[dropTarget][aPath]['ext'] = aPath.split('.')[-1]
                    self.FilesAndDirs[dropTarget][aPath]['oldName'] = '.'.join(basename.split('.')[:-1])

                    textTuple = ("", self.FilesAndDirs[dropTarget][aPath]['oldName'], "", "", "", "")
                    dropTarget.WriteTextTuple(textTuple)
        dropTarget.SetColumnWidth(1, wx.LIST_AUTOSIZE)

        for row in range(dropTarget.ItemCount):
            dropTarget.CheckItem(row, True)

        if dropTarget.ItemCount > 0:
            self.generateBttn.Enable(True)

    def SetCallbackFunc(self, target, dropCallbacFunc=None):
        # Create a dropFiles event association for this control.
        #    [ SetDropTarget ] is a built-in method for (all ?) controls.
        self.SetDropTarget(FilesDropTarget(target))

        # Install the callback-function for this class's parent-widget dropFiles-event.
        target.dropFunc = dropCallbacFunc


if __name__=="__main__":
    app = wx.App()
    frame = MainFrame(None)
    frame.Show()
    app.MainLoop()
