const links = [...document.querySelectorAll("[data-nav-link]")];
const sections = links
  .map((link) => {
    const id = link.getAttribute("href");
    return id ? document.querySelector(id) : null;
  })
  .filter(Boolean);

const setActiveLink = (id) => {
  links.forEach((link) => {
    const isActive = link.getAttribute("href") === `#${id}`;
    link.toggleAttribute("data-active", isActive);
  });
};

const observer = new IntersectionObserver(
  (entries) => {
    const visible = entries
      .filter((entry) => entry.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

    if (visible?.target?.id) {
      setActiveLink(visible.target.id);
    }
  },
  {
    rootMargin: "-20% 0px -60% 0px",
    threshold: [0.2, 0.45, 0.7]
  }
);

sections.forEach((section) => observer.observe(section));

const stamp = document.querySelector("[data-verified-date]");
if (stamp) {
  stamp.textContent = "Last reviewed against the public DeepSeek-V4 model card on April 24, 2026.";
}
