from __future__ import print_function
from argparse import Namespace
import numpy as np
import vtk
from vtk.util import numpy_support
import pymesh
from createCTF import CreateCTF


def unstr_to_poly_data(xyz, connect, attribute):
    points = vtk.vtkPoints()
    points.SetData(numpy_support.numpy_to_vtk(xyz))

    polys = vtk.vtkCellArray()
    ndim1, ndim2 = connect.shape
    connect2 = np.zeros((ndim1, ndim2+1), dtype=np.int64)
    # number of points in the cell
    connect2[:, 0] = ndim2
    connect2[:, 1:] = connect
    polys.SetCells(ndim1, numpy_support.numpy_to_vtkIdTypeArray(connect2))

    scalars = numpy_support.numpy_to_vtk(num_array=attribute, deep=True, array_type=vtk.VTK_FLOAT)

    poly_data = vtk.vtkPolyData()
    poly_data.SetPoints(points)
    poly_data.SetPolys(polys)
    poly_data.GetCellData().SetScalars(scalars)
    poly_data.Modified()
    return poly_data


def draw(poly_data, color_scale='Diverging', write_file=False, file_name='unstr.png'):
    ctf = vtk.vtkColorTransferFunction()
    lut = vtk.vtkLookupTable()
    args = Namespace(colorScale=color_scale, vlog=False)
    ctf, lut = CreateCTF(args, ctf, lut)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(poly_data)

    mapper.SetLookupTable(lut)
    data_array = poly_data.GetCellData().GetScalars()
    if data_array is not None:
        np_attribute = numpy_support.vtk_to_numpy(data_array)
        min_val = np_attribute.min()
        max_val = np_attribute.max()
    else:
        min_val = 0
        max_val = 1
    mapper.SetScalarRange(min_val, max_val)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetSpecular(0.3)

    camera = vtk.vtkCamera()
    camera.SetPosition(0, 0e3, 20e3)
    camera.SetFocalPoint(0, 0e3, -10e3)
    camera.Zoom(1.0)

    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(0, 0, 0)
    renderer.SetActiveCamera(camera)
    renderer.ResetCamera()

    light_kit = vtk.vtkLightKit()
    light_kit.MaintainLuminanceOn()
    light_kit.SetKeyLightIntensity(0.75)
    light_kit.SetKeyLightWarmth(0.60)
    light_kit.SetFillLightWarmth(0.4)
    light_kit.SetBackLightWarmth(0.5)
    light_kit.SetHeadLightWarmth(0.5)
    light_kit.AddLightsToRenderer(renderer)

    ren_win = vtk.vtkRenderWindow()
    ren_win.AddRenderer(renderer)
    ren_win.SetSize(1300, 900)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(ren_win)
    ren_win.Render()
    iren.Start()

    if write_file:
        render_large = vtk.vtkRenderLargeImage()
        render_large.SetInput(renderer)
        render_large.SetMagnification(1)
        writer = vtk.vtkPNGWriter()
        writer.SetInputConnection(render_large.GetOutputPort())
        writer.SetFileName('../../output-vtk/' + file_name)
        writer.Write()
        print('done writing %s' %file_name)
        del render_large
        del writer


def clean(poly_data):
    cleaner = vtk.vtkCleanPolyData()
    cleaner.SetInputData(poly_data)
    cleaner.Update()

    cleaned = vtk.vtkPolyData()
    cleaned.ShallowCopy(cleaner.GetOutput())
    print("Cleaned:", cleaned.GetNumberOfPoints(), "points", cleaned.GetNumberOfPolys(), "polygons")
    # draw(cleaned, color_scale='Rainbow', write_file=True, file_name='before.png')
    return cleaned
    
    
def decimate(poly_data, reduction, data_is_big):
    decimator = None
    #decimator = vtk.vtkDecimatePro()
    #decimator.PreserveTopologyOn()
    #decimator.SplittingOff()
    #decimator.BoundaryVertexDeletionOff()
    #decimator.SetMaximumError(vtk.VTK_DOUBLE_MAX)
    if data_is_big:
        decimator = vtk.vtkQuadricClustering()
        decimator.SetNumberOfXDivisions(1024)
        decimator.SetNumberOfYDivisions(1024)
        decimator.SetNumberOfZDivisions(1024)
    else:
        decimator = vtk.vtkQuadricDecimation()
        decimator.SetTargetReduction(reduction)
    decimator.SetInputData(poly_data)
    decimator.Update()

    decimated = vtk.vtkPolyData()
    decimated.ShallowCopy(decimator.GetOutput())
    print("Decimated:", decimated.GetNumberOfPoints(), "points", decimated.GetNumberOfPolys(), "polygons, by ", type(decimator))
    # draw(decimated, color_scale='Rainbow', write_file=True, file_name='after.png')
    return decimated


def poly_data_to_unstr(poly_data):
    points = numpy_support.vtk_to_numpy(poly_data.GetPoints().GetData())

    polys = poly_data.GetPolys()
    ndim1 = poly_data.GetNumberOfPolys()
    connect = numpy_support.vtk_to_numpy(polys.GetData()).reshape((ndim1, -1))
    connect = connect[:, 1:]

    data_array = poly_data.GetCellData().GetScalars()
    if data_array is not None:
        np_attribute = numpy_support.vtk_to_numpy(data_array)
    else:
        np_attribute = None

    return points, connect, np_attribute


def map_cell_attribute(xyz, connect, attribute, decimated):
    mesh = pymesh.form_mesh(xyz, connect)
    mesh.add_attribute("face_scalar")
    mesh.set_attribute("face_scalar", attribute)

    decimated_xyz, decimated_connect, _ = poly_data_to_unstr(decimated)
    decimated_mesh = pymesh.form_mesh(decimated_xyz, decimated_connect)

    pymesh.map_face_attribute(mesh, decimated_mesh, "face_scalar")
    print('attributes in new mesh mapped')
    return decimated_xyz, decimated_connect, decimated_mesh.get_attribute("face_scalar")
