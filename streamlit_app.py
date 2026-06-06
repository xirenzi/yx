# -*- coding: utf-8 -*-
"""混水电竞招募表单 - Streamlit 版本
部署到 Streamlit Cloud: https://share.streamlit.io
本地运行:  streamlit run streamlit_app.py
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

# ===================================================================
# 配置：从 Streamlit secrets 读取（部署后在 Streamlit Cloud 后台填写）
# 本地测试时可以取消下面的注释，直接填在这里
# ===================================================================
# SMTP 配置
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT   = 465

# 从 secrets 读取，本地测试可以改成直接填字符串
# st.secrets["QQ_EMAIL"]    → 发件邮箱
# st.secrets["QQ_AUTH_CODE"] → 授权码
# st.secrets["TO_EMAIL"]     → 收件邮箱（多个用逗号分隔）


def send_email(to_emails: list, subject: str, html_body: str) -> bool:
    """用 QQ 邮箱 SMTP 发送邮件，返回是否成功"""
    sender_email    = st.secrets["QQ_EMAIL"]
    sender_password = st.secrets["QQ_AUTH_CODE"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = sender_email
    msg["To"]      = ", ".join(to_emails)
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context, timeout=15) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_emails, msg.as_string())
        return True
    except Exception as e:
        st.error(f"发信失败：{e}")
        return False


# ===================================================================
# 页面配置
# ===================================================================
st.set_page_config(
    page_title="混水电竞｜大神招募",
    page_icon="🎮",
    layout="centered",
)

# ===================================================================
# 自定义 CSS（模仿官网暗色风格）
# ===================================================================
st.markdown("""
<style>
/* 全局暗色 */
.stApp {
    background: linear-gradient(180deg, #070a12 0%, #0b1020 44%, #070a12 100%);
    color: #f8fafc;
}

/* 标题 */
h1, h2, h3 { color: #f8fafc !important; }
h1 { font-size: 2rem !important; }

/* 输入框暗色 */
input, textarea, .stTextInput>div>div>input, .stTextArea>div>div>textarea {
    background: rgba(2, 6, 23, 0.6) !important;
    color: #f8fafc !important;
    border: 1px solid rgba(148, 163, 184, 0.25) !important;
    border-radius: 8px !important;
}
input:focus, textarea:focus {
    border-color: #22d3ee !important;
    box-shadow: 0 0 0 3px rgba(34, 211, 238, 0.12) !important;
}

/* 按钮渐变 */
.stButton>button {
    background: linear-gradient(135deg, #4f7cff, #22d3ee) !important;
    color: #020617 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    font-size: 1rem !important;
}
.stButton>button:hover {
    opacity: 0.9;
}

/* 成功提示 */
.element-container:has(.alert-success) {
    background: rgba(34, 197, 94, 0.15) !important;
    border: 1px solid rgba(34, 197, 94, 0.35) !important;
    border-radius: 8px !important;
    padding: 12px !important;
}
/* 错误提示 */
.element-container:has(.alert-danger) {
    background: rgba(239, 68, 68, 0.15) !important;
    border: 1px solid rgba(239, 68, 68, 0.35) !important;
    border-radius: 8px !important;
    padding: 12px !important;
}

/* 分割线 */
hr { border-color: rgba(148, 163, 184, 0.18) !important; }

/* 复选框 */
.stCheckbox label { color: #94a3b8 !important; font-size: 0.9rem !important; }
</style>
""", unsafe_allow_html=True)

# ===================================================================
# 页面内容
# ===================================================================
st.markdown("# 🎮 混水电竞｜大神招募")
st.markdown("欢迎有实力、有责任心、服务态度稳定的玩家加入混水电竞。")
st.markdown("**未成年人禁止加入，请理性消费。**")
st.divider()

with st.form("recruit_form", clear_on_submit=True):
    st.markdown("### 📝 填写申请信息")
    nickname = st.text_input(
        "游戏昵称 *",
        placeholder="请输入你的游戏昵称",
        max_chars=50,
    )
    contact = st.text_input(
        "常用联系方式 *",
        placeholder="微信 / QQ / 手机号",
        max_chars=100,
    )
    maps = st.text_input(
        "擅长地图/玩法 *",
        placeholder="例如：长弓溪谷、航天基地",
        max_chars=200,
    )
    schedule = st.text_input(
        "在线时间 *",
        placeholder="例如：工作日晚上、周末全天",
        max_chars=200,
    )
    intro = st.text_area(
        "自我介绍 *",
        placeholder="简单说明你的经验、风格和可协作时间",
        height=100,
        max_chars=1000,
    )
    agreed = st.checkbox(
        "我已了解并接受工作室服务规范，不私联客户、不私下交易。 *"
    )
    submitted = st.form_submit_button("🚀 提交申请")

    if submitted:
        # 验证
        if not nickname or not contact or not maps or not schedule or not intro:
            st.error("请填写所有必填项（带 * 的字段）")
        elif not agreed:
            st.error("请先勾选「接受工作室服务规范」")
        else:
            with st.spinner("正在提交申请..."):
                # 收件邮箱：从 secrets 读取，多个用逗号分隔
                to_raw = st.secrets.get("TO_EMAIL", "")
                to_emails = [e.strip() for e in to_raw.split(",") if e.strip()]

                if not to_emails:
                    st.error("未配置收件邮箱，请联系管理员在 Streamlit secrets 中填写 TO_EMAIL")
                else:
                    html = f"""
                    <h2>混水电竞 - 新招募申请</h2>
                    <p><strong>游戏昵称：</strong>{nickname}</p>
                    <p><strong>联系方式：</strong>{contact}</p>
                    <p><strong>擅长地图/玩法：</strong>{maps}</p>
                    <p><strong>在线时间：</strong>{schedule}</p>
                    <p><strong>自我介绍：</strong><br/>{intro.replace(chr(10), "<br/>")}</p>
                    <hr/>
                    <p style="color:#888;font-size:12px;">来自混水电竞招募表单（Streamlit）</p>
                    """
                    ok = send_email(to_emails, f"混水电竞招募申请 - {nickname}", html)
                    if ok:
                        st.success("✅ 申请已提交！请联系官方客服进一步沟通。")
                        st.balloons()
                    else:
                        st.error("提交失败，请稍后重试或联系客服。")

st.divider()
st.markdown("#### 📌 招募要求")
col1, col2 = st.columns(2)
with col1:
    st.markdown("- 熟悉三角洲行动地图和资源点")
    st.markdown("- 有稳定在线时间")
with col2:
    st.markdown("- 遵守服务规范")
    st.markdown("- 不私联客户、不私下交易")

st.caption("混水电竞工作室 © 2024 · 未成年人禁止加入")
