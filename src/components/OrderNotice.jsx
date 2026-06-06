import { useState } from "react";

import { noticeGroups } from "../content.js";
import SectionTitle from "./SectionTitle.jsx";
import NoticeAccordion from "./NoticeAccordion.jsx";

export default function OrderNotice() {
  const [activeGroup, setActiveGroup] = useState(noticeGroups[0].id);

  const focusGroup = (groupId) => {
    setActiveGroup(groupId);
    document.getElementById(`notice-${groupId}`)?.scrollIntoView({
      behavior: "smooth",
      block: "center",
    });
  };

  return (
    <section className="page-section notice-section" id="notice">
      <SectionTitle
        eyebrow="Rules"
        title="下单须知"
        description="为了保障双方体验，请在咨询和下单前完整阅读以下规则。"
      />

      <div className="alert-card">
        <strong>重要提醒</strong>
        <span>未成年人禁止下单，请理性消费；下单前请确认服务内容、规则和限制。</span>
      </div>

      <div className="notice-desktop">
        <aside className="notice-index" aria-label="规则目录">
          {noticeGroups.map((group) => (
            <button
              key={group.id}
              className={activeGroup === group.id ? "is-active" : ""}
              type="button"
              onClick={() => focusGroup(group.id)}
            >
              {group.title}
            </button>
          ))}
        </aside>

        <div className="notice-stack">
          {noticeGroups.map((group) => (
            <article
              className={`notice-card tone-${group.tone}`}
              id={`notice-${group.id}`}
              key={group.id}
            >
              <h3>{group.title}</h3>
              <ul>
                {group.items.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </article>
          ))}
        </div>
      </div>

      <div className="notice-mobile">
        {noticeGroups.map((group) => (
          <NoticeAccordion group={group} key={group.id} />
        ))}
      </div>
    </section>
  );
}
