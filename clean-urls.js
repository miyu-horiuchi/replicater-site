(function () {
  var path = location.pathname;
  if (/\/index\.html$/.test(path)) {
    var clean = path.replace(/\/index\.html$/, '') || '/';
    location.replace(clean + location.search + location.hash);
    return;
  }
  if (/\.html$/.test(path)) {
    var clean = path.replace(/\.html$/, '');
    if (clean === '/index') clean = '/';
    if (clean === '/lab') clean = '/';
    location.replace(clean + location.search + location.hash);
    return;
  }
  if (path.length > 1 && /\/$/.test(path)) {
    location.replace(path.replace(/\/$/, '') + location.search + location.hash);
  }
})();
