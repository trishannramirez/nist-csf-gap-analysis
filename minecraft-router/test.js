const assert = require('assert');
const { planRoute } = require('./router');
const base = { owSpeed: 5.612, neSpeed: 5.612, portalWait: 4, buildTime: 60 };

// Long trip: Nether should win by a lot.
let r = planRoute({ ...base, start: { x: 0, z: 0 }, end: { x: 10000, z: 0 } });
assert(r.usesNether && r.time < r.directTime / 3, 'long trip uses Nether');
assert.strictEqual(Math.round(r.time), Math.round(2 * 64 + 1250 / 5.612));

// Short trip: walking wins.
r = planRoute({ ...base, start: { x: 0, z: 0 }, end: { x: 200, z: 0 } });
assert(!r.usesNether && Math.abs(r.time - r.directTime) < 1e-9, 'short trip walks');

// Existing portals avoid build cost.
r = planRoute({ ...base, start: { x: 0, z: 0 }, end: { x: 10000, z: 0 }, allowBuild: false,
  portals: [{ dim: 'ow', x: 0, z: 0 }, { dim: 'ow', x: 10000, z: 0 }] });
assert(r.usesNether && Math.round(r.time) === Math.round(2 * 4 + 1250 / 5.612));

// No build, no portals: forced direct.
r = planRoute({ ...base, start: { x: 0, z: 0 }, end: { x: 10000, z: 0 }, allowBuild: false });
assert(!r.usesNether);
console.log('all tests passed');
