import { useState } from "react";

import { navItems } from "../content.js";
import { scrollToSection } from "../utils/scroll.js";

export default function Header({ onContact }) {
  const [isOpen, setIsOpen] = useState(false);

  const handleNav = (target) => {
    scrollToSection(target);
    setIsOpen(false);
  };

  return (
    <header className="site-header">
      <div className="header-shell">
        <button className="brand-button" type="button" onClick={() => handleNav("hero")}>
          <span className="brand-mark">混</span>
          <span>
            <strong>混水电竞</strong>
            <small>三角洲行动工作室</small>
          </span>
        </button>

        <nav className="desktop-nav" aria-label="主导航">
          {navItems.map((item) => (
            <button key={item.target} type="button" onClick={() => handleNav(item.target)}>
              {item.label}
            </button>
          ))}
        </nav>

        <div className="header-actions">
          <button className="ghost-button compact" type="button" onClick={onContact}>
            立即咨询
          </button>
          <button
            className="menu-toggle"
            type="button"
            aria-label={isOpen ? "关闭菜单" : "打开菜单"}
            aria-expanded={isOpen}
            onClick={() => setIsOpen((current) => !current)}
          >
            <span className="menu-lines" aria-hidden="true">
              <i />
              <i />
              <i />
            </span>
            <strong>{isOpen ? "关闭" : "菜单"}</strong>
          </button>
        </div>
      </div>

      <nav className={`mobile-nav ${isOpen ? "is-open" : ""}`} aria-label="移动端导航">
        {navItems.map((item) => (
          <button key={item.target} type="button" onClick={() => handleNav(item.target)}>
            {item.label}
          </button>
        ))}
      </nav>
    </header>
  );
}
