#!/usr/bin/env python3
"""Parametric FAKEOUT-REVERSAL SVG schematic + animation generator (house style).

Deterministic, ~0 model tokens. The offensive twin of breakout_svg.py: renders the
failed-breakout reversal lifecycle, the sweep-and-reverse vs sweep-and-go fork, the
named-patterns family (turtle soup, SFP, Wyckoff spring/upthrust, poor high-low /
failed auction), absorption + CVD-divergence reversals, the CHoCH-reclaim entry,
SL/target geometry, the options-tape re-defense reads (OI re-defense, failed OI
migration, positive-GEX pin regime, max-pain magnet), the regime decision tree, and
the 10-point reversal scorecard. Matches scripts/candle_svg.py house style.

Usage:
  python fakeout_svg.py <out_dir>           # all schematics + infographics
  python fakeout_svg.py <out_dir> --anim    # also animated lifecycle/sweep/turtle/spring/choch
"""
import os, sys

# ---- house style (shared with candle_svg.py / breakout_svg.py) -------------
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
#  CORE: candle-series scene renderer  (verbatim from breakout_svg.py)
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
    extra=scene.get("yextra",[])
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
            s.append(f'<text x="{x0+3:.1f}" y="{yp-5:.1f}" fill="{lv["color"]}" font-size="11" '
                     f'font-weight="600" opacity="{0 if anim else 1}">{esc(lv["label"])}'
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
                 f'font-weight="{700 if bold else 500}">{text}</text>')
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

# ---- 1. HERO: the fakeout-reversal lifecycle (animated) --------------------
# prior up-drive into resistance -> coil/equal-highs -> SWEEP above (bull trap) ->
# close back inside -> CHoCH down -> retest of broken level (fails) -> revert down.
_life=[(40,43,39,42),(42,46,41,45),(45,49,44,48),(48,52,47,51),(51,55,50,54),(54,58,53,57),
       (57,60,56,58),(58,61,57,59),(59,60,57,58),     # coil, equal highs ~60-61 = buy-side liquidity
       (59,64,58,59),                                  # ④ SWEEP above 60 (wick 64), CLOSES BACK at 59 = the trap
       (59,60,55,56),                                  # ⑤ rejection — bearish close back inside
       (56,57,51,52),                                  # ⑥ CHoCH — breaks the prior swing low
       (52,60,51,57),                                  # ⑦ retest of broken level (60) from below — FAILS (close 57)
       (57,58,52,53),(53,54,48,49),(49,50,44,45),(45,47,42,43)]  # ⑧ revert down to opposite edge
S(name="The Fakeout-Reversal Lifecycle", slug="lifecycle",
  subtitle="Up-drive → coil → SWEEP above (bull trap) → close back inside → CHoCH → failed retest → revert",
  candles=_life,
  levels=[lvl(60,"Resistance / equal highs (buy-side liquidity)",GOLD),
          lvl(44,"Range low / mean → reversal target",TEAL,w=1.2)],
  zones=[dict(x0=6,x1=8,y0=57,y1=61,fill=ZONE_Y,stroke=SUB,dash="4 3",label="coil / equal highs"),
         dict(x0=11,x1=12,y0=57,y1=61,fill=ZONE_R,stroke=BEAR,label="failed retest (OB)")],
  arrows=[dict(x0=9,y0=63,x1=9,y1=60.5,color=GOLD,label="sweep stops",w=2,ldy=-6,t=0.2),
          dict(x0=10,y0=58,x1=10,y1=52,color=BEAR,label="CHoCH↓",w=2.8,ldy=14,t=0.4),
          dict(x0=15.4,y0=49,x1=16,y1=43,color=BEAR,label="revert",w=2.6,t=0.8)],
  annot=[dict(x=0.5,y=0.055,yfrac=True,text="① drive  ② coil  ③ sweep  ④ close back in  ⑤ CHoCH  ⑥ failed retest  ⑦ revert",
              color=TEXT,fs=11,fw=600)],
  sl_tp=dict(entry=59,sl=65,tps=[(50,"TP1"),(44,"TP2")]),
  caption="The whole game: did the break get ACCEPTED (real → stand aside) or REJECTED (failed → fade it)?")

# ---- 2. the fork: sweep-and-reverse (TRADE) vs sweep-and-go (STAND ASIDE) ---
S(name="SWEEP-AND-REVERSE (the trade)", slug="sweep-and-reverse",
  subtitle="Poke beyond the level → long wick → close back inside → reverse",
  candles=[(48,51,47,50),(50,54,49,53),(53,57,52,56),
           (56,62,55,57),                     # sweep above 57 (wick 62), closes back at 57
           (57,58,52,53),(53,55,49,50),(50,51,45,46)],
  levels=[lvl(57,"Level (equal highs = liquidity)",GOLD)],
  arrows=[dict(x0=3,y0=60.5,x1=3,y1=57.5,color=GOLD,w=2.2,label="grab stops"),
          dict(x0=5,y0=54,x1=6,y1=46,color=BEAR,w=2.8,label="trap reverses")],
  delta=[2,5,9,11,5,-3,-9],
  delta_note="delta rolls over AT the sweep = absorption", delta_note_col=BEAR,
  caption="Took the liquidity, FAILED to hold → the breakout buyers are trapped fuel → fade it.")
