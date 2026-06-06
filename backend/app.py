# -*- coding: utf-8 -*-
"""
混水电竞招募表单后端
配置页面：http://localhost:5000
API 接收：POST http://localhost:5000/api/recruit
用 QQ 邮箱 SMTP 发信
"""
import json
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域请求
CONFIG_FILE = "config.json"

# ---------- 配置读写 ----------

def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"accounts": [], "recipients": []}

def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

# ---------- 发邮件 ----------

def send_email(account, password, to_emails, subject, html_body):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = account
    msg["To"]      = ", ".join(to_emails)
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.qq.com", 465, context=context, timeout=15) as server:
        server.login(account, password)
        server.sendmail(account, to_emails, msg.as_string())

# ---------- 路由 ----------

INDEX_HTML = r"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>混水电竞 - 邮箱配置</title>
<style>
  *{box-sizing:border-box;font-family:"PingFang SC","Microsoft YaHei",sans-serif}
  body{margin:0;background:#0b1020;color:#f8fafc;min-height:100vh;display:flex;align-items:center;justify-content:center}
  .card{background:rgba(15,23,42,.85);border:1px solid rgba(148,163,184,.18);border-radius:12px;padding:32px;width:min(100%,480px);margin:24px}
  h1{margin:0 0 4px;font-size:1.5rem}
  .sub{color:#94a3b8;font-size:.85rem;margin-bottom:24px}
  label{display:block;margin-top:16px;font-weight:700;font-size:.9rem}
  input{width:100%;margin-top:6px;padding:10px 12px;border:1px solid rgba(148,163,184,.25);border-radius:8px;background:rgba(2,6,23,.6);color:#f8fafc;font-size:.95rem}
  input:focus{outline:none;border-color:#22d3ee;box-shadow:0 0 0 3px rgba(34,211,238,.12)}
  button{margin-top:24px;width:100%;padding:12px;border:none;border-radius:8px;font-size:1rem;font-weight:700;cursor:pointer;background:linear-gradient(135deg,#4f7cff,#22d3ee);color:#020617}
  button:hover{opacity:.9}
  .toast{margin-top:16px;padding:12px;border-radius:8px;font-weight:700;display:none}
  .toast.ok{background:rgba(34,197,94,.15);border:1px solid rgba(34,197,94,.35);color:#bbf7d0;display:block}
  .toast.err{background:rgba(239,68,68,.15);border:1px solid rgba(239,68,68,.35);color:#fecaca;display:block}
  .tip{color:#94a3b8;font-size:.78rem;margin-top:4px}
  .section{margin-top:28px;padding-top:20px;border-top:1px solid rgba(148,163,184,.15)}
  .section h2{margin:0 0 12px;font-size:1.05rem}
  .acc-item,.rec-item{display:flex;gap:8px;align-items:center;background:rgba(2,6,23,.45);border:1px solid rgba(148,163,184,.15);border-radius:8px;padding:10px 14px;margin-top:8px;font-size:.88rem}
  .acc-item span,.rec-item span{flex:1}
  .del-btn{border:none;background:rgba(239,68,68,.2);color:#f87171;border-radius:6px;padding:4px 10px;cursor:pointer;font-size:.8rem}
  .del-btn:hover{background:rgba(239,68,68,.35)}
</style>
</head>
<body>
<div class="card">
  <h1>📧 邮箱配置</h1>
  <p class="sub">配置 QQ 邮箱账号，用于接收招募申请表单</p>

  <!-- 添加发件账号 -->
  <div class="section">
    <h2>发件邮箱（QQ 邮箱）</h2>
    <label>QQ 邮箱地址</label>
    <input id="accEmail" placeholder="123456789@qq.com"/>
    <label>SMTP 授权码 <span class="tip">QQ邮箱 → 设置 → 账户 → 开启SMTP → 生成授权码</span></label>
    <input id="accPass" type="password" placeholder="填授权码，不是 QQ 密码"/>
    <button onclick="addAccount()">添加发件账号</button>
  </div>

  <!-- 已添加的发件账号 -->
  <div class="section" id="accList">
    <h2>已配置的发件账号</h2>
    <div id="accItems"><p class="tip">暂无账号，请先添加</p></div>
  </div>

  <!-- 添加收件邮箱 -->
  <div class="section">
    <h2>收件邮箱（接收申请邮件）</h2>
    <label>收件邮箱地址</label>
    <input id="recEmail" placeholder="3574327015@qq.com"/>
    <button onclick="addRecipient()">添加收件邮箱</button>
  </div>

  <div class="section" id="recList">
    <h2>已配置的收件邮箱</h2>
    <div id="recItems"><p class="tip">暂无收件邮箱</p></div>
  </div>

  <div id="toast" class="toast"></div>
</div>

<script>
async function api(path, opt={}){
  const r = await fetch(path, opt);
  return r.json();
}
async function load(){
  const cfg = await api("/api/config");
  // 发件账号
  const accDiv = document.getElementById("accItems");
  if(cfg.accounts.length===0){accDiv.innerHTML='<p class="tip">暂无账号，请先添加</p>';}
  else{accDiv.innerHTML=cfg.accounts.map((a,i)=>`<div class="acc-item"><span>${a.email} <small style="color:#64748b">(${a.password_mask||'***'})</small></span><button class="del-btn" onclick="delAccount(${i})">删除</button></div>`).join("");}
  // 收件邮箱
  const recDiv = document.getElementById("recItems");
  if(cfg.recipients.length===0){recDiv.innerHTML='<p class="tip">暂无收件邮箱</p>';}
  else{recDiv.innerHTML=cfg.recipients.map((r,i)=>`<div class="rec-item"><span>${r}</span><button class="del-btn" onclick="delRecipient(${i})">删除</button></div>`).join("");}
}
async function addAccount(){
  const email=document.getElementById("accEmail").value.trim();
  const pass=document.getElementById("accPass").value.trim();
  if(!email||!pass)return show("请填写完整",true);
  const r=await api("/api/config/account",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email,password:pass})});
  if(r.ok){document.getElementById("accEmail").value="";document.getElementById("accPass").value="";show("添加成功！");load();}else{show(r.error||"添加失败",true);}
}
async function delAccount(i){
  await api("/api/config/account/"+i,{method:"DELETE"});load();
}
async function addRecipient(){
  const email=document.getElementById("recEmail").value.trim();
  if(!email)return show("请填写邮箱",true);
  const r=await api("/api/config/recipient",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email})});
  if(r.ok){document.getElementById("recEmail").value="";show("添加成功！");load();}else{show(r.error||"添加失败",true);}
}
async function delRecipient(i){
  await api("/api/config/recipient/"+i,{method:"DELETE"});load();
}
function show(msg,err){const t=document.getElementById("toast");t.className="toast "+(err?"err":"ok");t.textContent=msg;setTimeout(()=>t.style.display="none",3000);}
load();
</script>
</body>
</html>"""

@app.route("/")
def index():
    return render_template_string(INDEX_HTML)

@app.route("/api/config", methods=["GET"])
def get_config():
    cfg = load_config()
    # 返回时隐藏授权码，只显示前2位+***
    for acc in cfg.get("accounts", []):
        pwd = acc.get("password", "")
        if pwd:
            acc["password_mask"] = pwd[:2] + "***"
        acc.pop("password", None)
    return jsonify(cfg)

@app.route("/api/config/account", methods=["POST"])
def add_account():
    data  = request.get_json(force=True)
    email = data.get("email", "").strip()
    pwd   = data.get("password", "").strip()
    if not email or not pwd:
        return jsonify({"error": "邮箱和授权码不能为空"}), 400
    cfg = load_config()
    if any(a["email"] == email for a in cfg["accounts"]):
        return jsonify({"error": "该邮箱已存在"}), 400
    cfg["accounts"].append({"email": email, "password": pwd})
    save_config(cfg)
    return jsonify({"ok": True})

@app.route("/api/config/account/<int:idx>", methods=["DELETE"])
def del_account(idx):
    cfg = load_config()
    if 0 <= idx < len(cfg["accounts"]):
        cfg["accounts"].pop(idx)
        save_config(cfg)
    return jsonify({"ok": True})

@app.route("/api/config/recipient", methods=["POST"])
def add_recipient():
    data  = request.get_json(force=True)
    email = data.get("email", "").strip()
    if not email:
        return jsonify({"error": "邮箱不能为空"}), 400
    cfg = load_config()
    if email in cfg["recipients"]:
        return jsonify({"error": "该邮箱已存在"}), 400
    cfg["recipients"].append(email)
    save_config(cfg)
    return jsonify({"ok": True})

@app.route("/api/config/recipient/<int:idx>", methods=["DELETE"])
def del_recipient(idx):
    cfg = load_config()
    if 0 <= idx < len(cfg["recipients"]):
        cfg["recipients"].pop(idx)
        save_config(cfg)
    return jsonify({"ok": True})

@app.route("/api/recruit", methods=["POST"])
def recruit():
    cfg = load_config()

    # 发件账号：优先配置文件，没有则读环境变量（生产环境）
    accounts = cfg.get("accounts", [])
    if accounts:
        acc = accounts[0]
        sender_email    = acc["email"]
        sender_password = acc["password"]
    else:
        sender_email    = os.getenv("QQ_EMAIL", "")
        sender_password = os.getenv("QQ_AUTH_CODE", "")
        if not sender_email or not sender_password:
            return jsonify({"error": "未配置发件邮箱，请先在配置页面添加，或设置环境变量 QQ_EMAIL / QQ_AUTH_CODE"}), 500

    if not cfg.get("recipients"):
        return jsonify({"error": "未配置收件邮箱"}), 500

    # 支持 JSON 和 FormData 两种格式
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()
    nickname = data.get("nickname", "")
    contact  = data.get("contact", "")
    maps     = data.get("maps", "")
    schedule = data.get("schedule", "")
    intro    = data.get("intro", "")

    html = f"""
    <h2>混水电竞 - 新招募申请</h2>
    <p><strong>游戏昵称：</strong>{nickname}</p>
    <p><strong>联系方式：</strong>{contact}</p>
    <p><strong>擅长地图/玩法：</strong>{maps}</p>
    <p><strong>在线时间：</strong>{schedule}</p>
    <p><strong>自我介绍：</strong><br/>{intro.replace(chr(10),"<br/>")}</p>
    <hr/>
    <p style="color:#888;font-size:12px;">来自混水电竞官网招募表单</p>
    """

    try:
        send_email(sender_email, sender_password, cfg["recipients"],
                   f"混水电竞招募申请 - {nickname}", html)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": f"发信失败：{str(e)}"}), 500

@app.route("/api/health")
def health():
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)