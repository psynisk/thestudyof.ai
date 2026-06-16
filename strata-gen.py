# Generates sjs-strata.svg — faint sediment/contour lines for the rail's lower space.
import math
W,H=460,210   # wide aspect so it can bleed to the sidebar edges without growing taller
COL="#615351"
lines=[]
# baselines from upper area down to the bottom; spacing tightens toward the bottom (compression)
ys=[]; y=44; gap=26
for i in range(9):
    ys.append(y); y+=gap; gap*=0.86      # each layer a little closer than the last
shift=(H-18)-ys[-1]                      # leave bottom padding so lines aren't clipped at the box edge
ys=[b+shift for b in ys]
for i,b in enumerate(ys):
    amp=7.5+2.2*math.sin(i*1.3)           # gently varying wave height
    wl=210+40*math.cos(i*0.9)             # varying wavelength
    ph=i*0.8                              # phase drift so layers aren't stacked copies
    pts=[]
    for k in range(0,81):
        x=W*k/80
        yy=b+amp*math.sin(2*math.pi*x/wl+ph)+1.2*math.sin(2*math.pi*x/(wl*0.37)+ph*1.7)
        pts.append((x,yy))
    d="M"+" L".join("%.1f %.1f"%p for p in pts)
    # lower (later) lines a touch stronger, as if nearer the surface
    op=0.45+0.04*i
    lines.append('<path d="%s" fill="none" stroke="%s" stroke-width="2" stroke-opacity="%.2f" stroke-linecap="round"/>'%(d,COL,min(op,0.72)))
svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d">\n  %s\n</svg>\n'%(W,H,"\n  ".join(lines))
open('sjs-strata.svg','w').write(svg)
print("written sjs-strata.svg,",len(ys),"layers")
