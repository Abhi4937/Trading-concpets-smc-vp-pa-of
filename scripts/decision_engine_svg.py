#!/usr/bin/env python3
"""Parametric INTRADAY-OPTIONS DECISION-ENGINE SVG schematic + animation generator.

Deterministic, ~0 model tokens. Renders the full intraday decision pipeline: map only
the qualified levels, read the open + regime, decide HOLD/BREAK/WAIT at a level, pick
one of five plays, fire an LTF trigger, then gate the option strike + stop budget.
Reuses the render_scene engine + infographic patterns from breakout_svg.py (house style).

Usage:
  python decision_engine_svg.py <base>           # charts/ + infographics
  python decision_engine_svg.py <base> --anim    # also anim/ animations
Static scenes + infographics -> <base>/charts/ ; animations -> <base>/anim/
"""
import os, sys

# ---- house style (shared with candle_svg.py / breakout_svg.py) --------------
BG="#131722"; GRID="#1b2230"; TEXT="#d1d4dc"; SUB="#787b86"
BULL="#089981"; BEAR="#f23645"; WICK="#b2b5be"
PRE="#5d606b"; GOLD="#f0b90b"; BLUE="#2962ff"; PURP="#9c27b0"; TEAL="#26c6da"
ZONE_G="rgba(8,153,129,0.13)"; ZONE_R="rgba(242,54,69,0.13)"; ZONE_Y="rgba(240,185,15,0.12)"
ZONE_B="rgba(41,98,255,0.12)"
W=860; H=460; PADL=26; PADR=26; PADT=58; PADB=58

def esc(t):
    """XML-escape dynamic text (& < >); leave unicode arrows/≥ intact."""
    return str(t).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

# =============================================================================
#  CORE: candle-series scene renderer  (copied verbatim from breakout_svg.py)
# =============================================================================
def _layout(scene):
    candles=scene["candles"]; n=len(candles)
    prof = scene.get("profile")
    delta = scene.get("delta")
    has_bracket = bool(scene.get("sl_tp"))
    right = PADR + (130 if prof else 0) + (160 if has_bracket else 0)
    plot_w = W-PADL-right
    plot_top = PADT
    plot_bot = H-PADB-(86 if delta else 0)
    plot_h = plot_bot-plot_top
    # price extent
    lows=[c[2] for c in candles]; highs=[c[1] for c in candles]
    extra=list(scene.get("yextra",[]))
    for lv in scene.get("levels",[]): extra.append(lv["y"])
    for z in scene.get("zones",[]): extra+=[z["y0"],z["y1"]]
    if scene.get("sl_tp"):
        st=scene["sl_tp"]; extra+=[st["entry"],st["sl"]]+[t[0] for t in st["tps"]]
    if prof: extra+=[prof.get("vah",0),prof.get("val",0),prof.get("poc",0)]
    lo=min(lows+extra); hi=max(highs+extra); rng=(hi-lo) or 1
    lo-=rng*0.10; hi+=rng*0.10
    slot=plot_w/(n+1)
    bw=min(slot*0.58, 26)
    def cx(i): return PADL+slot*(i+0.7)
    def y(p): return plot_top+(hi-p)/(hi-lo)*plot_h
    return dict(n=n,slot=slot,bw=bw,cx=cx,y=y,lo=lo,hi=hi,
                plot_top=plot_top,plot_bot=plot_bot,plot_w=plot_w,
                x_left=PADL,x_right=PADL+plot_w,prof=prof,delta=delta)

def _frame(scene,L):
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Segoe UI,Arial,sans-serif">']
    s.append(f'<rect width="{W}" height="{H}" rx="12" fill="{BG}"/>')
    for gy in range(int(L["plot_top"]), int(L["plot_bot"]), 40):
        s.append(f'<line x1="{PADL}" y1="{gy}" x2="{L["x_right"]:.0f}" y2="{gy}" stroke="{GRID}" stroke-width="1"/>')
    s.append(f'<text x="{PADL}" y="28" fill="{TEXT}" font-size="19" font-weight="700">{esc(scene["name"])}</text>')
    if scene.get("subtitle"):
        s.append(f'<text x="{PADL}" y="47" fill="{SUB}" font-size="12.5">{esc(scene["subtitle"])}</text>')
    return s

def _candles(scene,L,anim=False):
    s=[]; cx=L["cx"]; y=L["y"]; bw=L["bw"]
    for i,(o,h,l,c) in enumerate(scene["candles"]):
        up=c>=o; col=BULL if up else BEAR; x=cx(i)
        beg=f'begin="{0.18*i:.2f}s" dur="0.30s" fill="freeze"' if anim else ""
        an_open=f'opacity="{0 if anim else 1}"'
        wick=f'<line x1="{x:.1f}" y1="{y(h):.1f}" x2="{x:.1f}" y2="{y(l):.1f}" stroke="{WICK}" stroke-width="1.5" {an_open}>'
        wick+= (f'<animate attributeName="opacity" from="0" to="1" {beg}/>' if anim else "") + '</line>'
        s.append(wick)
        top=y(max(o,c)); bot=y(min(o,c)); bh=max(bot-top,2)
        rect=(f'<rect x="{x-bw/2:.1f}" y="{top:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="1.5" '
              f'fill="{col}" stroke="{col}" {an_open}>')
        rect+= (f'<animate attributeName="opacity" from="0" to="1" {beg}/>' if anim else "") + '</rect>'
        s.append(rect)
    return s

def _overlays(scene,L,anim=False):
    s=[]; cx=L["cx"]; y=L["y"]; n=L["n"]; bw=L["bw"]
    odelay = 0.18*n+0.2 if anim else 0
    for z in scene.get("zones",[]):
        x0=cx(z["x0"])-bw if z["x0"]>=0 else PADL
        x1=cx(z["x1"])+bw if z["x1"]<n else L["x_right"]
        ya=y(max(z["y0"],z["y1"])); yb=y(min(z["y0"],z["y1"]))
        op=f'<animate attributeName="opacity" from="0" to="1" begin="{odelay:.2f}s" dur="0.4s" fill="freeze"/>' if anim else ""
        s.append(f'<rect x="{x0:.1f}" y="{ya:.1f}" width="{x1-x0:.1f}" height="{yb-ya:.1f}" '
                 f'fill="{z.get("fill",ZONE_Y)}" stroke="{z.get("stroke",GOLD)}" stroke-width="1.1" '
                 f'stroke-dasharray="{z.get("dash","")}" opacity="{0 if anim else 1}" rx="2">{op}</rect>')
        if z.get("label"):
            s.append(f'<text x="{x0+5:.1f}" y="{ya+14:.1f}" fill="{z.get("stroke",GOLD)}" '
                     f'font-size="11" font-weight="600" opacity="{0 if anim else 1}">{esc(z["label"])}'
                     +(f'<animate attributeName="opacity" from="0" to="1" begin="{odelay:.2f}s" dur="0.4s" fill="freeze"/>' if anim else "")+'</text>')
    for cv in scene.get("curves",[]):
        pts=cv["points"]
        d="M"+" L".join(f"{cx(px):.1f},{y(pp):.1f}" for px,pp in pts)
        op=f'<animate attributeName="opacity" from="0" to="1" begin="{odelay:.2f}s" dur="0.4s" fill="freeze"/>' if anim else ""
        s.append(f'<path d="{d}" stroke="{cv.get("color",PURP)}" stroke-width="{cv.get("w",2)}" fill="none" '
                 f'stroke-dasharray="{cv.get("dash","")}" opacity="{0 if anim else 1}">{op}</path>')
        if cv.get("label"):
            lx,lp=pts[-1]
            s.append(f'<text x="{cx(lx)+4:.1f}" y="{y(lp)-4:.1f}" fill="{cv.get("color",PURP)}" font-size="10.5" '
                     f'font-weight="600" opacity="{0 if anim else 1}">{esc(cv["label"])}'
                     +(f'<animate attributeName="opacity" from="0" to="1" begin="{odelay:.2f}s" dur="0.4s" fill="freeze"/>' if anim else "")+'</text>')
    for lv in scene.get("levels",[]):
        yp=y(lv["y"]); x0=PADL+L["plot_w"]*lv.get("x0_frac",0); x1=PADL+L["plot_w"]*lv.get("x1_frac",1)
        dash=lv.get("dash","6 4") if lv.get("dash",True) else ""
        op=f'<animate attributeName="opacity" from="0" to="1" begin="{odelay:.2f}s" dur="0.4s" fill="freeze"/>' if anim else ""
        s.append(f'<line x1="{x0:.1f}" y1="{yp:.1f}" x2="{x1:.1f}" y2="{yp:.1f}" stroke="{lv["color"]}" '
                 f'stroke-width="{lv.get("w",1.6)}" stroke-dasharray="{dash}" opacity="{0 if anim else 1}">{op}</line>')
        if lv.get("label"):
            anchor=lv.get("anchor","start")
            tx = x1-3 if anchor=="end" else x0+3
            s.append(f'<text x="{tx:.1f}" y="{yp-5:.1f}" fill="{lv["color"]}" font-size="11" '
                     f'font-weight="600" text-anchor="{anchor}" opacity="{0 if anim else 1}">{esc(lv["label"])}'
                     +(f'<animate attributeName="opacity" from="0" to="1" begin="{odelay:.2f}s" dur="0.4s" fill="freeze"/>' if anim else "")+'</text>')
    defs=set()
    for a in scene.get("arrows",[]):
        x0=cx(a["x0"]) if a["x0"]>=0 else PADL+4
        x1=cx(a["x1"]) if a["x1"]<n else L["x_right"]-4
        y0=y(a["y0"]); y1=y(a["y1"]); col=a.get("color",GOLD)
        head=a.get("head",True); mid=f'marker-end="url(#bar_{col[1:]})"' if head else ""
        if head: defs.add(col)
        op=f'<animate attributeName="opacity" from="0" to="1" begin="{odelay+a.get("t",0):.2f}s" dur="0.4s" fill="freeze"/>' if anim else ""
        s.append(f'<path d="M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}" stroke="{col}" stroke-width="{a.get("w",2.6)}" '
                 f'fill="none" stroke-dasharray="{a.get("dash","")}" {mid} opacity="{0 if anim else 1}">{op}</path>')
        if a.get("label"):
            lx=(x0+x1)/2; ly=(y0+y1)/2+a.get("ldy",-6)
            s.append(f'<text x="{lx:.1f}" y="{ly:.1f}" fill="{col}" font-size="10.5" font-weight="600" '
                     f'text-anchor="middle" opacity="{0 if anim else 1}">{esc(a["label"])}'
                     +(f'<animate attributeName="opacity" from="0" to="1" begin="{odelay+a.get("t",0):.2f}s" dur="0.4s" fill="freeze"/>' if anim else "")+'</text>')
    if defs:
        s.append('<defs>')
        for col in defs:
            s.append(f'<marker id="bar_{col[1:]}" markerWidth="9" markerHeight="9" refX="6" refY="4.5" orient="auto">'
                     f'<path d="M0,0 L9,4.5 L0,9 z" fill="{col}"/></marker>')
        s.append('</defs>')
    for t in scene.get("annot",[]):
        x=cx(t["x"]) if isinstance(t["x"],int) else PADL+L["plot_w"]*t["x"]
        yp=y(t["y"]) if not t.get("yfrac") else L["plot_top"]+(L["plot_bot"]-L["plot_top"])*t["y"]
        op=f'<animate attributeName="opacity" from="0" to="1" begin="{odelay:.2f}s" dur="0.4s" fill="freeze"/>' if anim else ""
        s.append(f'<text x="{x:.1f}" y="{yp:.1f}" fill="{t.get("color",TEXT)}" font-size="{t.get("fs",11)}" '
                 f'font-weight="{t.get("fw",500)}" text-anchor="{t.get("anchor","middle")}" '
                 f'opacity="{0 if anim else 1}">{esc(t["text"])}'+(op if anim else "")+'</text>')
    return s

