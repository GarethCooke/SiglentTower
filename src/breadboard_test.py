# breadboard_test.py — the lighting breadboard test (XIAO ESP32-S3 + SN74AHCT125N), 2026-10-25. Output: parts/wiring/breadboard-test.png
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
R,K,Y,G,B="#d62728","#222","#d49a00","#2ca02c","#1f77b4"
fig,ax=plt.subplots(figsize=(15,8.6)); ax.set_xlim(0,150); ax.set_ylim(0,86); ax.axis("off")
def tag(x,y,t,c,ha="center",va="center",fs=9.5):
    ax.text(x,y,t,ha=ha,va=va,fontsize=fs,color="w" if c not in ("#fff",) else K,weight="bold",
            bbox=dict(boxstyle="round,pad=0.3",fc=c,ec=c))
def w(pts,c,lw=3):
    xs,ys=zip(*pts); ax.plot(xs,ys,color=c,lw=lw,solid_capstyle="round",zorder=1)
ax.text(1,83,"Lighting — breadboard test.  Red tag = + rail (5 V), black tag = − rail (GND).  Every other leg is wired as drawn.",fontsize=12.5,weight="bold")
# ---- XIAO ESP32-S3
ax.add_patch(FancyBboxPatch((8,22),20,48,boxstyle="round,pad=0.4",fc="#2b6cb0",ec=K))
ax.text(14,46,"SEEED XIAO ESP32-S3",color="w",ha="center",va="center",fontsize=11,weight="bold",rotation=90)
ax.text(18,21,"USB-C end — the diode lets it stay\nplugged in while CH1 is on",ha="center",va="top",fontsize=8.5)
pins=["5V","GND","D1","D4","3V3","D2","D0","D3"]; py={}
for i,p in enumerate(pins):
    y=66-i*6; py[p]=y; ax.add_patch(Rectangle((26,y-1),3,2,fc="#cc0",ec=K,zorder=3))
    ax.text(24.6,y,p,ha="right",va="center",fontsize=11,color="w",weight="bold")
w([(29,py["5V"]),(40,py["5V"])],R); ax.add_patch(plt.Polygon([(36.4,py["5V"]-1.3),(36.4,py["5V"]+1.3),(33.4,py["5V"])],fc=K,ec=K,zorder=6)); ax.add_patch(Rectangle((32.7,py["5V"]-1.3),0.6,2.6,fc=K,ec=K,zorder=6)); tag(40,py["5V"],"+",R,ha="left"); ax.text(34.5,py["5V"]+3,"SR3200, stripe → XIAO",ha="center",fontsize=8)
tag(33,py["GND"],"−",K,ha="left"); w([(29,py["GND"]),(33,py["GND"])],K)
w([(29,py["D4"]),(33,py["D4"])],B); tag(33,py["D4"],"→ button",B,ha="left")
for p in ("3V3","D2","D3"): ax.text(30.5,py[p],"empty",va="center",fontsize=8.5,color="#888")
# ---- chip: notch left; bottom 1..7 L->R, top 14..8 L->R
cx0,cy0,cw,ch=62,38,49,13
ax.add_patch(Rectangle((cx0,cy0),cw,ch,fc="#333",ec=K,zorder=2)); ax.add_patch(Circle((cx0,cy0+ch/2),2.2,fc="w",ec=K,zorder=3))
ax.text(cx0+cw/2,cy0+ch/2,"SN74AHCT125N\nnotch on the LEFT, writing the right way up",color="w",ha="center",va="center",fontsize=9,zorder=3)
px=lambda i: cx0+4+i*6.8
top={14:("+",R),13:("−",K),12:("−",K),11:("empty",None),10:("−",K),9:("−",K),8:("empty",None)}
bot={1:("−",K),4:("−",K),7:("−",K)}
for i in range(7):
    x=px(i)
    ax.add_patch(Rectangle((x-1,cy0+ch),2,3,fc="#bbb",ec=K,zorder=3)); ax.add_patch(Rectangle((x-1,cy0-3),2,3,fc="#bbb",ec=K,zorder=3))
    t,c=top[14-i]
    if c: w([(x,cy0+ch+3),(x,cy0+ch+7)],c); tag(x,cy0+ch+8.5,t,c)
    else: ax.text(x,cy0+ch+6,t,ha="center",fontsize=8.5,color="#888")
    if i+1 in bot:
        t,c=bot[i+1]; tag(x,cy0-4.6,t,c)
# data wires
import numpy as np
x2,x3,x5,x6=px(1),px(2),px(4),px(5)
def hline_hops(x0,x1,y,hops,c):
    xs=[x0]; ys=[y]
    for h in sorted(hops):
        t=np.linspace(np.pi,0,20); xs+= list(h+1.4*np.cos(t)); ys+= list(y+1.4*np.sin(t))
    xs.append(x1); ys.append(y); ax.plot(xs,ys,color=c,lw=3,zorder=1,solid_capstyle="round")
w([(29,py["D0"]),(44,py["D0"]),(44,24),(x2,24),(x2,cy0-3)],Y)
w([(29,py["D1"]),(50,py["D1"]),(50,28.5)],G); hline_hops(50,x5,28.5,[x2,x3],G); w([(x5,28.5),(x5,cy0-3)],G)
for x,c,lab,yy in ((x3,Y,"LEFT strip (bus 1) — data in",10),(x6,G,"RIGHT strip (bus 2) — data in",4.5)):
    w([(x,cy0-3),(x,22)],c); ax.add_patch(Rectangle((x-1.6,15),3.2,7,fc="#dcb",ec=K,zorder=3))
    ax.text(x+2.3,18.5,"330 Ω",fontsize=9,va="center"); w([(x,15),(x,yy),(118,yy)],c); tag(119,yy,"→ "+lab,c,ha="left")
ax.text(x2+3,31.2,"wires hop = they cross, not joined",fontsize=7.5,color="#555")
# ---- other parts, as tagged boxes
ax.add_patch(FancyBboxPatch((116,58),31,19,boxstyle="round,pad=0.4",fc="#f4f4ff",ec=K))
ax.text(131.5,74.5,"SPD3303X-E  CH1  5.00 V  1.0 A",ha="center",fontsize=9.5,weight="bold")
tag(124,68,"+ terminal → +",R); tag(140,68,"− terminal → −",K)
ax.text(131.5,61,"turn CH1 on only when every wire is in",ha="center",fontsize=8.5,style="italic")
ax.add_patch(FancyBboxPatch((116,34),31,19,boxstyle="round,pad=0.4",fc="#fff",ec=K))
ax.text(131.5,50,"each strip's power wires",ha="center",fontsize=9.5,weight="bold")
tag(124,43,"5 V wire → +",R); tag(140,43,"GND wire → −",K)
ax.text(131.5,37,"1000 µF: + leg → +, striped leg → −",ha="center",fontsize=9)
ax.add_patch(FancyBboxPatch((2,1),44,14,boxstyle="round,pad=0.4",fc="#fff",ec=K))
ax.add_patch(Circle((8,8),4,fc="#ddd",ec=K)); ax.add_patch(Circle((8,8),2,fc=B,ec=K))
ax.text(14,12,"8 mm button",fontsize=9.5,weight="bold")
ax.text(14,8.3,"switch pin → D4,  other switch pin → −",fontsize=9,va="center")
ax.text(14,4.3,"LED + leg → +,  LED − leg → −",fontsize=9,va="center")
import os; fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "parts", "wiring", "breadboard-test.png"),dpi=110,bbox_inches="tight")
