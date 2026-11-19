/* Minecraft Nether/Overworld route planner — core logic (browser + Node). */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.MCRouter = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const NETHER_SCALE = 8;

  // Approximate travel speeds in blocks/second (straight line, no obstacles).
  const SPEEDS = {
    walk:        { label: 'Walk',                       bps: 4.317 },
    sprint:      { label: 'Sprint',                     bps: 5.612 },
    sprintjump:  { label: 'Sprint-jump',                bps: 7.127 },
    boat:        { label: 'Boat on water',              bps: 8.0 },
    boatice:     { label: 'Boat on packed/regular ice', bps: 40 },
    boatblue:    { label: 'Boat on blue ice',           bps: 72.7 },
    elytra:      { label: 'Elytra + rockets (approx.)', bps: 33.5 },
  };

  const dist = (a, b) => Math.hypot(a.x - b.x, a.z - b.z);

  /**
   * Plan the fastest route between start and end using Dijkstra over a small
   * graph of Overworld ('ow') and Nether ('ne') nodes.
   *
   * opts: {
   *   start:{x,z}, end:{x,z}            Overworld coordinates
   *   owSpeed, neSpeed                  blocks/second in each dimension
   *   portalWait                        seconds standing in a portal (4 in survival)
   *   buildTime                         seconds to build+light a new portal
   *   allowBuild                        may build new portals at start / end
   *   portals: [{dim:'ow'|'ne', x, z}]  existing portals (coordinates in that dimension)
   * }
   */
  function planRoute(opts) {
    const { start, end, owSpeed, neSpeed } = opts;
    const portalWait = opts.portalWait ?? 4;
    const buildTime = opts.buildTime ?? 60;
    const allowBuild = opts.allowBuild !== false;
    const portals = opts.portals || [];

    const nodes = [];
    const edges = []; // explicit portal edges: [i, j, cost, kind, note]
    const add = (id, dim, x, z, label) => { nodes.push({ id, dim, x, z, label }); return nodes.length - 1; };

    const iA = add('A', 'ow', start.x, start.z, 'Start');
    const iB = add('B', 'ow', end.x, end.z, 'Destination');

    if (allowBuild) {
      const nA = add('newA', 'ne', start.x / NETHER_SCALE, start.z / NETHER_SCALE, 'New Nether side of start portal');
      const nB = add('newB', 'ne', end.x / NETHER_SCALE, end.z / NETHER_SCALE, 'New Nether portal near destination');
      // Build in the Overworld at start (Nether side auto-generates);
      // build in the Nether at end/8 (Overworld side auto-generates near the destination).
      edges.push([iA, nA, buildTime + portalWait, 'build', 'Build portal at start']);
      edges.push([iB, nB, buildTime + portalWait, 'build', 'Build portal in Nether above destination']);
    }

    portals.forEach((p, k) => {
      const ow = p.dim === 'ne' ? { x: p.x * NETHER_SCALE, z: p.z * NETHER_SCALE } : { x: p.x, z: p.z };
      const ne = p.dim === 'ne' ? { x: p.x, z: p.z } : { x: p.x / NETHER_SCALE, z: p.z / NETHER_SCALE };
      const a = add('p' + k + 'ow', 'ow', ow.x, ow.z, 'Existing portal ' + (k + 1) + ' (Overworld)');
      const b = add('p' + k + 'ne', 'ne', ne.x, ne.z, 'Existing portal ' + (k + 1) + ' (Nether)');
      edges.push([a, b, portalWait, 'portal', 'Use existing portal ' + (k + 1)]);
    });

    const n = nodes.length;
    const adj = Array.from({ length: n }, () => []);
    for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
      if (i !== j && nodes[i].dim === nodes[j].dim) {
        const d = dist(nodes[i], nodes[j]);
        const speed = nodes[i].dim === 'ow' ? owSpeed : neSpeed;
        adj[i].push({ to: j, cost: d / speed, kind: 'travel', dist: d });
      }
    }
    for (const [i, j, c, kind, note] of edges) {
      adj[i].push({ to: j, cost: c, kind, note });
      adj[j].push({ to: i, cost: c, kind, note: 'Step through portal' });
    }

    // Dijkstra (dense graph, n is tiny).
    const best = Array(n).fill(Infinity), prev = Array(n).fill(null), done = Array(n).fill(false);
    best[iA] = 0;
    for (let it = 0; it < n; it++) {
      let u = -1;
      for (let i = 0; i < n; i++) if (!done[i] && (u < 0 || best[i] < best[u])) u = i;
      if (u < 0 || best[u] === Infinity) break;
      done[u] = true;
      for (const e of adj[u]) {
        if (best[u] + e.cost < best[e.to]) { best[e.to] = best[u] + e.cost; prev[e.to] = { from: u, edge: e }; }
      }
    }

    const steps = [];
    for (let v = iB; prev[v]; v = prev[v].from) steps.unshift({ ...prev[v].edge, from: nodes[prev[v].from], to: nodes[v] });

    const directDist = dist(nodes[iA], nodes[iB]);
    const directTime = directDist / owSpeed;
    return {
      time: best[iB], directTime, directDist,
      saved: directTime - best[iB],
      steps, usesNether: steps.some(s => s.kind !== 'travel'),
    };
  }

  function fmtTime(sec) {
    if (!isFinite(sec)) return '—';
    sec = Math.round(sec);
    const h = Math.floor(sec / 3600), m = Math.floor((sec % 3600) / 60), s = sec % 60;
    return (h ? h + 'h ' : '') + (h || m ? m + 'm ' : '') + s + 's';
  }

  return { NETHER_SCALE, SPEEDS, planRoute, fmtTime, dist };
});