def _profile(scene,L):
    p=scene.get("profile")
    if not p: return []
    s=[]; y=L["y"]
    x0=L["x_right"]+14; maxw=110
    s.append(f'<text x="{x0}" y="{L["plot_top"]-8}" fill="{SUB}" font-size="10.5">Volume Profile</text>')
    for (pc, wfrac, kind) in p["bins"]:
        yp=y(pc); bw_=maxw*wfrac; h_=p.get("binh",13)
        col = {"hvn":"#3a4f6d","lvn":"#22303f","poc":GOLD}.get(kind,"#2b3a4d")
        s.append(f'<rect x="{x0:.1f}" y="{yp-h_/2:.1f}" width="{bw_:.1f}" height="{h_:.1f}" fill="{col}" rx="1.5"/>')
        if p.get("show_labels") and kind in ("hvn","lvn","poc"):
            tag={"hvn":"HVN","lvn":"LVN","poc":"POC"}[kind]
            s.append(f'<text x="{x0+bw_+4:.1f}" y="{yp+3:.1f}" fill="{SUB}" font-size="9">{tag}</text>')
    for key,col,lab in [("vah",TEAL,"VAH"),("val",TEAL,"VAL"),("poc",GOLD,"POC")]:
        if key in p:
            yp=y(p[key])
            s.append(f'<line x1="{PADL}" y1="{yp:.1f}" x2="{x0+maxw:.1f}" y2="{yp:.1f}" stroke="{col}" '
                     f'stroke-width="1.3" stroke-dasharray="2 3"/>')
            s.append(f'<text x="{x0+maxw:.1f}" y="{yp+3:.1f}" fill="{col}" font-size="10" text-anchor="end">{lab}</text>')
    return s

def _delta(scene,L):
    d=scene.get("delta")
    if not d: return []
    s=[]; cx=L["cx"]; n=L["n"]
    top=L["plot_bot"]+22; bot=H-PADB+4; mid=(top+bot)/2
    s.append(f'<text x="{PADL}" y="{top-4}" fill="{SUB}" font-size="10.5">Cumulative Delta (net aggressive buy−sell)</text>')
    s.append(f'<line x1="{PADL}" y1="{mid:.1f}" x2="{L["x_right"]:.0f}" y2="{mid:.1f}" stroke="{GRID}" stroke-width="1"/>')
    dmax=max(1,max(abs(v) for v in d)); amp=(bot-top)/2*0.85
    pts=[]
    for i,v in enumerate(d):
        pts.append((cx(i), mid - v/dmax*amp))
    for i in range(1,len(pts)):
        col=BULL if d[i]>=d[i-1] else BEAR
        s.append(f'<line x1="{pts[i-1][0]:.1f}" y1="{pts[i-1][1]:.1f}" x2="{pts[i][0]:.1f}" y2="{pts[i][1]:.1f}" '
                 f'stroke="{col}" stroke-width="2.2"/>')
    for i,(x,yy) in enumerate(pts):
        s.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="2.2" fill="{BULL if d[i]>=0 else BEAR}"/>')
    if scene.get("delta_note"):
        s.append(f'<text x="{L["x_right"]:.0f}" y="{top-4}" fill="{scene.get("delta_note_col",GOLD)}" '
                 f'font-size="10.5" font-weight="600" text-anchor="end">{esc(scene["delta_note"])}</text>')
    return s

def _bracket(scene,L):
    st=scene.get("sl_tp")
    if not st: return []
    s=[]; y=L["y"]
    x = L["x_right"] + (130 if scene.get("profile") else 0) + 20
    risk=abs(st["entry"]-st["sl"]) or 1
    def lab(price,text,col,bold=True):
        yp=y(price)
        s.append(f'<line x1="{x:.1f}" y1="{yp:.1f}" x2="{x+58:.1f}" y2="{yp:.1f}" stroke="{col}" stroke-width="2"/>')
        s.append(f'<text x="{x+62:.1f}" y="{yp+4:.1f}" fill="{col}" font-size="10.5" '
                 f'font-weight="{700 if bold else 500}">{esc(text)}</text>')
    lab(st["entry"],"Entry",BLUE)
    lab(st["sl"],"SL",BEAR)
    for price,name in st["tps"]:
        r=abs(price-st["entry"])/risk
        lab(price,f'{name} ({r:.1f}R)',BULL,bold=False)
    ye=y(st["entry"]); ys=y(st["sl"])
    s.append(f'<rect x="{x:.1f}" y="{min(ye,ys):.1f}" width="56" height="{abs(ys-ye):.1f}" fill="{ZONE_R}"/>')
    yt=y(st["tps"][0][0])
    s.append(f'<rect x="{x:.1f}" y="{min(ye,yt):.1f}" width="56" height="{abs(yt-ye):.1f}" fill="{ZONE_G}"/>')
    return s

def render_scene(scene, anim=False):
    L=_layout(scene)
    s=_frame(scene,L)
    s+=_profile(scene,L)
    s+=_overlays(scene,L,anim=False) if not anim else []
    s+=_candles(scene,L,anim=anim)
    if anim: s+=_overlays(scene,L,anim=True)
    s+=_delta(scene,L)
    s+=_bracket(scene,L)
    if scene.get("caption"):
        s.append(f'<text x="{W/2}" y="{H-14}" fill="{SUB}" font-size="12" text-anchor="middle">{esc(scene["caption"])}</text>')
    s.append("</svg>")
    return "\n".join(s)

# =============================================================================
#  SCENE CATALOG  (price on a normalised 0..100 scale; index = bar position)
# =============================================================================
def lvl(y,label,color=GOLD,dash=True,**k): return dict(y=y,label=label,color=color,dash=dash,**k)

SCENES=[]
def S(**kw): SCENES.append(kw); return kw

# ---- level-map : only the QUALIFIED levels (declutter teach scene) ----------
_lm=[(50,53,49,52),(52,55,51,54),(54,57,53,55),(55,57,52,53),
     (53,56,52,55),(55,58,54,56),(56,59,55,58),(58,61,57,60),
     (60,62,58,59),(59,61,57,58),(58,60,56,57),(57,60,56,59)]
_lm_bins=[(70,0.30,"lvn"),(66,0.45,"hvn"),(62,1.00,"poc"),(58,0.62,"hvn"),
          (54,0.40,"hvn"),(50,0.26,"lvn"),(46,0.22,"lvn")]
S(name="Level Map — only what matters", slug="level-map",
  subtitle="Mark 4–6 QUALIFIED levels: fresh OB + one FVG + swing H/L + PDH/PDL + a liquidity pool",
  candles=_lm,
  profile=dict(bins=_lm_bins,poc=62,vah=66,val=54,binh=14),
  levels=[lvl(68,"PDH",SUB,w=1.3),lvl(46,"PDL",SUB,w=1.3),
          lvl(62,"swing high = equal-highs liquidity",GOLD)],
  zones=[dict(x0=0,x1=5,y0=47,y1=49.3,fill=ZONE_G,stroke=BULL,label="fresh OB (demand)"),
         dict(x0=6,x1=7,y0=58,y1=61,fill=ZONE_B,stroke=BLUE,label="fresh FVG")],
  caption="Decluttered: only fresh, HTF-aligned, near-price levels. Everything else stays off the chart.")

