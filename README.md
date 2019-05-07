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
