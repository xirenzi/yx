import { navItems } from "../content.js";
import { scrollToSection } from "../utils/scroll.js";

export default function Footer() {
  const footerLinks = navItems.filter((item) =>
    ["services", "notice", "recruit", "contact"].includes(item.target),
  );

  return (
    <footer className="site-footer">
      <div>
        <h2>混水电竞</h2>
        <p>专注三角洲行动护航服务展示与规则说明</p>
      </div>
      <nav aria-label="页脚导航">
        {footerLinks.map((item) => (
          <button key={item.target} type="button" onClick={() => scrollToSection(item.target)}>
            {item.label}
          </button>
        ))}
      </nav>
      <p className="footer-note">
        本网站仅用于工作室服务展示、规则说明与客服引导。请理性消费，未成年人禁止下单。游戏相关权益归原厂商所有。
      </p>
    </footer>
  );
}