S(name="SWEEP-AND-GO (stand aside)", slug="sweep-and-go",
  subtitle="Same poke — but it CLOSES beyond and accepts → it is a real break, not a reversal",
  candles=[(48,51,47,50),(50,54,49,53),(53,57,52,56),
           (56,63,55,62),                     # sweep AND closes well above 57 = conviction
           (62,66,61,65),(65,69,64,68),(68,72,67,71)],
  levels=[lvl(57,"Level (broken & accepted)",GOLD)],
  arrows=[dict(x0=3,y0=57,x1=3,y1=62,color=BULL,w=2.8,label="conviction close"),
          dict(x0=5,y0=66,x1=6,y1=71,color=BULL,w=2.6,label="accept + run")],
  delta=[2,5,9,14,19,24,29],
  delta_note="delta EXPANDS with price = initiative", delta_note_col=BULL,
  caption="This is NOT your trade — the sweep kept going (sweep-and-GO). Do not fade a real break.")

# ---- 3. named patterns: turtle soup (animated) -----------------------------
S(name="Turtle Soup (false break of the prior low)", slug="turtle-soup",
  subtitle="Stab below an obvious N-bar low, then SNAP BACK above it → reverse up",
  candles=[(58,59,55,56),(56,57,52,53),(53,54,49,50),(50,51,45,46),
           (46,48,44,45),                     # makes the obvious low ~44
           (45,47,43,46),
           (45,46,40,45),                     # SWEEP below 44 (wick 40), CLOSES back at 45 above it
           (45,50,44,49),(49,54,48,53),(53,58,52,57)],
  levels=[lvl(44,"Prior N-bar low (sell-side liquidity)",BEAR)],
  zones=[dict(x0=6,x1=7,y0=40,y1=45,fill=ZONE_G,stroke=BULL,label="sweep + reclaim")],
  arrows=[dict(x0=6,y0=42.5,x1=6,y1=40,color=GOLD,w=2,label="grab",ldy=11),
          dict(x0=8,y0=50,x1=9,y1=57,color=BULL,w=2.6,label="reverse up")],
  caption="Raschke's Turtle Soup: the obvious low is bait — buy the reclaim close back above it.")

# ---- 4. swing failure pattern (SFP) at a high ------------------------------
S(name="Swing Failure Pattern (SFP)", slug="sfp",
  subtitle="Take the prior swing high's liquidity, then close back below it → reverse down",
  candles=[(46,49,45,48),(48,52,47,51),(51,55,50,54),(54,58,53,57),
           (57,59,56,58),                     # approaches prior swing high 59
           (58,63,57,58),                     # SWEEP above 59 (wick 63), CLOSES back at 58 below it = SFP
           (58,59,54,55),(55,56,51,52),(52,53,48,49)],
  levels=[lvl(59,"Prior swing high (buy-side liquidity)",GOLD)],
  zones=[dict(x0=5,x1=6,y0=59,y1=63,fill=ZONE_R,stroke=BEAR,label="failed swing (SFP)")],
  arrows=[dict(x0=5,y0=61.5,x1=5,y1=59,color=GOLD,w=2,label="sweep high"),
          dict(x0=6,y0=57,x1=7,y1=52,color=BEAR,w=2.6,label="close back below")],
  caption="The high is taken but not held — a single candle that sweeps and closes back inside = short the failure.")

# ---- 5. Wyckoff spring (animated) ------------------------------------------
S(name="Wyckoff Spring", slug="wyckoff-spring",
  subtitle="A final shakeout BELOW range support that immediately reclaims → markup",
  candles=[(52,56,51,55),(55,57,50,51),(51,53,47,52),(52,56,48,55),(55,57,47,48),
           (48,50,46,47),                     # rests on support
           (47,49,42,48),                     # SPRING: stab below 46 (wick 42), CLOSES back at 48 inside range
           (48,52,47,51),(51,55,50,54),(54,58,53,57),(57,60,56,59)],
  levels=[lvl(46,"Support / range low (the spring level)",TEAL),
          lvl(58,"Range high → reversal target",GOLD,dash=True)],
  zones=[dict(x0=6,x1=7,y0=42,y1=46,fill=ZONE_G,stroke=BULL,label="spring (shakeout)")],
  arrows=[dict(x0=6,y0=44.5,x1=6,y1=42,color=GOLD,w=2,label="shake out",ldy=11),
          dict(x0=8,y0=52,x1=10,y1=59,color=BULL,w=2.6,label="markup")],
  caption="Wyckoff Spring: the last weak hands are shaken out below support, then price reclaims → the reversal long.")

