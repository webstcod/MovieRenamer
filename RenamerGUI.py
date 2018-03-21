# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jan 23 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

from customClasses import CustomCheckListReport
import wx
import wx.xrc


###########################################################################
## Class MainFrame
###########################################################################

class MainFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(872, 536), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        self.MenuBar = wx.MenuBar(0)
        self.SetMenuBar(self.MenuBar)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.TheNotebook = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.MovieRenamer = wx.Panel(self.TheNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.movieList = CustomCheckListReport(self.MovieRenamer, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                               wx.LC_REPORT | wx.LC_SINGLE_SEL)
        mainSizer.Add(self.movieList, 1, wx.ALL | wx.EXPAND, 5)

        bttnSizer = wx.BoxSizer(wx.HORIZONTAL)

        bttnSizer.Add((0, 0), 1, wx.EXPAND, 5)

        self.generateBttn = wx.Button(self.MovieRenamer, wx.ID_ANY, u"Generate", wx.DefaultPosition, wx.DefaultSize, 0)
        bttnSizer.Add(self.generateBttn, 0, wx.ALL, 5)

        bttnSizer.Add((0, 0), 1, wx.EXPAND, 5)

        self.renameBttn = wx.Button(self.MovieRenamer, wx.ID_ANY, u"Rename", wx.DefaultPosition, wx.DefaultSize, 0)
        bttnSizer.Add(self.renameBttn, 0, wx.ALL, 5)

        mainSizer.Add(bttnSizer, 0, wx.EXPAND, 5)

        self.MovieRenamer.SetSizer(mainSizer)
        self.MovieRenamer.Layout()
        mainSizer.Fit(self.MovieRenamer)
        self.TheNotebook.AddPage(self.MovieRenamer, u"Movie Renamer", False)
        self.GenreOrganizer = wx.Panel(self.TheNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                       wx.TAB_TRAVERSAL)
        bSizer12 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer13 = wx.BoxSizer(wx.VERTICAL)

        moviesCheckListChoices = []
        self.moviesCheckList = wx.CheckListBox(self.GenreOrganizer, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                               moviesCheckListChoices, 0)
        bSizer13.Add(self.moviesCheckList, 1, wx.ALL | wx.EXPAND, 5)

        self.browse4MoviesBttn = wx.Button(self.GenreOrganizer, wx.ID_ANY, u"Browse", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        bSizer13.Add(self.browse4MoviesBttn, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer12.Add(bSizer13, 1, wx.EXPAND, 5)

        bSizer14 = wx.BoxSizer(wx.VERTICAL)

        self.genreOutDirPicker = wx.DirPickerCtrl(self.GenreOrganizer, wx.ID_ANY, wx.EmptyString, u"Select a folder",
                                                  wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE)
        bSizer14.Add(self.genreOutDirPicker, 0, wx.ALL | wx.EXPAND, 5)

        bSizer14.Add((0, 0), 1, wx.EXPAND, 5)

        bSizer15 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer15.Add((0, 0), 1, wx.EXPAND, 5)

        self.generateGenresBttn = wx.Button(self.GenreOrganizer, wx.ID_ANY, u"Generate", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        bSizer15.Add(self.generateGenresBttn, 0, wx.ALL, 5)

        bSizer14.Add(bSizer15, 0, wx.EXPAND, 5)

        bSizer12.Add(bSizer14, 1, wx.EXPAND, 5)

        self.GenreOrganizer.SetSizer(bSizer12)
        self.GenreOrganizer.Layout()
        bSizer12.Fit(self.GenreOrganizer)
        self.TheNotebook.AddPage(self.GenreOrganizer, u"Genre Setup", False)
        self.MusicRenamer = wx.Panel(self.TheNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        mainSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.musicReport = CustomCheckListReport(self.MusicRenamer, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                                 wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.musicReport.SetToolTip(u"Drag and drop your files here!")

        mainSizer1.Add(self.musicReport, 1, wx.ALL | wx.EXPAND, 5)

        bttnSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        bttnSizer1.Add((0, 0), 1, wx.EXPAND, 5)

        self.gatherBttn = wx.Button(self.MusicRenamer, wx.ID_ANY, u"Gather Data", wx.DefaultPosition, wx.DefaultSize, 0)
        bttnSizer1.Add(self.gatherBttn, 0, wx.ALL, 5)

        bttnSizer1.Add((0, 0), 1, wx.EXPAND, 5)

        self.exectueBttn = wx.Button(self.MusicRenamer, wx.ID_ANY, u"Execute", wx.DefaultPosition, wx.DefaultSize, 0)
        bttnSizer1.Add(self.exectueBttn, 0, wx.ALL, 5)

        mainSizer1.Add(bttnSizer1, 0, wx.EXPAND, 5)

        self.MusicRenamer.SetSizer(mainSizer1)
        self.MusicRenamer.Layout()
        mainSizer1.Fit(self.MusicRenamer)
        self.TheNotebook.AddPage(self.MusicRenamer, u"Music Renamer", False)
        self.TVRenamer = wx.Panel(self.TheNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.TheNotebook.AddPage(self.TVRenamer, u"TV Renamer", False)

        bSizer1.Add(self.TheNotebook, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        self.StatusBar = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)

        self.Centre(wx.BOTH)

    def __del__(self):
        pass


