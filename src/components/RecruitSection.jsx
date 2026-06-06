import { useState } from "react";

import { recruitCards } from "../content.js";
import SectionTitle from "./SectionTitle.jsx";

export default function RecruitSection({ onContact }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [toastVisible, setToastVisible] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const formData = new FormData(form);

    setIsSubmitting(true);
    setToastVisible(false);

    try {
      const response = await fetch(
        "http://yxapi.hljcxcx.top/api/recruit",
        {
          method: "POST",
          body: formData,
          headers: { Accept: "application/json" },
        }
      );
      if (response.ok) {
        form.reset();
        setToastVisible(true);
      } else {
        alert("提交失败，请稍后重试或联系客服。");
      }
    } catch {
      alert("网络错误，请检查连接后重试。");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="page-section recruit-section" id="recruit">
      <SectionTitle
        eyebrow="Join Us"
        title="大神招募"
        description="欢迎有实力、有责任心、服务态度稳定的玩家加入混水电竞。"
      />

      <div className="recruit-layout">
        <div className="recruit-copy reveal">
          <div className="recruit-card-grid">
            {recruitCards.map((card) => (
              <article className="requirement-card" key={card.title}>
                <h3>{card.title}</h3>
                <p>{card.content}</p>
              </article>
            ))}
          </div>

          <div className="recruit-list">
            <strong>招募对象</strong>
            <ul>
              <li>三角洲行动高水平玩家，熟悉地图和资源点。</li>
              <li>有稳定在线时间，能保持良好沟通。</li>
              <li>能遵守工作室服务规范，不私联客户、不私下交易。</li>
            </ul>
          </div>

          <button className="ghost-button" type="button" onClick={onContact}>
            联系客服
          </button>
        </div>

        <form className="recruit-form reveal" onSubmit={handleSubmit}>
          <label>
            游戏昵称
            <input name="nickname" required placeholder="请输入你的游戏昵称" />
          </label>
          <label>
            常用联系方式
            <input name="contact" required placeholder="微信 / QQ / 手机号" />
          </label>
          <label>
            擅长地图/玩法
            <input name="maps" required placeholder="例如：长弓溪谷、航天基地" />
          </label>
          <label>
            在线时间
            <input name="schedule" required placeholder="例如：工作日晚上、周末全天" />
          </label>
          <label>
            自我介绍
            <textarea
              name="intro"
              rows="4"
              required
              placeholder="简单说明你的经验、风格和可协作时间"
            />
          </label>
          <label className="checkbox-row">
            <input name="accepted" type="checkbox" required />
            <span>我已了解并接受工作室服务规范，不私联客户、不私下交易。</span>
          </label>

          <button className="primary-button" type="submit" disabled={isSubmitting}>
            {isSubmitting ? "记录中..." : "申请加入"}
          </button>

          {toastVisible ? (
            <div className="toast-message" role="status">
              申请信息已记录，请联系官方客服进一步沟通。
            </div>
          ) : null}
        </form>
      </div>
    </section>
  );
}
