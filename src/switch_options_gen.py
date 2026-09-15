import cairosvg
out=[]
def emit(s): out.append(s)
def rect(x,y,w,h,fill="none",stroke="#222",sw=0.8,dash=None,rx=0):
    d=f' stroke-dasharray="{dash}"' if dash else ""
    emit(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
def text(x,y,s,size=9,anchor="start",weight="normal",fill="#222"):
    s=s.replace("&","&amp;")
    emit(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}">{s}</text>')
def circ(cx,cy,r,fill,stroke="#222",sw=0.8): emit(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
EXT="#3a3f47"; INST="#e3e6ea"; PR="#2f6f73"; DK="#1b3f42"; SCR="#16263a"
def front(ox,oy,title,variant):
    S=1.0
    def X(x): return ox+x*S
    def Z(z): return oy+(340-z)*S      # show z 60..340
    text(ox,oy-10,title,11,weight="bold")
    # uprights + right inner upright
    rect(X(0),Z(340),20,280,fill=EXT); rect(X(341),Z(340),20,280,fill=EXT)
    rect(X(251),Z(247.5),20,(247.5-68),fill=EXT)
    rect(X(271),Z(88),70,20,fill="#555")
    # PSU + AWG faces
    rect(X(23),Z(243),225,143,fill=INST); rect(X(35),Z(225),115,75,fill=SCR)
    for i in range(6): rect(X(40+i*18),Z(116),8,8,fill="#222")
    rect(X(23),Z(336),214,88,fill=INST); rect(X(35),Z(325),90,63,fill=SCR)
    # column + bottom facia
    rect(X(273),Z(336),65,245,fill=PR); rect(X(285.5),Z(328),40,10,fill=DK,rx=3)
    rect(X(23),Z(86),315,26,fill=PR)
    # variant
    if variant=="A":
        rect(X(242),Z(336),26,88,fill="#2a2f36")                    # fixed panel replaces the slot
        rect(X(247),Z(310),16,30,fill="#111",rx=2); rect(X(249),Z(306),12,11,fill="#2f9e44",rx=1)  # rocker, lit top half
        text(X(255),Z(270),"I",7,"middle",fill="#ddd")
        text(X(255),Z(262),"O",7,"middle",fill="#ddd")
        rect(X(242),Z(268),26,20,fill="#2a2f36",stroke="#444")
        text(X(255),Z(250),"rocker",6,"middle",fill="#888")
    else:
        rect(X(242),Z(336),26,88,fill=PR); rect(X(247),Z(328),16,8,fill=DK,rx=3)  # mini slot stays
        rect(X(341),Z(205),20,40,fill="#2a2f36")                    # bezel in the upright face
        circ(X(351),Z(185),8,"#111"); circ(X(351),Z(185),6.5,"#2f9e44"); circ(X(351),Z(185),4,"#111")
    for z in (243,336): emit(f'<line x1="{X(23)}" y1="{Z(z)}" x2="{X(338)}" y2="{Z(z)}" stroke="#ccc" stroke-width="0.4"/>')
front(40,40,"A — mains rocker in a fixed panel where the mini slot was (slot dropped)","A")
front(440,40,"B — 16 mm ring-lit push button in the front-right upright, PSU height (slot kept)","B")
notes=[
"A: 16 A illuminated rocker (30 × 16), switches the rear strip's live via a 2-core in a printed conduit down the inside of the column housing. Real mains wiring in the stack; earth the frame.",
"B: 16 mm anti-vandal ring-lit push, latching or momentary. Rated 3–5 A — enough for the stack (~2.6 A at full PSU load) but marginal; better used as a LOW-VOLTAGE input to an ESP32 that drives a smart plug on the strip. No mains inside the frame.",
"Either way the strip stays vertical on the rear cross rails; LAN and USB-B run down the rear-right post in slot clips, mains down the rear-left, PSU fan centre kept clear.",
]
y=350
for n in notes: text(40,y,n,8,fill="#333"); y+=13
svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 400" width="860" height="400" font-family="Helvetica, Arial, sans-serif"><rect width="860" height="400" fill="#fff"/>'+"\n".join(out)+'</svg>'
cairosvg.svg2pdf(bytestring=svg.encode(),write_to='/mnt/user-data/outputs/front-switch-options.pdf')
cairosvg.svg2png(bytestring=svg.encode(),write_to='/mnt/user-data/outputs/front-switch-options.png',output_width=1720)
print('ok')
