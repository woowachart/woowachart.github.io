"use strict";

(() => {
  const key = "woowachart-language";
  const valid = (value) => value === "ko" || value === "en";

  // Real links still work without JavaScript. Save before normal navigation.
  document.addEventListener("click", (event) => {
    const link = event.target.closest("a[data-language]");
    if (!link || !valid(link.dataset.language)) return;
    try {
      localStorage.setItem(key, link.dataset.language);
    } catch (_) {
      // A blocked store must not bounce an explicit Korean choice back to English.
      const destination = new URL(link.href);
      destination.searchParams.set("lang", link.dataset.language);
      link.href = destination.href;
    }
  });

  // Direct /en/ visits always stay in English, even with a saved Korean choice.
  if (document.documentElement.lang !== "ko") return;
  let preferred = new URLSearchParams(location.search).get("lang");
  if (!valid(preferred)) {
    try {
      preferred = localStorage.getItem(key);
    } catch (_) { /* Language detection also works when storage is unavailable. */ }
  }
  if (!valid(preferred)) {
    const browserLanguage = (navigator.languages && navigator.languages[0]) || navigator.language || "ko";
    preferred = browserLanguage.toLowerCase().startsWith("ko") ? "ko" : "en";
  }
  if (preferred === "en") {
    // lang.js runs before the head links are parsed; preserve the policy filename.
    const filename = location.pathname.split("/").pop();
    const page = /^(terms|privacy|refund|contact)\.html$/.test(filename) ? filename : "";
    location.replace("en/" + page + location.search + location.hash);
  }
})();
