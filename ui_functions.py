from visual import *
from visual.controls import *
import wx
import scatterplot
import random

def open_file(evt):
	open_dialog=wx.FileDialog(None,"Open Dataset","","","CSV files (*.csv)|*.csv|Any files (*)|*",style=wx.FD_OPEN)
	if open_dialog.ShowModal()==wx.ID_OK:
		filename=open_dialog.GetPath()
		scatterplot.import_datafile(filename)
	scatterplot.render()

def toggle_axes(evt):
    scatterplot.axis_enabled=not scatterplot.axis_enabled
    scatterplot.render()

def toggle_grid(evt):
	scatterplot.grid_faces_enabled = (bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)))
	scatterplot.render()

def toggle_grid3d(evt):
	scatterplot.grid_interior_enabled = not scatterplot.grid_interior_enabled
	scatterplot.render()


