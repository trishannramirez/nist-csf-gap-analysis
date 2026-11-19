# Minecraft Nether Route Planner

Browser app that finds the fastest route between two Overworld points, deciding
whether Nether portals (1 Nether block = 8 Overworld blocks) beat walking.

Open `index.html` in a browser. Logic lives in `router.js` (Dijkstra over
Overworld/Nether nodes); run `node test.js` for tests.

Models: travel speed per dimension, portal wait, portal build time, optional
existing portals. Not modelled: terrain, Y level, portal link-radius quirks.
