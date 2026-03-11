/**
 * Football API Dashboard — script.js
 * ─────────────────────────────────────────────────────────────────
 * Architecture:
 *   1. CONFIG         — API base URL and section definitions
 *   2. STATE          — In-memory cache of fetched data
 *   3. renderTable()  — Generic table builder
 *   4. load*()        — Per-section fetch + render functions
 *   5. filterTable()  — Client-side live search (no extra API call)
 *   6. Collapsibles   — Toggle show/hide per section
 *   7. Init           — Wire up events and kick off initial loads
 * ─────────────────────────────────────────────────────────────────
 */

/* ── 1. CONFIG ─────────────────────────────────────────────────── */

const API_BASE = "http://127.0.0.1:8000/api";

// Section definitions — extend here to add new sections later
const SECTIONS = {
  teams:   { countId: "teams-count",   containerId: "teams-container" },
  players: { countId: "players-count", containerId: "players-container" },
  matches: { countId: "matches-count", containerId: "matches-container" },
  stats:   { countId: "stats-count",   containerId: "stats-container" },
};


/* ── 2. STATE ──────────────────────────────────────────────────── */

// Cache all fetched rows so live search filters locally without re-fetching
const state = {
  teams:   [],
  players: [],
  matches: [],
  stats:   [],
};


/* ── 3. RENDER HELPERS ─────────────────────────────────────────── */

/**
 * renderTable(containerId, headers, rows)
 * Builds an HTML table and injects it into a container div.
 *
 * @param {string}   containerId  - id of the wrapper div
 * @param {string[]} headers      - array of column header labels
 * @param {Array[]}  rows         - array of cell-value arrays (one per row)
 */
function renderTable(containerId, headers, rows) {
  const container = document.getElementById(containerId);
  if (!container) return;

  if (rows.length === 0) {
    container.innerHTML = `<div class="empty-state">No results found.</div>`;
    return;
  }

  // Build <thead>
  const headCells = headers.map(h => `<th>${h}</th>`).join("");

  // Build <tbody> — each cell value is escaped to prevent XSS
  const bodyRows = rows.map(row => {
    const cells = row.map(cell => `<td>${escapeHtml(String(cell ?? "—"))}</td>`).join("");
    return `<tr>${cells}</tr>`;
  }).join("");

  container.innerHTML = `
    <table>
      <thead><tr>${headCells}</tr></thead>
      <tbody>${bodyRows}</tbody>
    </table>`;
}

/** Minimal HTML escaper — prevents injected HTML from API data */
function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

/** Update the count badge next to a section heading */
function setCount(sectionKey, n) {
  const el = document.getElementById(SECTIONS[sectionKey].countId);
  if (el) el.textContent = n.toLocaleString();
}

/** Show a loading spinner inside a container */
function setLoading(containerId) {
  const el = document.getElementById(containerId);
  if (el) el.innerHTML = `<div class="loading-state">Loading…</div>`;
}

/** Show an error message inside a container */
function setError(containerId, msg) {
  const el = document.getElementById(containerId);
  if (el) el.innerHTML = `<div class="error-state">⚠ ${escapeHtml(msg)}</div>`;
}


/* ── 4. LOAD FUNCTIONS ─────────────────────────────────────────── */

/**
 * loadTeams()
 * Fetches all teams and caches them.
 * Live search then filters state.teams client-side.
 */
