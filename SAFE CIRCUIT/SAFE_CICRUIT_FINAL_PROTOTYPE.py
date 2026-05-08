# GROUP 3 BSEE 1-B HUMBLY PRESENTS SAFE CIRCUIT-Pls enjoy the code there
# a few comments there where I have rambled on my thought process, please ignore some of them or treat them as cool bonuses or easter eggs
# Group Members: Diaz, Cantuba, Bejo
#Tkinter was used for the GUI 

import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
import math, platform

#FONTS 
_OS = platform.system()
FF  = ("Segoe UI" if _OS=="Windows" else "Helvetica Neue" if _OS=="Darwin" else "DejaVu Sans")
def F(sz, w="normal"): return (FF, sz, w)

GRID = 20
TR   = 8      # terminal radius
JR   = 6      # junction dot radius
SEG_HIT = 6   # px from a wire segment to count as a hit


#THEMES

THEMES = {
    "dark": {
        "bg_app":"#0d1117","bg_canvas":"#161b27","bg_card":"#1c2333",
        "bg_tb":"#090d14","bg_tab_on":"#1c2333","bg_tab_off":"#0d1117",
        "border":"#30374a","tx_pri":"#e6edf3","tx_sec":"#8b949e","tx_muted":"#484f58",
        "grid":"#1c2333","st_bg":"#090d14","st_fg":"#6e7681",
        "w_default":"#30374a","w_hot":"#f85149","w_neu":"#388bfd",
        "w_gnd":"#3fb950","w_dead":"#21262d","w_short":"#f0883e",
        "t_def":"#484f58","t_hot":"#f85149","t_neu":"#388bfd",
        "t_gnd":"#3fb950","t_hov":"#bc8cff","t_act":"#3fb950",
        "j_dot":"#e6edf3","j_rim":"#30374a",
        "p_body":"#0d1117","p_rim":"#30374a",
        "p_hot_bg":"#2d0a0a","p_hot_rim":"#f85149",
        "p_neu_bg":"#0a1433","p_neu_rim":"#388bfd",
        "p_gnd_bg":"#051a0a","p_gnd_rim":"#3fb950",
        "sw_off_bg":"#2d0f0f","sw_off_rim":"#f85149",
        "sw_on_bg":"#0d2015","sw_on_rim":"#3fb950",
        "sw3_bg":"#0d1f3a","sw3_rim":"#388bfd",
        "sw4_bg":"#1a0d3a","sw4_rim":"#bc8cff",
        "bl_off_bg":"#161b27","bl_off_rim":"#484f58",
        "bl_on_bg":"#3b2600","bl_on_rim":"#f0a72b","bl_glow":"#5c3800",
        "ou_off_bg":"#161b27","ou_off_rim":"#484f58",
        "ou_on_bg":"#0d2015","ou_on_rim":"#3fb950","ou_pin":"#3fb950",
        "sp_off_bg":"#161b27","sp_off_rim":"#484f58",
        "sp_on_bg":"#200d36","sp_on_rim":"#bc8cff",
        "sp_hot_pin":"#f85149","sp_gnd_pin":"#3fb950",
    },
    "light": {
        "bg_app":"#f0f4f8","bg_canvas":"#ffffff","bg_card":"#ffffff",
        "bg_tb":"#1e293b","bg_tab_on":"#ffffff","bg_tab_off":"#e8eef4",
        "border":"#cbd5e1","tx_pri":"#0f172a","tx_sec":"#475569","tx_muted":"#94a3b8",
        "grid":"#e8edf4","st_bg":"#e2e8f0","st_fg":"#334155",
        "w_default":"#94a3b8","w_hot":"#dc2626","w_neu":"#1d4ed8",
        "w_gnd":"#16a34a","w_dead":"#d1d5db","w_short":"#f97316",
        "t_def":"#64748b","t_hot":"#dc2626","t_neu":"#1d4ed8",
        "t_gnd":"#16a34a","t_hov":"#8b5cf6","t_act":"#16a34a",
        "j_dot":"#1e293b","j_rim":"#cbd5e1",
        "p_body":"#1e293b","p_rim":"#475569",
        "p_hot_bg":"#450a0a","p_hot_rim":"#dc2626",
        "p_neu_bg":"#172554","p_neu_rim":"#1d4ed8",
        "p_gnd_bg":"#052e16","p_gnd_rim":"#16a34a",
        "sw_off_bg":"#fef2f2","sw_off_rim":"#dc2626",
        "sw_on_bg":"#f0fdf4","sw_on_rim":"#16a34a",
        "sw3_bg":"#eff6ff","sw3_rim":"#3b82f6",
        "sw4_bg":"#f5f3ff","sw4_rim":"#6366f1",
        "bl_off_bg":"#f8fafc","bl_off_rim":"#94a3b8",
        "bl_on_bg":"#fef9c3","bl_on_rim":"#ca8a04","bl_glow":"#fef08a",
        "ou_off_bg":"#f8fafc","ou_off_rim":"#94a3b8",
        "ou_on_bg":"#f0fdf4","ou_on_rim":"#16a34a","ou_pin":"#64748b",
        "sp_off_bg":"#f8fafc","sp_off_rim":"#94a3b8",
        "sp_on_bg":"#fdf4ff","sp_on_rim":"#a21caf",
        "sp_hot_pin":"#9f1239","sp_gnd_pin":"#16a34a",
    }
}

def snap(v): return round(v / GRID) * GRID

#  DATA CLASSES
class Terminal:
    def __init__(self, cid, idx, rx, ry, label=""):
        self.comp_id=cid; self.index=idx; self.rx=rx; self.ry=ry; self.label=label
    @property
    def tid(self): return (self.comp_id, self.index)

class Component:
    _nid=0
    def __init__(self, ctype, x, y):
        self.id=Component._nid; Component._nid+=1
        self.type=ctype; self.x=snap(x); self.y=snap(y)
        self.state={}; self.terminals=[]; self.w=self.h=40
        self._init()

    def _init(self):
        c=self.id
        if self.type=="breaker":
            # Dual (1-pole) circuit breaker: L-in top, L-out bottom-left, N-out bottom-right
            # rating stored in state["amps"], toggled ON/OFF, can TRIP (ata) if di nag bug 
            self.w,self.h=80,90
            self.state={"on":True,"tripped":False,"amps":20,"load_amps":0.0}
            self.terminals=[
                Terminal(c,0,-20,-45,"L"),   # hot input  (from hot bus)
                Terminal(c,1, 20,-45,"N"),   # neutral input (from neu bus) neu means neutral btw
                Terminal(c,2,-20, 45,"L"),   # hot output (to circuit)
                Terminal(c,3, 20, 45,"N"),   # neutral output (to circuit)
            ]
            self.hot_in_tid    = (c,0)
            self.neu_in_tid    = (c,1)
            self.hot_out_tid   = (c,2)
            self.neu_out_tid   = (c,3)
        elif self.type=="hot_bus":
            # Terminals spaced to match 5 breaker slots though it's a bit chunky 
            # bus centre y ≈ 325, slots at y=68+i*96+48 → offsets from 325
            self.w,self.h=24,530
            offs=[-221,-125,-29,67,163]   # relative y for slots 1-5
            self.terminals=[Terminal(c,i,0,offs[i],f"L{i+1}") for i in range(5)]
            self.hot_tids=[(c,i) for i in range(5)]
        elif self.type=="neu_bus":
            self.w,self.h=24,530
            offs=[-221,-125,-29,67,163]
            self.terminals=[Terminal(c,i,0,offs[i],f"N{i+1}") for i in range(5)]
            self.neutral_tids=[(c,i) for i in range(5)]
        elif self.type=="gnd_bus":
            self.w,self.h=260,52
            # IN on the left end, G1-G4 spread across the bottom
            self.terminals=[
                Terminal(c,0,-120,0,"IN"),
                Terminal(c,1,-60,24,"G1"),
                Terminal(c,2,-20,24,"G2"),
                Terminal(c,3, 20,24,"G3"),
                Terminal(c,4, 60,24,"G4"),
            ]
            self.ground_tids=[(c,1),(c,2),(c,3),(c,4)]
            self.gnd_in_tid=(c,0)
        elif self.type=="switch":
            self.w,self.h=80,42; self.state={"closed":False}
            self.terminals=[Terminal(c,0,-40,0,"IN"),Terminal(c,1,40,0,"OUT")]
        elif self.type=="switch3":
            self.w,self.h=88,56; self.state={"pos":0}
            self.terminals=[Terminal(c,0,-44,0,"COM"),Terminal(c,1,44,-18,"T1"),Terminal(c,2,44,18,"T2")]
        elif self.type=="switch4":
            self.w,self.h=88,56; self.state={"cross":False}
            self.terminals=[Terminal(c,0,-44,-18,"L1"),Terminal(c,1,-44,18,"L2"),
                            Terminal(c,2,44,-18,"R1"),Terminal(c,3,44,18,"R2")]
        elif self.type=="bulb":
            self.w,self.h=60,60; self.state={"on":False}
            self.terminals=[Terminal(c,0,-30,0,"L"),Terminal(c,1,30,0,"N")]
        elif self.type=="outlet":
            self.w,self.h=64,50; self.state={"on":False}
            self.terminals=[Terminal(c,0,-32,0,"L"),Terminal(c,1,32,0,"N")]
        elif self.type=="spoutlet":
            self.w,self.h=72,60; self.state={"on":False,"grounded":False}
            self.terminals=[Terminal(c,0,-36,0,"L"),Terminal(c,1,36,0,"N"),Terminal(c,2,0,30,"G")]

    def abs_term(self, idx):
        t=self.terminals[idx]; return self.x+t.rx, self.y+t.ry

    def hit_terminal(self, mx, my, pad=4):
        for i,t in enumerate(self.terminals):
            if math.hypot(mx-(self.x+t.rx), my-(self.y+t.ry))<=TR+pad: return i
        return -1

    def hit_body(self, mx, my):
        hw,hh=self.w//2,self.h//2
        return self.x-hw<=mx<=self.x+hw and self.y-hh<=my<=self.y+hh