# ---- ib-travel : Initial Balance + travel to a level -----------------------
_ib=[(50,53,46,52),(52,55,49,50),(50,55,48,54),(54,55,49,50),  # IB build 46-55 (first hour)
     (50,55,49,54),(54,56,50,51),                              # still inside IB
     (51,57,50,56),(56,59,55,58),(58,62,57,61),(61,64,60,63),  # travels up to the level
     (63,65,62,64)]
S(name="IB Travel — first hour, then travel to a level", slug="ib-travel",
  subtitle="The opening range (Initial Balance) is the launch pad; price travels to the next mapped level",
  candles=_ib,
  levels=[lvl(55,"IB high",GOLD),lvl(46,"IB low",TEAL),
          lvl(64,"target level (PDH / OI-wall)",BLUE,dash=True)],
  zones=[dict(x0=0,x1=5,y0=46,y1=55,fill=ZONE_Y,stroke=SUB,dash="4 3",label="Initial Balance (9:15–10:15)")],
  arrows=[dict(x0=6,y0=53,x1=9,y1=62,color=BULL,w=2.6,label="travels to the level")],
  caption="No trade INSIDE the IB; the edges define where price goes looking for liquidity.")

# ---- at-level-fork : 3 outcomes HOLD / BREAK / WAIT -------------------------
_alf=[(48,51,47,50),(50,53,49,52),(52,55,51,54),(54,57,53,56),
      (56,58,55,57),(57,59,56,58),(58,59,57,58)]  # arrives AT the level (~58)
S(name="At a Level — the 3-way fork", slug="at-level-fork",
  subtitle="Price arrives at a mapped level. Three outcomes — read which one, then act.",
  candles=_alf,
  yextra=[68,46],
  levels=[lvl(58,"the level",GOLD)],
  arrows=[dict(x0=6,y0=57.5,x1=6.6,y1=50,color=BEAR,w=2.6,label="HOLD → reject down",ldy=16,t=0.2),
          dict(x0=6,y0=58.5,x1=6.6,y1=65,color=BULL,w=2.6,label="BREAK → close through",ldy=-8,t=0.4),
          dict(x0=6,y0=58,x1=6.7,y1=58,color=SUB,w=2.2,label="WAIT → inside / unclear",ldy=-8,t=0.6,dash="5 4")],
  annot=[dict(x=0.5,y=0.12,yfrac=True,text="① HOLD = fade (reversal)   ② BREAK = go with it   ③ WAIT = no edge yet",
              color=TEXT,fs=11.5,fw=600)],
  caption="You do not predict the fork — you let price pick the branch, then take the matching play.")

# ---- hammer-sweep-branch : both directions ---------------------------------
_hsb=[(56,57,53,54),(54,55,51,52),(52,53,49,50),(50,52,48,49),  # falling into demand
      (49,51,44,50),  # sweep wick to 44 then hammer close back at 50
      (50,53,49,52),(52,55,51,54),(54,57,53,56)]  # reaction up
S(name="Sweep + Hammer at Demand — both branches", slug="hammer-sweep-branch",
  subtitle="A sweep wick + hammer at demand: it either reverses long OR fails into a breakdown",
  candles=_hsb,
  levels=[lvl(48,"demand / equal lows (liquidity)",TEAL)],
  zones=[dict(x0=3,x1=5,y0=44,y1=50,fill=ZONE_G,stroke=BULL,label="sweep + hammer (reclaim)")],
  arrows=[dict(x0=5,y0=51,x1=7,y1=56,color=BULL,w=2.6,label="continue up (reversal long)",ldy=-8,t=0.3),
          dict(x0=5,y0=49,x1=7,y1=43,color=BEAR,w=2.4,label="fail → breakdown / fakeout",ldy=14,t=0.5,dash="5 4")],
  annot=[dict(x=0.5,y=0.93,yfrac=True,text="reclaim & hold = long; close back below the wick = the hammer failed",
              color=SUB,fs=10.5)],
  caption="A hammer is only a signal once it RECLAIMS; a hammer that breaks lower is a trap.")

# ---- wait-vs-retest : first-touch vs retest --------------------------------
_wvr=[(50,52,49,51),(51,53,50,52),(52,54,51,53),  # approach
      (53,61,52,60),  # break candle through 55
      (60,62,58,59),  # push
      (59,60,54,55),  # pullback / retest into broken level 55
      (55,57,54,56),  # confirmation hold
      (56,61,55,60),(60,65,59,64)]  # continuation
S(name="First-Touch vs Retest Entry", slug="wait-vs-retest",
  subtitle="Chase the break (first-touch, wide stop) — or wait for the retest (tight stop)",
  candles=_wvr,
  levels=[lvl(55,"broken level → now support",GOLD)],
  zones=[dict(x0=5,x1=6,y0=54,y1=57,fill=ZONE_G,stroke=BULL,label="retest zone")],
  arrows=[dict(x0=3,y0=57,x1=3,y1=60,color=SUB,w=2.2,label="first-touch (wide stop)",ldy=-8),
          dict(x0=6,y0=55,x1=7,y1=61,color=BULL,w=2.6,label="retest entry (tight stop)",ldy=-8)],
  sl_tp=dict(entry=56,sl=53,tps=[(61,"TP1"),(64,"TP2")]),
  caption="The retest stop is tighter (under the reclaimed level), so the same target is a better R.")

# ---- grinding-up-case : the worked scenario --------------------------------
_guc=[(64,66,62,63),(63,64,60,61),(61,62,57,58),(58,59,54,55),  # high then fall
      (55,56,51,52),(52,53,48,49),  # fall into demand
      (49,51,45,50),  # sweep + bullish reaction at demand 47
      (50,52,49,51),(51,53,50,52),(52,54,51,53),  # slow grind up
      (53,55,52,54),(54,56,53,55),(55,58,54,57),  # grind to resistance ~58
      (57,59,56,58)]  # about to break
S(name="Worked Case — fall, sweep, grind to resistance", slug="grinding-up-case",
  subtitle="High → fall to demand → sweep + reaction → slow grind to resistance → about to break",
  candles=_guc,
  levels=[lvl(58,"resistance (target / break level)",GOLD),lvl(47,"demand zone",TEAL)],
  zones=[dict(x0=5,x1=6,y0=45,y1=49,fill=ZONE_G,stroke=BULL,label="demand: sweep + reaction")],
  arrows=[dict(x0=6,y0=50,x1=12,y1=57,color=BULL,w=2.2,head=False,dash="5 4",label="slow grind up"),
          dict(x0=6,y0=47,x1=7,y1=53,color=TEAL,w=2.4,label="① reversal-at-demand",ldy=14,t=0.3),
          dict(x0=12,y0=56,x1=13,y1=61,color=GOLD,w=2.6,label="② wait-for-breakout",ldy=-8,t=0.5)],
  caption="Two valid plays: aggressive reversal at demand, or patient breakout at resistance.")

# ---- fvg-ltf-entry : LTF FVG entry + failure note --------------------------
_fle=[(50,52,49,51),(51,53,50,52),(52,54,51,53),
      (53,61,52,60),  # impulse leaves an FVG between 54 and 57
      (60,61,57,58),  # pulls back into FVG
      (58,60,55,56),  # entry candle reacts inside the FVG
      (56,60,55,59),(59,64,58,63),(63,67,62,66)]
S(name="LTF FVG Entry — and when to skip it", slug="fvg-ltf-entry",
  subtitle="Enter on a reaction INSIDE a fresh FVG; skip it if the gap fully fills with no reaction",
  candles=_fle,
  levels=[lvl(55,"FVG support edge",BLUE,dash=True)],
  zones=[dict(x0=2,x1=4,y0=54,y1=57,fill=ZONE_B,stroke=BLUE,label="LTF FVG (imbalance)")],
  arrows=[dict(x0=5,y0=56,x1=6,y1=62,color=BULL,w=2.6,label="valid entry (reaction)")],
  annot=[dict(x=0.30,y=0.16,yfrac=True,text="SKIP: FVG fully filled / no reaction = no imbalance edge left",
              color=BEAR,fs=10.5)],
  sl_tp=dict(entry=57,sl=54,tps=[(63,"TP1"),(66,"TP2")]),
  caption="A fresh FVG is a magnet+springboard; a fully-mitigated FVG is just air — stand aside.")

# ---- footprint-read : absorption + imbalance via delta ---------------------
_fpr=[(50,53,49,52),(52,55,51,54),(54,57,53,56),(56,59,55,58),(58,60,57,59),(59,60,57,58)]
S(name="Footprint Read — absorption & imbalance", slug="footprint-read",
  subtitle="Price keeps ticking up but delta stalls = sellers absorbing the aggressive buyers",
  candles=_fpr,
  levels=[lvl(60,"price still making highs",GOLD)],
  delta=[4,9,14,15,13,9],  # delta peaks then fades while price rises = absorption
  delta_note="delta STALLS while price rises = absorption", delta_note_col=BEAR,
  annot=[dict(x=0.5,y=0.10,yfrac=True,text="bid/ask imbalance: aggressive buys hitting a passive wall = no follow-through",
              color=SUB,fs=10.5)],
  caption="Effort (delta) without result (price acceptance) warns the up-move is being absorbed.")

# ---- targets-map : targets drawn as levels ---------------------------------
_tm=[(50,53,49,52),(52,55,51,54),(54,58,53,57),(57,62,56,61),  # break + run
     (61,64,60,63),(63,66,62,65),(65,68,64,67),(67,70,66,69)]
_tm_bins=[(78,0.30,"lvn"),(74,0.55,"hvn"),(70,1.00,"poc"),(66,0.45,"hvn"),
          (62,0.35,"lvn"),(58,0.50,"hvn"),(54,0.30,"lvn")]
