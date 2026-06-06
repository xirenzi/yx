import { scrollToSection } from "../utils/scroll.js";

const heroStats = [
  { label: "服务方向", value: "三角洲行动护航" },
  { label: "在线时间", value: "7:00 - 24:00" },
  { label: "服务原则", value: "规则透明 / 稳定执行" },
  { label: "年龄限制", value: "未成年人禁止下单" },
];

export default function HeroSection({ onContact }) {
  return (
    <section className="hero-section page-section" id="hero">
      <div className="hero-copy reveal">
        <p className="hero-kicker">混水电竞官方展示站</p>
        <h1>
          <span>混水电竞｜三角洲行动</span>
          <span>护航工作室</span>
        </h1>
        <p className="hero-lead">
          专注三角洲行动护航服务，透明规则、稳定执行、专业导师在线协作。
        </p>
        <p className="hero-note">
          下单前请认真阅读服务说明，确认规则后再联系客服咨询。未成年人禁止下单。
        </p>

        <div className="hero-actions">
          <button
            className="primary-button"
            type="button"
            onClick={() => scrollToSection("services")}
          >
            查看服务分类
          </button>
          <button
            className="secondary-button"
            type="button"
            onClick={() => scrollToSection("notice")}
          >
            阅读下单须知
          </button>
          <button className="ghost-button" type="button" onClick={onContact}>
            咨询客服
          </button>
        </div>
      </div>

      <div className="hero-panel reveal" aria-label="工作室服务信息">
        <div className="panel-topline">
          <span className="status-dot" />
          <span>Studio Status</span>
        </div>
        <div className="hero-cover-frame">
          <img src="/hero-cover.jpg" alt="三角洲行动护航封面" />
          <div className="hero-cover-overlay">
            <span>规则确认后再沟通服务</span>
            <strong>三角洲行动护航</strong>
          </div>
        </div>
        <div className="hero-stat-grid">
          {heroStats.map((stat) => (
            <div className="hero-stat" key={stat.label}>
              <span>{stat.label}</span>
              <strong>{stat.value}</strong>
            </div>
          ))}
        </div>
        <div className="minor-warning">未成年人禁止下单，请理性消费。</div>
      </div>
    </section>
  );
}
