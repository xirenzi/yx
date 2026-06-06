import { useState } from "react";

import SectionTitle from "./SectionTitle.jsx";

export default function ContactSection() {
  const [dialogOpen, setDialogOpen] = useState(false);

  return (
    <section className="page-section contact-section" id="contact">
      <SectionTitle
        eyebrow="Contact"
        title="联系客服"
        description="如需咨询服务详情、订单规则、售后问题或加入工作室，请通过官方客服渠道联系。"
        align="center"
      />

      <div className="contact-layout reveal">
        <div className="contact-info">
          <div className="contact-badge">官方渠道优先</div>
          <h3>咨询前先确认规则，沟通更高效。</h3>
          <p>
            客服在线时间：7:00 - 24:00。24 小时支持自助下单和查看订单信息。
          </p>
          <div className="contact-actions">
            <button className="primary-button" type="button" onClick={() => setDialogOpen(true)}>
              咨询客服
            </button>
            <button className="secondary-button" type="button" onClick={() => setDialogOpen(true)}>
              小程序入口
            </button>
          </div>
        </div>

        <div className="placeholder-grid" aria-label="官方入口占位">
          <div className="placeholder-box">
            <span>客服二维码</span>
            <strong>待上传</strong>
          </div>
          <div className="placeholder-box">
            <span>小程序入口</span>
            <strong>待配置</strong>
          </div>
        </div>
      </div>

      {dialogOpen ? (
        <div className="modal-backdrop" role="presentation" onClick={() => setDialogOpen(false)}>
          <div
            className="contact-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="contact-modal-title"
            onClick={(event) => event.stopPropagation()}
          >
            <h3 id="contact-modal-title">官方客服提示</h3>
            <p>请添加官方客服或进入小程序咨询，避免私下交易风险。</p>
            <button className="primary-button" type="button" onClick={() => setDialogOpen(false)}>
              我知道了
            </button>
          </div>
        </div>
      ) : null}
    </section>
  );
}
