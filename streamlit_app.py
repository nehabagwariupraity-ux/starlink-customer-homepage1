import csv
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="StarLink customer home", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
:root { --red:#e3203b; --ink:#17131a; --muted:#817a82; --line:#ebe7e4; }
html,body,[class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background:#f8f7f5; color:var(--ink); }
.block-container { max-width:1180px; padding:1.5rem 2rem 3rem; }
header[data-testid="stHeader"] { background:#fff; }
.brand { display:flex; align-items:center; gap:10px; color:var(--red); font:800 26px Manrope; letter-spacing:-1.5px; }
.mark { display:inline-grid; place-items:center; width:30px; height:30px; border-radius:50%; background:var(--red); color:#fff; font-size:17px; }
.nav { display:flex; gap:30px; align-items:center; border-bottom:1px solid var(--line); margin:0 -2rem 2.2rem; padding:0 2rem; height:62px; background:#fff; }
.nav span { color:#7c757d; font-size:14px; padding:22px 0 19px; }
.nav .selected { color:var(--ink); font-weight:700; border-bottom:3px solid var(--red); }
.profile { margin-left:auto; color:#6f6870; font-size:12px; display:flex; gap:9px; align-items:center; }
.avatar { display:grid; place-items:center; width:34px; height:34px; border-radius:50%; background:#fce5e9; color:#c61c37; font-weight:700; }
h1,h2,h3 { font-family:'Manrope',sans-serif; color:var(--ink); }
h1 { font-size:32px; letter-spacing:-1.1px; margin:0 0 .4rem; }
h2 { font-size:22px; letter-spacing:-.6px; margin:.1rem 0 .9rem; }
h3 { font-size:17px; margin:.55rem 0 .45rem; }
.eyebrow { color:var(--red); font-size:10px; letter-spacing:1.5px; font-weight:700; margin:0 0 .55rem; }
.subtle { color:var(--muted); font-size:13px; }
.card { border:1px solid var(--line); border-radius:14px; background:#fff; padding:1.5rem; min-height:215px; box-shadow:0 4px 14px #1e161c06; }
.card-head { display:flex; justify-content:space-between; align-items:center; color:#716a70; font-size:10px; letter-spacing:1.1px; font-weight:700; }
.pill { border-radius:5px; padding:6px 8px; color:#bf790c; background:#fff5dc; font-size:9px; letter-spacing:1px; }
.amount { font:800 32px Manrope; margin-top:1.15rem; }
.due { color:#8e878c; font-size:12px; margin:.25rem 0 1.2rem; }
.divider { border-top:1px solid #f0eded; margin:1rem 0; }
.plan-name { font:700 22px Manrope; margin:1.5rem 0 .2rem; }
.plan-features { display:flex; gap:14px; color:#777078; font-size:11px; margin-top:1.3rem; }
.plan-features span:before { content:'✓'; color:#2d9d59; font-weight:700; margin-right:4px; }
.section { margin-top:3rem; }
.section-head { display:flex; justify-content:space-between; align-items:end; margin-bottom:1rem; }
.updated { color:#918a8f; font-size:11px; }
.dot { color:#45b873; font-size:16px; vertical-align:-1px; }
.usage-number { font:800 29px Manrope; margin-top:1.6rem; }
.usage-bar { background:#f3e9ea; height:8px; border-radius:10px; overflow:hidden; margin:.8rem 0 .45rem; }
.usage-bar span { display:block; height:100%; background:linear-gradient(90deg,var(--red),#f06a72); border-radius:10px; }
.usage-foot { display:flex; justify-content:space-between; color:#928b90; font-size:11px; }
.signal { background:#fffaf5; }
.signal-icon { float:right; background:#fff1e5; border-radius:10px; padding:9px; color:#d87929; font-size:20px; }
.signal p { color:#7f7775; line-height:1.6; font-size:12px; max-width:290px; }
.recommendation { min-height:230px; }
.recommendation.featured { background:linear-gradient(135deg,#fff 55%,#fff5f5); border-color:#f2b6be; }
.rec-icon { display:inline-grid; place-items:center; width:35px; height:35px; background:#fce5e9; border-radius:10px; color:var(--red); font-size:18px; }
.rec-kicker { color:#d83048; font-size:9px; letter-spacing:1px; font-weight:700; margin-top:.65rem; }
.rec-copy { color:#7f777d; font-size:12px; line-height:1.5; min-height:42px; }
.rec-price { color:#312a30; font-size:15px; font-weight:700; margin:1rem 0; }
.saving { color:#2f9456; }
.support { display:flex; align-items:center; gap:15px; border:1px solid var(--line); border-radius:12px; background:#fff; padding:1rem 1.2rem; margin-top:3rem; }
.support strong { font-size:13px; }.support p { margin:3px 0 0; color:#8a8389; font-size:11px; }
div.stButton > button { border-radius:8px; border:1px solid #e4dfe0; font-weight:600; color:#4f4850; background:#fff; }
div.stButton > button[kind="primary"] { background:var(--red); border-color:var(--red); color:#fff; }
div[data-testid="stHorizontalBlock"] { gap:1.1rem; }
@media (max-width: 800px) { .block-container{padding:1rem}.nav{margin:0 -1rem 1.5rem;padding:0 1rem;gap:14px}.nav span{font-size:12px}.profile{display:none}h1{font-size:27px}.plan-features{flex-wrap:wrap}.section{margin-top:2.2rem} }
</style>
""", unsafe_allow_html=True)

CSV_PATH = Path(__file__).with_name("customer_usage.csv")

if "toast" not in st.session_state:
    st.session_state.toast = ""

def load_customers():
    with CSV_PATH.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))

def save_customers(customers):
    with CSV_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=customers[0].keys())
        writer.writeheader()
        writer.writerows(customers)

customers = load_customers()
customer_names = [customer["name"] for customer in customers]
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<div style="max-width:460px;margin:4rem auto 0;text-align:center"><div class="brand" style="justify-content:center"><span class="mark">⚡</span>StarLink<span style="color:#f5a100">.</span></div><h1 style="margin-top:1.5rem">Sign in to your account</h1><p class="subtle">Choose your customer profile to view personalized usage and recommendations.</p></div>', unsafe_allow_html=True)
    with st.form("sign_in_form"):
        login_name = st.selectbox("Customer", customer_names)
        login_pin = st.text_input("4-digit PIN", type="password", max_chars=4, placeholder="Try 1234")
        submitted = st.form_submit_button("Sign in", type="primary", use_container_width=True)
        if submitted:
            matched = next(item for item in customers if item["name"] == login_name)
            if login_pin == matched["pin"]:
                st.session_state.logged_in = True
                st.session_state.selected_name = login_name
                st.rerun()
            else:
                st.error("Incorrect PIN. Please try again.")
    st.stop()

selected_name = st.session_state.selected_name
customer = next(item for item in customers if item["name"] == selected_name)
allocated_gb = float(customer["allocated_data_gb"])
used_gb = float(customer["data_used_gb"])
remaining_gb = max(0, allocated_gb - used_gb)
usage_percent = min(100, round((used_gb / allocated_gb) * 100)) if allocated_gb else 0
recommended_gb = max(allocated_gb * 2, used_gb + 5) if remaining_gb == 0 else allocated_gb

def apply_addon():
    customer["allocated_data_gb"] = str(int(recommended_gb))
    customer["data_used_gb"] = str(int(used_gb))
    customer["last_action"] = f"Upgraded to {int(recommended_gb)}GB plan"
    save_customers(customers)
    st.session_state.toast = f"{customer['name']}'s plan is now {int(recommended_gb)}GB."

def notify(message):
    st.session_state.toast = message

st.markdown(f'<div class="nav"><div class="brand"><span class="mark">⚡</span>StarLink<span style="color:#f5a100">.</span></div><span class="selected">Overview</span><span>Usage</span><span>Bills & payments</span><span>Support</span><div class="profile"><span class="avatar">{selected_name[:2].upper()}</span><span><b>{selected_name}</b><br>Personal account</span>⌄</div></div>', unsafe_allow_html=True)
if st.button("Sign out", key="sign_out"):
    st.session_state.logged_in = False
    st.rerun()

st.markdown(f'<p class="eyebrow">TUESDAY, OCTOBER 20, 2026</p><h1>Good morning, {selected_name} <span style="color:#e3203b">✦</span></h1><p class="subtle">Here’s your account at a glance.</p>', unsafe_allow_html=True)
st.write("")

bill_col, plan_col = st.columns([1.12, .88])
with bill_col:
    st.markdown(f'<div class="card"><div class="card-head"><span>▣ &nbsp; CURRENT BILL</span><span class="pill">● DUE SOON</span></div><div class="amount">₹39.99</div><div class="due">Due on <b>28 October 2026</b></div><div class="divider"></div><span class="subtle">Auto-pay is <b>off</b></span></div>', unsafe_allow_html=True)
    if st.button("Pay bill  →", type="primary", key="pay", use_container_width=False): notify("Payment flow opened for your current bill.")
with plan_col:
    st.markdown(f'<div class="card"><div class="card-head"><span>▣ &nbsp; YOUR PLAN</span><span style="color:#31844e">ACTIVE</span></div><div class="plan-name">{customer["plan_name"]}</div><b>₹39.99 <span class="subtle">/ month</span></b><div class="plan-features"><span>{int(allocated_gb)} GB data</span><span>1,000 min</span><span>200 SMS</span></div><br><span style="color:#d71c37;font-weight:700;font-size:12px">View plan details →</span></div>', unsafe_allow_html=True)

st.markdown('<div class="section-head section"><div><p class="eyebrow">PERSONALIZED FOR YOU</p><h2>Make the most of your connection</h2></div><span class="updated">Updated just now <span class="dot">•</span></span></div>', unsafe_allow_html=True)
usage_col, signal_col = st.columns([1.22, .78])
with usage_col:
    st.markdown(f'<div class="card"><div class="card-head"><span>▥ &nbsp; THIS MONTH’S USAGE</span><span>1–31 Oct</span></div><div class="usage-number">{used_gb:g} GB <span class="subtle">of {allocated_gb:g} GB</span></div><div class="usage-bar"><span style="width:{usage_percent}%"></span></div><div class="usage-foot"><span><b>{usage_percent}%</b> used</span><span>{remaining_gb:g} GB remaining</span></div><div class="divider"></div><div class="usage-foot"><span>Allocated: <b>{allocated_gb:g} GB</b></span><span>Used: <b>{used_gb:g} GB</b></span></div></div>', unsafe_allow_html=True)
with signal_col:
    st.markdown('<div class="card signal"><span class="signal-icon">⌁</span><p class="eyebrow" style="color:#d97626">YOUR CONNECTION</p><h3>Everything looks good</h3><p>Great coverage in your area. Your 4G+ connection is performing at its best.</p><div class="divider"></div><span style="font-size:11px;color:#6c6462">▂▃▅▇ Strong signal</span></div>', unsafe_allow_html=True)

st.markdown('<div class="section-head section"><div><p class="eyebrow">SMART RECOMMENDATIONS</p><h2>Picked for your needs</h2><p class="subtle">Based on your usage, bill history, and offers available to you.</p></div><span class="pill" style="color:#b46f13">⚡ AI-powered</span></div>', unsafe_allow_html=True)
rec1, rec2 = st.columns(2)
with rec1:
    rec_copy = f"You have used {used_gb:g}GB of your {allocated_gb:g}GB allocation. Add more data to keep browsing without interruption." if remaining_gb == 0 else f"You have {remaining_gb:g}GB remaining. Your current {allocated_gb:g}GB plan is the best fit right now."
    rec_kicker = "RECOMMENDED DATA PLAN" if remaining_gb == 0 else "CURRENT PLAN RECOMMENDED"
    rec_price = "+₹20 <span class=\"subtle\">per month</span>" if remaining_gb == 0 else "No change needed"
    st.markdown(f'<div class="card recommendation featured"><span class="rec-icon">⚡</span><div class="rec-kicker">{rec_kicker}</div><h3>{int(recommended_gb)}GB StarLink plan</h3><div class="rec-copy">{rec_copy}</div><div class="rec-price">{rec_price}</div></div>', unsafe_allow_html=True)
    if remaining_gb == 0:
        if st.button(f"Select {int(recommended_gb)}GB add-on  →", type="primary", key="upgrade"): apply_addon()
    else:
        st.button(f"Keep {int(recommended_gb)}GB plan", key="upgrade", disabled=True)
with rec2:
    st.markdown('<div class="card recommendation"><span class="rec-icon">✓</span><div class="rec-kicker">SPECIAL OFFER</div><h3>10% off with Auto-pay</h3><div class="rec-copy">A simple way to save on your StarLink bill every month when you turn on Auto-pay.</div><div class="rec-price saving">10% off <span class="subtle">your monthly bill</span></div></div>', unsafe_allow_html=True)
    if st.button("Enable offer  →", key="autopay"): notify("Auto-pay offer selected.")

st.markdown('<div class="support"><span style="font-size:22px">?</span><div><strong>Need help with your account?</strong><p>Find answers or chat with us anytime.</p></div></div>', unsafe_allow_html=True)
if st.session_state.toast:
    st.success(st.session_state.toast)
