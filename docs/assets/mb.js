// Shared analytics + click tracking. No-ops safely when goatcounter code is unset.
(function () {
  var c = window.MB_CONFIG || {};
  window.MB = {
    track: function (name) {
      try { if (window.goatcounter && window.goatcounter.count) window.goatcounter.count({ path: "event/" + name, title: name, event: true }); } catch (e) {}
    }
  };
  if (c.goatcounter) {
    var s = document.createElement("script");
    s.async = true; s.src = "https://gc.zgo.at/count.js";
    s.setAttribute("data-goatcounter", "https://" + c.goatcounter + ".goatcounter.com/count");
    document.head.appendChild(s);
  }
  document.addEventListener("click", function (e) {
    var el = e.target.closest && e.target.closest("[data-track]");
    if (el) window.MB.track(el.getAttribute("data-track"));
  });
  window.MB.renderOffers = function (slug, box) {
    var o = (c.offers && c.offers[slug]) || [];
    if (!o.length) { box.hidden = true; return; }
    box.innerHTML = "<h2>Recommended tools <small>(sponsored links)</small></h2>" + o.map(function (x) {
      return '<p><a href="' + encodeURI(x.url) + '" rel="sponsored noopener" target="_blank" data-track="offer-' + slug + '">' +
        String(x.label).replace(/</g, "&lt;") + "</a> " + String(x.note || "").replace(/</g, "&lt;") + "</p>";
    }).join("") + "<p><small>We may earn a commission if you sign up, at no cost to you.</small></p>";
  };
})();