# ---- 6. Wyckoff upthrust / UTAD --------------------------------------------
S(name="Upthrust After Distribution (UTAD)", slug="wyckoff-upthrust",
  subtitle="A stab ABOVE range resistance that fails back inside → markdown",
  candles=[(50,54,49,53),(53,55,48,49),(49,53,47,52),(52,54,45,46),(46,55,45,54),
           (54,56,52,53),                     # tests resistance
           (53,58,52,46),                     # UPTHRUST: stab above 56 (wick 58), CLOSES back at 46 inside range
           (46,47,42,43),(43,44,39,40),(40,41,36,37)],
  levels=[lvl(56,"Resistance / range high (the upthrust level)",GOLD),
          lvl(44,"Support / range low → reversal target",TEAL,dash=True)],
  zones=[dict(x0=6,x1=6,y0=56,y1=58,fill=ZONE_R,stroke=BEAR,label="upthrust")],
  arrows=[dict(x0=6,y0=57.5,x1=6,y1=56,color=GOLD,w=2,label="stab up"),
          dict(x0=7,y0=45,x1=9,y1=37,color=BEAR,w=2.6,label="markdown")],
  caption="UTAD: a false break above resistance that closes back inside → the reversal short (mirror of the spring).")

# ---- 7. absorption reversal (order flow) -----------------------------------
S(name="Absorption Reversal", slug="absorption-reversal",
  subtitle="Heavy aggressive buying SOAKED UP at the level — big delta, no price progress → reverse",
  candles=[(50,53,49,52),(52,55,51,54),(54,57,53,56),(56,58,55,57),
           (57,58,56,57),(57,58,55,56),(56,57,52,53),(53,54,49,50)],
  levels=[lvl(58,"Level — passive sellers absorbing",GOLD)],
  arrows=[dict(x0=6,y0=55,x1=7,y1=50,color=BEAR,w=2.6,label="reversal")],
  delta=[3,8,14,20,24,27,18,8],
  delta_note="big +delta, NO price progress = absorption", delta_note_col=BEAR,
  caption="Buyers keep hitting the offer but price can't advance — a passive seller is absorbing → fade the stall.")

# ---- 8. cumulative-delta divergence reversal -------------------------------
S(name="CVD-Divergence Reversal", slug="cvd-divergence-reversal",
  subtitle="Price prints a higher high; cumulative delta makes a LOWER high → buyers exhausting",
  candles=[(50,53,49,52),(52,56,51,55),(55,58,54,57),(57,60,56,58),(58,62,57,59),(59,60,55,56)],
  levels=[lvl(62,"New price high (unconfirmed)",GOLD)],
  delta=[4,9,15,17,13,6],
  delta_note="price HH, delta LOWER high = divergence", delta_note_col=BEAR,
  caption="Effort (delta) no longer matches result (price) — the highest-trust reversal tell on the NSE feed.")

# ---- 9. poor high / failed auction (volume profile) ------------------------
_vp_bins=[(64,0.18,"lvn"),(60,0.26,"lvn"),(56,0.46,"hvn"),(52,0.70,"hvn"),
          (50,1.00,"poc"),(48,0.72,"hvn"),(44,0.42,"hvn"),(40,0.24,"lvn")]
S(name="Poor High / Failed Auction", slug="poor-high-low-failed-auction",
  subtitle="A thin, unfinished 'poor high' gets revisited; price is drawn back to the naked POC",
  candles=[(56,58,55,57),(57,60,56,59),(59,63,58,62),(62,64,61,63),
           (63,64,60,61),(61,62,57,58),(58,59,54,55),(55,56,50,51)],
  profile=dict(bins=_vp_bins,poc=50,vah=56,val=46,binh=15),
  levels=[lvl(64,"Poor / single-print high (unfinished auction)",GOLD),
          lvl(50,"Naked POC → magnet & target",TEAL,dash=True)],
  arrows=[dict(x0=4,y0=62,x1=7,y1=52,color=BEAR,w=2.6,label="pulled back to the magnet")],
  caption="A poor high (no excess, thin volume) is an unfinished auction — price returns to test it, then reverts to the naked POC.")

