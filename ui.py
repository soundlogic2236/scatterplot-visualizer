from visual import *
from visual.controls import *
import wx
import scatterplot
import ui_functions

L = 320
Hgraph = 400
# Create a window. Note that w.win is the wxPython "Frame" (the window).
# window.dwidth and window.dheight are the extra width and height of the window
# compared to the display region inside the window. If there is a menu bar,
# there is an additional height taken up, of amount window.menuheight.
# The default style is wx.DEFAULT_FRAME_STYLE; the style specified here
# does not enable resizing, minimizing, or full-sreening of the window.
w = window(width=2*(L+window.dwidth), height=L+window.dheight+window.menuheight+Hgraph,
           menus=False, title='Widgets',
           style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)

# Place a 3D display widget in the left half of the window.
d = 20
disp = display(window=w, x=d, y=d, width=L*d, height=L*d, background=color.black, center=vector(.5,.5,.5), range = 1)


# Place buttons, radio buttons, a scrolling text object, and a slider
# in the right half of the window. Positions and sizes are given in
# terms of pixels, and pos(0,0) is the upper left corner of the window.
p = w.panel # Refers to the full region of the window in which to place widgets



m = wx.MenuBar()

file_menu = wx.Menu()
view_menu = wx.Menu()
options_menu = wx.Menu()
edit_menu = wx.Menu()

item = file_menu.Append(-1, "Load Data\tCtrl-L", "Load")
w.win.Bind(wx.EVT_MENU, ui_functions.open_file, item)

file_menu.AppendSeparator()

item = file_menu.Append(-1, "Open Plot\tCtrl-O", "Open")

item = file_menu.Append(-1, "Save Plot\tCtrl-S", "Save")

file_menu.AppendSeparator()

item = file_menu.Append(-1, "Export\tCtrl-E", "Export")

file_menu.AppendSeparator()

item = file_menu.Append(-1, "Quit\tCtrl-Q", "Exit")
w.win.Bind(wx.EVT_MENU, w._OnExitApp, item)

item = edit_menu.Append(-1, 'Undo\tCtrl-Z', 'Make box cyan')

item = edit_menu.Append(-1, 'Redo\tCtrl-Y', 'Make box cyan')

edit_menu.AppendSeparator()

item = edit_menu.Append(-1, 'Cut\tCtrl-X', 'Make box cyan')

item = edit_menu.Append(-1, 'Copy\tCtrl-C', 'Make box cyan')

item = edit_menu.Append(-1, 'Paste\tCtrl-V', 'Make box cyan')

edit_menu.AppendSeparator()

item = edit_menu.Append(-1, 'Select All\tCtrl-A', 'Make box cyan')


item = view_menu.Append(-1, 'Frame limits', 'Make box cyan')

item = view_menu.Append(-1, 'Equalise Axes', 'Make box cyan')

item = view_menu.Append(-1, 'Restore Default View', 'Make box cyan')

item = view_menu.Append(-1, 'Show Toolbar', 'Make box cyan')


item = options_menu.Append(-1, 'Titles & Labels', 'Make box cyan')

item = options_menu.Append(-1, 'Axes', 'Make box cyan')
w.win.Bind(wx.EVT_MENU, ui_functions.toggle_axes, item)

item = options_menu.Append(-1, 'Grid', 'Make box cyan')
w.win.Bind(wx.EVT_MENU, ui_functions.toggle_grid, item)

item = options_menu.Append(-1, '3d Grid', 'Make box cyan')
w.win.Bind(wx.EVT_MENU, ui_functions.toggle_grid3d, item)

item = options_menu.Append(-1, 'Data Points', 'Make box cyan')

item = options_menu.Append(-1, 'Export Formats', 'Make box cyan')


m.Append(file_menu, '&File')
m.Append(edit_menu, '&Edit')
m.Append(view_menu, '&View')
m.Append(options_menu, '&Options')


w.win.SetMenuBar(m)

while True:
    rate(100)