async function loadTeams() {
  setLoading("teams-container");
  try {
    const res = await fetch(`${API_BASE}/teams/`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    state.teams = await res.json();
    setCount("teams", state.teams.length);
    renderTeams(state.teams);
  } catch (err) {
    console.error("loadTeams error:", err);
    setError("teams-container", `Could not load teams. Is the API running? (${err.message})`);
  }
}

function renderTeams(teams) {
  const rows = teams.map(t => [
    t.id,
    t.name,
    // Wrap league in a styled tag for visual polish
    `<span class="league-tag">${escapeHtml(t.league ?? "Unknown")}</span>`,
    t.country ?? "Unknown",
  ]);
  // Pass raw HTML — renderTable normally escapes, so use a specialised call here
  renderTableRaw("teams-container", ["ID", "Name", "League", "Country"], rows);
}


/**
 * loadPlayers()
 * Fetches all players and caches them.
 */
async function loadPlayers() {
  setLoading("players-container");
  try {
    const res = await fetch(`${API_BASE}/players/`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    state.players = await res.json();
    setCount("players", state.players.length);
    renderPlayers(state.players);
  } catch (err) {
    console.error("loadPlayers error:", err);
    setError("players-container", `Could not load players. (${err.message})`);
  }
}

function renderPlayers(players) {
  const rows = players.map(p => [
    p.id,
    p.name,
    `<span class="pos-tag">${escapeHtml(p.position ?? "—")}</span>`,
    p.nationality ?? "—",
    // team_name comes from the serializer's human-readable field
    p.team_name ?? p.team ?? "—",
  ]);
  renderTableRaw("players-container", ["ID", "Name", "Position", "Nationality", "Team"], rows);
}


/**
 * loadMatches()
 * Fetches all matches. No live search — just show/hide.
 */
async function loadMatches() {
  setLoading("matches-container");
  try {
    const res = await fetch(`${API_BASE}/matches/`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    state.matches = await res.json();
    setCount("matches", state.matches.length);
    renderMatches(state.matches);
  } catch (err) {
    console.error("loadMatches error:", err);
    setError("matches-container", `Could not load matches. (${err.message})`);
  }
}

function renderMatches(matches) {
  const rows = matches.map(m => {
    // Build a formatted score pill — show "vs" if no score yet
    const home = m.home_score ?? null;
    const away = m.away_score ?? null;
    const score = (home !== null && away !== null)
      ? `<span class="score-pill">${home} – ${away}</span>`
      : `<span class="score-pill" style="color:var(--text-muted)">vs</span>`;

    return [
      m.id,
      m.home_team_name ?? m.home_team ?? "—",
      m.away_team_name ?? m.away_team ?? "—",
      m.date ?? "—",
      score,
      m.season ?? "—",
    ];
  });
  renderTableRaw("matches-container",
    ["ID", "Home Team", "Away Team", "Date", "Score", "Season"], rows);
}


/**
 * loadStats()
 * Fetches all stats. Can be slow with many rows — displays a spinner.
 */
async function loadStats() {
  setLoading("stats-container");
  try {
    const res = await fetch(`${API_BASE}/stats/`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    state.stats = await res.json();
    setCount("stats", state.stats.length);
    renderStats(state.stats);
  } catch (err) {
    console.error("loadStats error:", err);
    setError("stats-container", `Could not load stats. (${err.message})`);
  }
}

function renderStats(stats) {
  const rows = stats.map(s => [
    s.id ?? "—",
    s.player_name ?? s.player ?? "—",
    s.match_info  ?? s.match ?? "—",   // <-- fixed
    s.goals           ?? 0,
    s.assists         ?? 0,
    s.minutes_played  ?? 0,
    s.shots           ?? 0,
    s.yellow_cards    ?? 0,
    s.red_cards       ?? 0,
  ]);
  renderTableRaw("stats-container",
    ["ID", "Player", "Match", "Goals", "Assists", "Mins", "Shots", "🟨", "🟥"], rows);
}


/**
 * renderTableRaw(containerId, headers, rows)
 * Like renderTable() but rows may contain pre-built HTML strings (e.g. pills/tags).
 * Use only with trusted/escaped content.
 */
function renderTableRaw(containerId, headers, rows) {
  const container = document.getElementById(containerId);
  if (!container) return;

  if (rows.length === 0) {
    container.innerHTML = `<div class="empty-state">No results found.</div>`;
    return;
  }

  const headCells = headers.map(h => `<th>${h}</th>`).join("");
  const bodyRows  = rows.map(row =>
    `<tr>${row.map(cell => `<td>${cell}</td>`).join("")}</tr>`
  ).join("");

  container.innerHTML = `
    <table>
      <thead><tr>${headCells}</tr></thead>
      <tbody>${bodyRows}</tbody>
    </table>`;
}


/* ── 5. LIVE SEARCH ────────────────────────────────────────────── */

/**
 * filterTable(query, dataKey, renderFn)
 * Filters cached data client-side by checking if the team/player name
 * includes the query string (case-insensitive). No extra API call needed.
 *
 * @param {string}   query    - text from the search input
 * @param {string}   dataKey  - key in state (e.g. "teams")
 * @param {Function} renderFn - the render function to call with filtered data
 */
function filterTable(query, dataKey, renderFn) {
  const q = query.trim().toLowerCase();
  // If search box is empty, show everything
  const filtered = q
    ? state[dataKey].filter(item => (item.name ?? "").toLowerCase().includes(q))
    : state[dataKey];
  renderFn(filtered);
}


/* ── 6. COLLAPSIBLES ───────────────────────────────────────────── */

/**
 * Wire up all .toggle-btn elements.
 * Toggling adds/removes the "collapsed" CSS class on the target container,
 * which transitions max-height and opacity (see styles.css).
 * The button text and icon rotate to reflect the state.
 */
function initCollapsibles() {
  document.querySelectorAll(".toggle-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const targetId = btn.dataset.target;
      const label    = btn.dataset.label ?? "Section";
      const target   = document.getElementById(targetId);
      if (!target) return;

      const isCollapsed = target.classList.toggle("collapsed");

      // Update button label and rotate the arrow icon
      btn.classList.toggle("collapsed", isCollapsed);
      btn.innerHTML = `<span class="toggle-icon">▾</span> ${isCollapsed ? "Show" : "Hide"}`;
    });
  });
}


/* ── 7. INIT ───────────────────────────────────────────────────── */

document.addEventListener("DOMContentLoaded", () => {

  // ── Collapsible buttons
  initCollapsibles();

  // ── Live search: Teams
  // Fires on every keystroke; filters state.teams in memory
  document.getElementById("team-search")?.addEventListener("input", e => {
    filterTable(e.target.value, "teams", renderTeams);
  });

  // ── Live search: Players
  document.getElementById("player-search")?.addEventListener("input", e => {
    filterTable(e.target.value, "players", renderPlayers);
  });

  // ── Initial data load (all sections on page load)
  loadTeams();
  loadPlayers();
  loadMatches();
  loadStats();
});
