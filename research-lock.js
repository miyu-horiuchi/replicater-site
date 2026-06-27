(function () {
  const STORAGE_PREFIX = 'paper-unlock:';
  const PAPERS = {
    'tokenization-trap': {
      hash: '7dcd20425882916eaa7afe9142ee27f1f07f6ddd89c80eb0f362f81b5e24df8f',
    },
  };

  async function sha256(text) {
    const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
    return Array.from(new Uint8Array(buf)).map(function (b) {
      return b.toString(16).padStart(2, '0');
    }).join('');
  }

  function isUnlocked(slug) {
    return sessionStorage.getItem(STORAGE_PREFIX + slug) === '1';
  }

  function setUnlocked(slug) {
    sessionStorage.setItem(STORAGE_PREFIX + slug, '1');
  }

  async function tryUnlock(slug, password) {
    var paper = PAPERS[slug];
    if (!paper) return false;
    var hash = await sha256(password);
    if (hash === paper.hash) {
      setUnlocked(slug);
      return true;
    }
    return false;
  }

  function ensureModal() {
    var modal = document.getElementById('paper-unlock-modal');
    if (modal) return modal;

    modal = document.createElement('div');
    modal.id = 'paper-unlock-modal';
    modal.className = 'paper-unlock-modal';
    modal.hidden = true;
    modal.innerHTML =
      '<div class="paper-unlock-dialog" role="dialog" aria-modal="true" aria-labelledby="paper-unlock-title">' +
        '<h2 id="paper-unlock-title" class="paper-unlock-title">Enter password</h2>' +
        '<p class="paper-unlock-lede">This paper is locked.</p>' +
        '<form class="paper-unlock-form">' +
          '<input type="password" class="paper-unlock-input" autocomplete="current-password" required />' +
          '<p class="paper-unlock-error" hidden>Incorrect password.</p>' +
          '<div class="paper-unlock-actions">' +
            '<button type="button" class="paper-unlock-cancel">Cancel</button>' +
            '<button type="submit" class="paper-unlock-submit">Unlock</button>' +
          '</div>' +
        '</form>' +
      '</div>';
    document.body.appendChild(modal);
    return modal;
  }

  function openUnlockModal(slug, onSuccess) {
    var modal = ensureModal();
    var form = modal.querySelector('.paper-unlock-form');
    var input = modal.querySelector('.paper-unlock-input');
    var error = modal.querySelector('.paper-unlock-error');
    var cancel = modal.querySelector('.paper-unlock-cancel');

    modal.hidden = false;
    input.value = '';
    error.hidden = true;
    input.focus();

    function closeModal() {
      modal.hidden = true;
      form.removeEventListener('submit', onSubmit);
      cancel.removeEventListener('click', closeModal);
      modal.removeEventListener('click', onBackdrop);
    }

    function onBackdrop(e) {
      if (e.target === modal) closeModal();
    }

    async function onSubmit(e) {
      e.preventDefault();
      var ok = await tryUnlock(slug, input.value);
      if (ok) {
        closeModal();
        onSuccess();
        return;
      }
      error.hidden = false;
      input.select();
    }

    form.addEventListener('submit', onSubmit);
    cancel.addEventListener('click', closeModal);
    modal.addEventListener('click', onBackdrop);
  }

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
    document.querySelectorAll('.paper-item--locked[data-paper-slug]').forEach(function (item) {
      var slug = item.dataset.paperSlug;
      var href = item.dataset.paperHref;
      if (!slug || !href) return;

      if (isUnlocked(slug)) {
        unlockListItem(item);
        return;
      }

      var trigger = item.querySelector('.paper-link--locked');
      if (!trigger) return;

      trigger.addEventListener('click', function () {
        openUnlockModal(slug, function () {
          unlockListItem(item);
          window.location.href = href;
        });
      });
    });
  }

  function initPaperGate() {
    var gate = document.getElementById('paper-gate');
    var content = document.getElementById('paper-content');
    if (!gate || !content) return;

    var slug = gate.dataset.paperSlug;
    if (!slug) return;

    if (isUnlocked(slug)) {
      gate.hidden = true;
      content.hidden = false;
      return;
    }

    gate.hidden = false;
    content.hidden = true;

    var form = gate.querySelector('.paper-unlock-form');
    var input = gate.querySelector('.paper-unlock-input');
    var error = gate.querySelector('.paper-unlock-error');

    form.addEventListener('submit', async function (e) {
      e.preventDefault();
      var ok = await tryUnlock(slug, input.value);
      if (ok) {
        gate.hidden = true;
        content.hidden = false;
        return;
      }
      error.hidden = false;
      input.select();
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initResearchList();
    initPaperGate();
  });
})();