# ── Junction node (lives on the canvas, not on a component) -Indian Youtber,2026
class Junction:
    _nid=0
    def __init__(self, x, y):
        self.id=Junction._nid; Junction._nid+=1
        self.x=snap(x); self.y=snap(y)
        self.item=None   # canvas oval id

    @property
    def tid(self): return ("J", self.id)

    def hit(self, mx, my, pad=4):
        return math.hypot(mx-self.x, my-self.y)<=JR+pad


# ── Wire: sequence of (x,y) points — the path sort of a cartesian plane type
class Wire:
    _nid=0
    def __init__(self, from_ep, to_ep, points):
        # from_ep / to_ep: (comp_id, term_idx) OR Junction.tid
        # points: list of (x,y) — the full routed path including endpoints
        
        self.id=Wire._nid; Wire._nid+=1
        self.from_tid=from_ep
        self.to_tid=to_ep
        self.points=points   # [(x0,y0), ..., (xn,yn)]
        self.items=[]        # canvas line segment ids

    def segments(self):
        """Return list of ((x1,y1),(x2,y2)) for each segment."""
        return [(self.points[i], self.points[i+1]) for i in range(len(self.points)-1)]



#  GEOMETRY HELPERS/GUIDE

def pt_seg_dist(px, py, x1, y1, x2, y2):
    dx,dy=x2-x1,y2-y1
    if dx==dy==0: return math.hypot(px-x1,py-y1)
    t=max(0.0,min(1.0,((px-x1)*dx+(py-y1)*dy)/(dx*dx+dy*dy)))
    return math.hypot(px-(x1+t*dx), py-(y1+t*dy))

def closest_point_on_seg(px, py, x1, y1, x2, y2):
    """Return the closest point (cx,cy) on segment (x1,y1)-(x2,y2) to (px,py), snapped to grid."""
    dx,dy=x2-x1,y2-y1
    if dx==dy==0: return snap(x1),snap(y1)
    t=max(0.0,min(1.0,((px-x1)*dx+(py-y1)*dy)/(dx*dx+dy*dy)))
    return snap(x1+t*dx), snap(y1+t*dy)

def l_route(x1, y1, x2, y2, bend_first="h"):
    """
    Return a 3-point L-shaped path: start, corner, end.
    bend_first='h' → go horizontal first then vertical.
    bend_first='v' → go vertical first then horizontal.
    """
    if bend_first=="h":
        return [(x1,y1),(x2,y1),(x2,y2)]
    else:
        return [(x1,y1),(x1,y2),(x2,y2)]

def build_routed_path(sx, sy, ex, ey, user_pts):
    """
    Build the full point list for a wire.
    user_pts: list of intermediate (x,y) the user clicked.
    Each sub-path between consecutive anchors is L-routed.
    """
    anchors=[(sx,sy)]+list(user_pts)+[(ex,ey)]
    full=[]
    for i in range(len(anchors)-1):
        ax,ay=anchors[i]; bx,by=anchors[i+1]
        seg=l_route(ax,ay,bx,by,"h")
        if i==0:
            full.extend(seg)
        else:
            full.extend(seg[1:])   # skip duplicate point
    # Deduplicate consecutive identical points
    deduped=[full[0]]
    for p in full[1:]:
        if p!=deduped[-1]: deduped.append(p)
    return deduped



#  SIMULATION SIDE

VOLTAGE = 220  # Philippine standard

def simulate(components, wires, junctions):
    HOT="__HOT__"; NEUT="__NEUT__"; GND="__GND__"
    adj={HOT:set(),NEUT:set(),GND:set()}

    def link(a,b):
        adj.setdefault(a,set()).add(b); adj.setdefault(b,set()).add(a)

    # Hot bus bar: all terminals are energised HOT
    for c in components.values():
        if c.type=="hot_bus":
            for t in c.hot_tids: link(HOT, t)
    # Neutral bus bar: all terminals are NEUTRAL
    for c in components.values():
        if c.type=="neu_bus":
            for t in c.neutral_tids: link(NEUT, t)
    # Ground bus bar: input connects to GND source; outputs propagate ground
    for c in components.values():
        if c.type=="gnd_bus":
            link(GND, c.gnd_in_tid)
            for t in c.ground_tids: link(GND, t)

    # Circuit breakers: when ON and not tripped, connect in→out for both L and N
    for c in components.values():
        if c.type=="breaker":
            if c.state["on"] and not c.state["tripped"]:
                link(c.hot_in_tid,  c.hot_out_tid)
                link(c.neu_in_tid,  c.neu_out_tid)

    # Switches
    for c in components.values():
        if   c.type=="switch"  and c.state["closed"]:
            link(c.terminals[0].tid,c.terminals[1].tid)
        elif c.type=="switch3":
            p=c.state["pos"]; link(c.terminals[0].tid,c.terminals[1+p].tid)
        elif c.type=="switch4":
            if not c.state["cross"]:
                link(c.terminals[0].tid,c.terminals[2].tid)
                link(c.terminals[1].tid,c.terminals[3].tid)
            else:
                link(c.terminals[0].tid,c.terminals[3].tid)
                link(c.terminals[1].tid,c.terminals[2].tid)

    for w in wires:
        link(w.from_tid, w.to_tid)

    def bfs(src):
        vis,q=({src}),deque([src])
        while q:
            n=q.popleft()
            for nb in adj.get(n,()):
                if nb not in vis: vis.add(nb); q.append(nb)
        return vis

    hot_set=bfs(HOT); neu_set=bfs(NEUT); gnd_set=bfs(GND)
    errors=[]

    if NEUT in hot_set: errors.append(("⚡ SHORT CIRCUIT: Hot directly connected to Neutral!","err"))
    if GND  in hot_set: errors.append(("⚡ GROUND FAULT: Hot connected to Ground!","err"))

    # Track load per breaker for overload detection
    breaker_loads = {}  # breaker comp_id → total watts

    for c in components.values():
        if c.type not in ("bulb","outlet","spoutlet"): continue
        t0,t1=c.terminals[0].tid,c.terminals[1].tid
        on=((t0 in hot_set and t1 in neu_set) or (t1 in hot_set and t0 in neu_set))
        c.state["on"]=on
        if c.type=="spoutlet": c.state["grounded"]=c.terminals[2].tid in gnd_set
        if on:
            # Attribute load to its upstream breaker
            load_w = {"bulb":60,"outlet":200,"spoutlet":200}.get(c.type,100)
            for br in components.values():
                if br.type!="breaker": continue
                if br.hot_out_tid in hot_set and br.hot_in_tid in hot_set:
                    breaker_loads[br.id] = breaker_loads.get(br.id,0) + load_w
        else:
            wired=any(w.from_tid==t0 or w.to_tid==t0 or w.from_tid==t1 or w.to_tid==t1 for w in wires)
            lbl=c.type.upper()+f" #{c.id}"
            if not wired:                                errors.append((f"○ {lbl}: not wired at all.","warn"))
            elif not(t0 in hot_set or t1 in hot_set):    errors.append((f"○ {lbl}: no Hot (L) path.","warn"))
            elif not(t0 in neu_set or t1 in neu_set):    errors.append((f"○ {lbl}: no Neutral (N) path.","warn"))
            else:                                        errors.append((f"○ {lbl}: circuit incomplete.","warn"))

    # Breaker overload check (80% continuous load rule) Though unlikely to even trip cuz of super low ampere rating ng bulbs
    for c in components.values():
        if c.type!="breaker": continue
        total_w = breaker_loads.get(c.id, 0)
        load_a  = total_w / VOLTAGE
        c.state["load_amps"] = load_a
        rated_a  = c.state["amps"]
        safe_a   = rated_a * 0.80
        was_tripped = c.state["tripped"]
        if load_a > rated_a:
            c.state["tripped"] = True
            errors.append((f"⚡ BREAKER #{c.id} ({rated_a}A) TRIPPED! Load={load_a:.1f}A","err"))
        elif not c.state["on"]:
            pass  # manually off
        else:
            if was_tripped and load_a <= safe_a:
                c.state["tripped"] = False   # auto-reset if load reduced
            if load_a > safe_a:
                errors.append((f"⚠ BREAKER #{c.id} ({rated_a}A): {load_a:.1f}A load near limit ({safe_a:.0f}A safe max)","warn"))

    for c in components.values():
        if c.type not in ("switch","switch3","switch4"): continue
        if not any(w.from_tid[0]==c.id or w.to_tid[0]==c.id for w in wires):
            nm={"switch":"Switch","switch3":"3-Way","switch4":"4-Way"}[c.type]
            errors.append((f"⚠ {nm} #{c.id}: not wired.","warn"))

    return hot_set, neu_set, gnd_set, errors