S(name="Targets Map — where to take profit", slug="targets-map",
  subtitle="Targets = next HVN · an OI-wall · a naked POC · a measured move",
  candles=_tm,
  profile=dict(bins=_tm_bins,poc=70,vah=74,val=58,binh=13,show_labels=True),
  levels=[lvl(66,"T1: next HVN",TEAL,dash=True),
          lvl(70,"T2: naked POC",GOLD,dash=True),
          lvl(74,"T3: OI-wall",BLUE,dash=True),
          lvl(78,"T4: measured move",PURP,dash=True)],
  arrows=[dict(x0=3,y0=58,x1=5,y1=64,color=BULL,w=2.6,label="run into targets")],
  caption="Stack exits at the next magnets; trail the last runner toward the measured move.")

def main_scenes(out):
    n=0
    for sc in SCENES:
        open(os.path.join(out,sc["slug"]+".svg"),"w",encoding="utf-8").write(render_scene(sc))
        n+=1
    return n

ANIM_SLUGS={"at-level-fork","hammer-sweep-branch","wait-vs-retest",
            "grinding-up-case","fvg-ltf-entry","ib-travel"}
def anim_scenes(out):
    n=0
    for sc in SCENES:
        if sc["slug"] in ANIM_SLUGS:
            open(os.path.join(out,sc["slug"]+".anim.svg"),"w",encoding="utf-8").write(render_scene(sc,anim=True))
            n+=1
    return n

# =============================================================================
#  SPECIAL RENDERERS (non-candle infographics)
# =============================================================================
def _svg_open(title,subtitle="",h=H):
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" font-family="Segoe UI,Arial,sans-serif">']
    s.append(f'<rect width="{W}" height="{h}" rx="12" fill="{BG}"/>')
    s.append(f'<text x="{PADL}" y="30" fill="{TEXT}" font-size="19" font-weight="700">{esc(title)}</text>')
    if subtitle: s.append(f'<text x="{PADL}" y="49" fill="{SUB}" font-size="12.5">{esc(subtitle)}</text>')
    return s

