const links = [...document.querySelectorAll('.section-nav a')];
const sections = links.map((link) => document.querySelector(link.getAttribute('href')));
const updateActive = () => {
  let current = 0;
  sections.forEach((section, index) => {
    if (section.getBoundingClientRect().top <= window.innerHeight * 0.35) current = index;
  });
  if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 4) {
    current = sections.length - 1;
  }
  links.forEach((link, index) => {
    link.classList.toggle('active', index === current);
    if (index === current) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
};
window.addEventListener('scroll', updateActive, { passive: true });
updateActive();

document.querySelectorAll('.paper-trigger').forEach((trigger) => {
  const panel = document.getElementById(trigger.getAttribute('aria-controls'));
  trigger.addEventListener('click', () => {
    const expanded = trigger.getAttribute('aria-expanded') === 'true';
    trigger.setAttribute('aria-expanded', String(!expanded));
    panel.classList.toggle('is-closed', expanded);
    panel.inert = expanded;
  });
});
