(function () {
  function stripLock() {
    var gate = document.getElementById('paper-gate');
    if (gate) gate.remove();

    var content = document.getElementById('paper-content');
    if (content) content.hidden = false;

    document.querySelectorAll('.paper-item--locked[data-paper-href]').forEach(function (item) {
      var href = item.dataset.paperHref;
      if (!href) return;

      item.classList.remove('paper-item--locked');

      var trigger = item.querySelector('.paper-link--locked');
      if (!trigger) return;

      var link = document.createElement('a');
      link.className = 'paper-link';
      link.href = href;
      while (trigger.firstChild) link.appendChild(trigger.firstChild);
      trigger.replaceWith(link);
    });

    var modal = document.getElementById('paper-unlock-modal');
    if (modal) modal.remove();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', stripLock);
  } else {
    stripLock();
  }
})();
