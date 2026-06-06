export function scrollToSection(targetId) {
  const section = document.getElementById(targetId);

  if (!section) {
    return;
  }

  section.scrollIntoView({
    behavior: "smooth",
    block: "start",
  });
}
