'use strict';
// Extensions and font loading can change the sticky header after first paint.
// Observe geometry, not the whole document or extension-specific internals.
(() => {
  const header = document.querySelector('.site-header');
  if (!header) return;
  const update = () => {
    document.documentElement.style.setProperty('--header-offset', `${Math.ceil(header.getBoundingClientRect().height) + 20}px`);
  };
  update();
  if ('ResizeObserver' in window) new ResizeObserver(update).observe(header);
  else window.addEventListener('resize', update, {passive: true});
})();
