(function () {
  function unlockListItem(item) {
    var href = item.dataset.paperHref;
    if (!href) return;

    item.classList.remove('paper-item--locked');

    var trigger = item.querySelector('.paper-link--locked');
    var link = document.createElement('a');
    link.className = 'paper-link';
    link.href = href;

    if (trigger) {
      Array.from(trigger.childNodes).forEach(function (child) {
        link.appendChild(child);
      });
      trigger.remove();
    }

    item.appendChild(link);
  }

  function initResearchList() {
    document.querySelectorAll('.paper-item--locked[data-paper-slug]').forEach(unlockListItem);
  }

  function initPaperGate() {
    var gate = document.getElementById('paper-gate');
    var content = document.getElementById('paper-content');
    if (!gate || !content) return;

    gate.hidden = true;
    content.hidden = false;
  }

  document.addEventListener('DOMContentLoaded', function () {
    initResearchList();
    initPaperGate();
  });
})();