def _wrap(s,x,y,text,fill,fs,maxch,lh=None,fw=None):
    """Greedy word-wrap. Appends <text> lines; returns the y AFTER the last line."""
    lh = lh or fs+3
    words=str(text).split(); line=""
    fwa=f' font-weight="{fw}"' if fw else ""
    for w_ in words:
        if line and len(line)+1+len(w_)>maxch:
            s.append(f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-size="{fs}"{fwa}>{esc(line)}</text>')
            line=w_; y+=lh
        else:
            line=(line+" "+w_).strip()
    if line:
        s.append(f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-size="{fs}"{fwa}>{esc(line)}</text>')
        y+=lh
    return y

def _box(s,x,y,w,h,stroke,fill="#161d2b",rx=8,sw=1.4):
    s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
             f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

def _arrowdef(s,name,col):
    s.append(f'<defs><marker id="{name}" markerWidth="9" markerHeight="9" refX="6" refY="4.5" '
             f'orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="{col}"/></marker></defs>')

# ---- master-flowchart : the hero -------------------------------------------
def render_master_flowchart():
    h=600
    s=_svg_open("The Intraday Decision Engine","Pre-open map → read open → at-level fork → pick play → LTF trigger → option + stop gate",h=h)
    cx=W/2; bw=560; bx=cx-bw/2
    steps=[("① PRE-OPEN: map the levels",BLUE,
            "Mark only 4–6 qualified levels — fresh OB/FVG, swing H/L, PDH/PDL, liquidity pools, OI walls."),
           ("② READ THE OPEN + REGIME",TEAL,
            "Gap-up / gap-down / flat · balance vs trend · GEX/PCR/max-pain · news gate. Sets fade-vs-break bias."),
           ("③ AT THE LEVEL — the fork",GOLD,
            "HOLD (reject → fade) · BREAK (close through → go) · WAIT (inside/unclear → no trade)."),
           ("④ PICK THE PLAY",PURP,
            "breakout · fakeout · reversal · pullback · continuation — chosen by the fork + regime."),
           ("⑤ LTF TRIGGER",BULL,
            "5m conviction close / sweep-&-go / retest of level·OB·FVG·VWAP with +delta. This is WHEN."),
           ("⑥ OPTION STRIKE + STOP-BUDGET GATE",GOLD,
            "Strike (ATM/1-OTM) · option-SL ≈ points×delta or ATR · per-instrument budget · R:R ≥ 2 · IV gate.")]
    y=72; bh=66; gap=20
    _arrowdef(s,"mfar",SUB)
    for i,(title,col,desc) in enumerate(steps):
        _box(s,bx,y,bw,bh,col)
        s.append(f'<text x="{bx+16:.1f}" y="{y+24:.1f}" fill="{col}" font-size="13.5" font-weight="700">{esc(title)}</text>')
        _wrap(s,bx+16,y+42,desc,SUB,10.5,84)
        if i<len(steps)-1:
            s.append(f'<path d="M{cx:.1f},{y+bh:.1f} L{cx:.1f},{y+bh+gap-2:.1f}" stroke="{SUB}" '
                     f'stroke-width="1.8" marker-end="url(#mfar)"/>')
        y+=bh+gap
    s.append(f'<text x="{cx:.1f}" y="{h-12}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'{esc("Top-down funnel: each gate must pass before you risk premium. Fail any gate → stand aside.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- five-plays-taxonomy ----------------------------------------------------
def render_five_plays():
    h=380
    s=_svg_open("The Five Plays","Every intraday trade is one of these — pick by the fork + the regime",h=h)
    cards=[("BREAKOUT",BULL,"Level BREAKS with a conviction close + volume → go with it."),
           ("FAKEOUT",BEAR,"Poke beyond, long wick, close back inside → fade the failed break."),
           ("REVERSAL",GOLD,"Sweep + reclaim at a level → turn against the prior move."),
           ("PULLBACK",BLUE,"After a break, retest the reclaimed level → tight-stop continuation."),
           ("CONTINUATION",TEAL,"Trend pauses (flag/IB), then resumes in the SAME direction.")]
    n=len(cards); cw=152; gap=14
    total=n*cw+(n-1)*gap; x0=(W-total)/2; y=84; ch=210
    for i,(t,col,desc) in enumerate(cards):
        x=x0+i*(cw+gap)
        _box(s,x,y,cw,ch,col)
        s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw:.1f}" height="34" rx="8" fill="{col}" opacity="0.20"/>')
        s.append(f'<text x="{x+cw/2:.1f}" y="{y+23:.1f}" fill="{col}" font-size="13.5" font-weight="700" text-anchor="middle">{esc(t)}</text>')
        s.append(f'<text x="{x+12:.1f}" y="{y+58:.1f}" fill="{TEXT}" font-size="10.5" font-weight="600">When it applies</text>')
        _wrap(s,x+12,y+76,desc,SUB,10.5,20)
    s.append(f'<text x="{W/2}" y="{h-14}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'{esc("Two go-with (breakout, continuation), three go-against / conditional (fakeout, reversal, pullback).")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- weighted-confluence ----------------------------------------------------
def render_weighted_confluence():
    h=440
    s=_svg_open("Weighted Confluence — weights shift with regime",
                "Structure vs Volume-Profile/Order-flow vs Options-flow — re-weighted by the regime",h=h)
    rows=[("Structure / levels",BLUE),("Volume Profile / order-flow",TEAL),("Options-flow (OI/GEX)",GOLD)]
    # two regimes, two stacked weight bars
    cols=[("Balance / positive-GEX",[0.30,0.30,0.40],"fade the edges; options pin dominates"),
          ("Trend / negative-GEX",[0.45,0.35,0.20],"trade the break; structure + flow lead")]
    bx=PADL+10; bw=W-2*PADL-20
    colw=(bw-40)/2
    legy=92
    for i,(name,col) in enumerate(rows):
        s.append(f'<rect x="{bx+i*150:.1f}" y="{legy-10:.1f}" width="12" height="12" rx="2" fill="{col}"/>')
        s.append(f'<text x="{bx+i*150+18:.1f}" y="{legy:.1f}" fill="{TEXT}" font-size="10.5">{esc(name)}</text>')
    palette=[BLUE,TEAL,GOLD]
    for ci,(cname,weights,note) in enumerate(cols):
        x=bx+ci*(colw+40); y=120; barh=240
        s.append(f'<text x="{x+colw/2:.1f}" y="{y-6:.1f}" fill="{TEXT}" font-size="12.5" font-weight="700" text-anchor="middle">{esc(cname)}</text>')
        _box(s,x,y,colw,barh,GRID,fill="#10141c",sw=1)
        yy=y
        for wi,wf in enumerate(weights):
            seg=barh*wf
            s.append(f'<rect x="{x:.1f}" y="{yy:.1f}" width="{colw:.1f}" height="{seg:.1f}" fill="{palette[wi]}" opacity="0.78"/>')
            s.append(f'<text x="{x+colw/2:.1f}" y="{yy+seg/2+4:.1f}" fill="#0c0f15" font-size="12" font-weight="700" text-anchor="middle">{int(wf*100)}%</text>')
            yy+=seg
        _wrap(s,x,y+barh+22,note,SUB,10.5,42)
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'{esc("Same inputs, different weights: in balance, options pin leads; in trend, structure + order-flow lead.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- level-grading ----------------------------------------------------------
def render_level_grading():
    h=470
    s=_svg_open("Level Grading — qualify or drop",
                "A level earns a place on the chart only if it passes the filter (cap: 3–6 levels)",h=h)
    keep=[("Fresh / untested","Not yet traded through — reaction still loaded."),
          ("HTF-aligned","Comes from 1h/15m bias, not invented on the LTF."),
          ("Near price","Reachable today; price can actually travel to it."),
          ("Resting liquidity","Equal highs/lows, OB/FVG, or an OI wall sits there.")]
    drop=[("Tested / mitigated","Already reacted — the fuel is gone."),
          ("Old / stale","From days ago, far from current value."),
          ("Too far","Out of today's expected range — irrelevant intraday.")]
    colw=(W-2*PADL-30)/2
    lx=PADL+10; rx=lx+colw+30; y=86
    s.append(f'<text x="{lx:.1f}" y="{y:.1f}" fill="{BULL}" font-size="14" font-weight="700">KEEP — qualifies</text>')
    s.append(f'<text x="{rx:.1f}" y="{y:.1f}" fill="{BEAR}" font-size="14" font-weight="700">DROP — declutter</text>')
    yk=y+16
    for t,d in keep:
        _box(s,lx,yk,colw,62,BULL);
        s.append(f'<text x="{lx+14:.1f}" y="{yk+24:.1f}" fill="{BULL}" font-size="12.5" font-weight="700">✓ {esc(t)}</text>')
        _wrap(s,lx+14,yk+44,d,SUB,10.5,52)
        yk+=74
    yd=y+16
    for t,d in drop:
        _box(s,rx,yd,colw,62,BEAR)
        s.append(f'<text x="{rx+14:.1f}" y="{yd+24:.1f}" fill="{BEAR}" font-size="12.5" font-weight="700">✗ {esc(t)}</text>')
        _wrap(s,rx+14,yd+44,d,SUB,10.5,52)
        yd+=74
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{GOLD}" font-size="11.5" font-weight="600" text-anchor="middle">'
             f'{esc("Hard cap ~3–6 levels. If a new one qualifies, drop the weakest — a clean chart is the edge.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- news-event-filter ------------------------------------------------------
def render_news_filter():
    h=460
    s=_svg_open("News / Event Filter — pre-market go/no-go",
                "Run the gate BEFORE the open; high-impact events change the rules of the day",h=h)
    rows=[("RBI policy / MPC",BEAR,"STAND ASIDE around the release; whipsaw risk is extreme."),
          ("Fed / FOMC, US CPI",BEAR,"STAND ASIDE near the print; gaps + violent reversals."),
          ("Results / earnings (stock)",GOLD,"WAIT for the first move to settle; avoid the gap candle."),
          ("Expiry day",GOLD,"TRADE smaller; pinning + theta crush distort levels late-day."),
          ("First 15 min (9:15–9:30)",GOLD,"WAIT — let the IB form; do not trade the auction noise."),
          ("Quiet / no events",BULL,"TRADE normally — the playbook applies in full.")]
    bx=PADL; bw=W-2*PADL; y=86; rh=50
    for name,col,desc in rows:
        _box(s,bx,y,bw,rh-8,GRID,fill="#1a2230",sw=1)
        s.append(f'<rect x="{bx:.1f}" y="{y:.1f}" width="6" height="{rh-8:.1f}" rx="3" fill="{col}"/>')
        s.append(f'<text x="{bx+18:.1f}" y="{y+26:.1f}" fill="{col}" font-size="12.5" font-weight="700">{esc(name)}</text>')
        s.append(f'<text x="{bx+250:.1f}" y="{y+26:.1f}" fill="{TEXT}" font-size="11.5">{esc(desc)}</text>')
        y+=rh
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'{esc("Three outcomes: TRADE · WAIT · STAND ASIDE. When in doubt on event risk, stand aside.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- open-types -------------------------------------------------------------
def render_open_types():
    h=400
    s=_svg_open("Open Types — how price travels to the level",
                "The open sets the first read: gap-up / gap-down / flat",h=h)
    panels=[("GAP-UP",BULL,[(0,30),(1,55),(2,52),(3,58),(4,54),(5,60)],
             "Opens above value. Expect a pullback to fill the gap or test PDH; fade exhaustion, buy held retests."),
            ("GAP-DOWN",BEAR,[(0,70),(1,45),(2,48),(3,42),(4,46),(5,40)],
             "Opens below value. Watch for a bounce to fill / test PDL; sell failed reclaims, buy sweeps of lows."),
            ("FLAT",TEAL,[(0,50),(1,52),(2,48),(3,51),(4,49),(5,50)],
             "Opens in value. Expect IB to build first; trade the edges of the opening range, not the middle.")]
    n=len(panels); pw=252; gap=18
    total=n*pw+(n-1)*gap; x0=(W-total)/2; py=82; ph=200
    for i,(t,col,pts,desc) in enumerate(panels):
        x=x0+i*(pw+gap)
        _box(s,x,py,pw,ph,col)
        s.append(f'<text x="{x+14:.1f}" y="{py+24:.1f}" fill="{col}" font-size="14" font-weight="700">{esc(t)}</text>')
        gx0=x+14; gw=pw-28; gy0=py+34; gh=66
        ys=[p[1] for p in pts]; lo=min(ys)-6; hi=max(ys)+6; rng=hi-lo
        def Y(v): return gy0+gh-(v-lo)/rng*gh
        def X(idx): return gx0+idx/(len(pts)-1)*gw
        d="M"+" L".join(f"{X(j):.1f},{Y(p[1]):.1f}" for j,p in enumerate(pts))
        s.append(f'<path d="{d}" stroke="{col}" stroke-width="2.4" fill="none"/>')
        s.append(f'<line x1="{gx0:.1f}" y1="{Y(50):.1f}" x2="{gx0+gw:.1f}" y2="{Y(50):.1f}" stroke="{SUB}" stroke-width="1" stroke-dasharray="4 3"/>')
        _wrap(s,x+14,py+118,desc,SUB,10,40)
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'{esc("The open tells you which levels are in play and whether to fade or follow first.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- regime-tree ------------------------------------------------------------
def render_regime_tree():
    h=470
    s=_svg_open("Regime Tree — fade or break?",
                "Read the regime first; it decides whether you fade levels or trade breaks",h=h)
    cx=W/2
    _box(s,cx-150,72,300,52,TEAL)
    s.append(f'<text x="{cx:.1f}" y="{96:.1f}" fill="{TEXT}" font-size="13" font-weight="700" text-anchor="middle">{esc("Read regime: GEX · PCR · max-pain · IV")}</text>')
    s.append(f'<text x="{cx:.1f}" y="{114:.1f}" fill="{SUB}" font-size="10.5" text-anchor="middle">{esc("structure: balance or trend?")}</text>')
    _arrowdef(s,"rtar",SUB)
    branches=[(cx-260,BULL,"BALANCE + positive-GEX","FADE levels → reversals",
               "Range holds, pin to max-pain. Buy support, sell resistance. Low IV-rank favours buying."),
              (cx,BEAR,"TREND + negative-GEX","Trade BREAKS",
               "Dealers chase price; breaks extend. Go with conviction closes. PCR + OI confirm direction."),
              (cx+260,GOLD,"MIXED / unclear","WAIT",
               "Conflicting signals (e.g. trend but positive-GEX). No edge — wait for alignment.")]
    by=170; bw=236; bh=150
    for x,col,head,verdict,desc in branches:
        bx=x-bw/2
        s.append(f'<path d="M{cx:.1f},124 L{x:.1f},{by-2:.1f}" stroke="{SUB}" stroke-width="1.6" marker-end="url(#rtar)"/>')
        _box(s,bx,by,bw,bh,col)
        s.append(f'<text x="{x:.1f}" y="{by+24:.1f}" fill="{col}" font-size="12" font-weight="700" text-anchor="middle">{esc(head)}</text>')
        s.append(f'<text x="{x:.1f}" y="{by+46:.1f}" fill="{TEXT}" font-size="13" font-weight="700" text-anchor="middle">{esc("→ "+verdict)}</text>')
        _wrap(s,bx+14,by+70,desc,SUB,10,30)
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'{esc("Positive-GEX = mean-reversion (fade). Negative-GEX = acceleration (break). Mixed = patience.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- ltf-lens ---------------------------------------------------------------
def render_ltf_lens():
    h=440
    s=_svg_open("LTF Lens — which read fits the moment",
                "On the LTF, choose the right lens: raw Price Action vs SMC vs Volume Profile",h=h)
    rows=[("Clean trend / momentum","Price Action",BULL,"Read candles, structure, BOS — keep it simple in a clear trend."),
          ("Sweeps & liquidity grabs","SMC",PURP,"OB/FVG, equal H/L, inducement — when stops are being hunted."),
          ("Range / acceptance / targets","Volume Profile",TEAL,"POC, HVN/LVN, value migration — for where price stalls or runs."),
          ("Absorption / who's winning","Order-flow / delta",GOLD,"CVD, footprint imbalance — to confirm effort vs result."),
          ("Choppy / no structure","STAND ASIDE",BEAR,"No lens fits cleanly = no trade; wait for a readable context.")]
    bx=PADL; bw=W-2*PADL; y=90; rh=58
    for situation,lens,col,desc in rows:
        _box(s,bx,y,bw,rh-8,GRID,fill="#1a2230",sw=1)
        s.append(f'<text x="{bx+16:.1f}" y="{y+22:.1f}" fill="{TEXT}" font-size="11.5" font-weight="600">{esc(situation)}</text>')
        s.append(f'<text x="{bx+16:.1f}" y="{y+40:.1f}" fill="{col}" font-size="12.5" font-weight="700">→ {esc(lens)}</text>')
        s.append(f'<text x="{bx+300:.1f}" y="{y+31:.1f}" fill="{SUB}" font-size="10.5">{esc(desc)}</text>')
        y+=rh
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'{esc("Match the lens to the situation — forcing one framework on every chart creates noise.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- option-sl-delta --------------------------------------------------------
def render_option_sl_delta():
    h=420
    s=_svg_open("Option SL via Delta",
                "Option-premium stop ≈ futures stop (points) × option delta",h=h)
    # formula box
    fx=PADL+10; fy=80
    _box(s,fx,fy,W-2*PADL-20,56,GOLD,fill="#1d2330")
    s.append(f'<text x="{W/2:.1f}" y="{fy+35:.1f}" fill="{GOLD}" font-size="17" font-weight="700" text-anchor="middle">'
             f'{esc("premium SL (pts)  ≈  futures stop (pts)  ×  delta")}</text>')
    # worked example as 3 stacked rows
    steps=[("Futures stop","40 pt","Nifty structural stop below the reclaimed level + ATR buffer.",BLUE),
           ("Option delta","0.50","ATM Nifty call ≈ 0.5 delta (verify on the live chain).",TEAL),
           ("Premium stop","40 × 0.5 ≈ 20 pt","If the option was bought at 120, exit ≈ 100.",BULL)]
    y=160; rh=66
    for name,val,desc,col in steps:
        _box(s,fx,y,W-2*PADL-20,rh-10,col,fill="#161d2b")
        s.append(f'<text x="{fx+16:.1f}" y="{y+24:.1f}" fill="{col}" font-size="12.5" font-weight="700">{esc(name)}</text>')
        s.append(f'<text x="{fx+16:.1f}" y="{y+44:.1f}" fill="{TEXT}" font-size="15" font-weight="700">{esc(val)}</text>')
        s.append(f'<text x="{fx+260:.1f}" y="{y+36:.1f}" fill="{SUB}" font-size="11">{esc(desc)}</text>')
        y+=rh
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{GOLD}" font-size="11.5" font-weight="600" text-anchor="middle">'
             f'{esc("Always VERIFY delta on the option chain — it drifts as price and time move.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- option-sl-atr ----------------------------------------------------------
def render_option_sl_atr():
    h=420
    s=_svg_open("Option / Futures SL via ATR",
                "Size the stop to volatility: stop (pts) = ATR × multiplier, then convert with delta",h=h)
    fx=PADL+10; fy=80
    _box(s,fx,fy,W-2*PADL-20,56,TEAL,fill="#1a2730")
    s.append(f'<text x="{W/2:.1f}" y="{fy+35:.1f}" fill="{TEAL}" font-size="17" font-weight="700" text-anchor="middle">'
             f'{esc("futures stop (pts)  =  ATR(14)  ×  multiplier (1.0–1.5)")}</text>')
    steps=[("ATR(14) on 5m","30 pt","Current Nifty 5m ATR — the market's normal swing.",BLUE),
           ("Multiplier","1.5×","Give the stop room beyond noise (use 1.0–1.5 intraday).",TEAL),
           ("Futures stop","30 × 1.5 ≈ 45 pt","Place SL 45 pt beyond invalidation.",GOLD),
           ("Premium stop","45 × 0.5 ≈ 22 pt","Convert with delta for the option-premium stop.",BULL)]
    y=160; rh=58
    for name,val,desc,col in steps:
        _box(s,fx,y,W-2*PADL-20,rh-10,col,fill="#161d2b")
        s.append(f'<text x="{fx+16:.1f}" y="{y+22:.1f}" fill="{col}" font-size="12" font-weight="700">{esc(name)}</text>')
        s.append(f'<text x="{fx+16:.1f}" y="{y+40:.1f}" fill="{TEXT}" font-size="14" font-weight="700">{esc(val)}</text>')
        s.append(f'<text x="{fx+260:.1f}" y="{y+31:.1f}" fill="{SUB}" font-size="11">{esc(desc)}</text>')
        y+=rh
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'{esc("ATR adapts the stop to the day's volatility — wider on volatile days, tighter on quiet ones.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- strike-selection -------------------------------------------------------
def render_strike_selection():
    h=420
    s=_svg_open("Strike Selection — ATM vs 1-OTM",
                "The trade-off: delta (responsiveness) vs premium (cost) vs theta (decay) vs breakeven",h=h)
    cols=["", "ATM", "1-OTM"]
    rows=[("Delta","~0.50","~0.35  (lower)"),
          ("Premium","Higher (₹ cost)","Lower (cheaper)"),
          ("Theta decay","Moderate","Faster (% of premium)"),
          ("Breakeven","Closer to spot","Further — needs a bigger move"),
          ("Best for","Reliable, level-to-level moves","Cheap directional punts / trends")]
    tx=PADL+10; tw=W-2*PADL-20; colw=tw/3
    y=86; hh=40
    # header
    s.append(f'<rect x="{tx:.1f}" y="{y:.1f}" width="{tw:.1f}" height="{hh:.1f}" rx="6" fill="#1d2330"/>')
    for ci,c in enumerate(cols):
        col=[TEXT,BLUE,GOLD][ci]
        s.append(f'<text x="{tx+ci*colw+colw/2:.1f}" y="{y+26:.1f}" fill="{col}" font-size="13.5" font-weight="700" text-anchor="middle">{esc(c)}</text>')
    y+=hh
    for ri,(label,a,b) in enumerate(rows):
        fill="#161d2b" if ri%2==0 else "#11161f"
        s.append(f'<rect x="{tx:.1f}" y="{y:.1f}" width="{tw:.1f}" height="{hh:.1f}" fill="{fill}"/>')
        s.append(f'<text x="{tx+14:.1f}" y="{y+26:.1f}" fill="{TEXT}" font-size="11.5" font-weight="600">{esc(label)}</text>')
        s.append(f'<text x="{tx+colw+colw/2:.1f}" y="{y+26:.1f}" fill="{TEXT}" font-size="11" text-anchor="middle">{esc(a)}</text>')
        s.append(f'<text x="{tx+2*colw+colw/2:.1f}" y="{y+26:.1f}" fill="{TEXT}" font-size="11" text-anchor="middle">{esc(b)}</text>')
        y+=hh
    s.append(f'<rect x="{tx:.1f}" y="86" width="{tw:.1f}" height="{y-86:.1f}" rx="6" fill="none" stroke="{GRID}" stroke-width="1.2"/>')
    for ci in (1,2):
        s.append(f'<line x1="{tx+ci*colw:.1f}" y1="86" x2="{tx+ci*colw:.1f}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'{esc("ATM = pay more for responsiveness; 1-OTM = cheaper but needs a bigger, faster move.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- stop-budget-table ------------------------------------------------------
def render_stop_budget_table():
    h=400
    s=_svg_open("Stop Budget by Instrument",
                "Typical point scale and a sensible per-trade stop budget per index (verify current values)",h=h)
    cols=["Instrument","Typical point scale","Stop budget (pts)","Note"]
    rows=[("Nifty","~22,000–25,000","30–50","baseline intraday stop"),
          ("BankNifty","~48,000–52,000","80–150","~2–3× Nifty (more volatile)"),
          ("FinNifty","~23,000–26,000","35–60","slightly above Nifty"),
          ("Sensex","~73,000–82,000","100–180","largest point scale")]
    tx=PADL+10; tw=W-2*PADL-20
    cw=[tw*0.20,tw*0.30,tw*0.22,tw*0.28]; y=90; hh=48
    s.append(f'<rect x="{tx:.1f}" y="{y:.1f}" width="{tw:.1f}" height="40" rx="6" fill="#1d2330"/>')
    xx=tx
    for ci,c in enumerate(cols):
        s.append(f'<text x="{xx+12:.1f}" y="{y+26:.1f}" fill="{TEAL}" font-size="12" font-weight="700">{esc(c)}</text>')
        xx+=cw[ci]
    y+=40
    palette=[TEXT,GOLD,BEAR,SUB]
    for ri,r in enumerate(rows):
        fill="#161d2b" if ri%2==0 else "#11161f"
        s.append(f'<rect x="{tx:.1f}" y="{y:.1f}" width="{tw:.1f}" height="{hh:.1f}" fill="{fill}"/>')
        xx=tx
        for ci,cell in enumerate(r):
            col=palette[ci]; fw="700" if ci==0 else "500"
            s.append(f'<text x="{xx+12:.1f}" y="{y+29:.1f}" fill="{col}" font-size="11.5" font-weight="{fw}">{esc(cell)}</text>')
            xx+=cw[ci]
        y+=hh
    s.append(f'<rect x="{tx:.1f}" y="90" width="{tw:.1f}" height="{y-90:.1f}" rx="6" fill="none" stroke="{GRID}" stroke-width="1.2"/>')
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{GOLD}" font-size="11.5" font-weight="600" text-anchor="middle">'
             f'{esc("Point scales drift — VERIFY current index values & ATR before sizing. BankNifty needs ~2–3× the Nifty budget.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- theta-decay ------------------------------------------------------------
def render_theta_decay():
    h=420
    s=_svg_open("Intraday Theta Decay",
                "Weekly-option premium bleeds all day and ACCELERATES after ~2:30pm IST",h=h)
    gx0=PADL+50; gx1=W-PADL-30; gy0=90; gy1=h-90
    # axes
    s.append(f'<line x1="{gx0}" y1="{gy0}" x2="{gx0}" y2="{gy1}" stroke="{SUB}" stroke-width="1.2"/>')
    s.append(f'<line x1="{gx0}" y1="{gy1}" x2="{gx1}" y2="{gy1}" stroke="{SUB}" stroke-width="1.2"/>')
    s.append(f'<text x="{PADL+8}" y="{(gy0+gy1)/2}" fill="{SUB}" font-size="10.5" transform="rotate(-90 {PADL+8} {(gy0+gy1)/2})" text-anchor="middle">premium (time value)</text>')
    # x ticks (times)
    times=["9:15","11:00","12:30","2:00","2:30","3:00","3:30"]
    fr=[0.0,0.28,0.45,0.66,0.74,0.86,1.0]
    for t,f in zip(times,fr):
        x=gx0+(gx1-gx0)*f
        s.append(f'<line x1="{x:.1f}" y1="{gy1:.1f}" x2="{x:.1f}" y2="{gy1+5:.1f}" stroke="{SUB}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{gy1+20:.1f}" fill="{SUB}" font-size="9.5" text-anchor="middle">{esc(t)}</text>')
    # decay curve: slow then accelerating. value(f) decreasing convex
    def val(f): return 100*(1 - 0.30*f - 0.70*(f**2.6))
    pts=[]
    steps=40
    for i in range(steps+1):
        f=i/steps; v=val(f)
        x=gx0+(gx1-gx0)*f; yv=gy1-(gy1-gy0)*(v/100.0)
        pts.append((x,yv))
    d="M"+" L".join(f"{x:.1f},{yv:.1f}" for x,yv in pts)
    s.append(f'<path d="{d}" stroke="{BEAR}" stroke-width="2.8" fill="none"/>')
    # accel marker at 2:30
    fx=gx0+(gx1-gx0)*0.74
    s.append(f'<line x1="{fx:.1f}" y1="{gy0:.1f}" x2="{fx:.1f}" y2="{gy1:.1f}" stroke="{GOLD}" stroke-width="1.4" stroke-dasharray="5 4"/>')
    s.append(f'<text x="{fx+6:.1f}" y="{gy0+16:.1f}" fill="{GOLD}" font-size="11" font-weight="600">~2:30pm: decay accelerates</text>')
    s.append(f'<text x="{gx0+60:.1f}" y="{gy0+40:.1f}" fill="{SUB}" font-size="10.5">slow bleed early →</text>')
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'{esc("Buying weeklies into the close fights theta — take profits / cut quicker in the last hour.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- iv-rank-gate -----------------------------------------------------------
def render_iv_rank_gate():
    h=420
    s=_svg_open("IV-Rank Gate — buy or spread?",
                "IV rank decides whether buying options is cheap or whether to prefer spreads",h=h)
    # gauge: a horizontal bar low->high
    bx=PADL+20; bw=W-2*PADL-40; by=110; bh=40
    s.append(f'<defs><linearGradient id="ivg" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0" stop-color="{BULL}"/><stop offset="0.5" stop-color="{GOLD}"/>'
             f'<stop offset="1" stop-color="{BEAR}"/></linearGradient></defs>')
    s.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="8" fill="url(#ivg)" opacity="0.85"/>')
    s.append(f'<text x="{bx:.1f}" y="{by-8:.1f}" fill="{SUB}" font-size="11">IV rank 0</text>')
    s.append(f'<text x="{bx+bw:.1f}" y="{by-8:.1f}" fill="{SUB}" font-size="11" text-anchor="end">IV rank 100</text>')
    cards=[("LOW IV (rank < 30)",BULL,by+bh+30,
            "Options are cheap → BUYING is OK. Long calls/puts, debit structures. Favourable for directional bets."),
           ("MID IV (30–60)",GOLD,by+bh+30,
            "Neutral → size normally; lean to spreads if a move is expected to be slow."),
           ("HIGH IV (rank > 60)",BEAR,by+bh+30,
            "Options are expensive → AVOID naked buying. Prefer SPREADS / credit to offset IV crush.")]
    n=len(cards); cw=(W-2*PADL-2*16)/3; x0=PADL; cy=by+bh+24; ch=150
    for i,(t,col,_,desc) in enumerate(cards):
        x=x0+i*(cw+16)
        _box(s,x,cy,cw,ch,col)
        s.append(f'<text x="{x+12:.1f}" y="{cy+24:.1f}" fill="{col}" font-size="12.5" font-weight="700">{esc(t)}</text>')
        _wrap(s,x+12,cy+46,desc,SUB,10.5,32)
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'{esc("High IV punishes option buyers via crush — when IV is rich, structure the trade as a spread.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- mid-trade-exit ---------------------------------------------------------
def render_mid_trade_exit():
    h=440
    s=_svg_open("Mid-Trade Exit — leave before the SL",
                "Exit when the THESIS breaks, not only when the stop is hit",h=h)
    rows=[("Delta flips","CVD turns against you / aggressive flow reverses — the order-flow thesis is gone.",BEAR),
          ("Level reclaims against you","The broken level is reclaimed back / your reclaim fails — structure invalidated.",BEAR),
          ("Time stop","Trade hasn't worked in N bars — dead trade ties up risk; release it.",GOLD),
          ("Theta bleed","Premium decaying with no follow-through — especially late-day weeklies.",GOLD),
          ("Confluence collapses","The reasons you entered (OB/FVG/regime) no longer hold.",PURP)]
    bx=PADL; bw=W-2*PADL; y=92; rh=60
    for name,desc,col in rows:
        _box(s,bx,y,bw,rh-10,GRID,fill="#1a2230",sw=1)
        s.append(f'<rect x="{bx:.1f}" y="{y:.1f}" width="6" height="{rh-10:.1f}" rx="3" fill="{col}"/>')
        s.append(f'<text x="{bx+18:.1f}" y="{y+24:.1f}" fill="{col}" font-size="12.5" font-weight="700">{esc(name)}</text>')
        _wrap(s,bx+18,y+42,desc,SUB,10.5,88)
        y+=rh
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{GOLD}" font-size="11.5" font-weight="600" text-anchor="middle">'
             f'{esc("The SL is the worst-case exit. The best exit is the moment the reason to be in vanishes.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- rr-sizing --------------------------------------------------------------
def render_rr_sizing():
    h=400
    s=_svg_open("R:R + Lot Sizing",
                "Risk a fixed fraction; let R:R and the per-lot risk decide the lots",h=h)
    fx=PADL+10
    _box(s,fx,80,W-2*PADL-20,50,BLUE,fill="#161d2b")
    s.append(f'<text x="{W/2:.1f}" y="{110:.1f}" fill="{BLUE}" font-size="15" font-weight="700" text-anchor="middle">'
             f'{esc("lots = (capital × risk%)  ÷  (premium-stop × lot size)")}</text>')
    steps=[("Capital / risk","₹1,00,000 × 1% = ₹1,000 risk","Never risk more than ~1% per trade.",TEAL),
           ("Premium stop","20 pt (from delta calc)","Per-unit risk on the option.",GOLD),
           ("Lot size","Nifty = 75","Risk per lot = 20 × 75 = ₹1,500.",PURP),
           ("Result","₹1,000 ÷ ₹1,500 ≈ 0 → take 1 lot only","Capital-constrained: 1 lot, or widen capital.",BULL)]
    y=148; rh=56
    for name,val,desc,col in steps:
        _box(s,fx,y,W-2*PADL-20,rh-10,col,fill="#11161f")
        s.append(f'<text x="{fx+16:.1f}" y="{y+22:.1f}" fill="{col}" font-size="12" font-weight="700">{esc(name)}</text>')
        s.append(f'<text x="{fx+16:.1f}" y="{y+40:.1f}" fill="{TEXT}" font-size="12.5" font-weight="600">{esc(val)}</text>')
        s.append(f'<text x="{fx+360:.1f}" y="{y+31:.1f}" fill="{SUB}" font-size="10.5">{esc(desc)}</text>')
        y+=rh
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'{esc("With small capital, lot indivisibility forces 1 lot — only A+ setups justify the fixed-lot risk.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- daily-loss-governor ----------------------------------------------------
def render_daily_loss_governor():
    h=420
    s=_svg_open("Daily Loss Governor",
                "Hard rules that stop you trading before a bad day becomes a blown account",h=h)
    rows=[("Max losses / day","2–3 losing trades → STOP for the day.",BEAR),
          ("Max ₹ loss / day","Down ~3% of capital → STOP, no exceptions.",BEAR),
          ("Max trades / day","Cap at ~3–5 quality setups; overtrading = revenge risk.",GOLD),
          ("Win lock-in","After a strong green day, bank it — don't give it back.",BULL),
          ("Capital-stress note","If sizing feels heavy or emotional, you're too big — cut size.",PURP)]
    bx=PADL; bw=W-2*PADL; y=92; rh=56
    for name,desc,col in rows:
        _box(s,bx,y,bw,rh-10,GRID,fill="#1a2230",sw=1)
        s.append(f'<rect x="{bx:.1f}" y="{y:.1f}" width="6" height="{rh-10:.1f}" rx="3" fill="{col}"/>')
        s.append(f'<text x="{bx+18:.1f}" y="{y+27:.1f}" fill="{col}" font-size="12.5" font-weight="700">{esc(name)}</text>')
        s.append(f'<text x="{bx+250:.1f}" y="{y+27:.1f}" fill="{TEXT}" font-size="11.5">{esc(desc)}</text>')
        y+=rh
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{GOLD}" font-size="11.5" font-weight="600" text-anchor="middle">'
             f'{esc("The governor is non-negotiable: survival first, profits second. Stop means stop.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- per-play-cards ---------------------------------------------------------
def render_per_play_cards():
    h=470
    s=_svg_open("Per-Play Cards",
                "Each play as a checklist: context gate · entry · SL · target · options note",h=h)
    plays=[("BREAKOUT",BULL,"trend / neg-GEX","conviction close beyond level","under reclaimed level + ATR","next HVN / measured move","ATM call/put; verify OI builds"),
           ("FAKEOUT",BEAR,"balance / pos-GEX","close back inside after the poke","beyond the failed wick","opposite edge / POC","fade with ATM; quick theta-aware exit"),
           ("REVERSAL",GOLD,"sweep + reclaim at level","reclaim candle holds","beyond the sweep wick","prior swing / value edge","ATM; size down, news-aware"),
           ("PULLBACK",BLUE,"post-break retest","reaction at reclaimed level/OB","under the level (tight)","prior high / next node","ATM/1-OTM; best R of the set"),
           ("CONTINUATION",TEAL,"trend pause (flag/IB)","break of the pause structure","under the flag/IB","measured move of leg","1-OTM ok in strong trend")]
    n=len(plays); cw=152; gap=14
    total=n*cw+(n-1)*gap; x0=(W-total)/2; y=80; ch=320
    labels=["Context","Entry","SL","Target","Options"]
    for i,(t,col,ctx,entry,sl,tgt,opt) in enumerate(plays):
        x=x0+i*(cw+gap)
        _box(s,x,y,cw,ch,col)
        s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw:.1f}" height="30" rx="8" fill="{col}" opacity="0.20"/>')
        s.append(f'<text x="{x+cw/2:.1f}" y="{y+20:.1f}" fill="{col}" font-size="12.5" font-weight="700" text-anchor="middle">{esc(t)}</text>')
        yy=y+46
        for lab,val in zip(labels,[ctx,entry,sl,tgt,opt]):
            s.append(f'<text x="{x+10:.1f}" y="{yy:.1f}" fill="{col}" font-size="9.5" font-weight="700">{esc(lab)}</text>')
            yy+=14
            yy=_wrap(s,x+10,yy,val,SUB,9.5,21,lh=12)
            yy+=6
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'{esc("Same skeleton, five contexts — drill them until the read-to-action is automatic.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- mtf-nesting : adapted from breakout_svg.render_mtf ---------------------
def render_mtf():
    h=566
    s=_svg_open("Multi-Timeframe Nesting","HTF decides DIRECTION · MTF decides WHERE · LTF decides WHEN",h=h)
    panels=[("1h — BIAS",BLUE,"Trend (BOS), PDH/PDL, prior-day value & naked POC, OI-wall band. → only trade in this direction.",
             [(30,40),(40,55),(55,52),(52,70),(70,66),(66,85)],"up"),
            ("30m — THE LEVEL",GOLD,"Initial Balance / range to break, the liquidity pool (equal highs/lows), the OI walls.",
             [(40,62),(62,60),(60,63),(63,61),(61,64),(64,63),(63,80)],"level"),
            ("5m — THE TRIGGER",BULL,"Conviction close beyond, stacked imbalances / +delta, sweep-and-go vs sweep-and-reverse, retest of level/OB/VWAP.",
             [(50,52),(52,55),(55,53),(53,49),(49,58),(58,57),(57,68),(68,66),(66,78)],"trigger")]
    px0=40; pw=440; py=78; ph=128
    for pi,(title,col,desc,pts,kind) in enumerate(panels):
        s.append(f'<rect x="{px0}" y="{py}" width="{pw}" height="{ph}" rx="8" fill="#161d2b" stroke="{col}" stroke-width="1.4"/>')
        s.append(f'<text x="{px0+14}" y="{py+24}" fill="{col}" font-size="14" font-weight="700">{esc(title)}</text>')
        gx0=px0+14; gw=pw-160; gy0=py+34; gh=ph-50
        ys=[p[1] for p in pts]; lo=min(ys)-4; hi=max(ys)+4; rng=hi-lo
        def Y(v): return gy0+gh-(v-lo)/rng*gh
        def X(i): return gx0+i/(len(pts)-1)*gw
        d="M"+" L".join(f"{X(i):.1f},{Y(p[1]):.1f}" for i,p in enumerate(pts))
        s.append(f'<path d="{d}" stroke="{col}" stroke-width="2.4" fill="none"/>')
        if kind in ("level","trigger"):
            lvy=Y(pts[1][1])
            s.append(f'<line x1="{gx0}" y1="{lvy:.1f}" x2="{gx0+gw}" y2="{lvy:.1f}" stroke="{GOLD}" stroke-width="1.2" stroke-dasharray="5 4"/>')
        tx=px0+pw-138; words=desc.split(); line=""; ty=py+22
        for w_ in words:
            if len(line)+len(w_)>22: s.append(f'<text x="{tx}" y="{ty}" fill="{SUB}" font-size="9.5">{esc(line)}</text>'); line=w_; ty+=13
            else: line=(line+" "+w_).strip()
        s.append(f'<text x="{tx}" y="{ty}" fill="{SUB}" font-size="9.5">{esc(line)}</text>')
        if pi<len(panels)-1:
            s.append(f'<path d="M{px0+pw/2},{py+ph} L{px0+pw/2},{py+ph+18}" stroke="{SUB}" stroke-width="1.6" marker-end="url(#mtfar)"/>')
        py+=ph+22
    s.append(f'<defs><marker id="mtfar" markerWidth="9" markerHeight="9" refX="6" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="{SUB}"/></marker></defs>')
    fx=px0+pw+30
    s.append(f'<text x="{fx}" y="{96}" fill="{TEXT}" font-size="13" font-weight="700">The funnel</text>')
    funnel=[("Align?",BLUE,"5m trigger must agree with 1h bias — else it is a counter-trend fade, not a trade."),
            ("Priority",GOLD,"HTF FVG/OB outranks LTF. The level is set on 1h/30m; the 5m never invents one."),
            ("Confirm",BULL,"Options layer (OI/IV/GEX) sets the environment; the 5m candle pulls the trigger.")]
    fy=116
    for t,c,desc in funnel:
        s.append(f'<text x="{fx}" y="{fy}" fill="{c}" font-size="12" font-weight="700">{esc(t)}</text>')
        words=desc.split(); line=""; ty=fy+16
        for w_ in words:
            if len(line)+len(w_)>30: s.append(f'<text x="{fx}" y="{ty}" fill="{SUB}" font-size="10">{esc(line)}</text>'); line=w_; ty+=13
            else: line=(line+" "+w_).strip()
        s.append(f'<text x="{fx}" y="{ty}" fill="{SUB}" font-size="10">{esc(line)}</text>')
        fy=ty+22
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'{esc("One timeframe lies; three timeframes agreeing is conviction.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- backtest-grid ----------------------------------------------------------
def render_backtest_grid():
    h=470
    s=_svg_open("Backtest Parameter Grid",
                "Sweep these parameters; judge with these metrics — find the robust region, not the peak",h=h)
    params=[("Stop budget (pts)",["30","40","50","60"],BLUE),
            ("R:R target",["1.5","2","3"],TEAL),
            ("Confirmation",["first-touch","retest"],GOLD),
            ("Regime filter",["on","off"],PURP),
            ("Strike",["ATM","1-OTM"],BULL)]
    bx=PADL+10; y=88; rowh=58; labw=170
    for name,vals,col in params:
        s.append(f'<text x="{bx:.1f}" y="{y+24:.1f}" fill="{col}" font-size="12" font-weight="700">{esc(name)}</text>')
        cx0=bx+labw; cw=64; gap=10
        for j,v in enumerate(vals):
            x=cx0+j*(cw+gap)
            _box(s,x,y,cw,34,col,fill="#161d2b")
            s.append(f'<text x="{x+cw/2:.1f}" y="{y+22:.1f}" fill="{TEXT}" font-size="11" text-anchor="middle">{esc(v)}</text>')
        y+=rowh
    # metrics box
    my=y+4
    _box(s,bx,my,W-2*PADL-20,60,GOLD,fill="#1d2330")
    s.append(f'<text x="{bx+14:.1f}" y="{my+24:.1f}" fill="{GOLD}" font-size="12.5" font-weight="700">Judge with</text>')
    metrics="Win-rate · Expectancy (R/trade) · MAE / MFE · Probability-of-Profit (PoP) · max drawdown"
    _wrap(s,bx+14,my+44,metrics,TEXT,11.5,84)
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'{esc("Prefer a broad plateau of good results over a single fragile peak — that is what survives live.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

SPECIALS={
    "master-flowchart":render_master_flowchart,
    "five-plays-taxonomy":render_five_plays,
    "weighted-confluence":render_weighted_confluence,
    "level-grading":render_level_grading,
    "news-event-filter":render_news_filter,
    "open-types":render_open_types,
    "regime-tree":render_regime_tree,
    "ltf-lens":render_ltf_lens,
    "option-sl-delta":render_option_sl_delta,
    "option-sl-atr":render_option_sl_atr,
    "strike-selection":render_strike_selection,
    "stop-budget-table":render_stop_budget_table,
    "theta-decay":render_theta_decay,
    "iv-rank-gate":render_iv_rank_gate,
    "mid-trade-exit":render_mid_trade_exit,
    "rr-sizing":render_rr_sizing,
    "daily-loss-governor":render_daily_loss_governor,
    "per-play-cards":render_per_play_cards,
    "mtf-nesting":render_mtf,
    "backtest-grid":render_backtest_grid,
}

def main():
    base=sys.argv[1]; do_anim="--anim" in sys.argv
    charts=os.path.join(base,"charts"); anim=os.path.join(base,"anim")
    os.makedirs(charts,exist_ok=True); os.makedirs(anim,exist_ok=True)
    n=main_scenes(charts)
    for slug,fn in SPECIALS.items():
        open(os.path.join(charts,slug+".svg"),"w",encoding="utf-8").write(fn())
    na=anim_scenes(anim) if do_anim else 0
    print(f"rendered {n} candle scenes + {len(SPECIALS)} infographics -> {charts}"
          + (f"  |  {na} anim -> {anim}" if do_anim else ""))

if __name__=="__main__":
    main()
