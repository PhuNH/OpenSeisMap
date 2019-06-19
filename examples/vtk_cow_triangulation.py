import vtk

colors = vtk.vtkNamedColors()
    
reader = vtk.vtkXMLPolyDataReader()
reader.SetFileName("../VTKData/Data/cow.vtp")
reader.Update()

filter = vtk.vtkTriangleFilter()
filter.SetInputConnection(reader.GetOutputPort())
filter.Update()

decimator = vtk.vtkDecimatePro()
decimator.SetInputData(filter.GetOutput())
decimator.SetTargetReduction(0.5)
decimator.PreserveTopologyOn()
decimator.Update()

mapper1 = vtk.vtkPolyDataMapper()
mapper1.SetInputConnection(reader.GetOutputPort())
actor1 = vtk.vtkActor()
actor1.SetMapper(mapper1)

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(decimator.GetOutputPort())
actor = vtk.vtkActor()
actor.SetMapper(mapper)

camera = vtk.vtkCamera()
camera.SetPosition(0, -1, 0)
camera.SetFocalPoint(0, 0, 0)
camera.SetViewUp(0, 0, 1)
camera.Elevation(300)
camera.Azimuth(30)

leftRen = vtk.vtkRenderer()
leftRen.AddActor(actor1)
leftRen.SetViewport(0.0, 0.0, 0.5, 1.0)
leftRen.SetBackground(colors.GetColor3d('Navy'))
leftRen.SetActiveCamera(camera)

rightRen = vtk.vtkRenderer()
rightRen.AddActor(actor)
rightRen.SetViewport(0.5, 0.0, 1.0, 1.0)
rightRen.SetBackground(colors.GetColor3d('Green'))
rightRen.SetActiveCamera(camera)

renWin = vtk.vtkRenderWindow()
renWin.SetSize(1200, 600)
renWin.AddRenderer(leftRen)
renWin.AddRenderer(rightRen)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()
    
renWin.Render()
iren.Start()
