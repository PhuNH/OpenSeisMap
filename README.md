# OpenSeisMap
OSM data > PostGIS

Tile expiry methods
Rendering is the process that generates tiles by taking as input:
- data to render: a database or file(s)
- how to render: styles and rules
Rendering daemons:
- mod_tile and renderd: OSM's servers
    mod_tile is a custom Apache module, used to serve tiles and request the rendering of tiles when they have changed or are not yet available.
    renderd is a rendering backend, taking requests from mod_tile, queueing requests in case there are many at the same time, and rendering tiles. Under the hood this calls mapnik.
- tilecache: tiledrawer.com

Zoom level:
- Low levels are from 0 to 8. They are "below" 9.
- Medium levels are from 9 to 12. They are "below" 13.
- High levels are the rest.

Meta tiles:
- Instead of dealing with tiles typically of size 256*256 pixel, mod_tile deals with areas of 8x8 tiles. An area like this is called a meta tile.
- Reasons: rendering efficiency, label placement simplication, and storage and transfer efficiency.