#  APPLICATION
class EIMSimulator:
    def __init__(self, root):
        self.root=root
        self.root.title("Safe Circuit")
        self.root.geometry("1220x760")

        self.root.iconbitmap(default='warning')
        self.theme_name="dark"; self.T=THEMES["dark"]

        self.components={}   # id → Component
        self.wires=[]        # list[Wire]
        self.junctions={}    # id → Junction

        self.mode="select"

        # Wire-drawing state
        self.wire_ep1=None       # first endpoint: tid or junction.tid
        self.wire_ep1_xy=None    # (x,y) of first endpoint
        self.wire_user_pts=[]    # intermediate bend points user clicked
        self.preview_items=[]    # canvas items for rubber-band preview

        # Drag state
        self.drag_comp=None; self.drag_off=(0,0)
        self.drag_junc=None

        self.hov_term=None   # (comp_id, term_idx) hovered
        self.hov_junc=None   # junction id hovered

        self.sim_done=False
        self.hot_set=self.neut_set=self.gnd_set=set()

        self._all_frames=[]; self._legend_items=[]
        self._build_ui()
        self._place_panel()

    #  UI 
    def _build_ui(self):
        T=self.T; self.root.configure(bg=T["bg_app"])
        self._build_toolbar()
        self.main_frame=tk.Frame(self.root,bg=T["bg_app"])
        self.main_frame.pack(fill="both",expand=True)
        self._all_frames.append(self.main_frame)
        self.left_frame=tk.Frame(self.main_frame,bg=T["bg_app"])
        self.left_frame.pack(side="left",fill="both",expand=True,padx=(8,4),pady=8)
        self._all_frames.append(self.left_frame)
        self._build_tab_area()
        self.right_frame=tk.Frame(self.main_frame,bg=T["bg_app"],width=310)
        self.right_frame.pack(side="right",fill="y",padx=(4,8),pady=8)
        self.right_frame.pack_propagate(False)
        self._all_frames.append(self.right_frame)
        self._build_info_panel()
        self.status_var=tk.StringVar(value="Panel Board placed. Select a tool to begin.")
        self.status_bar=tk.Label(self.root,textvariable=self.status_var,
            font=F(10),bg=T["st_bg"],fg=T["st_fg"],anchor="w",padx=14,pady=5)
        self.status_bar.pack(fill="x",side="bottom")

        self._set_mode("select")

    # ── Toolbar 
    def _build_toolbar(self):
        T=self.T
        self.toolbar=tk.Frame(self.root,bg=T["bg_tb"],pady=0)
        self.toolbar.pack(fill="x")
        tk.Frame(self.toolbar,bg="#388bfd",height=2).pack(fill="x")
        self.tb_inner=tk.Frame(self.toolbar,bg=T["bg_tb"],pady=7,padx=10)
        self.tb_inner.pack(fill="x")
        self.tool_btns={}

        def sep():
            tk.Frame(self.tb_inner,bg="#21262d",width=1).pack(side="left",fill="y",padx=10,pady=3)
        def glbl(t):
            tk.Label(self.tb_inner,text=t,font=F(8),bg=T["bg_tb"],fg="#484f58").pack(side="left",padx=(0,5))

        glbl("SWITCHES")
        for lbl,mode,col in [("Single-Pole","place_switch","#388bfd"),
                              ("3-Way","place_switch3","#58a6ff"),
                              ("4-Way","place_switch4","#bc8cff")]:
            b=self._tb_btn(lbl,lambda m=mode:self._set_mode(m),col)
            b.pack(side="left",padx=2); self.tool_btns[mode]=(b,col)

        sep(); glbl("PANEL")
        for lbl,mode,col in [("Breaker","place_breaker","#f85149"),
                              ("GND Bus","place_gnd_bus","#3fb950")]:
            b=self._tb_btn(lbl,lambda m=mode:self._set_mode(m),col)
            b.pack(side="left",padx=2); self.tool_btns[mode]=(b,col)

        sep(); glbl("LOADS")
        for lbl,mode,col in [("Bulb","place_bulb","#f0a72b"),
                              ("Outlet","place_outlet","#3fb950"),
                              ("SP Outlet","place_spoutlet","#bc8cff")]:
            b=self._tb_btn(lbl,lambda m=mode:self._set_mode(m),col)
            b.pack(side="left",padx=2); self.tool_btns[mode]=(b,col)

        sep(); glbl("TOOLS")
        for lbl,mode,col in [("Select/Move","select","#6e7681"),
                              ("Draw Wire","wire","#3fb950"),
                              ("Delete","delete","#f85149")]:
            b=self._tb_btn(lbl,lambda m=mode:self._set_mode(m),col)
            b.pack(side="left",padx=2); self.tool_btns[mode]=(b,col)

        sep()
        tk.Button(self.tb_inner,text="⚡  Simulate",command=self._simulate,
            font=F(10,"bold"),bg="#1a7f37",fg="white",relief="flat",
            padx=14,pady=5,cursor="hand2",activebackground="#2da44e",activeforeground="white",bd=0
        ).pack(side="left",padx=2)
        tk.Button(self.tb_inner,text="Reset View",command=self._reset_sim,
            font=F(9),bg="#21262d",fg="#c9d1d9",relief="flat",padx=10,pady=5,cursor="hand2",
            activebackground="#30363d",activeforeground="white",bd=0).pack(side="left",padx=2)
        tk.Button(self.tb_inner,text="Clear All",command=self._clear_all,
            font=F(9),bg="#3d1a1a",fg="#ffa198",relief="flat",padx=10,pady=5,cursor="hand2",
            activebackground="#5c2020",activeforeground="white",bd=0).pack(side="left",padx=2)

        sep()
        self.theme_btn=tk.Button(self.tb_inner,text="☀  Light Mode",command=self._toggle_theme,
            font=F(9,"bold"),bg="#21262d",fg="#e3b341",relief="flat",padx=10,pady=5,cursor="hand2",
            activebackground="#30363d",activeforeground="#f0c040",bd=0)
        self.theme_btn.pack(side="right",padx=2)

    def _tb_btn(self,text,cmd,color):
        return tk.Button(self.tb_inner,text=text,command=cmd,
            font=F(9,"bold"),bg="#21262d",fg="#c9d1d9",relief="flat",
            padx=11,pady=5,cursor="hand2",activebackground=color,activeforeground="white",bd=0)

    # ── Tab area 
    def _build_tab_area(self):
        T=self.T
        self.tab_strip=tk.Frame(self.left_frame,bg=T["bg_app"])
        self.tab_strip.pack(fill="x")
        self._all_frames.append(self.tab_strip)
        self.tab_content=tk.Frame(self.left_frame,bg=T["bg_app"])
        self.tab_content.pack(fill="both",expand=True)
        self._all_frames.append(self.tab_content)
        self.tab_btns={}; self.tab_frames={}

        for name,label in [("canvas","  ⬡  Wiring Canvas  "),("legend","  ⚡  Guide  ")]:
            f=tk.Frame(self.tab_content,bg=T["bg_canvas"],
                       highlightthickness=1,highlightbackground=T["border"])
            self.tab_frames[name]=f

        self._make_tab_btn("canvas","  ⬡  Wiring Canvas  ")
        self._make_tab_btn("legend","  ⚡  Component Guide  ")
        self._build_canvas_tab()
        self._build_legend_tab()
        self._switch_tab("canvas")

    def _make_tab_btn(self,name,label):
        b=tk.Button(self.tab_strip,text=label,font=F(10,"bold"),relief="flat",bd=0,
            padx=16,pady=8,cursor="hand2",command=lambda n=name:self._switch_tab(n))
        b.pack(side="left"); self.tab_btns[name]=b
        self._style_tab_btn(name,active=(name=="canvas"))

    def _style_tab_btn(self,name,active):
        T=self.T; b=self.tab_btns[name]
        b.configure(bg=T["bg_tab_on"] if active else T["bg_tab_off"],
                    fg=T["tx_pri"]    if active else T["tx_sec"])

    def _switch_tab(self,name):
        for n,f in self.tab_frames.items():
            f.pack_forget(); self._style_tab_btn(n,active=(n==name))
        self.tab_frames[name].pack(fill="both",expand=True)
        self.active_tab=name

    def _build_canvas_tab(self):
        f=self.tab_frames["canvas"]
        self.canvas=tk.Canvas(f,bg=self.T["bg_canvas"],highlightthickness=0,cursor="crosshair")
        self.canvas.pack(fill="both",expand=True,padx=1,pady=1)
        self.canvas.bind("<Button-1>",       self._on_click)
        self.canvas.bind("<B1-Motion>",      self._on_drag)
        self.canvas.bind("<ButtonRelease-1>",self._on_release)
        self.canvas.bind("<Motion>",         self._on_motion)
        self.canvas.bind("<Button-3>",       self._on_right_click)
        self.canvas.bind("<Configure>",      lambda e:(self._draw_grid(), self._draw_breaker_panel_bg()))
        self.root.bind("<Escape>",           self._on_escape)

    def _build_legend_tab(self):
        T=self.T; f=self.tab_frames["legend"]
        f.configure(bg=T["bg_canvas"])
        outer=tk.Frame(f,bg=T["bg_canvas"]); outer.pack(fill="both",expand=True,padx=20,pady=16)

        def section(title):
            tk.Label(outer,text=title,font=F(12,"bold"),bg=T["bg_canvas"],fg=T["tx_pri"]).pack(anchor="w",pady=(12,3))
            tk.Frame(outer,bg=T["border"],height=1).pack(fill="x",pady=(0,6))

        def row(label,detail,color=None):
            r=tk.Frame(outer,bg=T["bg_canvas"]); r.pack(fill="x",pady=2)
            if color:
                c=tk.Canvas(r,width=36,height=14,bg=T["bg_canvas"],highlightthickness=0)
                c.pack(side="left",padx=(0,10)); c.create_line(2,7,34,7,fill=color,width=4,capstyle="round")
            tk.Label(r,text=label,font=F(10,"bold"),bg=T["bg_canvas"],fg=T["tx_pri"]).pack(side="left")
            tk.Label(r,text="  "+detail,font=F(10),bg=T["bg_canvas"],fg=T["tx_sec"]).pack(side="left")

        section("Wire Colours")
        row("Hot / Live","Energised from panel",T["w_hot"])
        row("Neutral","Return path",T["w_neu"])
        row("Ground","Earth / safety",T["w_gnd"])
        row("Dead","No current",T["w_dead"])
        row("Unsimulated","Not tested yet",T["w_default"])

        section("Wire Drawing Tips")
        for tip in [
            "Left-click a terminal or junction to START a wire.",
            "Left-click a BREAKER to toggle ON/OFF.  Right-click to set its ampere rating.",
            "Left-click a BREAKER that is TRIPPED to reset it (reduce load first).",
            "Left-click the destination terminal to FINISH the wire — it auto-routes as an L-shape.",
            "RIGHT-CLICK anywhere while drawing to add a bend point and steer the wire manually.",
            "Left-click on an EXISTING wire to create a T-junction and branch from it.",
            "Junction dots (●) are draggable and act as full connection points.",
            "Right-click a switch (outside wire mode) to toggle it quickly.",
        ]:
            r=tk.Frame(outer,bg=T["bg_canvas"]); r.pack(fill="x",pady=2)
            tk.Label(r,text="→",font=F(11),bg=T["bg_canvas"],fg=T["w_gnd"]).pack(side="left",padx=(0,8))
            tk.Label(r,text=tip,font=F(10),bg=T["bg_canvas"],fg=T["tx_sec"],
                wraplength=500,justify="left").pack(side="left")

    # ── Info panel 
    def _build_info_panel(self):
        T=self.T; self._legend_items.clear()

        def card(title):
            outer=tk.Frame(self.right_frame,bg=T["bg_app"],pady=4); outer.pack(fill="x")
            self._all_frames.append(outer)
            tk.Label(outer,text=title,font=F(10,"bold"),bg=T["bg_app"],fg=T["tx_pri"]).pack(anchor="w")
            inner=tk.Frame(outer,bg=T["bg_card"],highlightthickness=1,
                           highlightbackground=T["border"],padx=12,pady=10)
            inner.pack(fill="x"); self._all_frames.append(inner); return inner

        lf=card("Wire Colour Legend")
        for ck,label in [("w_hot","Hot / Live (L)"),("w_neu","Neutral (N)"),
                         ("w_gnd","Ground (G)"),("w_dead","Dead / Open"),("w_default","Not simulated")]:
            row=tk.Frame(lf,bg=T["bg_card"]); row.pack(fill="x",pady=3)
            self._all_frames.append(row)
            c=tk.Canvas(row,width=46,height=12,bg=T["bg_card"],highlightthickness=0); c.pack(side="left")
            line=c.create_line(3,6,43,6,fill=T[ck],width=4,capstyle="round")
            lbl=tk.Label(row,text=label,font=F(10),bg=T["bg_card"],fg=T["tx_sec"]); lbl.pack(side="left",padx=(6,0))
            self._legend_items.append((c,line,ck,row,lbl))

        rf=card("Simulation Results")
        self.counter_row=tk.Frame(rf,bg=T["bg_card"]); self.counter_row.pack(fill="x",pady=(0,6))
        self._all_frames.append(self.counter_row)
        self.loads_lbl=tk.Label(self.counter_row,text="0 / 0  loads powered",
            font=F(12,"bold"),bg=T["bg_card"],fg=T["tx_sec"]); self.loads_lbl.pack(anchor="w")
        tk.Frame(rf,bg=T["border"],height=1).pack(fill="x",pady=(0,6))
        self.result_text=tk.Text(rf,width=30,height=14,font=F(10),bg=T["bg_app"],
            fg=T["tx_sec"],relief="flat",wrap="word",state="disabled",cursor="arrow",padx=4,pady=4)
        self.result_text.pack(fill="both")
        self.result_text.tag_configure("ok",  foreground="#3fb950",font=F(10,"bold"))
        self.result_text.tag_configure("err", foreground="#f85149",font=F(10,"bold"))
        self.result_text.tag_configure("warn",foreground="#e3b341",font=F(10))
        self.result_text.tag_configure("info",foreground="#8b949e",font=F(10))
        self.result_text.tag_configure("head",foreground=T["tx_pri"],font=F(11,"bold"))
        self._set_results([("Press  ⚡ Simulate\nto test your circuit.\n","info")])

    # ── Theme 
    def _toggle_theme(self):
        self.theme_name="light" if self.theme_name=="dark" else "dark"
        self.T=THEMES[self.theme_name]
        self.theme_btn.configure(
            text="☀  Light Mode" if self.theme_name=="dark" else "☾  Dark Mode",
            fg="#e3b341" if self.theme_name=="dark" else "#58a6ff")
        self._apply_theme()

    def _apply_theme(self):
        T=self.T
        self.root.configure(bg=T["bg_app"])
        self.toolbar.configure(bg=T["bg_tb"]); self.tb_inner.configure(bg=T["bg_tb"])
        for f in self._all_frames:
            try: f.configure(bg=T["bg_app"])
            except: pass
        self.canvas.configure(bg=T["bg_canvas"])
        for n,f in self.tab_frames.items():
            f.configure(bg=T["bg_canvas"],highlightbackground=T["border"])
        self.tab_strip.configure(bg=T["bg_app"]); self.tab_content.configure(bg=T["bg_app"])
        for n in self.tab_btns: self._style_tab_btn(n,active=(n==self.active_tab))
        self.status_bar.configure(bg=T["st_bg"],fg=T["st_fg"])
        for c_w,line_id,ck,row,lbl in self._legend_items:
            c_w.configure(bg=T["bg_card"]); c_w.itemconfig(line_id,fill=T[ck])
            row.configure(bg=T["bg_card"]); lbl.configure(bg=T["bg_card"],fg=T["tx_sec"])
        self.counter_row.configure(bg=T["bg_card"])
        self.loads_lbl.configure(bg=T["bg_card"],fg=T["tx_sec"])
        self.result_text.configure(bg=T["bg_app"],fg=T["tx_sec"])
        self.result_text.tag_configure("ok",  foreground="#3fb950")
        self.result_text.tag_configure("err", foreground="#f85149")
        self.result_text.tag_configure("warn",foreground="#e3b341")
        self.result_text.tag_configure("info",foreground=T["tx_sec"])
        self.result_text.tag_configure("head",foreground=T["tx_pri"])
        f=self.tab_frames["legend"]
        for w in f.winfo_children(): w.destroy()
        self._build_legend_tab()
        self._draw_grid()
        self._draw_breaker_panel_bg()
        for comp in self.components.values(): self._redraw_comp(comp)
        for w in self.wires: self._draw_wire(w)
        for j in self.junctions.values(): self._draw_junction(j)

    # ── Grid 
    def _draw_grid(self):
        self.canvas.delete("grid")
        W=self.canvas.winfo_width() or 900
        H=self.canvas.winfo_height() or 640
        for x in range(0,W+GRID,GRID): self.canvas.create_line(x,0,x,H,fill=self.T["grid"],tags="grid")
        for y in range(0,H+GRID,GRID): self.canvas.create_line(0,y,W,y,fill=self.T["grid"],tags="grid")
        self.canvas.tag_lower("grid")

    # ── Place breaker panel area + ground bus 
    def _place_panel(self):
        P=EIMSimulator
        self._draw_breaker_panel_bg()
        # Hot bus — centred on left strip
        hb=Component("hot_bus",(P.BUS_L_X1+P.BUS_L_X2)//2,(P.BUS_Y1+P.BUS_Y2)//2)
        self.components[hb.id]=hb; self._redraw_comp(hb)
        # Neutral bus — centred on right strip
        nb=Component("neu_bus",(P.BUS_R_X1+P.BUS_R_X2)//2,(P.BUS_Y1+P.BUS_Y2)//2)
        self.components[nb.id]=nb; self._redraw_comp(nb)
        # Ground bus bar — centred in ground section
        g=Component("gnd_bus",(P.PNL_X1+P.PNL_X2)//2,(P.GND_Y1+P.GND_Y2)//2)
        self.components[g.id]=g; self._redraw_comp(g)

    # Panel layout constants — used here and for breaker snapping/ still flawed btw needs fixing
    PNL_X1, PNL_X2 = 20, 340        # enclosure left/right
    PNL_Y1, PNL_Y2 = 20, 720        # enclosure top/bottom
    PNL_TITLE_H    = 34              # height of title bar
    BUS_L_X1,BUS_L_X2 = 28, 52      # hot bus strip x range
    BUS_R_X1,BUS_R_X2 = 308, 332    # neutral bus strip x range
    BUS_Y1, BUS_Y2 = 60, 590        # bus bars top/bottom
    GND_Y1, GND_Y2 = 600, 715       # ground bus section
    SLOT_X1,SLOT_X2= 58, 302        # breaker slot area
    SLOT_Y_START   = 68              # y of first slot top
    SLOT_H         = 96              # height per slot (breaker h=90 + 6 gap)
    N_SLOTS        = 5

    def _draw_breaker_panel_bg(self):
        """Draw the distribution board enclosure — single pass, no duplicates."""
        T=self.T
        self.canvas.delete("panel_bg")
        P=EIMSimulator  # access class-level layout constants

        # ── Outer enclosure 
        self.canvas.create_rectangle(P.PNL_X1,P.PNL_Y1,P.PNL_X2,P.PNL_Y2,
            fill=T["p_body"],outline=T["p_rim"],width=3,tags="panel_bg")

        # ── Title bar 
        ty2=P.PNL_Y1+P.PNL_TITLE_H
        self.canvas.create_rectangle(P.PNL_X1,P.PNL_Y1,P.PNL_X2,ty2,
            fill=T["p_hot_bg"],outline="",tags="panel_bg")
        self.canvas.create_text((P.PNL_X1+P.PNL_X2)//2, P.PNL_Y1+P.PNL_TITLE_H//2,
            text="DISTRIBUTION BOARD",
            font=F(9,"bold"),fill="#e6edf3",tags="panel_bg")

        # ── Hot bus strip (left) — decorative only, no label 
        self.canvas.create_rectangle(P.BUS_L_X1,P.BUS_Y1,P.BUS_L_X2,P.BUS_Y2,
            fill=T["p_hot_bg"],outline=T["p_hot_rim"],width=1,tags="panel_bg")

        # ── Neutral bus strip (right) — decorative only 
        self.canvas.create_rectangle(P.BUS_R_X1,P.BUS_Y1,P.BUS_R_X2,P.BUS_Y2,
            fill=T["p_neu_bg"],outline=T["p_neu_rim"],width=1,tags="panel_bg")

        # ── Breaker slot guides 
        for i in range(P.N_SLOTS):
            sy=P.SLOT_Y_START+i*P.SLOT_H
            self.canvas.create_rectangle(P.SLOT_X1,sy,P.SLOT_X2,sy+P.SLOT_H-6,
                fill="",outline=T["tx_muted"],width=1,dash=(5,4),tags="panel_bg")
            self.canvas.create_text(P.SLOT_X1+8, sy+8,
                text=f"S{i+1}",font=F(7),fill=T["tx_muted"],anchor="nw",tags="panel_bg")

        # ── Ground bus section (fix this boi!!)
        self.canvas.create_rectangle(P.PNL_X1+4,P.GND_Y1,P.PNL_X2-4,P.GND_Y2,
            fill=T["p_gnd_bg"],outline=T["p_gnd_rim"],width=1,tags="panel_bg")
        self.canvas.create_text(P.PNL_X1+22, P.GND_Y1+10,
            text="⏚  GROUND BUS",font=F(8,"bold"),fill=T["p_gnd_rim"],
            anchor="nw",tags="panel_bg")

        self.canvas.tag_lower("panel_bg")
        self.canvas.tag_lower("grid")

    def _snap_to_slot(self,x,y):
        """If placing a breaker, snap it to the nearest free slot in the panel."""
        P=EIMSimulator
        cx=(P.SLOT_X1+P.SLOT_X2)//2   # horizontal centre of slots = 180
        # Only snap if user clicked inside the panel area
        if not (P.PNL_X1<=x<=P.PNL_X2 and P.BUS_Y1<=y<=P.BUS_Y2):
            return x,y
        # Find closest slot centre
        best_y,best_d=y,9999
        for i in range(P.N_SLOTS):
            sy=P.SLOT_Y_START+i*P.SLOT_H+(P.SLOT_H-6)//2
            d=abs(y-sy)
            if d<best_d: best_d,best_y=d,sy
        return cx,best_y

    def _add_component(self,ctype,x,y):
        if ctype=="breaker": x,y=self._snap_to_slot(x,y)
        c=Component(ctype,x,y); self.components[c.id]=c
        self._redraw_comp(c); self._invalidate_sim(); return c

    
    #  DRAWING
    def _redraw_comp(self,comp):
        tag=f"c{comp.id}"; self.canvas.delete(tag)
        getattr(self,f"_draw_{comp.type}")(comp,tag)
        self._draw_terminals(comp,tag)
        self.canvas.tag_raise(tag); self.canvas.tag_lower("grid")

    # ── Hot bus bar — no body drawn, background already shows the strip
    def _draw_hot_bus(self,c,tag):
        pass   # terminals drawn by _draw_terminals

    def _draw_neu_bus(self,c,tag):
        pass   # terminals drawn by _draw_terminals

    # ── Breaker 
    def _draw_breaker(self,c,tag):
        T=self.T; x,y,hw,hh=c.x,c.y,c.w//2,c.h//2
        on=c.state.get("on",True)
        tripped=c.state.get("tripped",False)
        amps=c.state.get("amps",20)
        load_a=c.state.get("load_amps",0.0)
        # Body colour
        if tripped:
            bg="#3d0a00"; rim="#f85149"
        elif on:
            bg=T["sw_on_bg"]; rim=T["sw_on_rim"]
        else:
            bg=T["sw_off_bg"]; rim=T["sw_off_rim"]
        # Shadow
        self.canvas.create_rectangle(x-hw+2,y-hh+2,x+hw+2,y+hh+2,
            fill=T["bg_app"],outline="",tags=tag)
        # Body
        self.canvas.create_rectangle(x-hw,y-hh,x+hw,y+hh,
            fill=bg,outline=rim,width=2,tags=tag)
        # Top label band
        self.canvas.create_rectangle(x-hw,y-hh,x+hw,y-hh+18,
            fill=rim,outline="",tags=tag)
        self.canvas.create_text(x,y-hh+9,text=f"CB  {amps}A",
            font=F(8,"bold"),fill=T["bg_app"],tags=tag)
        # IN / OUT side labels
        self.canvas.create_text(x,y-hh+26,text="◀ IN",
            font=F(7),fill=T["tx_muted"],tags=tag)
        self.canvas.create_text(x,y+hh-10,text="OUT ▶",
            font=F(7),fill=T["tx_muted"],tags=tag)
        # Toggle rocker symbol
        if tripped:
            self.canvas.create_text(x,y-8,text="TRIPPED",font=F(9,"bold"),fill="#f85149",tags=tag)
            self.canvas.create_text(x,y+8,text="⚡ OVERLOAD",font=F(8),fill="#f0883e",tags=tag)
        elif on:
            # Rocker in ON position (right side down)
            self.canvas.create_rectangle(x-14,y-22,x+14,y+22,
                fill=T["sw_on_rim"],outline="",tags=tag)
            self.canvas.create_rectangle(x+2,y-20,x+12,y+4,
                fill=T["bg_app"],outline="",tags=tag)
            self.canvas.create_text(x-5,y+8,text="ON",font=F(9,"bold"),fill=T["bg_app"],tags=tag)
        else:
            self.canvas.create_rectangle(x-14,y-22,x+14,y+22,
                fill=T["sw_off_rim"],outline="",tags=tag)
            self.canvas.create_rectangle(x-12,y-4,x-2,y+20,
                fill=T["bg_app"],outline="",tags=tag)
            self.canvas.create_text(x+4,y-8,text="OFF",font=F(9,"bold"),fill=T["bg_app"],tags=tag)
        # Load bar at bottom
        if on and not tripped and load_a>0:
            rated=amps; pct=min(load_a/rated,1.0)
            bar_w=int((hw*2-8)*pct)
            bar_col="#3fb950" if pct<0.8 else ("#e3b341" if pct<1.0 else "#f85149")
            self.canvas.create_rectangle(x-hw+4,y+hh-10,x+hw-4,y+hh-4,
                fill=T["bg_app"],outline=T["border"],width=1,tags=tag)
            self.canvas.create_rectangle(x-hw+4,y+hh-10,x-hw+4+bar_w,y+hh-4,
                fill=bar_col,outline="",tags=tag)
            self.canvas.create_text(x,y+hh+10,text=f"{load_a:.1f}A / {amps}A",
                font=F(8),fill=T["tx_sec"],tags=tag)

    def _draw_gnd_bus(self,c,tag):
        T=self.T; x,y,hw,hh=c.x,c.y,c.w//2,c.h//2
        # Body — single rectangle, no duplicate
        self.canvas.create_rectangle(x-hw,y-hh,x+hw,y+hh,
            fill=T["p_gnd_bg"],outline=T["p_gnd_rim"],width=2,tags=tag)
        # Copper bus bar strip
        self.canvas.create_rectangle(x-hw+6,y-5,x+hw-6,y+5,
            fill="#92400e",outline="#78350f",width=1,tags=tag)
        # ⏚ symbol
        self.canvas.create_text(x-hw+16,y,text="⏚",
            font=F(10,"bold"),fill=T["p_gnd_rim"],tags=tag)
        # Terminal labels drawn inline (skip — _draw_terminals handles dots;
        # add small text labels beside each terminal)
        for i,t in enumerate(c.terminals):
            tx,ty=c.x+t.rx,c.y+t.ry
            oy=-14 if i==0 else 14
            self.canvas.create_text(tx,ty+oy,text=t.label,
                font=F(7,"bold"),fill=T["tx_sec"],tags=tag)

    # ── Switch 
    def _draw_switch(self,c,tag):
        T=self.T; x,y,hw,hh=c.x,c.y,c.w//2,c.h//2
        closed=c.state.get("closed",False)
        bg=T["sw_on_bg"] if closed else T["sw_off_bg"]
        rim=T["sw_on_rim"] if closed else T["sw_off_rim"]
        self.canvas.create_rectangle(x-hw,y-hh,x+hw,y+hh,fill=bg,outline=rim,width=2,tags=tag)
        self.canvas.create_text(x,y-8,text="SWITCH",font=F(9,"bold"),fill=T["tx_pri"],tags=tag)
        self.canvas.create_text(x,y+8,text="CLOSED ●" if closed else "OPEN ○",font=F(9,"bold"),fill=rim,tags=tag)
        t0x=c.x+c.terminals[0].rx; t1x=c.x+c.terminals[1].rx
        if closed: self.canvas.create_line(t0x+TR,y,t1x-TR,y,fill=rim,width=2.5,tags=tag)
        else:      self.canvas.create_line(t0x+TR,y,x,y-14,fill=rim,width=2.5,tags=tag)

    def _draw_switch3(self,c,tag):
        T=self.T; x,y,hw,hh=c.x,c.y,c.w//2,c.h//2; pos=c.state.get("pos",0)
        self.canvas.create_rectangle(x-hw,y-hh,x+hw,y+hh,fill=T["sw3_bg"],outline=T["sw3_rim"],width=2,tags=tag)
        self.canvas.create_text(x-4,y-9,text="3-WAY",font=F(9,"bold"),fill=T["tx_pri"],tags=tag)
        self.canvas.create_text(x-2,y+9,text=f"→ T{pos+1}",font=F(9,"bold"),fill=T["sw3_rim"],tags=tag)
        cx,cy=c.x+c.terminals[0].rx,c.y+c.terminals[0].ry
        ax,ay=c.x+c.terminals[1+pos].rx,c.y+c.terminals[1+pos].ry
        self.canvas.create_line(cx+TR,cy,ax-TR,ay,fill=T["sw3_rim"],width=2.5,tags=tag)
        for i,lbl in enumerate(["COM","T1","T2"]):
            tx,ty=c.x+c.terminals[i].rx,c.y+c.terminals[i].ry
            dx=-20 if i==0 else 20
            self.canvas.create_text(tx+dx,ty,text=lbl,font=F(8),fill=T["tx_sec"],tags=tag)

    def _draw_switch4(self,c,tag):
        T=self.T; x,y,hw,hh=c.x,c.y,c.w//2,c.h//2; cross=c.state.get("cross",False)
        self.canvas.create_rectangle(x-hw,y-hh,x+hw,y+hh,fill=T["sw4_bg"],outline=T["sw4_rim"],width=2,tags=tag)
        self.canvas.create_text(x,y-9,text="4-WAY",font=F(9,"bold"),fill=T["tx_pri"],tags=tag)
        self.canvas.create_text(x,y+9,text="CROSSED" if cross else "STRAIGHT",font=F(9,"bold"),fill=T["sw4_rim"],tags=tag)
        pts=[(c.x+c.terminals[i].rx,c.y+c.terminals[i].ry) for i in range(4)]
        if not cross:
            self.canvas.create_line(pts[0][0]+TR,pts[0][1],pts[2][0]-TR,pts[2][1],fill=T["sw4_rim"],width=2.5,tags=tag)
            self.canvas.create_line(pts[1][0]+TR,pts[1][1],pts[3][0]-TR,pts[3][1],fill=T["sw4_rim"],width=2.5,tags=tag)
        else:
            self.canvas.create_line(pts[0][0]+TR,pts[0][1],pts[3][0]-TR,pts[3][1],fill=T["sw4_rim"],width=2.5,tags=tag)
            self.canvas.create_line(pts[1][0]+TR,pts[1][1],pts[2][0]-TR,pts[2][1],fill=T["sw4_rim"],width=2.5,tags=tag)
        for i,lbl in enumerate(["L1","L2","R1","R2"]):
            tx,ty=c.x+c.terminals[i].rx,c.y+c.terminals[i].ry
            dx=-16 if i<2 else 16
            self.canvas.create_text(tx+dx,ty,text=lbl,font=F(8),fill=T["tx_sec"],tags=tag)

    def _draw_bulb(self,c,tag):
        T=self.T; x,y,r=c.x,c.y,24; on=c.state.get("on",False)
        bg=T["bl_on_bg"] if on else T["bl_off_bg"]; rim=T["bl_on_rim"] if on else T["bl_off_rim"]
        if on:
            for gr in [r+14,r+8]:
                self.canvas.create_oval(x-gr,y-gr,x+gr,y+gr,fill=T["bl_glow"],outline="",tags=tag)
        self.canvas.create_oval(x-r,y-r,x+r,y+r,fill=bg,outline=rim,width=2,tags=tag)
        d=10
        self.canvas.create_line(x-d,y-d,x+d,y+d,fill=rim,width=1.5,tags=tag)
        self.canvas.create_line(x+d,y-d,x-d,y+d,fill=rim,width=1.5,tags=tag)
        self.canvas.create_text(x,y+r+13,text="BULB",font=F(9,"bold"),fill=T["tx_sec"],tags=tag)
        if on: self.canvas.create_text(x,y+r+25,text="ON ★",font=F(9,"bold"),fill=T["bl_on_rim"],tags=tag)

    def _draw_outlet(self,c,tag):
        T=self.T; x,y,hw,hh=c.x,c.y,c.w//2,c.h//2; on=c.state.get("on",False)
        bg=T["ou_on_bg"] if on else T["ou_off_bg"]; rim=T["ou_on_rim"] if on else T["ou_off_rim"]
        self.canvas.create_rectangle(x-hw,y-hh,x+hw,y+hh,fill=bg,outline=rim,width=2,tags=tag)
        for sx in [x-12,x+3]:
            self.canvas.create_rectangle(sx,y-10,sx+8,y+5,fill=T["ou_pin"] if on else T["border"],outline=T["tx_muted"],width=1,tags=tag)
        self.canvas.create_oval(x-5,y+8,x+5,y+18,fill=T["w_gnd"] if on else T["border"],outline=T["tx_muted"],width=1,tags=tag)
        self.canvas.create_text(x,y-hh-11,text="OUTLET",font=F(9,"bold"),fill=T["tx_sec"],tags=tag)
        if on: self.canvas.create_text(x,y+hh+11,text="LIVE",font=F(9,"bold"),fill=T["ou_on_rim"],tags=tag)

    def _draw_spoutlet(self,c,tag):
        T=self.T; x,y,hw,hh=c.x,c.y,c.w//2,c.h//2
        on=c.state.get("on",False); gnd=c.state.get("grounded",False)
        bg=T["sp_on_bg"] if on else T["sp_off_bg"]; rim=T["sp_on_rim"] if on else T["sp_off_rim"]
        self.canvas.create_rectangle(x-hw,y-hh,x+hw,y+hh,fill=bg,outline=rim,width=2,tags=tag)
        for sx in [x-14,x+3]:
            self.canvas.create_rectangle(sx,y-17,sx+9,y-3,fill=T["sp_hot_pin"] if on else T["border"],outline=T["tx_muted"],width=1,tags=tag)
        gc=T["sp_gnd_pin"] if gnd else T["border"]
        self.canvas.create_oval(x-7,y+5,x+7,y+19,fill=gc,outline=T["tx_muted"],width=1,tags=tag)
        self.canvas.create_text(x,y-hh-11,text="SP OUTLET",font=F(9,"bold"),fill=T["sp_on_rim"] if on else T["tx_sec"],tags=tag)
        if on:
            self.canvas.create_text(x,y+hh+11,text="LIVE + GND" if gnd else "LIVE",
                font=F(9,"bold"),fill=T["sp_gnd_pin"] if gnd else T["sp_on_rim"],tags=tag)
        elif gnd:
            self.canvas.create_text(x,y+hh+11,text="GND only",font=F(9),fill=T["w_gnd"],tags=tag)

    def _draw_terminals(self,comp,tag):
        T=self.T
        for i,t in enumerate(comp.terminals):
            tx,ty=comp.x+t.rx,comp.y+t.ry; tid=t.tid
            if   self.wire_ep1 and self._ep_is((comp.id,i)): color=T["t_act"]
            elif self.hov_term==(comp.id,i): color=T["t_hov"]
            elif self.sim_done:
                if   tid in self.hot_set:  color=T["t_hot"]
                elif tid in self.neut_set: color=T["t_neu"]
                elif tid in self.gnd_set:  color=T["t_gnd"]
                else:                      color=T["t_def"]
            elif comp.type=="panel":
                color=T["t_hot"] if i<3 else (T["t_neu"] if i<6 else T["t_gnd"])
            else: color=T["t_def"]
            self.canvas.create_oval(tx-TR,ty-TR,tx+TR,ty+TR,fill=color,outline=T["bg_canvas"],width=2,
                tags=(tag,f"trm_{comp.id}_{i}"))
            if comp.type not in ("panel",) and t.label:
                ox=(-14 if t.rx<0 else 14) if t.rx!=0 else 14
                oy=(-14 if t.ry<0 else 14) if t.ry!=0 else 0
                self.canvas.create_text(tx+ox,ty+oy,text=t.label,font=F(8),fill=T["tx_muted"],tags=tag)

    def _ep_is(self,tid):
        """True if the first wire endpoint matches this terminal id."""
        return self.wire_ep1==tid

    # ── Junction ─────────────────────────────────────────────────
    def _draw_junction(self,j):
        T=self.T
        if j.item: self.canvas.delete(j.item)
        color=T["t_hov"] if self.hov_junc==j.id else T["j_dot"]
        j.item=self.canvas.create_oval(j.x-JR,j.y-JR,j.x+JR,j.y+JR,
            fill=color,outline=T["j_rim"],width=1.5,tags=f"junc_{j.id}")
        self.canvas.tag_raise(f"junc_{j.id}")

    def _place_junction_on_wire(self,wire,px,py):
        """
        Split 'wire' into two wires at point (px,py) and insert a Junction there.
        Returns the new Junction.
        """
        j=Junction(px,py); self.junctions[j.id]=j

        # Find which segment of the wire (px,py) is closest to, and split points there
        best_seg=0; best_d=1e9
        for si,((x1,y1),(x2,y2)) in enumerate(wire.segments()):
            d=pt_seg_dist(px,py,x1,y1,x2,y2)
            if d<best_d: best_d=d; best_seg=si

        split_pt=(snap(px),snap(py))
        pts_a=wire.points[:best_seg+1]+[split_pt]
        pts_b=[split_pt]+wire.points[best_seg+1:]

        # Remove old wire canvas items
        for it in wire.items: self.canvas.delete(it)
        self.wires.remove(wire)

        # Create two new wires
        wa=Wire(wire.from_tid,j.tid,pts_a); self.wires.append(wa); self._draw_wire(wa)
        wb=Wire(j.tid,wire.to_tid,pts_b);  self.wires.append(wb); self._draw_wire(wb)

        self._draw_junction(j)
        return j

    # ── Wire drawing ─────────────────────────────────────────────
    def _draw_wire(self,wire):
        T=self.T
        for it in wire.items: self.canvas.delete(it)
        wire.items=[]
        color=self._wire_color(wire)
        pts=wire.points
        if len(pts)<2: return
        for i in range(len(pts)-1):
            x1,y1=pts[i]; x2,y2=pts[i+1]
            it=self.canvas.create_line(x1,y1,x2,y2,fill=color,width=3,
                capstyle="round",joinstyle="round",tags=f"w{wire.id}")
            wire.items.append(it)
        self.canvas.tag_lower(f"w{wire.id}")
        self.canvas.tag_lower("grid")

    def _wire_color(self,wire):
        T=self.T
        if not self.sim_done: return T["w_default"]
        fh=wire.from_tid in self.hot_set; fn=wire.from_tid in self.neut_set; fg=wire.from_tid in self.gnd_set
        th=wire.to_tid   in self.hot_set; tn=wire.to_tid   in self.neut_set; tg=wire.to_tid   in self.gnd_set
        if (fh and tn) or (fn and th): return T["w_short"]
        if fh and th: return T["w_hot"]
        if fn and tn: return T["w_neu"]
        if fg and tg: return T["w_gnd"]
        return T["w_dead"]

    def _redraw_wires_for_comp(self,comp):
        for w in self.wires:
            if (isinstance(w.from_tid,tuple) and len(w.from_tid)==2 and w.from_tid[0]==comp.id) or \
               (isinstance(w.to_tid,  tuple) and len(w.to_tid  )==2 and w.to_tid[0]  ==comp.id):
                self._draw_wire(w)

    def _redraw_wires_for_junc(self,j):
        for w in self.wires:
            if w.from_tid==j.tid or w.to_tid==j.tid:
                self._draw_wire(w)

    # ── Preview rubber-band ───────────────────────────────────────
    def _clear_preview(self):
        for it in self.preview_items: self.canvas.delete(it)
        self.preview_items=[]

    def _draw_preview(self,mx,my):
        T=self.T; self._clear_preview()
        if not self.wire_ep1: return
        sx,sy=self.wire_ep1_xy

        # Collect all anchor points so far
        all_pts=[(sx,sy)]+list(self.wire_user_pts)+[(snap(mx),snap(my))]

        # Draw each sub-segment as L-route
        for i in range(len(all_pts)-1):
            ax,ay=all_pts[i]; bx,by=all_pts[i+1]
            route=l_route(ax,ay,bx,by,"h")
            for j in range(len(route)-1):
                x1,y1=route[j]; x2,y2=route[j+1]
                it=self.canvas.create_line(x1,y1,x2,y2,
                    fill=T["t_act"],width=2,dash=(8,4),tags="wire_prev")
                self.preview_items.append(it)
        self.canvas.tag_raise("wire_prev")

    # ── Endpoint resolution ───────────────────────────────────────
    def _ep_xy(self,ep):
        """Return (x,y) for an endpoint tid — could be a component terminal or junction."""
        if isinstance(ep,tuple) and ep[0]=="J":
            j=self.junctions.get(ep[1]); return (j.x,j.y) if j else (0,0)
        cid,tidx=ep; c=self.components.get(cid)
        return c.abs_term(tidx) if c else (0,0)

    # ════════════════════════════════════════════════════════════════
    #  CANVAS EVENTS
    # ════════════════════════════════════════════════════════════════
    def _on_click(self,event):
        mx,my=event.x,event.y

        # ── 1. Terminal hit? ──────────────────────────────────────
        th=self._find_terminal(mx,my)
        if th:
            cid,tidx=th
            if self.mode=="wire":
                if self.wire_ep1 is None:
                    self._start_wire((cid,tidx))
                else:
                    self._finish_wire((cid,tidx))
            return

        # ── 2. Junction hit? ─────────────────────────────────────
        jh=self._find_junction(mx,my)
        if jh:
            j=self.junctions[jh]
            if self.mode=="wire":
                if self.wire_ep1 is None:
                    self._start_wire(j.tid,x=j.x,y=j.y)
                else:
                    self._finish_wire(j.tid)
            elif self.mode=="delete":
                self._delete_junction(j)
            return

        # ── 3. Existing wire hit? ─────────────────────────────────
        wh=self._find_wire(mx,my)
        if wh:
            if self.mode=="wire":
                # Tap into wire → place junction, then start new wire from it
                cx,cy=closest_point_on_seg(mx,my,*self._wire_hit_seg(wh,mx,my))
                j=self._place_junction_on_wire(wh,cx,cy)
                self._invalidate_sim()
                if self.wire_ep1 is None:
                    self._start_wire(j.tid,x=j.x,y=j.y)
                else:
                    self._finish_wire(j.tid)
            elif self.mode=="delete":
                self._delete_wire(wh)
            return

        # ── 4. Component body hit? ────────────────────────────────
        comp=self._find_comp(mx,my)
        if comp:
            FIXED=("gnd_bus","hot_bus","neu_bus")
            if self.mode=="delete" and comp.type not in FIXED:
                self._delete_comp(comp); return
            if self.mode=="select":
                if comp.type in ("switch","switch3","switch4"):
                    self._toggle_switch(comp); return
                if comp.type=="breaker":
                    self._toggle_breaker(comp); return
                if comp.type not in ("hot_bus","neu_bus","gnd_bus"):
                    self.drag_comp=comp; self.drag_off=(mx-comp.x,my-comp.y)
            return

        # ── 5. Empty canvas ───────────────────────────────────────
        if self.mode.startswith("place_"):
            self._add_component(self.mode[6:],snap(mx),snap(my))
        elif self.mode=="wire":
            if self.wire_ep1 is not None:
                self._cancel_wire()

    def _toggle_switch(self,comp):
        if   comp.type=="switch":  comp.state["closed"]=not comp.state["closed"]
        elif comp.type=="switch3": comp.state["pos"]=1-comp.state["pos"]
        elif comp.type=="switch4": comp.state["cross"]=not comp.state["cross"]
        self._redraw_comp(comp)
        if self.sim_done: self._run_sim()

    def _toggle_breaker(self,comp):
        """Toggle breaker ON/OFF; if tripped, reset trip first."""
        if comp.state["tripped"]:
            comp.state["tripped"]=False
            comp.state["load_amps"]=0.0
            self._set_status(f"Breaker #{comp.id} trip reset. Toggle again to turn OFF.")
        else:
            comp.state["on"]=not comp.state["on"]
        self._redraw_comp(comp)
        if self.sim_done: self._run_sim()

    def _set_breaker_amps(self,comp):
        """Show a small dialog to change the breaker ampere rating."""
        RATINGS=[6,10,15,20,30,40,50,60,100]
        dlg=tk.Toplevel(self.root)
        dlg.title(f"Breaker #{comp.id} — Set Rating")
        dlg.geometry("260x220")
        dlg.resizable(False,False)
        dlg.configure(bg=self.T["bg_card"])
        dlg.grab_set()
        tk.Label(dlg,text="Select Ampere Rating:",font=F(11,"bold"),
            bg=self.T["bg_card"],fg=self.T["tx_pri"]).pack(pady=(16,8))
        var=tk.IntVar(value=comp.state["amps"])
        frame=tk.Frame(dlg,bg=self.T["bg_card"]); frame.pack()
        cols=3
        for i,r in enumerate(RATINGS):
            rb=tk.Radiobutton(frame,text=f"{r}A",variable=var,value=r,
                font=F(10,"bold"),bg=self.T["bg_card"],fg=self.T["tx_pri"],
                selectcolor=self.T["bg_app"],activebackground=self.T["bg_card"],
                indicatoron=False,width=4,padx=6,pady=4,relief="flat",
                bd=1,highlightthickness=1)
            rb.grid(row=i//cols,column=i%cols,padx=4,pady=3)
        def apply():
            comp.state["amps"]=var.get()
            comp.state["tripped"]=False
            comp.state["load_amps"]=0.0
            self._redraw_comp(comp)
            if self.sim_done: self._run_sim()
            dlg.destroy()
        tk.Button(dlg,text="Apply",command=apply,
            font=F(10,"bold"),bg="#1a7f37",fg="white",
            relief="flat",padx=20,pady=6,cursor="hand2").pack(pady=12)

    def _on_drag(self,event):
        if self.drag_comp:
            cw=self.canvas.winfo_width(); ch=self.canvas.winfo_height()
            hw=self.drag_comp.w//2; hh=self.drag_comp.h//2
            nx=max(hw,min(cw-hw,snap(event.x-self.drag_off[0])))
            ny=max(hh,min(ch-hh,snap(event.y-self.drag_off[1])))
            self.drag_comp.x=nx; self.drag_comp.y=ny
            self._redraw_comp(self.drag_comp)
            self._update_wires_for_comp(self.drag_comp)

        if self.drag_junc:
            j=self.drag_junc
            j.x=snap(event.x); j.y=snap(event.y)
            self._draw_junction(j)
            self._update_wires_for_junc(j)

    def _on_release(self,event):
        self.drag_comp=None; self.drag_off=(0,0); self.drag_junc=None

    def _on_motion(self,event):
        mx,my=event.x,event.y

        # Update terminal hover
        new_hov=self._find_terminal(mx,my)
        if new_hov!=self.hov_term:
            old=self.hov_term[0] if self.hov_term else None
            new=new_hov[0]       if new_hov       else None
            self.hov_term=new_hov
            for cid in set(filter(None,[old,new])):
                c=self.components.get(cid)
                if c: self._redraw_comp(c)

        # Update junction hover
        new_jh=self._find_junction(mx,my)
        if new_jh!=self.hov_junc:
            old_jid=self.hov_junc; self.hov_junc=new_jh
            for jid in set(filter(None,[old_jid,new_jh])):
                j=self.junctions.get(jid)
                if j: self._draw_junction(j)

        # Update wire preview
        if self.mode=="wire" and self.wire_ep1:
            self._draw_preview(mx,my)

    def _on_right_click(self,event):
        mx,my=event.x,event.y
        # While drawing a wire: right-click adds a bend point
        if self.mode=="wire" and self.wire_ep1 is not None:
            self.wire_user_pts.append((snap(mx),snap(my)))
            n=len(self.wire_user_pts)
            self._set_status(f"Bend point {n} added.  Right-click to add more.  Left-click a terminal to finish.  Esc to cancel.")
            self._draw_preview(mx,my)
            return
        # Otherwise: right-click toggles a switch / opens breaker rating
        comp=self._find_comp(mx,my)
        if comp and comp.type in ("switch","switch3","switch4"):
            self._toggle_switch(comp)
        elif comp and comp.type=="breaker":
            self._set_breaker_amps(comp)

    def _on_escape(self,event=None):
        self._cancel_wire(); self._set_mode("select")

    # ── Wire endpoint management ──────────────────────────────────
    def _start_wire(self,ep,x=None,y=None):
        self.wire_ep1=ep
        self.wire_user_pts=[]
        if x is None or y is None:
            self.wire_ep1_xy=self._ep_xy(ep)
        else:
            self.wire_ep1_xy=(x,y)
        if isinstance(ep,tuple) and ep[0]!="J":
            c=self.components.get(ep[0])
            if c: self._redraw_comp(c)
        self._set_status("Wire started.  Left-click a terminal to finish.  Right-click to add bend points.  Esc to cancel.")

    def _finish_wire(self,ep2):
        ep1=self.wire_ep1
        if ep1==ep2 or self._wire_exists(ep1,ep2):
            self._cancel_wire(); return

        sx,sy=self.wire_ep1_xy
        ex,ey=self._ep_xy(ep2)
        pts=build_routed_path(sx,sy,ex,ey,self.wire_user_pts)

        w=Wire(ep1,ep2,pts); self.wires.append(w)
        self._draw_wire(w); self._invalidate_sim()
        self._cancel_wire()

    def _cancel_wire(self):
        old_ep=self.wire_ep1
        self.wire_ep1=None; self.wire_ep1_xy=None; self.wire_user_pts=[]
        self._clear_preview()
        if old_ep and isinstance(old_ep,tuple) and old_ep[0]!="J":
            c=self.components.get(old_ep[0])
            if c: self._redraw_comp(c)

    def _wire_exists(self,t1,t2):
        return any((w.from_tid==t1 and w.to_tid==t2) or
                   (w.from_tid==t2 and w.to_tid==t1) for w in self.wires)

    # ── Wire update after drag ────────────────────────────────────
    def _update_wires_for_comp(self,comp):
        """Recompute wire endpoints that touch this component's terminals."""
        for w in self.wires:
            changed=False
            for i,t in enumerate(comp.terminals):
                if w.from_tid==(comp.id,i):
                    nx,ny=comp.abs_term(i)
                    w.points[0]=(nx,ny); changed=True
                if w.to_tid==(comp.id,i):
                    nx,ny=comp.abs_term(i)
                    w.points[-1]=(nx,ny); changed=True
            if changed: self._draw_wire(w)

    def _update_wires_for_junc(self,j):
        for w in self.wires:
            changed=False
            if w.from_tid==j.tid:
                w.points[0]=(j.x,j.y); changed=True
            if w.to_tid==j.tid:
                w.points[-1]=(j.x,j.y); changed=True
            if changed: self._draw_wire(w)

    # ── Delete helpers ────────────────────────────────────────────
    def _delete_comp(self,comp):
        to_del=[w for w in self.wires
                if (isinstance(w.from_tid,tuple) and w.from_tid[0]==comp.id) or
                   (isinstance(w.to_tid,  tuple) and w.to_tid[0]  ==comp.id)]
        for w in to_del:
            for it in w.items: self.canvas.delete(it)
        self.wires=[w for w in self.wires if w not in to_del]
        self.canvas.delete(f"c{comp.id}"); del self.components[comp.id]
        self._invalidate_sim()

    def _delete_wire(self,wire):
        for it in wire.items: self.canvas.delete(it)
        if wire in self.wires: self.wires.remove(wire)
        self._invalidate_sim()

    def _delete_junction(self,j):
        # Also delete all wires connected to this junction
        to_del=[w for w in self.wires if w.from_tid==j.tid or w.to_tid==j.tid]
        for w in to_del:
            for it in w.items: self.canvas.delete(it)
        self.wires=[w for w in self.wires if w not in to_del]
        if j.item: self.canvas.delete(j.item)
        del self.junctions[j.id]
        self._invalidate_sim()

    # ── Find helpers ─────────────────────────────────────────────
    def _find_terminal(self,mx,my):
        best,result=TR+6,None
        for comp in self.components.values():
            idx=comp.hit_terminal(mx,my)
            if idx>=0:
                tx,ty=comp.abs_term(idx); d=math.hypot(mx-tx,my-ty)
                if d<best: best,result=d,(comp.id,idx)
        return result

    def _find_junction(self,mx,my):
        for j in self.junctions.values():
            if j.hit(mx,my): return j.id
        return None

    def _find_comp(self,mx,my):
        for comp in reversed(list(self.components.values())):
            if comp.hit_body(mx,my): return comp
        return None

    def _find_wire(self,mx,my):
        for w in self.wires:
            for (x1,y1),(x2,y2) in w.segments():
                if pt_seg_dist(mx,my,x1,y1,x2,y2)<SEG_HIT: return w
        return None

    def _wire_hit_seg(self,wire,mx,my):
        """Return (x1,y1,x2,y2) of the segment of wire closest to (mx,my)."""
        best_d,best_seg=1e9,None
        for (x1,y1),(x2,y2) in wire.segments():
            d=pt_seg_dist(mx,my,x1,y1,x2,y2)
            if d<best_d: best_d=d; best_seg=(x1,y1,x2,y2)
        return best_seg

    # ════════════════════════════════════════════════════════════════
    #  SIMULATION
    # ════════════════════════════════════════════════════════════════
    def _simulate(self): self._run_sim()

    def _run_sim(self):
        hot,neu,gnd,errors=simulate(self.components,self.wires,self.junctions)
        self.hot_set=hot; self.neut_set=neu; self.gnd_set=gnd; self.sim_done=True
        for comp in self.components.values(): self._redraw_comp(comp)
        for w in self.wires: self._draw_wire(w)
        for j in self.junctions.values(): self._draw_junction(j)

        n_loads=sum(1 for c in self.components.values() if c.type in("bulb","outlet","spoutlet"))
        n_on   =sum(1 for c in self.components.values() if c.type in("bulb","outlet","spoutlet") and c.state["on"])
        all_ok=n_on==n_loads and n_loads>0 and not errors

        self.loads_lbl.configure(text=f"{n_on} / {n_loads}  loads powered",
            fg=self.T["w_gnd"] if all_ok else (self.T["w_hot"] if errors else self.T["tx_sec"]))

        lines=[("Simulation Results\n","head")]
        if not errors and n_loads>0:
            lines.append(("✓  All circuits working!\n\n","ok"))
        elif n_loads==0:
            lines.append(("No loads placed.\nAdd a Bulb, Outlet, or\nSP Outlet first.\n\n","warn"))
        else:
            for msg,tag in errors: lines.append((msg+"\n",tag))
            lines.append(("\n","info"))
        lines.append(("━━━━━━━━━━━━━━━━\n","info"))
        lines.append(("■  Red   = Hot\n","err"))
        lines.append(("■  Blue  = Neutral\n","info"))
        lines.append(("■  Green = Ground\n","ok"))
        lines.append(("■  Gray  = Dead\n","info"))
        self._set_results(lines)

    def _reset_sim(self):
        self.sim_done=False; self.hot_set=self.neut_set=self.gnd_set=set()
        for c in self.components.values():
            if c.type in("bulb","outlet","spoutlet"):
                c.state["on"]=False
                if c.type=="spoutlet": c.state["grounded"]=False
            self._redraw_comp(c)
        for w in self.wires:
            for it in w.items: self.canvas.itemconfig(it,fill=self.T["w_default"])
        for j in self.junctions.values(): self._draw_junction(j)
        self.loads_lbl.configure(text="0 / 0  loads powered",fg=self.T["tx_sec"])
        self._set_results([("Simulation reset.\nPress ⚡ Simulate again.\n","info")])

    def _invalidate_sim(self):
        if self.sim_done:
            self.sim_done=False
            for w in self.wires:
                for it in w.items: self.canvas.itemconfig(it,fill=self.T["w_default"])

    def _clear_all(self):
        if not messagebox.askyesno("Clear All","Remove all components and wires?\nPanel Board will remain."): return
        pid=next((cid for cid,c in self.components.items() if c.type=="panel"),None)
        for cid in list(self.components):
            if cid!=pid: self.canvas.delete(f"c{cid}")
        for w in self.wires:
            for it in w.items: self.canvas.delete(it)
        for j in self.junctions.values():
            if j.item: self.canvas.delete(j.item)
        panel=self.components.get(pid)
        self.components={pid:panel} if panel else {}
        self.wires=[]; self.junctions={}
        self.sim_done=False; self.hot_set=self.neut_set=self.gnd_set=set()
        self._draw_breaker_panel_bg()
        self.loads_lbl.configure(text="0 / 0  loads powered",fg=self.T["tx_sec"])
        self._set_results([("Canvas cleared.\n","info")])

    # ── Mode & status ─────────────────────────────────────────────
    def _set_mode(self,mode):
        old=self.mode; self.mode=mode
        if mode!="wire" and old=="wire": self._cancel_wire()
        for m,(btn,color) in self.tool_btns.items():
            btn.configure(bg=color if m==mode else "#21262d",
                          fg="white" if m==mode else "#c9d1d9")
        cursors={"select":"arrow","wire":"crosshair","delete":"X_cursor"}
        self.canvas.configure(cursor=cursors.get(mode,"plus" if mode.startswith("place_") else "arrow"))
        msgs={
            "select":        "Select/Move: drag components or junctions.  Click a switch to toggle.",
            "wire":          "Draw Wire: left-click terminal to start/finish.  Right-click to add bend points.  Click wire to T-tap.",
            "delete":        "Delete: click any component, wire, or junction dot to remove.",
            "place_switch":  "Placing Single-Pole Switch — click canvas to place.",
            "place_switch3": "Placing 3-Way Switch (COM + T1 + T2).",
            "place_switch4": "Placing 4-Way Switch (L1, L2, R1, R2).",
            "place_breaker": "Placing Circuit Breaker — left-click to toggle ON/OFF, right-click to set ampere rating.",
            "place_gnd_bus": "Placing Ground Bus Bar — wire GND-IN from an earth source, G1-G4 to loads.",
            "place_bulb":    "Placing Bulb (terminals LEFT and RIGHT).",
            "place_outlet":  "Placing Outlet.",
            "place_spoutlet":"Placing Special Purpose Outlet (L + N + Ground).",
        }
        self._set_status(msgs.get(mode,""))

    def _set_status(self,msg): self.status_var.set(msg)

    def _set_results(self,lines):
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0","end")
        for text,tag in lines: self.result_text.insert("end",text,tag)
        self.result_text.configure(state="disabled")


# ═══════════════════════════════════════════════════════════════════
if __name__=="__main__":
    root=tk.Tk()
    EIMSimulator(root)
    root.mainloop()
