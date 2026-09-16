'use strict';
const zh = document.body.dataset.lang === 'zh';
const txt = (en, cn) => zh ? cn : en;
const cards = [...document.querySelectorAll('.demo-card')];
// Native video controls remain available without JavaScript.
for (const card of cards) {
  const videos = [...card.querySelectorAll('video')];
  const controls = card.querySelector('.pair-controls');
  const play = card.querySelector('.pair-play');
  const status = card.querySelector('.play-status');
  controls.hidden = false;
  let starting = false;
  const update = () => {
    const playing = videos.some(v => !v.paused && !v.ended);
    play.textContent = playing ? txt('Ⅱ Pause both', 'Ⅱ 同时暂停') : txt('▶ Play both', '▶ 同时播放');
  };
  const start = async (restart = false) => {
    if (starting) return;
    starting = true;
    play.disabled = true;
    status.textContent = '';
    for (const other of document.querySelectorAll('video')) if (!videos.includes(other)) other.pause();
    if (restart || videos.every(v => v.ended)) for (const v of videos) v.currentTime = 0;
    const results = await Promise.allSettled(videos.map(v => v.play()));
    if (results.some(r => r.status === 'rejected')) {
      videos.forEach(v => v.pause());
      status.textContent = txt('Playback could not start. Try the individual video controls.', '视频未能启动，请使用各视频自带的播放按钮。');
    }
    play.disabled = false;
    starting = false;
    update();
  };
  play.addEventListener('click', () => {
    if (videos.some(v => !v.paused && !v.ended)) videos.forEach(v => v.pause());
    else start();
  });
  card.querySelector('.pair-restart').addEventListener('click', () => start(true));
  card.querySelector('.pair-speed').addEventListener('change', e => {
    videos.forEach(v => { v.playbackRate = Number(e.target.value); });
  });
  videos.forEach(v => {
    ['play', 'pause', 'ended'].forEach(event => v.addEventListener(event, update));
    v.addEventListener('error', () => { status.textContent = txt('Video unavailable. Please reload or open the MP4 directly.', '视频暂时不可用，请刷新页面或直接打开 MP4。'); });
  });
}
const filters = document.querySelector('.filters');
filters.hidden = false;
filters.querySelectorAll('button').forEach(button => button.addEventListener('click', () => {
  filters.querySelectorAll('button').forEach(b => {
    b.classList.toggle('active', b === button);
    b.setAttribute('aria-pressed', b === button ? 'true' : 'false');
  });
  cards.forEach(card => {
    card.hidden = button.dataset.filter !== 'All' && button.dataset.filter !== card.dataset.suite;
    if (card.hidden) card.querySelectorAll('video').forEach(v => v.pause());
  });
}));
const stageButtons = document.querySelector('.walk-tabs');
stageButtons.hidden = false;
const selectStage = id => {
  stageButtons.querySelectorAll('button').forEach(b => {
    const active = b.dataset.stage === id;
    b.classList.toggle('active', active);
    b.setAttribute('aria-pressed', String(active));
  });
  document.querySelectorAll('.walk-panel').forEach(p => { p.hidden = p.id !== `stage-${id}`; });
};
stageButtons.querySelectorAll('button').forEach(b => b.addEventListener('click', () => selectStage(b.dataset.stage)));
selectStage('teach');
const copy = document.getElementById('copy-citation');
copy.hidden = false;
copy.addEventListener('click', async () => {
  const code = document.getElementById('bibtex');
  const status = document.getElementById('copy-status');
  try {
    await navigator.clipboard.writeText(code.textContent);
    status.textContent = txt('Citation copied.', '引用已复制。');
  } catch {
    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(code);
    selection.removeAllRanges();
    selection.addRange(range);
    status.textContent = txt('Citation selected. Press Ctrl/Cmd+C to copy.', '引用已选中，按 Ctrl/Cmd+C 复制。');
  }
});
const dialog = document.getElementById('image-dialog');
if (typeof dialog.showModal === 'function') {
  document.querySelectorAll('.zoom').forEach(link => link.addEventListener('click', e => {
    e.preventDefault();
    dialog.querySelector('img').src = link.href;
    dialog.querySelector('img').alt = link.querySelector('img').alt;
    dialog.querySelector('p').textContent = link.closest('figure').querySelector('figcaption').textContent;
    dialog.showModal();
    document.body.classList.add('modal-open');
  }));
  dialog.querySelector('button').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', e => { if (e.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => document.body.classList.remove('modal-open'));
}
document.addEventListener('visibilitychange', () => {
  if (document.hidden) document.querySelectorAll('video').forEach(v => v.pause());
});
