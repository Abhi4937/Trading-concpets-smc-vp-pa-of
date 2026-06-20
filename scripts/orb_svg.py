#!/usr/bin/env python3
"""Parametric OPENING-RANGE-BREAKOUT (ORB) SVG schematic + animation generator.

Deterministic, ~0 model tokens. Renders the ORB lifecycle, real-vs-trap, entry
models (break-close vs retest), sweep-and-go vs sweep-and-reverse, SL/target
geometry & measured move, VWAP/volume confluence, narrow-vs-wide IB, plus the
options/regime/honest-edge infographics. Reuses the render_scene engine +
infographic patterns from breakout_svg.py / decision_engine_svg.py (house style).

Usage:
  python orb_svg.py <base>           # charts/ + infographics
  python orb_svg.py <base> --anim    # also anim/ animations
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
#  CORE: candle-series scene renderer  (copied from decision_engine_svg.py)
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

# ---- 1. orb-lifecycle (HERO, animated) -------------------------------------
# 9:15-9:30 builds the opening range (OR) box; break above; shallow retest holds;
# run to target.
_orb_life=[(50,55,49,54),(54,56,48,49),(49,56,48,55),(55,57,50,51),  # OR forms 48-57 (first 15m)
           (51,56,50,55),(55,57,52,53),                              # coils inside OR
           (53,58,52,57),(57,64,56,63),                              # BREAK above OR-high 57 (close 63)
           (63,65,60,61),(61,64,57,62),                              # shallow retest of OR-high, holds
           (62,67,61,66),(66,71,65,70),(70,75,69,74)]                # run to target
S(name="ORB Lifecycle", slug="orb-lifecycle",
  subtitle="Opening range (9:15–9:30) → break above → shallow retest holds → run to target",
  candles=_orb_life,
  levels=[lvl(57,"OR high (break level)",GOLD,anchor="start"),
          lvl(48,"OR low",SUB,w=1.2,anchor="start")],
  zones=[dict(x0=0,x1=3,y0=48,y1=57,fill=ZONE_Y,stroke=SUB,dash="4 3",label="Opening Range (first 15m)"),
         dict(x0=8,x1=9,y0=57,y1=61,fill=ZONE_G,stroke=BULL,label="retest holds")],
  arrows=[dict(x0=7,y0=54,x1=7,y1=62,color=BULL,w=2.8,label="ORB break",ldy=14,t=0.4),
          dict(x0=11,y0=67,x1=11.6,y1=73,color=BULL,w=2.6,label="run",ldy=12,t=0.8)],
  annot=[dict(x=0.5,y=0.06,yfrac=True,text="① OR forms  ② break + close  ③ retest holds  ④ run to target",
              color=TEXT,fs=11.5,fw=600)],
  sl_tp=dict(entry=62,sl=56,tps=[(70,"T1"),(75,"T2")]),
  caption="The whole game: did the break ACCEPT beyond the OR (real) or get REJECTED back in (trap)?")

# ---- 2. orb-real-vs-trap (animated) ----------------------------------------
# real break: conviction close beyond OR, delta expands.  Shown with a trap
# annotation + a delta that would roll over on a trap.
_rvt=[(50,54,49,53),(53,55,48,49),(49,55,48,54),(54,56,50,51),  # OR 48-55
      (51,55,50,54),(54,56,52,53),                              # coils inside
      (53,57,52,56),(56,64,55,63),                              # REAL break: big body close >55
      (63,66,62,65),(65,68,64,67),(67,70,66,69)]                # value accepts, extends
S(name="ORB: Real Break vs Trap", slug="orb-real-vs-trap",
  subtitle="Real = conviction close + value accepts + delta EXPANDS · Trap = poke, long wick, close back in, delta ROLLS OVER",
  candles=_rvt,
  levels=[lvl(55,"OR high",GOLD,anchor="start")],
  zones=[dict(x0=0,x1=3,y0=48,y1=55,fill=ZONE_Y,stroke=SUB,dash="4 3",label="Opening Range")],
  arrows=[dict(x0=7,y0=53,x1=7,y1=62,color=BULL,w=2.8,label="REAL: conviction close",ldy=16,t=0.4),
          dict(x0=8.6,y0=67,x1=9.2,y1=69,color=BULL,w=2.4,label="value accepts → extends",ldy=-10,t=0.8)],
  annot=[dict(x=0.34,y=0.12,yfrac=True,
              text="TRAP would: poke above, long upper wick, close back INSIDE the OR, reverse",
              color=BEAR,fs=10.5)],
  delta=[2,5,4,3,5,4,9,16,21,26,30],
  delta_note="REAL: delta EXPANDS with price (trap: it ROLLS OVER)", delta_note_col=BULL,
  caption="On a trap, volume can spike but delta fades at the high = absorption → fade / stand aside.")

# ---- 3. entry-break-vs-retest ----------------------------------------------
_ebr=[(50,53,49,52),(52,54,48,49),(49,54,48,53),(53,55,50,51),  # OR 48-54
      (51,55,50,54),                                            # coil
      (54,62,53,61),                                            # break candle, close 61
      (61,63,59,60),(60,62,55,56),                              # pullback / retest to broken OR edge 54
      (56,58,54,57),                                            # confirmation hold at retest
      (57,62,56,61),(61,66,60,65)]                              # continuation
S(name="Entry: Break-Close vs Retest", slug="entry-break-vs-retest",
  subtitle="Break-close entry (at the close beyond OR) vs retest entry (pullback to the broken OR edge, tighter SL)",
  candles=_ebr,
  levels=[lvl(54,"OR high → broken (now support)",GOLD,anchor="start")],
  zones=[dict(x0=7,x1=8,y0=54,y1=57,fill=ZONE_G,stroke=BULL,label="retest zone")],
  arrows=[dict(x0=5,y0=57,x1=5,y1=61,color=SUB,w=2.2,label="① break-close entry (wider SL)",ldy=-8),
          dict(x0=8,y0=56,x1=9,y1=62,color=BULL,w=2.6,label="② retest entry (tighter SL)",ldy=-8)],
  sl_tp=dict(entry=57,sl=53,tps=[(62,"T1"),(65,"T2")]),
  caption="Same level, two entries: the retest stop sits under the reclaimed OR edge → better R for the same target.")

# ---- 4. sweep-and-go-vs-reverse (animated) ---------------------------------
_sgr=[(50,53,49,52),(52,54,48,49),(49,54,48,53),(53,55,50,51),  # OR 48-54
      (51,55,50,54),(54,56,52,53),                              # coil under OR-high
      (53,58,52,55),                                            # SWEEP of OR-high (wick 58) closes 55
      (55,60,54,59),(59,64,58,63),(63,68,62,67)]                # sweep-and-GO: continues up
S(name="OR-High Sweep: Go vs Reverse", slug="sweep-and-go-vs-reverse",
  subtitle="The fork — a sweep of the OR high either CONTINUES up (go) or closes back in and REVERSES down",
  candles=_sgr,
  levels=[lvl(54,"OR high (swept)",GOLD,anchor="start")],
  zones=[dict(x0=0,x1=3,y0=48,y1=54,fill=ZONE_Y,stroke=SUB,dash="4 3",label="Opening Range")],
  arrows=[dict(x0=6,y0=57,x1=6,y1=54,color=BEAR,w=2,label="sweep the OR high",ldy=-8,t=0.2),
          dict(x0=7.4,y0=58,x1=9,y1=66,color=BULL,w=2.6,label="GO: reclaims & continues",ldy=-8,t=0.5),
          dict(x0=7,y0=55,x1=8,y1=49,color=BEAR,w=2.2,label="REVERSE: closes back in → fade",ldy=14,t=0.6,dash="5 4")],
  annot=[dict(x=0.5,y=0.93,yfrac=True,
              text="reclaim & hold above OR-high = go long; close back inside the OR = the sweep failed → short",
              color=SUB,fs=10.5)],
  caption="A sweep is only a long once it RECLAIMS; a sweep that closes back inside the OR is the short signal.")

# ---- 5. sl-target-geometry -------------------------------------------------
_stg=[(50,53,49,52),(52,54,48,49),(49,54,48,53),(53,55,50,51),  # OR 48-54
      (51,55,50,54),(54,62,53,61),                              # break, close 61
      (61,63,59,60),(60,62,56,57),                              # retest to OR edge ~57
      (57,60,55,59),(59,65,58,64),(64,69,63,68),(68,73,67,72)]  # run to targets
S(name="ORB Stop & Target Geometry", slug="sl-target-geometry",
  subtitle="SL at opposite OR end (ATR / OR-midpoint alternatives); T1 = measured move (OR width); T2 = next level",
  candles=_stg,
  levels=[lvl(54,"OR high (break level)",GOLD,anchor="start"),
          lvl(48,"OR low → SL anchor (or ATR / OR-mid)",BEAR,dash=True,anchor="start"),
          lvl(60,"T1 = measured move",BULL,dash=True,anchor="start",x0_frac=0.0,x1_frac=0.42),
          lvl(72,"T2 = next level / PDH",TEAL,dash=True,anchor="start",x0_frac=0.0,x1_frac=0.42)],
  zones=[dict(x0=6,x1=7,y0=54,y1=57,fill=ZONE_G,stroke=BULL,label="retest entry")],
  annot=[dict(x=0.30,y=0.10,yfrac=True,text="measured move = OR width (54−48 = 6) projected up",
              color=SUB,fs=10.5,anchor="start")],
  sl_tp=dict(entry=54,sl=48,tps=[(60,"T1"),(72,"T2"),(78,"T3 trail")]),
  caption="Risk to the opposite OR end (where the idea is wrong); first target = the OR width itself.")

# ---- 6. measured-move-target -----------------------------------------------
_mmt=[(50,53,49,52),(52,54,48,49),(49,54,48,53),(53,55,50,51),  # OR 48-54 (width 6)
      (51,55,50,54),(54,61,53,60),                              # break from 54
      (60,63,59,62),(62,66,61,65),(65,68,64,67),(67,70,66,69)]  # runs into T1, then T2
S(name="ORB Measured-Move Target", slug="measured-move-target",
  subtitle="Project the OR width from the break point → T1; the next level (PDH) → T2",
  candles=_mmt,
  levels=[lvl(54,"OR high (break point)",GOLD,anchor="start"),
          lvl(48,"OR low",SUB,w=1.2,anchor="start"),
          lvl(60,"T1 = break + OR width (54 + 6)",BULL,dash=True,anchor="end"),
          lvl(69,"T2 = next level / PDH",TEAL,dash=True,anchor="end")],
  arrows=[dict(x0=1,y0=49,x1=1,y1=53,color=SUB,w=1.8,head=True,dash="4 3",label="OR width",ldy=2),
          dict(x0=5,y0=56,x1=6,y1=61,color=BULL,w=2.6,label="break")],
  annot=[dict(x=0.5,y=0.10,yfrac=True,text="T1 = break point + (OR high − OR low)",color=TEXT,fs=11,fw=600)],
  caption="The simplest, most robust ORB target: the range projects its own height onto the move.")

# ---- 7. retest-shrinks-stop ------------------------------------------------
_rss=[(50,53,49,52),(52,54,48,49),(49,54,48,53),(53,55,50,51),  # OR 48-54
      (51,55,50,54),(54,63,53,62),                              # break, close 62 (chase here)
      (62,64,60,61),(61,63,56,57),                              # pullback / retest to 54-57
      (57,59,55,58),(58,63,57,62),(62,67,61,66)]                # continuation
S(name="Retest Shrinks the Stop", slug="retest-shrinks-stop",
  subtitle="Chasing the break = wide SL (entry 62 → OR-low 48 ≈ 14 pt) vs retest entry = tight SL (57 → 54 ≈ 3 pt)",
  candles=_rss,
  levels=[lvl(54,"OR high → reclaimed",GOLD,anchor="start"),
          lvl(48,"OR low (chaser's SL)",BEAR,dash=True,anchor="start")],
  zones=[dict(x0=6,x1=7,y0=54,y1=57,fill=ZONE_G,stroke=BULL,label="retest entry")],
  arrows=[dict(x0=5,y0=58,x1=5,y1=62,color=SUB,w=2.2,label="chase entry ≈ 62",ldy=-8),
          dict(x0=5.5,y0=62,x1=5.5,y1=49,color=BEAR,w=1.6,head=True,dash="4 3",label="wide SL ≈ 14 pt",ldy=2),
          dict(x0=7,y0=57,x1=8,y1=62,color=BULL,w=2.6,label="retest entry ≈ 57",ldy=-8),
          dict(x0=7.5,y0=57,x1=7.5,y1=54,color=TEAL,w=1.6,head=True,dash="4 3",label="tight SL ≈ 3 pt",ldy=2)],
  caption="Same trade, same target — the retest cuts the stop ~4–5× → far better R and survivable size.")

# ---- 8. vwap-volume-confluence ---------------------------------------------
_vvc=[(50,54,46,53),(53,55,49,50),(50,56,48,55),(55,57,51,52),  # OR builds 46-57
      (52,56,50,55),(55,57,53,54),                              # coils inside
      (54,58,53,57),(57,64,56,63),                              # break ABOVE OR + above VWAP
      (63,66,61,62),(62,65,58,63),                              # shallow retest above VWAP
      (63,68,62,67),(67,72,66,71)]                              # trend leg
S(name="ORB + VWAP / Volume Confluence", slug="vwap-volume-confluence",
  subtitle="A-grade ORB breaks on the RIGHT side of VWAP with volume EXPANSION on the break candle",
  candles=_vvc,
  levels=[lvl(57,"OR high (break level)",GOLD,anchor="start"),
          lvl(46,"OR low",SUB,w=1.2,anchor="start")],
  curves=[dict(points=[(0,50),(2,51),(4,52),(6,53),(8,55),(10,58),(11,61)],color=PURP,label="VWAP",w=2.2)],
  zones=[dict(x0=0,x1=3,y0=46,y1=57,fill=ZONE_Y,stroke=SUB,dash="4 3",label="Opening Range"),
         dict(x0=8,x1=9,y0=57,y1=61,fill=ZONE_G,stroke=BULL,label="retest above VWAP")],
  arrows=[dict(x0=7,y0=55,x1=7,y1=63,color=BULL,w=2.8,label="break (right side of VWAP)")],
  delta=[2,4,3,5,4,3,8,17,15,18,24,30],
  delta_note="volume / delta EXPANDS on the break candle", delta_note_col=BULL,
  caption="Right side of VWAP + above-average volume on the break = the highest-quality ORB filter.")

# ---- 9. narrow-vs-wide-ib (two panels via annotation, single chart x2) -----
# Implemented as a dedicated narrow scene; the wide case is contrasted by annot.
_nib=[(50,52,49,51),(51,53,50,52),(52,53,50,51),(51,53,50,52),  # NARROW first hour 49-53
      (52,53,51,52),(52,54,51,53),                              # very tight
      (53,58,52,57),(57,62,56,61),(61,66,60,65),(65,70,64,69)]  # breaks & trends (breakout-prone)
S(name="Narrow vs Wide Initial Balance", slug="narrow-vs-wide-ib",
  subtitle="Narrow IB (tight first hour) = breakout-prone & trends · Wide IB (large first hour) = rotation / fade",
  candles=_nib,
  levels=[lvl(53,"narrow IB high",GOLD,anchor="start"),
          lvl(49,"narrow IB low",SUB,w=1.2,anchor="start")],
  zones=[dict(x0=0,x1=5,y0=49,y1=53,fill=ZONE_Y,stroke=BULL,dash="4 3",label="NARROW IB → energy stored")],
  arrows=[dict(x0=6,y0=55,x1=9,y1=68,color=BULL,w=2.6,label="narrow IB → break trends")],
  annot=[dict(x=0.5,y=0.10,yfrac=True,
              text="WIDE IB (large first hour): range already used the day's energy → expect rotation / fade the edges",
              color=BEAR,fs=10.5)],
  caption="Tight first-hour range stores energy for a clean break; a wide IB has already spent it → mean-revert.")

# =============================================================================
def main_scenes(out):
    n=0
    for sc in SCENES:
        open(os.path.join(out,sc["slug"]+".svg"),"w",encoding="utf-8").write(render_scene(sc))
        n+=1
    return n

ANIM_SLUGS={"orb-lifecycle","orb-real-vs-trap","entry-break-vs-retest",
            "sweep-and-go-vs-reverse","retest-shrinks-stop"}
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

def _miniprice(s,x,y,w,h,col,pts,level=None):
    """Tiny line sketch in a box region; pts as (i,val) on any scale."""
    ys=[p[1] for p in pts]; lo=min(ys)-6; hi=max(ys)+6; rng=(hi-lo) or 1
    def Y(v): return y+h-(v-lo)/rng*h
    def X(i): return x+i/(len(pts)-1)*w
    d="M"+" L".join(f"{X(i):.1f},{Y(p[1]):.1f}" for i,p in enumerate(pts))
    if level is not None:
        s.append(f'<line x1="{x:.1f}" y1="{Y(level):.1f}" x2="{x+w:.1f}" y2="{Y(level):.1f}" '
                 f'stroke="{GOLD}" stroke-width="1.1" stroke-dasharray="4 3"/>')
    s.append(f'<path d="{d}" stroke="{col}" stroke-width="2.4" fill="none"/>')

# ---- or-window-comparison --------------------------------------------------
def render_or_window():
    h=440
    s=_svg_open("Opening-Range Window — which timeframe?",
                "5 / 15 / 30 / 60-min OR windows — speed vs reliability tradeoff",h=h)
    cols=["Window","Signals","False breaks","Best for"]
    rows=[("5-min OR",GOLD,"fast, frequent","HIGH","scalpers; needs tight filters"),
          ("15-min OR",BULL,"balanced (default)","moderate","the standard intraday choice"),
          ("30-min OR",TEAL,"fewer, cleaner","low","positional intraday / swing-style"),
          ("60-min / 9:15–11:15",BLUE,"rare, high-quality","lowest","slow trend-day continuation")]
    tx=PADL+10; tw=W-2*PADL-20
    cw=[tw*0.24,tw*0.24,tw*0.18,tw*0.34]; y=86; hh=58
    s.append(f'<rect x="{tx:.1f}" y="{y:.1f}" width="{tw:.1f}" height="40" rx="6" fill="#1d2330"/>')
    xx=tx
    for ci,c in enumerate(cols):
        s.append(f'<text x="{xx+12:.1f}" y="{y+26:.1f}" fill="{TEAL}" font-size="12" font-weight="700">{esc(c)}</text>')
        xx+=cw[ci]
    y+=40
    for ri,(name,col,sig,fb,best) in enumerate(rows):
        fill="#161d2b" if ri%2==0 else "#11161f"
        s.append(f'<rect x="{tx:.1f}" y="{y:.1f}" width="{tw:.1f}" height="{hh:.1f}" fill="{fill}"/>')
        s.append(f'<rect x="{tx:.1f}" y="{y:.1f}" width="6" height="{hh:.1f}" rx="3" fill="{col}"/>')
        xx=tx
        cells=[name,sig,fb,best]
        for ci,cell in enumerate(cells):
            c=col if ci==0 else (BEAR if (ci==2 and fb=="HIGH") else TEXT)
            fw="700" if ci==0 else "500"
            s.append(f'<text x="{xx+(16 if ci==0 else 12):.1f}" y="{y+34:.1f}" fill="{c}" font-size="11.5" font-weight="{fw}">{esc(cell)}</text>')
            xx+=cw[ci]
        y+=hh
    s.append(f'<rect x="{tx:.1f}" y="126" width="{tw:.1f}" height="{y-126:.1f}" rx="6" fill="none" stroke="{GRID}" stroke-width="1.2"/>')
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{GOLD}" font-size="11.5" font-weight="600" text-anchor="middle">'
             f'{esc("Default to the 15-min OR; widen the window when you want fewer, cleaner signals.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- open-types ------------------------------------------------------------
def render_open_types():
    h=400
    s=_svg_open("Open Types — how the OR forms & resolves",
                "Gap-up / gap-down / flat: each shapes the opening range differently",h=h)
    panels=[("GAP-UP",BULL,[(0,30),(1,58),(2,54),(3,60),(4,56),(5,62)],55,
             "Opens above value. OR forms high; watch for gap-fill pullback then OR-high break, or fade exhaustion."),
            ("GAP-DOWN",BEAR,[(0,70),(1,42),(2,46),(3,40),(4,44),(5,38)],45,
             "Opens below value. OR forms low; sell failed OR-high reclaims, or buy a sweep of the OR low."),
            ("FLAT",TEAL,[(0,50),(1,52),(2,48),(3,53),(4,49),(5,55)],50,
             "Opens in value. OR is the cleanest read; trade the OR edges, not the middle. Best ORB setup.")]
    n=len(panels); pw=252; gap=18
    total=n*pw+(n-1)*gap; x0=(W-total)/2; py=82; ph=210
    for i,(t,col,pts,lvl_,desc) in enumerate(panels):
        x=x0+i*(pw+gap)
        _box(s,x,py,pw,ph,col)
        s.append(f'<text x="{x+14:.1f}" y="{py+24:.1f}" fill="{col}" font-size="14" font-weight="700">{esc(t)}</text>')
        _miniprice(s,x+14,py+34,pw-28,66,col,pts,level=lvl_)
        _wrap(s,x+14,py+124,desc,SUB,10,40)
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'{esc("The open type tells you whether to expect a gap-fill, a fade, or a clean OR-edge break.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- dalton-open-types -----------------------------------------------------
def render_dalton_open_types():
    h=420
    s=_svg_open("Dalton's Four Open Types",
                "How the auction opens tells you the day's conviction — and whether to trust the OR break",h=h)
    panels=[("OPEN-DRIVE",BULL,[(0,40),(1,48),(2,57),(3,66),(4,74),(5,82)],
             "Opens and drives one way with no look back. Highest conviction — trade the break, do not fade."),
            ("OPEN-TEST-DRIVE",TEAL,[(0,50),(1,42),(2,46),(3,55),(4,66),(5,76)],
             "Tests the opposite side first (a sweep), then drives. Enter on the reclaim after the test."),
            ("OPEN-REJECTION-REVERSE",GOLD,[(0,50),(1,62),(2,68),(3,55),(4,44),(5,36)],
             "Pushes one way, gets rejected, reverses hard. The classic ORB trap — fade the failed extreme."),
            ("OPEN-AUCTION",PURP,[(0,50),(1,56),(2,46),(3,54),(4,48),(5,52)],
             "Balances in a range, no conviction. Lowest-quality ORB — wait for a clean edge or stand aside.")]
    n=len(panels); cw=(W-2*PADL-3*14)/4; x0=PADL; py=80; ch=270
    for i,(t,col,pts,desc) in enumerate(panels):
        x=x0+i*(cw+14)
        _box(s,x,py,cw,ch,col)
        s.append(f'<text x="{x+cw/2:.1f}" y="{py+22:.1f}" fill="{col}" font-size="11.5" font-weight="700" text-anchor="middle">{esc(t)}</text>')
        _miniprice(s,x+12,py+34,cw-24,70,col,pts,level=50)
        _wrap(s,x+12,py+122,desc,SUB,9.5,24,lh=12)
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'{esc("Conviction ladder: drive > test-drive > rejection-reverse > auction. The opening type rates the break.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- oi-confluence ---------------------------------------------------------
def render_oi_confluence():
    h=400
    s=_svg_open("Options-OI Confluence with the ORB",
                "Read fresh OI vs OI re-defense vs distance from max-pain to confirm or fade the break",h=h)
    rows=[("Fresh OI in break direction",BULL,"CONFIRM",
           "Long buildup on an up-break (call OI builds at the next strike) = fresh money backs the move."),
          ("OI re-defense at the strike",BEAR,"FADE",
           "Writers add OI at the broken strike (re-defending it) = the break is being sold into → fade risk."),
          ("Break away from max-pain",BULL,"REAL",
           "Price pulling AWAY from max pain = real directional pressure, not a pin. Supports the break."),
          ("Break INTO a heavy-OI wall",GOLD,"CAUTION",
           "Breaking straight into a large opposing OI strike = expect a stall / rejection at the wall.")]
    bx=PADL; bw=W-2*PADL; y=88; rh=68
    for name,col,tag,desc in rows:
        _box(s,bx,y,bw,rh-10,GRID,fill="#1a2230",sw=1)
        s.append(f'<rect x="{bx:.1f}" y="{y:.1f}" width="6" height="{rh-10:.1f}" rx="3" fill="{col}"/>')
        s.append(f'<text x="{bx+18:.1f}" y="{y+24:.1f}" fill="{TEXT}" font-size="12.5" font-weight="700">{esc(name)}</text>')
        s.append(f'<text x="{bx+bw-14:.1f}" y="{y+24:.1f}" fill="{col}" font-size="12" font-weight="700" text-anchor="end">{esc(tag)}</text>')
        _wrap(s,bx+18,y+42,desc,SUB,10.5,84)
        y+=rh
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'{esc("The chart shows the break; the option chain tells you whether fresh money agrees with it.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- daytype-decision-tree -------------------------------------------------
def render_daytype_tree():
    h=470
    s=_svg_open("Day-Type Decision Tree — trade, fade, or stand aside",
                "The regime decides whether to trade the OR break, fade it, or skip the day",h=h)
    cx=W/2
    _box(s,cx-160,72,320,52,TEAL)
    s.append(f'<text x="{cx:.1f}" y="{96:.1f}" fill="{TEXT}" font-size="13" font-weight="700" text-anchor="middle">{esc("Read day-type / regime: trend vs balance · GEX")}</text>')
    s.append(f'<text x="{cx:.1f}" y="{114:.1f}" fill="{SUB}" font-size="10.5" text-anchor="middle">{esc("then apply the matching ORB action")}</text>')
    _arrowdef(s,"dtar",SUB)
    branches=[(cx-262,BULL,"TREND / negative-GEX","TRADE the break",
               "Dealers chase price; OR break extends. Go with the conviction close, target the measured move."),
              (cx,BEAR,"BALANCE / positive-GEX","FADE the break",
               "Range/pin day. OR breaks fail; fade the poke back into the range, target the opposite OR edge."),
              (cx+262,GOLD,"CHOP / no edge","STAND ASIDE",
               "Overlapping bars, no conviction, news risk. No clean OR break to trade — wait or skip.")]
    by=170; bw=240; bh=150
    for x,col,head,verdict,desc in branches:
        bx=x-bw/2
        s.append(f'<path d="M{cx:.1f},124 L{x:.1f},{by-2:.1f}" stroke="{SUB}" stroke-width="1.6" marker-end="url(#dtar)"/>')
        _box(s,bx,by,bw,bh,col)
        s.append(f'<text x="{x:.1f}" y="{by+24:.1f}" fill="{col}" font-size="12" font-weight="700" text-anchor="middle">{esc(head)}</text>')
        s.append(f'<text x="{x:.1f}" y="{by+46:.1f}" fill="{TEXT}" font-size="13" font-weight="700" text-anchor="middle">{esc("→ "+verdict)}</text>')
        _wrap(s,bx+14,by+70,desc,SUB,10,30)
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'{esc("Negative-GEX / trend = trade breaks. Positive-GEX / balance = fade them. Chop = no trade.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- honest-edge -----------------------------------------------------------
def render_honest_edge():
    h=460
    s=_svg_open("The Honest Edge — naive ORB option-buying is not a strategy",
                "Illustrative single-source backtest (Zerodha): naive ORB on Nifty options",h=h)
    # two stat cards: option BUYING vs option SELLING
    cards=[("Naive ORB — option BUYING",BEAR,"~48%","win rate","~45%","max drawdown",
            "Premium decay + false breaks eat the wins. A coin-flip with a brutal drawdown."),
           ("Naive ORB — option SELLING",GOLD,"marginally\nbetter","win rate","~6%","max drawdown",
            "Theta works for you, so drawdown is far smaller — but it is still not an edge by itself.")]
    n=len(cards); cw=(W-2*PADL-30)/2; x0=PADL; y=90; ch=210
    for i,(t,col,wr,wrl,dd,ddl,note) in enumerate(cards):
        x=x0+i*(cw+30)
        _box(s,x,y,cw,ch,col)
        s.append(f'<text x="{x+16:.1f}" y="{y+28:.1f}" fill="{col}" font-size="13.5" font-weight="700">{esc(t)}</text>')
        # two big stats side by side
        sx=x+16; sy=y+78
        for j,(big,lab) in enumerate([(wr,wrl),(dd,ddl)]):
            bx=sx+j*(cw/2-4)
            parts=str(big).split("\n")
            yy=sy
            for p in parts:
                s.append(f'<text x="{bx:.1f}" y="{yy:.1f}" fill="{TEXT}" font-size="22" font-weight="800">{esc(p)}</text>')
                yy+=22
            s.append(f'<text x="{bx:.1f}" y="{yy+2:.1f}" fill="{SUB}" font-size="10.5">{esc(lab)}</text>')
        _wrap(s,x+16,y+150,note,SUB,10.5,46)
    # punchline band
    py=y+ch+18
    _box(s,PADL,py,W-2*PADL,52,GOLD,fill="#1d2330")
    s.append(f'<text x="{W/2:.1f}" y="{py+22:.1f}" fill="{GOLD}" font-size="14" font-weight="700" text-anchor="middle">'
             f'{esc("The edge is SELECTIVITY, not the break.")}</text>')
    s.append(f'<text x="{W/2:.1f}" y="{py+42:.1f}" fill="{TEXT}" font-size="11.5" text-anchor="middle">'
             f'{esc("Profits come from the confluence filters (regime, VWAP, volume, OI, R:R) — not from buying every OR break.")}</text>')
    s.append(f'<text x="{W/2}" y="{h-10}" fill="{SUB}" font-size="10.5" text-anchor="middle">'
             f'{esc("Numbers are illustrative, from a single Zerodha backtest — directional, not a guarantee.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- orb-scorecard ---------------------------------------------------------
def render_scorecard():
    h=480
    s=_svg_open("ORB Confluence Scorecard — A+ / A / skip",
                "Count the confluences; the grade decides size (and whether to trade at all)",h=h)
    factors=["Regime aligns (trend / neg-GEX) with break direction",
             "Break on the right side of VWAP",
             "Volume EXPANSION on the break candle",
             "Fresh OI buildup in the break direction",
             "Price breaking AWAY from max-pain",
             "Clean retest of the OR edge holds",
             "R:R to first target ≥ 2:1",
             "Not late on an expiry day (theta-hostile)"]
    y=96
    for f in factors:
        s.append(f'<circle cx="{PADL+10}" cy="{y-4}" r="6" fill="none" stroke="{SUB}" stroke-width="1.5"/>')
        s.append(f'<text x="{PADL+28}" y="{y}" fill="{TEXT}" font-size="12.5">{esc(f)}</text>')
        y+=34
    bx=560
    bands=[("A+ break","≥ 7 / 8","full size",BULL),
           ("A break","5–6 / 8","½–¾ size",TEAL),
           ("skip","≤ 4 / 8","no trade / paper",BEAR)]
    by=112
    for t,cnt,act,col in bands:
        _box(s,bx,by,W-PADR-bx,58,col,fill="#1a2230")
        s.append(f'<text x="{bx+14:.1f}" y="{by+24:.1f}" fill="{col}" font-size="14" font-weight="700">{esc(t)}</text>')
        s.append(f'<text x="{bx+14:.1f}" y="{by+44:.1f}" fill="{TEXT}" font-size="11">{esc(cnt+" — "+act)}</text>')
        by+=74
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'{esc("The grade sets the SIZE. Only A+ gets full risk; A gets reduced; anything less waits.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- options-translation ---------------------------------------------------
def render_options_translation():
    h=430
    s=_svg_open("Spot OR Break → the Option Trade",
                "Translate the spot ORB into a strike, a delta, and a premium stop",h=h)
    fx=PADL+10; fy=80
    _box(s,fx,fy,W-2*PADL-20,56,GOLD,fill="#1d2330")
    s.append(f'<text x="{W/2:.1f}" y="{fy+35:.1f}" fill="{GOLD}" font-size="16" font-weight="700" text-anchor="middle">'
             f'{esc("premium stop  ≈  point-stop × delta   (or 20% of entry premium)")}</text>')
    steps=[("Pick the strike","ATM / near-ATM","Delta 0.4–0.6, premium ≈ ₹0.5 per spot point. Avoid deep OTM lottery strikes.",BLUE),
           ("Direction","up-break → call · down-break → put","Match the option to the OR break direction.",TEAL),
           ("Premium stop","20% of entry premium","If bought at 120, hard stop near 96 (≈20%).",GOLD),
           ("…or delta-based","point-stop × delta","30-pt spot stop × 0.5 delta ≈ 15 premium points.",BULL)]
    y=160; rh=58
    for name,val,desc,col in steps:
        _box(s,fx,y,W-2*PADL-20,rh-10,col,fill="#161d2b")
        s.append(f'<text x="{fx+16:.1f}" y="{y+22:.1f}" fill="{col}" font-size="12" font-weight="700">{esc(name)}</text>')
        s.append(f'<text x="{fx+16:.1f}" y="{y+40:.1f}" fill="{TEXT}" font-size="13.5" font-weight="700">{esc(val)}</text>')
        s.append(f'<text x="{fx+330:.1f}" y="{y+31:.1f}" fill="{SUB}" font-size="10.5">{esc(desc)}</text>')
        y+=rh
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{GOLD}" font-size="11.5" font-weight="600" text-anchor="middle">'
             f'{esc("Deep-OTM looks cheap but the delta is tiny — the spot break barely moves the premium. Stay near ATM.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- expiry-theta ----------------------------------------------------------
def render_expiry_theta():
    h=420
    s=_svg_open("Expiry-Day Theta — late ORB buying is theta-hostile",
                "Intraday premium decay steepens on Nifty Tuesday weekly-expiry afternoons",h=h)
    gx0=PADL+50; gx1=W-PADL-30; gy0=92; gy1=h-90
    s.append(f'<line x1="{gx0}" y1="{gy0}" x2="{gx0}" y2="{gy1}" stroke="{SUB}" stroke-width="1.2"/>')
    s.append(f'<line x1="{gx0}" y1="{gy1}" x2="{gx1}" y2="{gy1}" stroke="{SUB}" stroke-width="1.2"/>')
    s.append(f'<text x="{PADL+8}" y="{(gy0+gy1)/2}" fill="{SUB}" font-size="10.5" transform="rotate(-90 {PADL+8} {(gy0+gy1)/2})" text-anchor="middle">premium (time value)</text>')
    times=["9:15","11:00","12:30","1:30","2:00","2:30","3:00","3:30"]
    fr=[0.0,0.26,0.42,0.58,0.66,0.74,0.86,1.0]
    for t,f in zip(times,fr):
        x=gx0+(gx1-gx0)*f
        s.append(f'<line x1="{x:.1f}" y1="{gy1:.1f}" x2="{x:.1f}" y2="{gy1+5:.1f}" stroke="{SUB}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{gy1+20:.1f}" fill="{SUB}" font-size="9.5" text-anchor="middle">{esc(t)}</text>')
    def val(f): return 100*(1 - 0.28*f - 0.72*(f**2.7))
    pts=[]; steps=40
    for i in range(steps+1):
        f=i/steps; v=val(f)
        x=gx0+(gx1-gx0)*f; yv=gy1-(gy1-gy0)*(v/100.0)
        pts.append((x,yv))
    d="M"+" L".join(f"{x:.1f},{yv:.1f}" for x,yv in pts)
    s.append(f'<path d="{d}" stroke="{BEAR}" stroke-width="2.8" fill="none"/>')
    fx=gx0+(gx1-gx0)*0.74
    s.append(f'<line x1="{fx:.1f}" y1="{gy0:.1f}" x2="{fx:.1f}" y2="{gy1:.1f}" stroke="{GOLD}" stroke-width="1.4" stroke-dasharray="5 4"/>')
    s.append(f'<text x="{fx+6:.1f}" y="{gy0+16:.1f}" fill="{GOLD}" font-size="11" font-weight="600">~2:30pm: decay accelerates</text>')
    s.append(f'<text x="{gx0+60:.1f}" y="{gy0+40:.1f}" fill="{SUB}" font-size="10.5">slow bleed early →</text>')
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'{esc("Buying weeklies into the expiry-day close fights theta — a late OR break must move fast or it bleeds.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- mtf-nesting (adapted from render_mtf) ---------------------------------
def render_mtf():
    h=566
    s=_svg_open("Multi-Timeframe Nesting for the ORB",
                "1h/30m REGIME → 15m OPENING RANGE → 5m TRIGGER",h=h)
    panels=[("1h / 30m — REGIME",BLUE,"Trend vs balance, PDH/PDL, prior-day value & naked POC, OI-wall band, GEX. → sets fade-vs-break bias.",
             [(30,40),(40,55),(55,52),(52,70),(70,66),(66,85)],"up"),
            ("15m — THE OPENING RANGE",GOLD,"The OR box (9:15–9:30) — the break level, its width (measured move), and the liquidity above/below.",
             [(40,62),(62,60),(60,63),(63,61),(61,64),(64,63),(63,80)],"level"),
            ("5m — THE TRIGGER",BULL,"Conviction close beyond the OR, sweep-and-go vs sweep-and-reverse, retest of OR edge / VWAP with +delta.",
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
    funnel=[("Align?",BLUE,"5m OR break must agree with the 1h/30m regime — else it is a counter-trend fade, not a trade."),
            ("Level",GOLD,"The OR is fixed on the 15m; the 5m never invents its own range — it only triggers the break."),
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
             f'{esc("Regime sets the bias, the 15m sets the range, the 5m pulls the trigger.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---- per-daytype-cards -----------------------------------------------------
def render_per_daytype_cards():
    h=420
    s=_svg_open("ORB Per Day-Type — three playbooks",
                "Trend-day · balance-day · gap-day each demand a different ORB approach",h=h)
    cards=[("TREND DAY",BULL,"trade the break",
            "Open-drive / neg-GEX. OR break extends. Enter the conviction close or first retest; target the measured move + next level. Trail the runner."),
           ("BALANCE DAY",GOLD,"trade the trap (fade)",
            "Range / pos-GEX / pin. OR breaks fail. Fade the poke back inside the OR; target the opposite OR edge / POC. Quick exits."),
           ("GAP DAY",TEAL,"let it settle",
            "Gap-up / gap-down. Skip the first OR candle; wait for the gap-fill or held retest, then trade the OR-edge break with the gap.")]
    n=len(cards); cw=(W-2*PADL-2*20)/3; x0=PADL; y=86; ch=270
    for i,(t,col,verdict,desc) in enumerate(cards):
        x=x0+i*(cw+20)
        _box(s,x,y,cw,ch,col)
        s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw:.1f}" height="34" rx="8" fill="{col}" opacity="0.20"/>')
        s.append(f'<text x="{x+cw/2:.1f}" y="{y+23:.1f}" fill="{col}" font-size="14" font-weight="700" text-anchor="middle">{esc(t)}</text>')
        s.append(f'<text x="{x+cw/2:.1f}" y="{y+58:.1f}" fill="{TEXT}" font-size="12.5" font-weight="700" text-anchor="middle">{esc("→ "+verdict)}</text>')
        _wrap(s,x+14,y+86,desc,SUB,10.5,30)
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'{esc("Same opening range, three different days — read the day-type first, then pick the playbook.")}</text>')
    s.append("</svg>")
    return "\n".join(s)

SPECIALS={
    "or-window-comparison":render_or_window,
    "open-types":render_open_types,
    "dalton-open-types":render_dalton_open_types,
    "oi-confluence":render_oi_confluence,
    "daytype-decision-tree":render_daytype_tree,
    "honest-edge":render_honest_edge,
    "orb-scorecard":render_scorecard,
    "options-translation":render_options_translation,
    "expiry-theta":render_expiry_theta,
    "mtf-nesting":render_mtf,
    "per-daytype-cards":render_per_daytype_cards,
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