# ---- 10. CHoCH-reclaim entry (animated, the A+ reversal entry) --------------
S(name="CHoCH-Reclaim Entry (A+ reversal)", slug="choch-reclaim-entry",
  subtitle="Sweep → CHoCH → pullback into the micro-OB (FVG fill) → confirmation candle → enter",
  candles=[(50,52,49,51),(51,54,50,53),(53,57,52,56),
           (56,61,55,56),                     # sweep above 57 (wick 61), close back at 56
           (56,57,52,53),                     # CHoCH — breaks the recent swing low
           (53,57,52,56),                     # pullback up into the micro-OB / broken level (the last up candle)
           (56,57,53,54),                     # confirmation bearish candle at the zone
           (54,55,50,51),(51,52,47,48)],
  levels=[lvl(57,"Swept level → now resistance",GOLD)],
  zones=[dict(x0=5,x1=6,y0=55,y1=57,fill=ZONE_R,stroke=BEAR,label="micro-OB (retest)")],
  arrows=[dict(x0=3,y0=59,x1=3,y1=56.5,color=GOLD,w=2,label="sweep"),
          dict(x0=4,y0=56,x1=4,y1=52,color=BEAR,w=2.4,label="CHoCH",ldy=42),
          dict(x0=6.4,y0=55,x1=7,y1=50,color=BEAR,w=2.6,label="confirm + go",ldy=34)],
  sl_tp=dict(entry=55,sl=62,tps=[(48,"TP1"),(42,"TP2")]),
  caption="The A+ reversal entry: sweep → CHoCH → reclaim into the micro-OB / FVG → confirm. Stop just beyond the SWEEP extreme.")

# ---- 11. opening-range fakeout + VWAP rejection ----------------------------
S(name="Opening-Range Fakeout + VWAP Reject", slug="orb-fakeout-vwap-reject",
  subtitle="Sweep the OR high, fail to hold, then LOSE VWAP → fade back into the range",
  candles=[(50,54,46,53),(53,55,49,50),(50,56,48,55),(55,58,51,52),  # IB builds 46-58
           (52,56,49,55),(55,57,53,56),                              # coils inside
           (56,61,55,56),                                            # SWEEP above IB high 58 (wick 61), close back 56
           (56,57,52,53),(53,54,49,50),(50,51,46,47)],               # reverts down through VWAP
  levels=[lvl(58,"IB / opening-range HIGH (swept)",GOLD),
          lvl(46,"IB / opening-range LOW → target",SUB,w=1.2)],
  curves=[dict(points=[(0,50),(2,52),(4,53),(6,55),(7,55),(8,53),(9,50)],color=PURP,label="VWAP",w=2.2)],
  zones=[dict(x0=6,x1=6,y0=58,y1=61,fill=ZONE_R,stroke=BEAR,label="false break (swept stops)")],
  arrows=[dict(x0=6,y0=59.5,x1=6,y1=57,color=GOLD,w=2,label="sweep OR high"),
          dict(x0=8,y0=54,x1=9,y1=47,color=BEAR,w=2.6,label="lose VWAP → fade")],
  caption="The opening-range fake before the real move: sweeps the OR high, can't hold, loses VWAP → fade into the IB.")

# ---- 12. SL / target geometry for a reversal -------------------------------
S(name="Reversal Stop & Target Geometry", slug="sl-target-geometry-reversal",
  subtitle="SL just beyond the SWEEP extreme (+ATR); targets ladder to the range mid/POC then the opposite edge",
  candles=[(46,49,45,48),(48,52,47,51),(51,56,50,55),(55,59,54,58),
           (58,60,57,59),                     # at resistance 60
           (59,65,58,59),                     # SWEEP to 65, close back 59
           (59,60,55,56),                     # rejection
           (56,61,55,57),                     # failed retest (entry zone ~58)
           (57,58,53,54),(54,55,49,50),(50,51,45,46),(46,47,42,43)],
  levels=[lvl(60,"Swept level (now resistance)",GOLD),
          lvl(66,"Beyond the sweep → SL anchor (+ATR buffer)",BEAR,dash=True),
          lvl(50,"TP1: range mid / POC",TEAL,dash=True),
          lvl(44,"TP2: opposite edge / liquidity",TEAL,dash=True)],
  zones=[dict(x0=7,x1=7,y0=58,y1=60,fill=ZONE_R,stroke=BEAR,label="failed-retest entry")],
  annot=[dict(x=0.34,y=0.20,yfrac=True,text="the RANGE is the measured move — fade across the box",color=SUB,fs=10.5)],
  sl_tp=dict(entry=58,sl=66,tps=[(50,"TP1"),(44,"TP2"),(40,"TP3 (trail)")]),
  caption="Risk to just beyond where the IDEA is wrong (the sweep extreme); targets are the structural magnets back inside.")

def main_scenes(out):
    n=0
    for sc in SCENES:
        open(os.path.join(out,sc["slug"]+".svg"),"w",encoding="utf-8").write(render_scene(sc))
        n+=1
    return n

ANIM_SLUGS={"lifecycle","sweep-and-reverse","turtle-soup","wyckoff-spring","choch-reclaim-entry"}
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

