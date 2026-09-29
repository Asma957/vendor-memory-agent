"""Vendor Memory Agent - dashboard UI (Streamlit)."""
import html
import re

import streamlit as st

import agents
import config
import memory

st.set_page_config(page_title="Vendor Memory Agent", page_icon="🧠", layout="wide",
                   initial_sidebar_state="collapsed")


def esc(x):
    return html.escape(str(x)).replace("$", "&#36;")


def md(x):
    return str(x).replace("$", "\\$")


def stale_terms(vendor, answer):
    """Labels of retired terms whose old values still appear in an answer (approximate text check)."""
    terms = memory.build_ledger()[vendor]["terms"]
    text = re.split(r"(?im)^#+\s*outdated", answer)[0]
    active = " ".join(t["value"] for t in terms if t["status"] == "active").lower()
    hits = []
    for t in terms:
        if t["status"] != "superseded":
            continue
        toks = [k for k in re.findall(r"24/7|\$?\d[\d,]*(?:\.\d+)?%?|waived", t["value"], flags=re.I)
                if k.lower() not in active]
        if any(re.search(r"(?<![\d.,])" + re.escape(k) + r"(?![\d])", text, flags=re.I) for k in toks):
            hits.append(t["label"])
    return hits


def compare_bar(vendor, res):
    def tile(title, res_, good):
        if "error" in res_:
            return f'<div class="cmp"><b>{title}</b><span class="sub">Not available</span></div>'
        hits = stale_terms(vendor, res_["answer"])
        n = len(hits)
        if good:
            head, col = ("No outdated term used", "#137A47") if n == 0 else (f"{n} outdated term(s) slipped through", "#B42318")
        else:
            head, col = ((f"{n} outdated term(s) quoted as current", "#B42318") if n
                         else ("No outdated term quoted this time", "#137A47"))
        detail = ", ".join(hits) if hits else "Every term matches the active contract."
        return (f'<div class="cmp"><span class="sub">{title}</span><b style="color:{col}">{head}</b>'
                f'<span class="sub">{esc(detail)}</span></div>')
    st.markdown('<div class="cmpwrap">' + tile("Before: standard memory agent", res["baseline"], False)
                + tile("After: Vendor Memory Agent", res["smart"], True) + '</div>'
                '<div class="sub" style="margin:6px 0 14px">Automatic check that looks for retired values in each answer. '
                'It is approximate, so read the briefs below too.</div>', unsafe_allow_html=True)


CATEGORY = {"Apex Logistics": ("Freight & Logistics", "#6C5CE7", "#EFECFD"),
            "Nimbus Cloud Services": ("Cloud & Hosting", "#0E9AA7", "#E2F5F7"),
            "Sterling Office Supplies": ("Office Supplies", "#E0812B", "#FCEFE0")}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
