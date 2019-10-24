import os

def myInterpS(args,x):
  #interpolation for polydata (surface)
  a = 0.
  b = 1.
  return a+b*x

def myInterpV(args,x):
  #interpolation for volume (wavefield)
  a = args.vcrange[0]
  b = args.vcrange[1]
  if args.vlog:
    return a*pow(b/a,x)
  else:
    return a+b*x

def CreateCTF(args, myCtf, myLut,bVolumeOutput=False):
  if bVolumeOutput:
     myColorScale = args.vcolorScale
     myInterp = myInterpV
  else:
     myColorScale = args.colorScale
     myInterp = myInterpS

  ######### volume output: Create the color map  #############
  prefixCP, extCP = os.path.splitext(myColorScale)
  print(prefixCP, extCP)
  if extCP=='.xml':
     #read the color plot as an Xml file
     myCtf.SetColorSpaceToRGB()
     import lxml.etree as ET
     tree = ET.parse(myColorScale)
     root = tree.getroot()
     for el in root.findall('Point'):
        x = float(el.get('x'))
        r = float(el.get('r'))
        g = float(el.get('g'))
        b = float(el.get('b'))
        myCtf.AddRGBPoint(myInterp(args,x), r,g,b)

  elif myColorScale=='Rainbow':
     myCtf.SetColorSpaceToRGB()
     myCtf.AddRGBPoint(myInterp(args,0.00), 0., 0., 1.)
     myCtf.AddRGBPoint(myInterp(args,0.25), 0., 1., 1.)
     myCtf.AddRGBPoint(myInterp(args,0.5), 0., 1., 0.)
     myCtf.AddRGBPoint(myInterp(args,0.75), 1., 1.0, 0.)
     myCtf.AddRGBPoint(myInterp(args,1.), 1., 0., 0.)
  elif myColorScale=='GreyRainbow':
     myCtf.SetColorSpaceToRGB()
     myCtf.AddRGBPoint(myInterp(args,0.), 1., 1., 1.)
     myCtf.AddRGBPoint(myInterp(args,0.005), 1., 1., 1.)
     myCtf.AddRGBPoint(myInterp(args,0.25), 0., 1., 1.)
     myCtf.AddRGBPoint(myInterp(args,0.5), 0., 1., 0.)
     myCtf.AddRGBPoint(myInterp(args,0.75), 1., 1.0, 0.)
     myCtf.AddRGBPoint(myInterp(args,1.), 1., 0., 0.)
  elif myColorScale=='RainbowInv':
     myCtf.SetColorSpaceToRGB()
     myCtf.AddRGBPoint(myInterp(args,0.), 1., 0., 0.)
     myCtf.AddRGBPoint(myInterp(args,0.25), 1., 1.0, 0.)
     myCtf.AddRGBPoint(myInterp(args,0.5), 0., 1., 0.)
     myCtf.AddRGBPoint(myInterp(args,0.75), 0., 1., 1.)
     myCtf.AddRGBPoint(myInterp(args,1.00), 0., 0., 1.)
  elif myColorScale=='SeisSol':
     myCtf.SetColorSpaceToRGB()
     myCtf.AddRGBPoint(myInterp(args,0.), 1., 1., 1.)
     myCtf.AddRGBPoint(myInterp(args,0.25), 0., 1., 1.)
     myCtf.AddRGBPoint(myInterp(args,0.5), 0., 0., 1.)
     myCtf.AddRGBPoint(myInterp(args,0.75), 1., 0.317647, 0.)
     myCtf.AddRGBPoint(myInterp(args,1.), 1., 0., 0.)
  elif myColorScale=='Kaikoura':
     myCtf.SetColorSpaceToRGB()
     myCtf.AddRGBPoint(myInterp(args,0.), 1., 1., 1. )
     myCtf.AddRGBPoint(myInterp(args,0.01), 92./255, 190./255, 215./255)
     myCtf.AddRGBPoint(myInterp(args,1.), 196./255, 119./255, 87./255)
  else:
     myCtf.SetColorSpaceToDiverging()
     myCtf.AddRGBPoint(myInterp(args,0.), 58./256., 76./256., 193./256.)
     myCtf.AddRGBPoint(myInterp(args,0.5), 221./256., 222./256., 222./256.)
     myCtf.AddRGBPoint(myInterp(args,1.), 180./256., 4./256., 38./256.)
  if bVolumeOutput & args.vlog:
     myCtf.SetScaleToLog10()


  #just for the scalar bar
  tableSize = 256
  myLut.SetNumberOfTableValues(tableSize)
  myLut.Build()
  for i in range(0,tableSize):
    rgb = list(myCtf.GetColor(myInterp(args,float(i)/float(tableSize-1))))+[1]
    myLut.SetTableValue(i,rgb)
  #nan to yellow
  #myCtf.SetNanColor(1,1,0)
  myCtf.SetNanColor(0.7,0.7,0.7)
  #myLut.SetNanColor(0.7,0.7,0.7,1)
  myLut.SetNanColor(1,1,1,1)
  return myCtf, myLut
