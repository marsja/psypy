# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 13:32:56 2015

@author: erik
"""

class Window():

    def createDlg(self):
        from psychopy import gui
        myDlg = gui.Dlg(title="Experiment")
        myDlg.addText('Subject info')
        myDlg.addField('Name:')
        myDlg.addField('Age:', 21)
        myDlg.addText('Experiment Info')
        myDlg.addField('Grating Ori:',45)
        myDlg.addField('Group:', choices=["Test", "Control"])
        myDlg.show()  # show dialog and wait for OK or Cancel
        if myDlg.OK:  # then the user pressed OK
            thisInfo = myDlg.data
            print thisInfo
        else:
            print 'user cancelled'
            
import wx


class Example(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs) 
            
        self.InitUI()
        
    def InitUI(self):    

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)
        
        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)

        self.SetSize((300, 200))
        self.SetTitle('Experiment')
        self.Centre()
        self.Show(True)
        
    def OnQuit(self, e):
        self.Close()

def main():
    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()