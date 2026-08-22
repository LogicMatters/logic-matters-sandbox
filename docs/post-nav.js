(function () {
  var path = window.location.pathname;
  if (!path.match(/\/blog\/[^/]+\.html$/)) return;

  fetch('/listings.json')
    .then(function (r) { return r.json(); })
    .then(function (data) {
      var listing = data.find(function (d) { return d.listing === '/blog/index.html'; });
      if (!listing) return;
      var items = listing.items;
      var idx = items.findIndex(function (p) { return path.endsWith(p) || p.endsWith(path); });
      if (idx < 0) return;

      var older = items[idx + 1] || null;
      var newer = items[idx - 1] || null;
      var parts = [];
      if (older) parts.push('<a href="' + older + '">← Previous post</a>');
      if (newer) parts.push('<a href="' + newer + '">Next post →</a>');
      if (!parts.length) return;

      var nav = document.createElement('div');
      nav.style.cssText = 'margin-top: 1.5em; text-align: center;';
      nav.innerHTML = parts.join(' &nbsp;|&nbsp; ');

      var main = document.querySelector('main.content') || document.querySelector('main');
      if (main) main.appendChild(nav);
    })
    .catch(function () {});
})();
