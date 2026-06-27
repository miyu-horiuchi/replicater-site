(function () {
  var path = location.pathname;
  if (!/\.html$/.test(path)) return;
  var clean = path.replace(/\.html$/, '');
  if (clean === '/index') clean = '/';
  location.replace(clean + location.search + location.hash);
})();
