# OpenSeisMap
OSM data > PostGIS

Tile expiry methods

Rendering is the process that generates tiles by taking as input:
- data to render: a database or file(s)
- how to render: styles and rules

Rendering daemons:
- mod\_tile and renderd: OSM's servers  
mod\_tile is a custom Apache module, used to serve tiles and request the rendering of tiles when they have changed or are not yet available.  
renderd is a rendering backend, taking requests from mod\_tile, queueing requests in case there are many at the same time, and rendering tiles. Under the hood this calls mapnik.
- tilecache: tiledrawer.com

Zoom level:
- Low levels are from 0 to 8. They are "below" 9.
- Medium levels are from 9 to 12. They are "below" 13.
- High levels are the rest.

Meta tiles:
- Instead of dealing with tiles typically of size 256\*256 pixel, mod\_tile deals with areas of 8x8 tiles. An area like this is called a meta tile.
- Reasons: rendering efficiency, label placement simplication, and storage and transfer efficiency.

XdmfConverter: Create a shapefile from an Xdmf file
- Input: Xdmf file path, data name, time step, output file path, epsg code (int).
- Can output vertex data and cell data to 2 different files. Default to work on cell data.  
- For vertex data: Create a 'vertices' layer, each feature in the layer has 2 attributes 'X' and 'Y'.  
For cell data: Create a 'cells' layer, in which each feature has 1 attribute 'Data'.
- Make use of vtkQuadricDecimation and pymesh.map_face_attribute

PyMesh build:
- Set $CC and $CXX to files in /usr/bin.
- Change links of libs in env to the local libs: libstdc++, libgomp (still there are warnings about libboost and libgmp).
- After running cmake in the main project, change in CMakeCache.txt: PYTHON\_EXECUTABLE:FILEPATH, PYTHON\_LIBRARY:FILEPATH; and run cmake again.

TileRenderer: sample Python code to create a tile (image) of the shapefile

GeoFunctions: helper functions

shp.conf:

environment.yml:

templates:
