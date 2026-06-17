# Generates sjs-hourglass.svg — the variable-weight calligraphic hourglass logo.
# Run:  python3 hourglass-gen.py   (writes sjs-hourglass.svg in the project)
# Knobs: fill color in the <svg ...> line at the bottom; loopw() = body/rim/belly
# weight + center-X thinness; sand() = J thickness; topbulb/sandj = geometry.
import math

def cub(p0,p1,p2,p3,t):
    mt=1-t
    return (mt**3*p0[0]+3*mt*mt*t*p1[0]+3*mt*t*t*p2[0]+t**3*p3[0],
            mt**3*p0[1]+3*mt*mt*t*p1[1]+3*mt*t*t*p2[1]+t**3*p3[1])
def cubd(p0,p1,p2,p3,t):
    mt=1-t
    return (3*mt*mt*(p1[0]-p0[0])+6*mt*t*(p2[0]-p1[0])+3*t*t*(p3[0]-p2[0]),
            3*mt*mt*(p1[1]-p0[1])+6*mt*t*(p2[1]-p1[1])+3*t*t*(p3[1]-p2[1]))
def quad(p0,p1,p2,t):
    mt=1-t
    return (mt*mt*p0[0]+2*mt*t*p1[0]+t*t*p2[0], mt*mt*p0[1]+2*mt*t*p1[1]+t*t*p2[1])
def quadd(p0,p1,p2,t):
    return (2*(1-t)*(p1[0]-p0[0])+2*t*(p2[0]-p1[0]), 2*(1-t)*(p1[1]-p0[1])+2*t*(p2[1]-p1[1]))

def evalseg(seg,lt):
    if seg[0]=='c': return cub(seg[1],seg[2],seg[3],seg[4],lt), cubd(seg[1],seg[2],seg[3],seg[4],lt)
    if seg[0]=='q': return quad(seg[1],seg[2],seg[3],lt), quadd(seg[1],seg[2],seg[3],lt)
    return (seg[1][0]+(seg[2][0]-seg[1][0])*lt, seg[1][1]+(seg[2][1]-seg[1][1])*lt), (seg[2][0]-seg[1][0],seg[2][1]-seg[1][1])

def sample(segs,n,closed):
    pts=[]; rng=range(n) if closed else range(n+1)
    for i in rng:
        gt=i/n; s=gt*len(segs); idx=min(int(s),len(segs)-1); lt=s-idx
        p,d=evalseg(segs[idx],lt); pts.append((gt,p,d))
    return pts

def offs(p,d,w):
    L=math.hypot(d[0],d[1]) or 1e-6
    return (p[0]-d[1]/L*w,p[1]+d[0]/L*w),(p[0]+d[1]/L*w,p[1]-d[0]/L*w)

def fmt(poly): return "M"+" L".join("%.2f %.2f"%(x,y) for x,y in poly)+" Z"

# closed variable-width band -> hollow (evenodd): outer loop + inner loop
def band(segs,n,wfn):
    pts=sample(segs,n,True); outer=[]; inner=[]
    for gt,p,d in pts:
        a,b=offs(p,d,wfn(gt)); outer.append(a); inner.append(b)
    return fmt(outer)+" "+fmt(inner)

# just the outer edge of a band (for the favicon keyline)
def outer_loop(segs,n,wfn):
    return fmt([offs(p,d,wfn(gt))[0] for gt,p,d in sample(segs,n,True)])

# open variable-width stroke with round caps (for the J)
def stroke(segs,n,wfn,M=10):
    pts=sample(segs,n,False); left=[]; right=[]
    for gt,p,d in pts:
        a,b=offs(p,d,wfn(gt)); left.append(a); right.append(b)
    p0,d0=pts[0][1],pts[0][2]; w0=wfn(0.0); pn,dn=pts[-1][1],pts[-1][2]; wn=wfn(1.0)
    a0=math.atan2(d0[0],-d0[1]); an=math.atan2(dn[0],-dn[1])
    endcap=[(pn[0]+wn*math.cos(an-math.pi*k/M),pn[1]+wn*math.sin(an-math.pi*k/M)) for k in range(1,M)]
    startcap=[(p0[0]+w0*math.cos(a0+math.pi-math.pi*k/M),p0[1]+w0*math.sin(a0+math.pi-math.pi*k/M)) for k in range(1,M)]
    return fmt(left+endcap+right[::-1]+startcap)

# width: thin at center crossing, gentle fullness through the bellies
def loopw(gt):
    d=min(gt,1-gt); r=min(d/0.13,1.0); s=r*r*(3-2*r)
    belly=0.6*(math.exp(-((gt-0.2)/0.09)**2)+math.exp(-((gt-0.8)/0.09)**2))
    return 1.05+1.6*s+belly
def sand(gt):  return 1.0+0.95*math.cos(math.pi*gt/2)

C=(48,70)   # crossing at canvas middle so the two bulbs balance
# TOP bulb: the rounded bulb, with a slightly flatter & wider crown
topbulb=[('c',C,(38,60),(12,53),(9,37)),
         ('c',(9,37),(7,24),(12,15),(24,12)),  # left shoulder to a wider corner
         ('q',(24,12),(48,10),(72,12)),         # flatter, wider top rim
         ('c',(72,12),(84,15),(89,24),(87,37)), # right shoulder
         ('c',(87,37),(84,53),(58,60),C)]
# BOTTOM bulb = exact mirror of the top about y=70
botbulb=[(s[0],)+tuple((x,140-y) for (x,y) in s[1:]) for s in topbulb]
# J sand: both ends buried in the walls, tail curls down inside the right wall
sandj=[('l',(9,103),(80,92)),('c',(80,92),(85,100),(87,110),(85,120))]

# main logo weight
topband=band(topbulb,240,loopw); botband=band(botbulb,240,loopw); jstroke=stroke(sandj,90,sand)
# favicon: thicker lineart so it holds up small
fw =lambda gt: loopw(gt)+1.0
fsw=lambda gt: sand(gt)+0.8
topband_f=band(topbulb,240,fw); botband_f=band(botbulb,240,fw); jstroke_f=stroke(sandj,90,fsw)

# --- fill the area below the J (the sand pile), favicon only ---
bpts=[p for gt,p,d in sample(botbulb,240,True)]   # bottom-bulb centerline (closed)
jpts=[p for gt,p,d in sample(sandj,40,False)]      # J bed centerline, left -> right
def _near(pt):
    bi,bd=0,1e9
    for i,q in enumerate(bpts):
        dd=(q[0]-pt[0])**2+(q[1]-pt[1])**2
        if dd<bd: bd,bi=dd,i
    return bi
il,ir=_near(jpts[0]),_near(jpts[-1])               # where the J meets each wall
arc=bpts[il:ir+1] if il<=ir else bpts[ir:il+1]      # the bottom arc between them
botfill=fmt(jpts+arc[::-1])                          # J on top, bottom arc beneath

# top funnel: the part of the top bulb below y=cut, draining toward the neck
def cap_region(segs,cut):
    pts=[p for gt,p,d in sample(segs,360,True)]; N=len(pts)
    fwd=[]; i=0
    while i<N and pts[i%N][1]>=cut: fwd.append(pts[i%N]); i+=1
    bwd=[]; i=N-1
    while i>0 and pts[i][1]>=cut: bwd.append(pts[i]); i-=1
    return fmt(bwd[::-1]+fwd)
topfill=cap_region(topbulb,50)

SAND="#C3B4AC"
def write_svg(path, color, bands, fills=(), keylines=()):
    s='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 140" fill="%s" fill-rule="evenodd">\n'%color
    for d,c in fills: s+='  <path d="%s" fill="%s"/>\n'%(d,c)   # sand fills, under everything
    # light keyline on only the OUTER edge — sits behind the dark bands so just a halo shows
    for p in keylines:
        s+='  <path d="%s" fill="none" stroke="%s" stroke-width="3.4" stroke-linejoin="round" stroke-linecap="round"/>\n'%(p,"#FFFFFF")
    for p in bands: s+='  <path d="%s"/>\n'%p
    s+='</svg>\n'
    open(path,'w').write(s)

write_svg('/Users/sarah/thestudyof.ai/static/sjs-hourglass.svg', '#433D37', [topband,botband,jstroke])
write_svg('/Users/sarah/thestudyof.ai/static/sjs-hourglass-favicon.svg', '#2A2521',
          [topband_f,botband_f,jstroke_f], fills=[(topfill,SAND),(botfill,SAND)],
          keylines=[outer_loop(topbulb,240,fw), outer_loop(botbulb,240,fw), jstroke_f])
print("written both")
