# This is a scatterplot visualiser. Well, actually it isn't, but it wants to grow up to be one.
# It now visualises data! Yay! It may not have much of a GUI, but it does visualise data!
import csv
import numpy
import visual
import wx
import random

points=[]

min_x=0
max_x=0
min_y=0
max_y=0
min_z=0
max_z=0

min_x_default=0
max_x_default=0
min_y_default=0
max_y_default=0
min_z_default=0
max_z_default=0

x_axis = None
y_axis = None
z_axis = None
axis_ball = None

axis_enabled = False;

grid_faces_enabled = (False,False,False,False,False,False)

grid_interior_enabled = False

grid_faces_grid = [[],[],[],[],[],[]]

grid_interior_lines= []

wireframe_box = None;

def import_datafile(filename):
    global points,min_x_default,max_x_default,min_y_default,max_y_default,min_y_default,max_z_default
    dataset = []
    with open(filename, 'rb') as datafile:
        lines = csv.reader(datafile, delimiter=' ', quotechar='|')
        i = 0
        did_warning=False
        for line in lines:
            dataset.append(parse_line(line))
            i += 1
            if i > 5000 and not did_warning:
                did_warning=True
                warning_box=wx.MessageDialog(None, 'There are over 5000 rows in this dataset. You can try to import it, but it may be slow or crash. Do you wish to continue?', 'Question',
                    wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
                warning_result=warning_box.ShowModal()
                if warning_result==wx.ID_NO:
                    return False
    transposed_set = numpy.transpose(dataset)
    min_x_default = numpy.amin(transposed_set[0])
    max_x_default = numpy.amax(transposed_set[0])
    min_y_default = numpy.amin(transposed_set[1])
    max_y_default = numpy.amax(transposed_set[1])
    min_z_default = numpy.amin(transposed_set[2])
    max_z_default = numpy.amax(transposed_set[2])

    set_view_to_default()

    points = []
    for data in dataset:
        points.append(DataPoint(*data))

    return True

def draw_axes():
    global x_axis,y_axis,z_axis,axis_ball

    if x_axis:
        x_axis.visible=False
        x_axis=None
    if y_axis:
        y_axis.visible=False
        y_axis=None
    if z_axis:
        z_axis.visible=False
        z_axis=None
    if axis_ball:
        axis_ball.visible=False
        axis_ball=None


    if not axis_enabled:
        return
    use_x=min_x!=max_x
    use_y=min_y!=max_y
    use_z=min_z!=max_z

    zero_coord=(min_x / (min_x - max_x),min_y / (min_y - max_y),min_z / (min_z - max_z))

    if use_x:
        x_axis = visual.arrow(pos=zero_coord, axis=(.3,0,0), shaftwidth=0.01, color=visual.color.red)
    if use_y:
        y_axis = visual.arrow(pos=zero_coord, axis=(0,.3,0), shaftwidth=0.01, color=visual.color.green)
    if use_z:
        z_axis = visual.arrow(pos=zero_coord, axis=(0,0,.3), shaftwidth=0.01, color=visual.color.blue)
    axis_ball = visual.sphere(pos=zero_coord, radius=.02, color=visual.color.yellow)

def make_box():
    global wireframe_box
    if not wireframe_box:
        wireframe_box=[]
        wireframe_box.append(visual.curve(pos=[(0,0,0),(0,0,1)],color=visual.color.white))
        wireframe_box.append(visual.curve(pos=[(0,0,0),(0,1,0)],color=visual.color.white))
        wireframe_box.append(visual.curve(pos=[(0,0,0),(1,0,0)],color=visual.color.white))
        wireframe_box.append(visual.curve(pos=[(0,1,0),(0,1,1)],color=visual.color.white))
        wireframe_box.append(visual.curve(pos=[(0,1,0),(1,1,0)],color=visual.color.white))
        wireframe_box.append(visual.curve(pos=[(0,0,1),(0,1,1)],color=visual.color.white))
        wireframe_box.append(visual.curve(pos=[(0,0,1),(1,0,1)],color=visual.color.white))
        wireframe_box.append(visual.curve(pos=[(1,0,0),(1,1,0)],color=visual.color.white))
        wireframe_box.append(visual.curve(pos=[(1,0,0),(1,0,1)],color=visual.color.white))
        wireframe_box.append(visual.curve(pos=[(1,1,1),(1,1,0)],color=visual.color.white))
        wireframe_box.append(visual.curve(pos=[(1,1,1),(0,1,1)],color=visual.color.white))
        wireframe_box.append(visual.curve(pos=[(1,1,1),(1,0,1)],color=visual.color.white))

def make_grid_interior():
    global grid_interior_lines
    gridlines = 20
    zero_coord=(min_x / (min_x - max_x),min_y / (min_y - max_y),min_z / (min_z - max_z))
    grid_length_x=(max_x-min_x)/gridlines
    grid_length_y=(max_y-min_y)/gridlines
    grid_length_z=(max_z-min_z)/gridlines
    pre_zero_lengths_x=numpy.floor(zero_coord[0]*gridlines)
    pre_zero_lengths_y=numpy.floor(zero_coord[1]*gridlines)
    pre_zero_lengths_z=numpy.floor(zero_coord[2]*gridlines)

    for gridline in grid_interior_lines:
        gridline.visible=False
    grid_interior_lines=[]

    if grid_interior_enabled:
        for i in range(gridlines):
            for j in range(gridlines):
                coord1=zero_coord[0]+(i-pre_zero_lengths_x)*1/gridlines
                coord2=zero_coord[1]+(j-pre_zero_lengths_y)*1/gridlines
                grid_interior_lines.append(visual.curve(pos=[(coord1,coord2,0),(coord1,coord2,1)]))
        for i in range(gridlines):
            for j in range(gridlines):
                coord1=zero_coord[0]+(i-pre_zero_lengths_x)*1/gridlines
                coord2=zero_coord[2]+(j-pre_zero_lengths_z)*1/gridlines
                grid_interior_lines.append(visual.curve(pos=[(coord1,0,coord2),(coord1,1,coord2)]))
        for i in range(gridlines):
            for j in range(gridlines):
                coord1=zero_coord[1]+(i-pre_zero_lengths_y)*1/gridlines
                coord2=zero_coord[2]+(j-pre_zero_lengths_z)*1/gridlines
                grid_interior_lines.append(visual.curve(pos=[(0,coord1,coord2),(1,coord1,coord2)]))


def make_grid_faces():
    global grid_faces_grid
    gridlines = 20
    zero_coord=(min_x / (min_x - max_x),min_y / (min_y - max_y),min_z / (min_z - max_z))
    grid_length_x=(max_x-min_x)/gridlines
    grid_length_y=(max_y-min_y)/gridlines
    grid_length_z=(max_z-min_z)/gridlines
    pre_zero_lengths_x=numpy.floor(zero_coord[0]*gridlines)
    pre_zero_lengths_y=numpy.floor(zero_coord[1]*gridlines)
    pre_zero_lengths_z=numpy.floor(zero_coord[2]*gridlines)

    for grid in grid_faces_grid:
        for gridline in grid:
            gridline.visible=False
    grid_faces_grid=[[],[],[],[],[],[]]

    for i in range(5):
        if grid_faces_enabled[i]:
            make_grid_face(i,gridlines,zero_coord,grid_length_x,grid_length_y,grid_length_z,pre_zero_lengths_x,pre_zero_lengths_y,pre_zero_lengths_z)

def make_grid_face(face_num,gridlines,zero_coord,grid_length_x,grid_length_y,grid_length_z,pre_zero_lengths_x,pre_zero_lengths_y,pre_zero_lengths_z):
    global grid_faces_grid
    if face_num==0:
        for i in range(gridlines):
            coord=zero_coord[0]+(i-pre_zero_lengths_x)*1/gridlines
            grid_faces_grid[0].append(visual.curve(pos=[(coord,0,0),(coord,1,0)]))
        for i in range(gridlines):
            coord=zero_coord[1]+(i-pre_zero_lengths_y)*1/gridlines
            grid_faces_grid[0].append(visual.curve(pos=[(0,coord,0),(1,coord,0)]))

    if face_num==1:
        for i in range(gridlines):
            coord=zero_coord[0]+(i-pre_zero_lengths_x)*1/gridlines
            grid_faces_grid[1].append(visual.curve(pos=[(coord,0,1),(coord,1,1)]))
        for i in range(gridlines):
            coord=zero_coord[1]+(i-pre_zero_lengths_y)*1/gridlines
            grid_faces_grid[1].append(visual.curve(pos=[(0,coord,1),(1,coord,1)]))

    if face_num==2:
        for i in range(gridlines):
            coord=zero_coord[0]+(i-pre_zero_lengths_x)*1/gridlines
            grid_faces_grid[2].append(visual.curve(pos=[(coord,0,0),(coord,0,1)]))
        for i in range(gridlines):
            coord=zero_coord[2]+(i-pre_zero_lengths_z)*1/gridlines
            grid_faces_grid[2].append(visual.curve(pos=[(0,0,coord),(1,0,coord)]))

    if face_num==3:
        for i in range(gridlines):
            coord=zero_coord[0]+(i-pre_zero_lengths_x)*1/gridlines
            grid_faces_grid[3].append(visual.curve(pos=[(coord,1,0),(coord,1,1)]))
        for i in range(gridlines):
            coord=zero_coord[2]+(i-pre_zero_lengths_z)*1/gridlines
            grid_faces_grid[3].append(visual.curve(pos=[(0,1,coord),(1,1,coord)]))

    if face_num==4:
        for i in range(gridlines):
            coord=zero_coord[1]+(i-pre_zero_lengths_y)*1/gridlines
            grid_faces_grid[4].append(visual.curve(pos=[(0,coord,0),(0,coord,1)]))
        for i in range(gridlines):
            coord=zero_coord[2]+(i-pre_zero_lengths_z)*1/gridlines
            grid_faces_grid[4].append(visual.curve(pos=[(0,0,coord),(0,1,coord)]))

    if face_num==5:
        for i in range(gridlines):
            coord=zero_coord[1]+(i-pre_zero_lengths_y)*1/gridlines
            grid_faces_grid[5].append(visual.curve(pos=[(1,coord,0),(1,coord,1)]))
        for i in range(gridlines):
            coord=zero_coord[2]+(i-pre_zero_lengths_z)*1/gridlines
            grid_faces_grid[5].append(visual.curve(pos=[(1,0,coord),(1,1,coord)]))


def render():
    make_points()
    draw_axes()
    make_box()
    make_grid_faces()
    make_grid_interior()


def set_view_to_default():
    global min_x,max_x,min_y,max_y,min_z,max_z
    min_x=min_x_default
    max_x=max_x_default
    min_y=min_y_default
    max_y=max_y_default
    min_z=min_z_default
    max_z=max_z_default

def make_points():
    global points,min_x,max_x,min_y,max_y,min_y,max_z
    for point in points:
        point.make_on_screen(min_x, max_x, min_y, max_y, min_z, max_z)

def parse_line(line):
    return [float(line[0]), float(line[1]), float(line[2]), random.random(), random.random(), random.random(), random.random()*4]


class DataPoint:
    x = 0
    y = 0
    z = 0
    r = 0
    g = 0
    b = 0
    size = 0
    visual_point = None

    def __init__(self, x, y, z, r, g, b, size):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.g = g
        self.b = b
        self.size = size

    def make_on_screen(self, min_x, max_x, min_y, max_y, min_z, max_z):
        # Convert it to coordinates between 0 and 1 so everything fits properly and we know where everything is

        # Clear our point if it exists
        self.clear_point()

        # Check if each axis is used by the view
        use_x=min_x!=max_x
        use_y=min_y!=max_y
        use_z=min_z!=max_z

        #Check if we are visible
        visible = True
        if not (use_x or min_x==self.x):
            visible=False
        if not (use_y or min_y==self.y):
            visible=False
        if not (use_y or min_y==self.y):
            visible=False

        if not visible:
            return

        if use_x:
            box_x = (self.x - min_x) / (max_x - min_x)
        else:
            box_x = 0
        if use_y:
            box_y = (self.y - min_y) / (max_y - min_y)
        else:
            box_y = 0
        if use_z:
            box_z = (self.z - min_z) / (max_z - min_z)
        else:
            box_z = 0
        # Make our point
        self.visual_point = visual.points(pos=[box_x, box_y, box_z], size=self.size, shape="round", color=(self.r, self.g, self.b))

    def clear_point(self):
        if self.visual_point:
            self.visual_point.visible = False
