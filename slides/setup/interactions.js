(function () {
  "use strict";

  function updateContextLab(lab) {
    const slider = lab.querySelector(".context-slider");
    if (!slider) return;

    const sources = Number(slider.value);
    const allocation = {
      instructions: 12,
      sources,
      conversation: 60 - sources,
      tools: 10,
      response: 18
    };

    const readout = lab.querySelector("[data-context-readout]");
    if (readout) readout.textContent = `${sources}%`;

    Object.entries(allocation).forEach(([key, value]) => {
      const segment = lab.querySelector(`[data-context-segment="${key}"]`);
      const label = lab.querySelector(`[data-context-value="${key}"]`);
      if (segment) segment.style.flexBasis = `${value}%`;
      if (label) label.textContent = `${value}%`;
    });
  }

  function initializeContextLabs(root) {
    root.querySelectorAll("[data-context-lab]").forEach((lab) => {
      if (lab.dataset.contextInitialized === "true") {
        updateContextLab(lab);
        return;
      }

      const slider = lab.querySelector(".context-slider");
      if (!slider) return;
      slider.addEventListener("input", () => updateContextLab(lab));
      lab.dataset.contextInitialized = "true";
      updateContextLab(lab);
    });
  }

  // A citation links to its entry in the References slide. Point it at the
  // source itself instead, and open every external link in a new tab so the
  // deck stays where it was.
  function linkCitationsToSources(root) {
    // Quarto rewrites each citation's href to "#/references", so the key comes
    // from the enclosing span: its data-cites lists one key per link, in order.
    root.querySelectorAll(".citation[data-cites]").forEach((span) => {
      const keys = span.dataset.cites.split(" ");
      span.querySelectorAll('a[role="doc-biblioref"]').forEach((cite, i) => {
        const entry = keys[i] && document.getElementById("ref-" + keys[i]);
        const source = entry && entry.querySelector('a[href^="http"]');
        if (source) cite.href = source.href;
      });
    });
    root.querySelectorAll('.reveal .slides a[href^="http"]').forEach((link) => {
      link.target = "_blank";
      link.rel = "noopener";
    });
  }

  // Label each slide with the title of the part (level-1 heading) it belongs to.
  function labelSections(root) {
    let part = "";
    root.querySelectorAll(".reveal .slides section.level1, .reveal .slides section.level2").forEach((slide) => {
      if (slide.classList.contains("level1")) {
        const heading = slide.querySelector("h1");
        part = heading ? heading.textContent.trim() : "";
        return;
      }
      if (!part || slide.querySelector(":scope > .section-label")) return;
      const label = document.createElement("p");
      label.className = "section-label";
      label.textContent = part;
      slide.prepend(label);
    });
  }

  function initialize() {
    labelSections(document);
    linkCitationsToSources(document);
    initializeContextLabs(document);
    if (window.Reveal && typeof window.Reveal.on === "function") {
      window.Reveal.on("slidechanged", (event) => {
        initializeContextLabs(event.currentSlide || document);
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize, { once: true });
  } else {
    initialize();
  }
})();
