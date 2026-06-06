import { useState } from "react";

export default function NoticeAccordion({ group }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <article className={`notice-accordion tone-${group.tone}`}>
      <button type="button" onClick={() => setIsOpen((current) => !current)}>
        <span>{group.title}</span>
        <strong>{isOpen ? "收起" : "展开"}</strong>
      </button>
      <div className={`notice-panel ${isOpen ? "is-open" : ""}`}>
        <ul>
          {group.items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </div>
    </article>
  );
}