def _wrap(s,text,x,y,maxchars,fill,fs,dy=13):
    words=str(text).split(); line=""; yy=y
    for w_ in words:
        if len(line)+len(w_)>maxchars:
            s.append(f'<text x="{x}" y="{yy}" fill="{fill}" font-size="{fs}">{esc(line)}</text>'); line=w_; yy+=dy
        else: line=(line+" "+w_).strip()
    s.append(f'<text x="{x}" y="{yy}" fill="{fill}" font-size="{fs}">{esc(line)}</text>')
    return yy

def render_oi_redefense():
    """The wall HOLDS: call OI RISING at the tested strike = writers re-defending."""
    s=_svg_open("OI Re-Defense — the wall HOLDS","Call OI RISING at the tested strike = writers defending the ceiling → the break fails")
    strikes=[("23 200 CE",0.30,SUB,"light — unchanged"),
             ("23 100 CE",0.42,SUB,"light — no fresh writing"),
             ("23 000 CE",0.92,BEAR,"TESTED strike — OI RISING ↑ (writers re-defend)"),
             ("22 900 CE",0.50,SUB,"unchanged"),
             ("22 800 CE",0.40,SUB,"unchanged")]
    x0=190; maxw=420; y=110; bh=34
    for name,frac,col,note in strikes:
        s.append(f'<text x="{PADL}" y="{y+4}" fill="{TEXT}" font-size="12" font-weight="600">{name}</text>')
        s.append(f'<rect x="{x0}" y="{y-14}" width="{maxw*frac:.0f}" height="{bh-10}" rx="3" fill="{col}" opacity="0.85"/>')
        s.append(f'<text x="{x0+maxw*frac+8:.0f}" y="{y+4}" fill="{col}" font-size="10.5">{esc(note)}</text>')
        y+=bh+8
    # price poke arrow
    s.append(f'<text x="{PADL}" y="{y+12}" fill="{GOLD}" font-size="11.5" font-weight="600">Price pokes ABOVE 23 000 — but the OI at 23 000 keeps RISING, not unwinding.</text>')
    s.append(f'<text x="{W/2}" y="{H-14}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'Compare the breakout note: a REAL break needs the wall OI to DROP (writers capitulate). Rising OI = the ceiling held → fade.</text>')
    s.append("</svg>")
    return "\n".join(s)

def render_failed_oi_migration():
    """No fresh OI at the next strike → the range is NOT re-pricing → fakeout."""
    s=_svg_open("Failed OI Migration","A real break MOVES the wall up; a fakeout leaves it where it was")
    cols=[("BEFORE the poke",230),("AT the poke (no migration)",560)]
    for label,cx in cols:
        s.append(f'<text x="{cx}" y="86" fill="{SUB}" font-size="12" text-anchor="middle" font-weight="600">{esc(label)}</text>')
    strikes=[("23 200",0.20,0.22),("23 100",0.28,0.30),("23 000 (wall)",0.95,0.97),("22 900",0.40,0.40)]
    y=120; bh=40; bw=180
    for name,before,after in strikes:
        wall = "wall" in name
        col=GOLD if wall else SUB
        s.append(f'<text x="{W/2}" y="{y+4}" fill="{TEXT}" font-size="11.5" text-anchor="middle">{name}</text>')
        s.append(f'<rect x="{230-bw*before:.0f}" y="{y-14}" width="{bw*before:.0f}" height="{bh-14}" rx="3" fill="{col}" opacity="0.8"/>')
        s.append(f'<rect x="560-{bw*after*0:.0f}" y="{y-14}" width="{bw*after:.0f}" height="{bh-14}" rx="3" fill="{col}" opacity="0.8"/>')
        y+=bh
    s.append(f'<text x="{W/2}" y="{y+6}" fill="{BEAR}" font-size="12.5" text-anchor="middle" font-weight="700">'
             f'✗ The 23 000 wall is STILL the wall — no fresh OI built at 23 100.</text>')
    s.append(f'<text x="{W/2}" y="{H-14}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'The chain did not re-price higher → the implied range is intact → the poke is a liquidity grab, not a breakout → fade.</text>')
    s.append("</svg>")
    return "\n".join(s)

def render_gex_pin_regime():
    """Positive-GEX pin = the reversal regime; negative-GEX trend = do NOT fade."""
    s=_svg_open("Dealer Gamma — which regime are you in?","POSITIVE GEX pins price (reversals work); NEGATIVE GEX lets it run (do NOT fade)")
    def path(x0,col,pts,label,note,fav):
        s.append(f'<text x="{x0}" y="100" fill="{col}" font-size="13.5" font-weight="700">{esc(label)}</text>')
        base=130; ph=210; pw=320
        s.append(f'<line x1="{x0}" y1="{base+ph/2}" x2="{x0+pw}" y2="{base+ph/2}" stroke="{GOLD}" stroke-width="1.3" stroke-dasharray="5 4"/>')
        s.append(f'<text x="{x0+pw}" y="{base+ph/2-4}" fill="{GOLD}" font-size="10" text-anchor="end">key strike / max-pain</text>')
        d=f'M{x0},{base+ph/2}'
        for dx,dy in pts: d+=f' L{x0+dx},{base+ph/2-dy}'
        s.append(f'<path d="{d}" stroke="{col}" stroke-width="2.6" fill="none"/>')
        tag = "← TRADE REVERSALS HERE" if fav else "← do NOT fade here"
        s.append(f'<text x="{x0}" y="{base+ph+22}" fill="{col}" font-size="11.5" font-weight="700">{tag}</text>')
        _wrap(s,note,x0,base+ph+40,52,SUB,10)
    pin=[(40,18),(80,-14),(120,16),(160,-10),(200,8),(240,-6),(280,4),(320,-2)]
    acc=[(40,6),(80,12),(120,10),(160,30),(200,55),(240,85),(280,120),(320,150)]
    path(40,TEAL,pin,"POSITIVE GEX → PIN / mean-reversion",
         "Dealers buy dips & sell rips — price is pinned to heavy-OI strikes. Sweeps fail; fade the edges back to the pin.",True)
    path(480,BEAR,acc,"NEGATIVE GEX → trend / acceleration",
         "Dealers chase price — sweeps become real breaks that run. Fading here is the cardinal error.",False)
    s.append(f'<text x="{W/2}" y="{H-12}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'Read GEX FIRST: a fakeout reversal is a positive-gamma / pinning / balance play. In negative gamma, stand aside.</text>')
    s.append("</svg>")
    return "\n".join(s)

def render_maxpain_magnet():
    """Price pokes away from max-pain then is magnetised back = the reversal target."""
    s=_svg_open("Max-Pain Magnet — the reversal target","Into expiry, price is pulled back toward max-pain / the largest-gamma strike")
    base=140; ph=210; pw=560; x0=150; mid=base+ph/2
    s.append(f'<line x1="{x0}" y1="{mid}" x2="{x0+pw}" y2="{mid}" stroke="{GOLD}" stroke-width="1.6" stroke-dasharray="6 4"/>')
    s.append(f'<text x="{x0}" y="{mid-8}" fill="{GOLD}" font-size="11" font-weight="600">max-pain / ATM wall (the pin)</text>')
    # path: starts at pin, pokes up (the fakeout), magnetised back down to pin
    pts=[(0,0),(60,10),(120,28),(170,52),(190,40),(230,18),(290,4),(360,-2),(440,2),(560,0)]
    d=f'M{x0},{mid}'
    for dx,dy in pts: d+=f' L{x0+dx},{mid-dy}'
    s.append(f'<path d="{d}" stroke="{TEAL}" stroke-width="2.8" fill="none"/>')
    s.append(f'<text x="{x0+175}" y="{mid-58}" fill="{BEAR}" font-size="11" font-weight="600">poke above (bull trap)</text>')
    s.append(f'<path d="M{x0+250},{mid-30} L{x0+330},{mid-6}" stroke="{TEAL}" stroke-width="2.2" marker-end="url(#mpar)"/>')
    s.append(f'<text x="{x0+300}" y="{mid-30}" fill="{TEAL}" font-size="11" font-weight="700">pulled back to the pin = your target</text>')
    s.append('<defs><marker id="mpar" markerWidth="9" markerHeight="9" refX="6" refY="4.5" orient="auto">'
             f'<path d="M0,0 L9,4.5 L0,9 z" fill="{TEAL}"/></marker></defs>')
    s.append(f'<text x="{W/2}" y="{H-14}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'On expiry afternoon the pin is strongest — fade pokes away from max-pain back toward it (PCR extremes warn of crowded positioning).</text>')
    s.append("</svg>")
    return "\n".join(s)

def render_reversal_scorecard():
    """The 10-point reversal confluence scorecard (inverted from the breakout one)."""
    s=_svg_open("Reversal Grading — confluence scorecard","Count the confluences; the grade decides the size (and whether to fade at all)",h=470)
    factors=["At a major HTF level / liquidity pool (PDH-PDL, range edge, equal H/L)",
             "BALANCE / range / positive-GEX (pin) regime — not a trend",
             "Sweep of the obvious liquidity (wick beyond the level)",
             "CLOSE back inside the level (failed break, not acceptance)",
             "Effort fails: low-vol poke OR absorption OR CVD divergence",
             "CHoCH / shift against the break (structure turns)",
             "Options re-defend: wall OI rising, no migration, premium flat",
             "Pinned toward / pulled to max-pain (esp. expiry afternoon)",
             "Clean reclaim / failed-retest entry with a confirmation candle",
             "R:R ≥ 2:1 to the range mid / opposite edge"]
    y=96
    for f in factors:
        s.append(f'<circle cx="{PADL+10}" cy="{y-4}" r="6" fill="none" stroke="{SUB}" stroke-width="1.5"/>')
        s.append(f'<text x="{PADL+28}" y="{y}" fill="{TEXT}" font-size="11.5">{esc(f)}</text>')
        y+=26
    bx=600
    bands=[("A+ fade","≥ 8 / 10","full size",BULL),
           ("A fade","6–7 / 10","½–¾ size",TEAL),
           ("Skip","≤ 5 / 10","no trade",BEAR)]
    by=110
    for t,cnt,act,col in bands:
        s.append(f'<rect x="{bx}" y="{by-22}" width="{W-PADR-bx}" height="56" rx="8" fill="#1a2230" stroke="{col}" stroke-width="1.4"/>')
        s.append(f'<text x="{bx+14}" y="{by}" fill="{col}" font-size="14" font-weight="700">{t}</text>')
        s.append(f'<text x="{bx+14}" y="{by+18}" fill="{TEXT}" font-size="11">{cnt} — {act}</text>')
        by+=72
    s.append(f'<text x="{W/2}" y="{470-12}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'Core disqualifiers: a NEGATIVE-GEX trend, or price still ACCEPTING beyond the level — those are no-trades regardless of count.</text>')
    s.append("</svg>")
    return "\n".join(s)

def render_regime_decision_tree():
    """One decision, two playbooks: read GEX/structure first."""
    s=_svg_open("Which game today? — read the regime FIRST","One read (GEX + structure) routes you to the breakout playbook OR this reversal playbook")
    # top box
    tx=W/2;
    s.append(f'<rect x="{tx-170}" y="80" width="340" height="48" rx="10" fill="#1a2230" stroke="{GOLD}" stroke-width="1.6"/>')
    s.append(f'<text x="{tx}" y="100" fill="{GOLD}" font-size="13.5" font-weight="700" text-anchor="middle">Read the regime: GEX + structure</text>')
    s.append(f'<text x="{tx}" y="118" fill="{SUB}" font-size="11" text-anchor="middle">Balance or trend? Pinning or expanding?</text>')
    # two branches
    s.append(f'<path d="M{tx-40},128 L210,180" stroke="{SUB}" stroke-width="1.6" marker-end="url(#dtar)"/>')
    s.append(f'<path d="M{tx+40},128 L650,180" stroke="{SUB}" stroke-width="1.6" marker-end="url(#dtar)"/>')
    s.append('<defs><marker id="dtar" markerWidth="9" markerHeight="9" refX="6" refY="4.5" orient="auto">'
             f'<path d="M0,0 L9,4.5 L0,9 z" fill="{SUB}"/></marker></defs>')
    boxes=[(60,190,TEAL,"REVERSAL game (this note)",
            ["Positive GEX / pinning","Balance / range / rotation","Expiry-afternoon, lunch chop","Price near / pulled to max-pain"],
            "→ Fade the swept edges back to the mean."),
           (470,190,BEAR,"BREAKOUT game (the twin)",
            ["Negative GEX / acceleration","Trend / expansion","Opening drive, post-event","Price away from max-pain"],
            "→ Trade the break in the trend direction.")]
    for x,y,col,title,items,foot in boxes:
        s.append(f'<rect x="{x}" y="{y}" width="330" height="190" rx="10" fill="#161d2b" stroke="{col}" stroke-width="1.6"/>')
        s.append(f'<text x="{x+18}" y="{y+28}" fill="{col}" font-size="14" font-weight="700">{esc(title)}</text>')
        yy=y+54
        for it in items:
            s.append(f'<text x="{x+18}" y="{yy}" fill="{TEXT}" font-size="11.5">• {esc(it)}</text>'); yy+=24
        s.append(f'<text x="{x+18}" y="{yy+8}" fill="{col}" font-size="11.5" font-weight="600">{esc(foot)}</text>')
    s.append(f'<text x="{W/2}" y="{H-14}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'Never fade a negative-GEX trend; never chase a breakout in a positive-GEX pin. The regime picks the playbook.</text>')
    s.append("</svg>")
    return "\n".join(s)

def render_patterns_taxonomy():
    """The named-patterns family at a glance."""
    s=_svg_open("The Fakeout-Reversal Family","Five names for the same engine: take the obvious liquidity, then fail to hold it",h=470)
    cards=[("Turtle Soup",BULL,"False break of an N-bar high/low, then snap back inside → fade. (Raschke & Connors)"),
           ("Swing Failure (SFP)",TEAL,"Sweep a prior swing high/low and CLOSE back beyond it → reverse. (ICT)"),
           ("Wyckoff Spring",BULL,"Shakeout BELOW range support that immediately reclaims → markup long."),
           ("Upthrust / UTAD",BEAR,"Stab ABOVE range resistance that fails back inside → markdown short."),
           ("Failed Auction / Poor High-Low",GOLD,"Thin, unfinished extreme is revisited → fade back to the naked POC. (Dalton)"),
           ("Stop-Hunt Reversal",PURP,"Liquidity grab at the obvious level (round #, PDH/PDL, IB edge) → reverse.")]
    cw=400; ch=110; gx=PADL; gy=80; gap=18
    for i,(name,col,desc) in enumerate(cards):
        cx=gx+(i%2)*(cw+gap); cy=gy+(i//2)*(ch+gap)
        s.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="9" fill="#161d2b" stroke="{col}" stroke-width="1.4"/>')
        s.append(f'<text x="{cx+16}" y="{cy+28}" fill="{col}" font-size="14" font-weight="700">{esc(name)}</text>')
        _wrap(s,desc,cx+16,cy+52,46,TEXT,11.5,15)
    s.append("</svg>")
    return "\n".join(s)

def render_mtf_reversal():
    """Multi-timeframe nesting for reversals: 1h regime/level -> 15m sweep -> 5m reclaim."""
    h=566
    s=_svg_open("Multi-Timeframe Nesting (reversal)","HTF gives the REGIME & level · MTF gives the SWEEP level · LTF gives the RECLAIM trigger",h=h)
    panels=[("1h — REGIME & LEVEL",BLUE,"Balance/range? Positive GEX? Mark the major level / liquidity pool you intend to fade.",
             [(30,60),(60,52),(52,68),(68,55),(55,70),(70,58)],"level"),
            ("15m — THE SWEEP LEVEL",GOLD,"The equal highs/lows / range edge being raided — where retail breakout stops are parked.",
             [(40,58),(58,60),(60,59),(59,66),(66,58),(58,57),(57,56)],"sweep"),
            ("5m — THE RECLAIM TRIGGER",BULL,"Sweep + close back inside → CHoCH → reclaim / failed-retest with a confirmation candle → enter.",
             [(50,58),(58,66),(66,58),(58,57),(57,52),(52,53),(53,48),(48,49),(49,44)],"trigger")]
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
        if kind in ("sweep","trigger"):
            lvy=Y(60 if kind=="sweep" else 58)
            s.append(f'<line x1="{gx0}" y1="{lvy:.1f}" x2="{gx0+gw}" y2="{lvy:.1f}" stroke="{GOLD}" stroke-width="1.2" stroke-dasharray="5 4"/>')
        tx=px0+pw-138
        _wrap(s,desc,tx,py+22,22,SUB,9.5)
        if pi<len(panels)-1:
            s.append(f'<path d="M{px0+pw/2},{py+ph} L{px0+pw/2},{py+ph+18}" stroke="{SUB}" stroke-width="1.6" marker-end="url(#mtfar)"/>')
        py+=ph+22
    s.append(f'<defs><marker id="mtfar" markerWidth="9" markerHeight="9" refX="6" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="{SUB}"/></marker></defs>')
    fx=px0+pw+30
    s.append(f'<text x="{fx}" y="96" fill="{TEXT}" font-size="13" font-weight="700">The funnel</text>')
    funnel=[("Regime",BLUE,"1h says balance/pinning — the only place a reversal is high-probability."),
            ("Where",GOLD,"15m marks the exact swept edge / liquidity pool; the 5m never invents it."),
            ("Trigger",BULL,"Sweep + close back + CHoCH + reclaim — only then do you fade.")]
    fy=116
    for t,c,desc in funnel:
        s.append(f'<text x="{fx}" y="{fy}" fill="{c}" font-size="12" font-weight="700">{t}</text>')
        fy=_wrap(s,desc,fx,fy+16,30,SUB,10)+22
    s.append(f'<text x="{W/2}" y="{h-12}" fill="{SUB}" font-size="11.5" text-anchor="middle">'
             f'You fade the IMMEDIATE break, but the target is back INTO higher-timeframe value.</text>')
    s.append("</svg>")
    return "\n".join(s)

SPECIALS={"oi-redefense":render_oi_redefense,"failed-oi-migration":render_failed_oi_migration,
          "gex-pin-regime":render_gex_pin_regime,"maxpain-magnet-target":render_maxpain_magnet,
          "reversal-scorecard":render_reversal_scorecard,"regime-decision-tree":render_regime_decision_tree,
          "patterns-taxonomy":render_patterns_taxonomy,"mtf-nesting-reversal":render_mtf_reversal}

def main():
    out=sys.argv[1]; do_anim="--anim" in sys.argv
    os.makedirs(out,exist_ok=True)
    n=main_scenes(out)
    for slug,fn in SPECIALS.items():
        open(os.path.join(out,slug+".svg"),"w",encoding="utf-8").write(fn())
    na=anim_scenes(out) if do_anim else 0
    print(f"rendered {n} scenes + {len(SPECIALS)} infographics" + (f" + {na} anim" if do_anim else "") + f" -> {out}")

if __name__=="__main__":
    main()