html, body, .stApp, button, input, textarea, [data-testid="stMarkdownContainer"] { font-family:'Plus Jakarta Sans',sans-serif; }
.stApp { background:#F4F6FB; }
header[data-testid="stHeader"], #MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], [data-testid="stExpandSidebarButton"] { display:none !important; }
.block-container, [data-testid="stMainBlockContainer"] { padding:1.2rem 2rem 6.5rem !important; max-width:1440px; }
[data-testid="stHorizontalBlock"] { flex-wrap:wrap; row-gap:1rem; }
/* ---- top navigation bar (replaces the sidebar, always visible at any zoom) ---- */
.st-key-topbar { background:#13143A; border-radius:16px; padding:12px 20px; margin-bottom:22px; box-shadow:0 8px 24px rgba(19,20,58,.18); }
.st-key-topbar [data-testid="stHorizontalBlock"] { align-items:center; column-gap:1rem; row-gap:.5rem; }
.st-key-topbar [data-testid="stHorizontalBlock"] > * { width:auto !important; min-width:0 !important; flex:0 0 auto !important; }
.st-key-topbar [data-testid="stHorizontalBlock"] > *:nth-child(2) { flex:1 1 330px !important; }
.tb-brand { display:flex; gap:11px; align-items:center; }
.tb-brand .lg { width:36px; height:36px; border-radius:10px; background:#7C6CF2; display:grid; place-items:center; font-size:18px; flex:none; }
.tb-brand b, .tb-brand small { white-space:nowrap; } .tb-brand b { color:#fff; font-size:.98rem; display:block; line-height:1.2; } .tb-brand small { color:#8F93C9; font-size:.72rem; }
.tb-user { display:flex; gap:10px; align-items:center; justify-content:flex-end; }
.tb-user b { color:#fff; font-size:.85rem; display:block; line-height:1.2; } .tb-user small { color:#8F93C9; font-size:.72rem; }
.av { width:34px; height:34px; border-radius:50%; background:#7C6CF2; color:#fff; display:grid; place-items:center; font-weight:700; flex:none; }
.st-key-topbar [role="radiogroup"] { gap:6px; flex-wrap:wrap; justify-content:center; }
.st-key-topbar [role="radiogroup"] label { padding:8px 16px; border-radius:999px; cursor:pointer; margin:0; }
.st-key-topbar [role="radiogroup"] label > div:first-child { display:none; }
.st-key-topbar [role="radiogroup"] label p { color:#C4C7EC; font-size:.88rem; white-space:nowrap; margin:0; }
.st-key-topbar [role="radiogroup"] label:hover { background:#1E1F52; }
.st-key-topbar [role="radiogroup"] label:has(input:checked) { background:#7C6CF2; }
.st-key-topbar [role="radiogroup"] label:has(input:checked) p { color:#fff; font-weight:600; }
/* ---- cards ---- */
[class*="st-key-card"], .st-key-controls { background:#fff; border:1px solid #E8EBF3; border-radius:16px; padding:20px 22px; min-width:0;
  box-shadow:0 1px 2px rgba(28,35,64,.04), 0 8px 24px rgba(28,35,64,.05); }
.st-key-hero { background:linear-gradient(120deg,#15153F 0%,#2B2470 100%); border-radius:18px; padding:28px 32px; }
.st-key-hero h2 { color:#fff; font-size:clamp(1.35rem,2.2vw,1.75rem); font-weight:800; line-height:1.2; margin:0 0 10px; padding:0; letter-spacing:-.02em; }
.st-key-hero p { color:#C9CBEF; font-size:.95rem; line-height:1.55; max-width:520px; }
.st-key-hero .stButton > button { background:#7C6CF2; color:#fff; border:0; border-radius:10px; padding:.65rem 1.5rem; font-weight:600; margin-top:10px; }
.st-key-hero .stButton > button:hover { background:#8B7DF5; color:#fff; }
/* ---- responsive grids: columns wrap by available width, no overlap at any zoom ---- */
[data-testid="stHorizontalBlock"]:has(.st-key-hero) > *:nth-child(1) { flex:2.25 1 640px !important; min-width:0 !important; width:auto !important; }
[data-testid="stHorizontalBlock"]:has(.st-key-hero) > *:nth-child(2) { flex:1 1 300px !important; min-width:0 !important; width:auto !important; }
.st-key-hero [data-testid="stHorizontalBlock"] > *:nth-child(1) { flex:3 1 300px !important; min-width:0 !important; width:auto !important; }
.st-key-hero [data-testid="stHorizontalBlock"] > *:nth-child(2) { flex:2 1 230px !important; min-width:0 !important; width:auto !important; }
.st-key-pair_v [data-testid="stHorizontalBlock"] > *, .st-key-pair_h1 [data-testid="stHorizontalBlock"] > *, .st-key-pair_h2 [data-testid="stHorizontalBlock"] > * { flex:1 1 330px !important; min-width:0 !important; width:auto !important; }
.st-key-pair_b [data-testid="stHorizontalBlock"] > * { flex:1 1 420px !important; min-width:0 !important; width:auto !important; }
.st-key-controls [data-testid="stHorizontalBlock"] > * { flex:1 1 200px !important; min-width:0 !important; width:auto !important; }
.st-key-mh_head [data-testid="stHorizontalBlock"] > * { flex:1 1 240px !important; min-width:0 !important; width:auto !important; }
.st-key-mh_head [data-testid="stHorizontalBlock"] > *:last-child { flex:0 1 240px !important; }
.st-key-qa [data-testid="stHorizontalBlock"] > * { flex:1 1 150px !important; min-width:0 !important; width:auto !important; }
/* ---- hero visual ---- */
.orb { display:flex; flex-direction:column; align-items:center; gap:12px; padding:4px 0; }
.core { width:92px; height:92px; border-radius:50%; flex:none;
  background:radial-gradient(circle,#8B7DF5 0%,#4B3FB8 60%,transparent 72%); display:grid; place-items:center; font-size:42px; }
.chips { display:flex; flex-direction:column; gap:8px; width:100%; align-items:stretch; }
.fl { background:rgba(255,255,255,.1); border:1px solid rgba(255,255,255,.18); color:#fff; font-size:.8rem; padding:8px 14px; border-radius:11px; text-align:center; }
/* ---- stats ---- */
.stats { display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:14px; margin:18px 0; }
@media (max-width:820px) { .stats { grid-template-columns:repeat(2,1fr); } }
.stat { background:#fff; border:1px solid #E8EBF3; border-radius:14px; padding:16px 18px; display:flex; gap:14px; align-items:center; min-width:0; }
.stat > div:last-child { min-width:0; }
.ico { width:44px; height:44px; border-radius:12px; display:grid; place-items:center; font-size:20px; flex:none; }
.stat small { color:#6B7390; font-size:.78rem; display:block; } .stat b { font-size:1.6rem; color:#1C2340; line-height:1.2; display:block; }
.stat em { font-style:normal; font-size:.72rem; color:#7A8199; display:block; line-height:1.3; }
.h { font-size:1rem; font-weight:700; color:#1C2340; margin:0 0 10px; }
.sub { font-size:.82rem; color:#6B7390; }
/* ---- lists ---- */
.li { display:flex; gap:12px; align-items:center; padding:11px 0; border-bottom:1px solid #EFF1F6; }
.li:last-child { border-bottom:0; } .li .t { font-size:.9rem; font-weight:600; color:#1C2340; } .li .d { font-size:.78rem; color:#6B7390; line-height:1.4; }
.li .g { flex:1; min-width:0; overflow-wrap:anywhere; } .li .dt { flex:none; white-space:nowrap; font-size:.78rem; color:#6B7390; }
.tag { font-size:.7rem; font-weight:600; padding:3px 10px; border-radius:999px; white-space:nowrap; flex:none; display:inline-block; }
.tag.ok { background:#E3F6EC; color:#137A47; } .tag.warn { background:#FDF0DA; color:#9A5B00; } .tag.info { background:#EFECFD; color:#5646D6; }
.dot { width:38px; height:38px; border-radius:11px; display:grid; place-items:center; font-weight:700; font-size:.85rem; flex:none; }
.ins { padding:11px 0; border-bottom:1px solid #EFF1F6; } .ins:last-child { border-bottom:0; }
.ins .tag { margin-bottom:6px; } .ins p { margin:0; font-size:.88rem; line-height:1.45; color:#1C2340; } .ins .sub { margin-top:3px; font-size:.75rem; }
.ba { padding:11px 0; border-bottom:1px solid #EFF1F6; } .ba:last-child { border-bottom:0; }
.ba .t { font-size:.9rem; font-weight:600; color:#1C2340; margin-bottom:6px; }
.ba .pair { display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:8px; }
.ba .pair div { font-size:.8rem; color:#6B7390; padding:8px 12px; border-radius:10px; background:#F7F8FC; overflow-wrap:anywhere; }
.row { display:grid; grid-template-columns:1fr auto; gap:2px 10px; padding:11px 0; border-bottom:1px solid #EFF1F6; }
.row:last-child { border-bottom:0; }
.lab { font-size:.76rem; color:#6B7390; } .val { font-size:.92rem; font-weight:600; color:#1C2340; overflow-wrap:anywhere; }
.row .tag { grid-row:1 / span 2; grid-column:2; align-self:center; }
.row.old .val { text-decoration:line-through; color:#98A0B5; font-weight:500; } .rep { font-size:.76rem; color:#9A5B00; }
.cmpwrap { display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:16px; }
.cmp { background:#fff; border:1px solid #E8EBF3; border-radius:14px; padding:14px 18px; display:flex; flex-direction:column; gap:3px; }
.cmp b { font-size:1.05rem; }
.page-h { font-size:1.55rem; font-weight:800; color:#1C2340; letter-spacing:-.02em; margin:0; }
/* ---- quick actions: full labels, no ellipsis ---- */
.st-key-qa .stButton > button { width:100%; min-height:58px; height:auto; white-space:normal; text-align:left; background:#fff; border:1px solid #E8EBF3;
  border-radius:12px; color:#1C2340; font-weight:600; font-size:.85rem; padding:.55rem .9rem; }
.st-key-qa .stButton > button p { white-space:normal !important; overflow:visible !important; text-overflow:clip !important; line-height:1.3; }
.st-key-qa .stButton > button:hover { border-color:#7C6CF2; color:#5646D6; }
.st-key-card_bl { border-top:3px solid #D92D20; } .st-key-card_bm { border-top:3px solid #7C6CF2; }
[class*="st-key-card_b"] h1, [class*="st-key-card_b"] h2, [class*="st-key-card_b"] h3, [class*="st-key-card_b"] h4 {
  font-size:.95rem !important; font-weight:700 !important; margin:16px 0 4px !important; padding:0 !important; color:#1C2340; }
[class*="st-key-card_b"] p, [class*="st-key-card_b"] li { font-size:.9rem; line-height:1.55; color:#2A3350; }
.stButton > button[kind="primary"] { background:#7C6CF2; border:0; border-radius:10px; font-weight:600; }
.stButton > button { border-radius:10px; }
/* ---- bottom ask bar: slim, no big opaque block ---- */
[data-testid="stBottom"], [data-testid="stBottom"] > div { background:transparent !important; }
[data-testid="stBottomBlockContainer"] { padding:1.4rem 2rem .8rem !important; max-width:1440px;
  background:linear-gradient(180deg,rgba(244,246,251,0) 0%,#F4F6FB 40%) !important; }
[data-testid="stChatInput"] { background:#fff; border:1px solid #E1E5F0; border-radius:16px; box-shadow:0 6px 20px rgba(28,35,64,.08); }
@media (max-width:700px) {
  .block-container, [data-testid="stMainBlockContainer"] { padding:.8rem 1rem 6.5rem !important; }
  [data-testid="stBottomBlockContainer"] { padding:1.2rem 1rem .6rem !important; }
  .st-key-hero { padding:22px 20px; } .tb-user small { display:none; }
}
</style>
""", unsafe_allow_html=True)

missing = [n for n, v in [("HINDSIGHT_API_KEY", config.HINDSIGHT_API_KEY), ("GROQ_API_KEY", config.GROQ_API_KEY)] if not v]
if missing:
    st.error(f"Missing settings: {', '.join(missing)}. Add them to .env (local) or Streamlit Secrets (cloud).")
    st.stop()


@st.cache_resource
def client_():
    return memory.get_client()


client = client_()
if "seeded" not in st.session_state:
    st.session_state.seeded = memory.is_seeded(client)
names = memory.vendor_names()
PAGES = ["🏠  Dashboard", "📝  Brief Studio", "🧠  Memory Hub"]
for k in ("_goto", "_vendor"):
    if k in st.session_state:
        st.session_state["page" if k == "_goto" else "cur_vendor"] = st.session_state.pop(k)
st.session_state.setdefault("cur_vendor", names[0])


def go(page):
    st.session_state["_goto"] = page
    st.rerun()


def generate(vendor, mode, question):
    want = {"Smart only": ["smart"], "Baseline only": ["baseline"]}.get(mode, ["baseline", "smart"])
    out = {}
    with st.spinner(f"Recalling {vendor} memories and writing the brief..."):
        for name in want:
            fn = agents.smart_brief if name == "smart" else agents.baseline_brief
            try:
                out[name] = fn(client, vendor, question)
            except Exception as e:
                out[name] = {"error": str(e)}
    st.session_state["result"] = {"vendor": vendor, "results": out}


@st.dialog("Add a contract update")
def update_dialog(vendor):
    st.caption(f"Vendor: {vendor}. The earlier value of the term you pick becomes outdated.")
    seen, choices = set(), {}
    for t in memory.build_ledger()[vendor]["terms"]:
        if t["key"] not in seen:
            seen.add(t["key"])
            choices[t["label"]] = t["key"]
    label = st.selectbox("Term that changed", list(choices.keys()))
    value = st.text_input("New value", placeholder="e.g. Fixed for 12 months")
    desc = st.text_input("What happened", placeholder="e.g. issued a revised rate card")
    if st.button("Save update", type="primary"):
        if not value.strip() or not desc.strip():
            st.warning("Enter both the new value and what happened.")
            return
        try:
            with st.spinner("Saving to Hindsight..."):
                memory.add_live_update(client, vendor, choices[label], label, value.strip(), desc)
            st.rerun()
        except Exception as e:
            st.error(f"Could not save the update: {e}")


# ---------------------------------------------------------------- top bar
with st.container(key="topbar"):
    tb1, tb2, tb3 = st.columns([1.3, 2.4, 1.1], vertical_alignment="center", gap="small")
    tb1.markdown('<div class="tb-brand"><div class="lg">🧠</div><div><b>Vendor Memory Agent</b>'
                 '<small>Remember. Retire. Negotiate.</small></div></div>', unsafe_allow_html=True)
    page = tb2.radio("Navigate", PAGES, key="page", horizontal=True, label_visibility="collapsed")
    tb3.markdown(f'<div class="tb-user"><div class="av">{esc(config.USER_NAME[:1].upper())}</div>'
                 f'<div><b>{esc(config.USER_NAME)}</b><small>Procurement workspace</small></div></div>',
                 unsafe_allow_html=True)

ledger = memory.build_ledger()
events = memory.load_events()
n_active = sum(1 for v in ledger.values() for t in v["terms"] if t["status"] == "active")
n_old = sum(1 for v in ledger.values() for t in v["terms"] if t["status"] == "superseded")


def term_rows(terms, old=False):
    if not terms:
        return '<div class="sub">Nothing here yet.</div>'
    if not old:
        return "".join(f'<div class="row"><div class="lab">{esc(t["label"])}</div><div class="val">{esc(t["value"])}</div>'
                       f'<span class="tag ok">Active</span></div>' for t in terms)
    return "".join(f'<div class="row old"><div class="lab">{esc(t["label"])}</div><div class="val">{esc(t["value"])}</div>'
                   f'<div class="rep">Replaced {t["replaced_by"]["date"]} by {esc(t["replaced_by"]["value"])}</div>'
                   f'<span class="tag warn">Outdated</span></div>' for t in terms)


def brief_card(res, kind):
    title, sub = (("Before: standard memory agent", "Trusts every recalled memory as current") if kind == "bl"
                  else ("After: Vendor Memory Agent", "Uses only active terms from the ledger"))
    with st.container(key=f"card_b{kind}"):
        st.markdown(f'<div class="h" style="margin:0">{title}</div><div class="sub">{sub}</div>', unsafe_allow_html=True)
        if "error" in res:
            st.error(res["error"])
            return
        st.markdown(md(res["answer"]))
        with st.expander(f"Memories recalled from Hindsight ({len(res['memories'])})"):
            for m in res["memories"]:
                st.markdown("- " + md(m["text"]))
        if res.get("ledger_text"):
            with st.expander("Supersession Ledger given to the agent"):
                st.code(res["ledger_text"], language=None)


# --------------------------------------------------------------- dashboard
if page == PAGES[0]:
    st.markdown(f'<div class="page-h">Welcome back, {esc(config.USER_NAME)}</div>'
                f'<div class="sub" style="margin-bottom:16px">Here is what changed across your vendors.</div>',
                unsafe_allow_html=True)
    if not st.session_state.seeded:
        with st.container(key="card_seed"):
            st.markdown('<div class="h">Load the demo memories</div><div class="sub">Memory is empty. '
                        'Save the demo vendor history into Hindsight once to begin.</div>', unsafe_allow_html=True)
            if st.button("Load demo data", type="primary"):
                bar = st.progress(0.0, text="Saving memories...")
                try:
                    memory.seed_all(client, progress=lambda i, t, v: bar.progress(i / t, text=f"{i}/{t}: {v}"))
                    st.session_state.seeded = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Could not load data: {e}")
    main, side = st.columns([2.25, 1], gap="large")
    with main:
        with st.container(key="hero"):
            a, b = st.columns([3, 2])
            with a:
                st.markdown("## Your AI-powered Vendor Memory Agent")
                st.markdown("It remembers how every vendor negotiates, and it knows when an old deal term has been "
                            "replaced, so you never walk into a meeting with outdated pricing.")
                if st.button("Ask Vendor Memory Agent", disabled=not st.session_state.seeded):
                    go(PAGES[1])
            with b:
                st.markdown('<div class="orb"><div class="core">🧠</div><div class="chips">'
                            '<div class="fl">Remembering negotiations</div>'
                            '<div class="fl">Tracking contract terms</div>'
                            '<div class="fl">Retiring outdated deals</div></div></div>',
                            unsafe_allow_html=True)
        cards = [("Vendors tracked", len(names), f"{len(names)} in memory", "#EFECFD", "🏢"),
                 ("Memories retained", len(events), "negotiations and contracts", "#E2F5F7", "💬"),
                 ("Active terms", n_active, "valid today", "#E3F6EC", "✅"),
                 ("Outdated terms", n_old, "retired by newer contracts", "#FDF0DA", "🗂️")]
        st.markdown('<div class="stats">' + "".join(
            f'<div class="stat"><div class="ico" style="background:{bg}">{ic}</div><div><small>{esc(l)}</small>'
            f'<b>{v}</b><em>{esc(s)}</em></div></div>' for l, v, s, bg, ic in cards) + "</div>", unsafe_allow_html=True)
        with st.container(key="pair_v"):
            c1, c2 = st.columns(2, gap="medium")
        with c1, st.container(key="card_v"):
            rows = ""
            for v in names:
                cat, fg, bg = CATEGORY.get(v, ("Vendor", "#6C5CE7", "#EFECFD"))
                last = max(e["date"] for e in events if e["vendor"] == v)
                o = sum(1 for t in ledger[v]["terms"] if t["status"] == "superseded")
                tag = f'<span class="tag warn">{o} outdated</span>' if o else '<span class="tag ok">Up to date</span>'
                rows += (f'<div class="li"><div class="dot" style="background:{bg};color:{fg}">{esc(v[:2].upper())}</div>'
                         f'<div class="g"><div class="t">{esc(v)}</div><div class="d">{cat}, last update {last}</div></div>{tag}</div>')
            st.markdown(f'<div class="h">Your vendors</div>{rows}', unsafe_allow_html=True)
        with c2, st.container(key="card_i"):
            ins = []
            for v in names:
                for t in ledger[v]["terms"]:
                    if t["status"] == "superseded":
                        ins.append((t["replaced_by"]["date"], "Contract change", "warn",
                                    f'{v}: {t["label"]} changed from {t["value"]} to {t["replaced_by"]["value"]}.'))
            ins = sorted(ins, reverse=True)[:3]
            st.markdown('<div class="h">Smart insights</div>' + "".join(
                f'<div class="ins"><span class="tag {c}">{esc(g)}</span><p>{esc(x)}</p><div class="sub">{esc(d)}</div></div>'
                for d, g, c, x in ins), unsafe_allow_html=True)
        with st.container(key="card_ba"):
            ex = [(v, t) for v in names for t in ledger[v]["terms"] if t["status"] == "superseded"]
            ex = [x for x in ex if x[0] == ex[0][0]][:3] if ex else []
            lines = "".join(
                f'<div class="ba"><div class="t">{esc(t["label"])}</div><div class="pair">'
                f'<div>Before: <b style="color:#B42318">{esc(t["value"])}</b></div>'
                f'<div>After: <b style="color:#137A47">{esc(t["replaced_by"]["value"])}</b></div></div></div>'
                for _, t in ex)
            st.markdown(f'<div class="h">Before vs after{" : " + esc(ex[0][0]) if ex else ""}</div>'
                        f'<div class="sub">A standard agent can quote the old value. The Vendor Memory Agent uses the new one.</div>'
                        f'{lines}', unsafe_allow_html=True)
            if st.button("See the live comparison", type="primary"):
                go(PAGES[1])
    with side:
        with st.container(key="card_q"):
            st.markdown('<div class="h">Quick actions</div>', unsafe_allow_html=True)
            with st.container(key="qa"):
                q1, q2 = st.columns(2)
                if q1.button("Generate a brief", use_container_width=True):
                    go(PAGES[1])
                if q2.button("Open Memory Hub", use_container_width=True):
                    go(PAGES[2])
                if q1.button("Add contract update", use_container_width=True, disabled=not st.session_state.seeded):
                    update_dialog(st.session_state["cur_vendor"])
                if q2.button("Compare agents", use_container_width=True):
                    go(PAGES[1])
        with st.container(key="card_a"):
            acts = "".join(
                f'<div class="li"><div class="g"><div class="t">{esc(e["vendor"])}</div><div class="d">'
                f'{"Contract update" if e["kind"] == "contract_update" else "Negotiation"} retained</div></div>'
                f'<div class="dt">{e["date"]}</div></div>' for e in list(reversed(events))[:5])
            st.markdown(f'<div class="h">Recent activity</div>{acts}', unsafe_allow_html=True)

# ------------------------------------------------------------ brief studio
elif page == PAGES[1]:
    st.markdown('<div class="page-h">Brief Studio</div><div class="sub" style="margin-bottom:16px">'
                'Same Hindsight memory, answered by a Baseline agent and a Smart agent.</div>', unsafe_allow_html=True)
    with st.container(key="controls"):
        c1, c2, c3 = st.columns([2, 1.4, 1], vertical_alignment="bottom")
        vendor = c1.selectbox("Vendor", names, index=names.index(st.session_state["cur_vendor"]))
        st.session_state["cur_vendor"] = vendor
        mode = c2.selectbox("View", ["Compare", "Smart only", "Baseline only"])
        if c3.button("Generate brief", type="primary", use_container_width=True, disabled=not st.session_state.seeded):
            generate(vendor, mode, "I have a meeting with this vendor tomorrow. Prepare my negotiation brief.")
    r = st.session_state.get("result")
    st.write("")
    if not r:
        st.info("Choose a vendor and select Generate brief. Or type a question in the bar below.")
    else:
        st.markdown(f'<div class="h">Negotiation brief for {esc(r["vendor"])}</div>', unsafe_allow_html=True)
        res = r["results"]
        if len(res) == 2:
            compare_bar(r["vendor"], res)
            with st.container(key="pair_b"):
                a, b = st.columns(2, gap="medium")
            with a:
                brief_card(res["baseline"], "l")
            with b:
                brief_card(res["smart"], "m")
        else:
            k, v = next(iter(res.items()))
            brief_card(v, "l" if k == "baseline" else "m")

# -------------------------------------------------------------- memory hub
else:
    with st.container(key="mh_head"):
        h1, h2 = st.columns([3, 1], vertical_alignment="bottom")
    h1.markdown('<div class="page-h">Memory Hub</div><div class="sub">What the agent remembers, and what it has retired.</div>',
                unsafe_allow_html=True)
    vendor = st.selectbox("Vendor", names, index=names.index(st.session_state["cur_vendor"]))
    st.session_state["cur_vendor"] = vendor
    if h2.button("Add contract update", type="primary", use_container_width=True, disabled=not st.session_state.seeded):
        update_dialog(vendor)
    vl = ledger[vendor]
    act = [t for t in vl["terms"] if t["status"] == "active"]
    old = [t for t in vl["terms"] if t["status"] == "superseded"]
    with st.container(key="pair_h1"):
        a, b = st.columns(2, gap="medium")
    with a, st.container(key="card_h1"):
        st.markdown(f'<div class="h">Active terms ({len(act)})</div>{term_rows(act)}', unsafe_allow_html=True)
    with b, st.container(key="card_h2"):
        st.markdown(f'<div class="h">Outdated terms ({len(old)})</div>{term_rows(old, True)}', unsafe_allow_html=True)
    with st.container(key="pair_h2"):
        c, d = st.columns(2, gap="medium")
    with c, st.container(key="card_h3"):
        st.markdown('<div class="h">Vendor behaviour</div>' + "".join(
            f'<div class="li"><div class="g"><div class="d" style="color:#1C2340">{esc(p["text"])}</div></div>'
            f'<div class="d">{p["date"]}</div></div>' for p in vl["patterns"]), unsafe_allow_html=True)
    with d, st.container(key="card_h4"):
        st.markdown('<div class="h">Hindsight observations</div><div class="sub">Facts Hindsight consolidates in the '
                    'background. New ones can take a minute.</div>', unsafe_allow_html=True)
        if st.button("Load observations"):
            try:
                st.session_state[f"obs_{vendor}"] = memory.hindsight_observations(client, vendor)
            except Exception as e:
                st.error(f"Could not load observations: {e}")
        obs = st.session_state.get(f"obs_{vendor}")
        if obs is not None and not obs:
            st.info("No observations yet. Try again in a minute.")
        for o in obs or []:
            st.markdown("- " + md(o["text"]) + (f" (evidence: {o['proof_count']})" if o["proof_count"] is not None else ""))

# ---------------------------------------------------------- bottom ask bar
if page != PAGES[2]:
    ask = st.chat_input("Ask me anything about your vendors, e.g. Prepare me for Apex Logistics tomorrow")
    if ask:
        v = memory.find_vendor(ask) or st.session_state["cur_vendor"]
        generate(v, "Compare", ask)
        st.session_state["_vendor"] = v
        go(PAGES[1])
