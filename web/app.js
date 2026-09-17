const CSV_PATH = 'top10_predictions.csv';

document.addEventListener('DOMContentLoaded', () => {
  Papa.parse(CSV_PATH, {
    download: true,
    header: true,
    skipEmptyLines: true,
    complete: ({ data }) => {
      const players = data
        .map(p => ({
          name: p.player_name || '',
          pct:  parseFloat(p.mvp_percentage) || 0
        }))
        .sort((a, b) => b.pct - a.pct)
        .slice(0, 10); 

      renderRanking(players);
      animateBars();
    },
    error: (err) => {
      document.getElementById('ranking').innerHTML =
        `<p style="color:#fff;text-align:center"> Error: ${err.message}</p>`;
    }
  });
});

const MEDALS = ['🥇', '🥈', '🥉'];
const RANK_CLASSES = ['rank-1', 'rank-2', 'rank-3'];
const NUM_CLASSES  = ['gold',   'silver', 'bronze'];

function renderRanking(players) {
  const container = document.getElementById('ranking');

  container.innerHTML = players.map((p, i) => {
    const rank      = i + 1;
    const rowClass  = RANK_CLASSES[i] ?? '';
    const numClass  = NUM_CLASSES[i]  ?? '';
    const badge     = i < 3 ? MEDALS[i] : rank;
    const pctRound  = p.pct.toFixed(1);
    const barWidth  = Math.round(p.pct);  

    return `
      <div class="player-row ${rowClass}">
        <div class="rank-num ${numClass}">${badge}</div>
        <div class="player-name">${escHtml(p.name)}</div>
        <div class="pct-area">
          <span class="pct-value">${pctRound}%</span>
          <div class="pct-bar-track">
            <div class="pct-bar-fill" data-pct="${barWidth}"></div>
          </div>
        </div>
      </div>`;
  }).join('');
}

function animateBars() {
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      document.querySelectorAll('.pct-bar-fill[data-pct]').forEach(el => {
        el.style.width = `${el.dataset.pct}%`;
      });
    });
  });
}

function escHtml(str) {
  return String(str)
    .replace(/&/g,'&amp;').replace(/</g,'&lt;')
    .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
