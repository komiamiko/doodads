"""
Small Python library for handling kissing circles.
k4curvature functions are related to Descartes' Theorem.
k4solve is the Problem of Apollonius solver.
"""

def k4curvaturedp(B,μ,k,n):
    """
    Generate the first 5 curvatures (including outer circle) for
    integer Apollonian gasket, with parameters satisfying:
    B^2+μ^2=kn
    0<=μ<=B/sqrt(3)
    2μ<=k<=n
    yielding
    (-B,B+k,B+n,B+k+n-2μ,B+k+n+2μ)
    Intended for integers, so it is Diophantine
    """
    u=B+k+n
    v=2*μ
    return -B,B+k,B+n,u-v,u+v

def k4curvaturedpnext(B=-1,μ=-1,k=-1,math=mp):
    """
    Given some parameters (which do not need to be valid),
    returns the lexicographically next valid tuple (B,μ,k,n)
    for the integer Apollonian gasket Diophantine equations
    """
    isqrt3=1/math.sqrt(3)
    if B<1:
        B=1
        μ=-1
    if μ<0:
        μ=0
        k=-1
    for B in count(B):
        for μ in range(μ,int(B*isqrt3)+1):
            H=B**2+μ**2
            k1=max(1,2*μ)
            k=k1 if k<k1 else k+1
            for k in range(k,int(math.sqrt(H))+1):
                n,n1=divmod(H,k)
                if n1 or gcd(gcd(B,k),n)!=1:continue
                return B,μ,k,n
            k=-1
        μ=0
        
def k4curvaturedpgenerate(start=(-1,-1,-1),stop=None,*args,**kwargs):
    """
    Generate in ascending lexicographical order (B,μ,k,n)
    for the integer Apollonian gasket Diophantine equations
    """
    stop=stop or (inf,)
    r=start
    while True:
        r=k4curvaturedpnext(r[0],r[1],r[2],*args,**kwargs)
        if r>=stop:break
        yield r
        
def k4curvature(a,b,c,s=1):
    """
    Each of four circles is tangent to the other 3.
    Given the curvatures (1/radius) for 3, what is
    the curvature of the fourth?
    Negative touches internally rather than externally.
    Use s=-1 to invert, which gets the outer bounding circle
    instead, or if one of the arguments is the outer bounding circle,
    gets the circle on the opposite side.
    Result for s=1 will be larger (smaller circle) than s=-1.
    """
    return a+b+c+s*2*iroot(2,a*b+b*c+c*a,safety=True)

def k4curvaturefractal(cs=(-10,18,23,27),nx=None,returnfull=False,ordering='tree'):
    """
    Repeatedly applies Descartes' theorem to generate curvatures.
    For 4 starting curvatures with the first negative, produces an
    Apollonian gasket.
    Ordering can be tree or sorted.
    """
    cs=sorted(cs)
    if not nx:nx=combinations(range(len(cs)),3)
    if ordering=='tree':
        nx=collections.deque(map(sorted,nx))
        for l in count(len(cs)):
            i,j,k=nx.popleft()
            a=cs[i]
            b=cs[j]
            c=cs[k]
            d=k4curvature(a,b,c)
            yield (i,j,k,l,a,b,c,d) if returnfull else d
            cs.append(d)
            nx.append((i,j,l))
            nx.append((i,k,l))
            nx.append((j,k,l))
    elif ordering=='sorted':
        nx=list(map(lambda ijk:
            (lambda i,j,k:
             (lambda i,j,k,a,b,c:
              (k4curvature(a,b,c),a,b,c,i,j,k)
              )(i,j,k,cs[i],cs[j],cs[k]))
            (*sorted(ijk)),nx))
        heapq.heapify(nx)
        for l in count(len(cs)):
            d,a,b,c,i,j,k = heapq.heappop(nx)
            yield (i,j,k,l,a,b,c,d) if returnfull else d
            cs.append(d)
            heapq.heappush(nx,(k4curvature(a,b,d),a,b,d,i,j,l))
            heapq.heappush(nx,(k4curvature(a,c,d),a,c,d,i,k,l))
            heapq.heappush(nx,(k4curvature(b,c,d),b,c,d,j,k,l))
    else:
        raise ValueError('Unrecognized ordering '+repr(ordering))
    
def k4solve(a,b,c,useexpand=False,math=math,convertto=float,debug=False):
    """
    Given three circles as (center x, center y, radius),
    find the (center x, center y, radius) of a circle tangent
    to the three. There can be up to 8 such circles,
    this returns the external tangent solution, unless
    useexpand is enabled, in which case all 8 are returned
    as a tuple where for result[i], if digit j in the 3-digit
    binary form of i is 1, then (a,b,c)[j] had its sign inverted.
    This means 7 will be the external tangent solution.
    """
    xs,ys,rs = np.transpose(tuple(map(lambda v:tuple(map(convertto,v)),(a,b,c))))
    if useexpand:
        xs = np.expand_dims(xs,axis=1)
        ys = np.expand_dims(ys,axis=1)
        rs = np.expand_dims(rs,axis=1)
        for i in range(3)[::-1]:
            crs = np.copy(rs)
            crs[i] *= -1
            rs = np.concatenate((rs,crs),axis=1)
    ydiff = np.roll(ys,1,axis=0)-np.roll(ys,2,axis=0)
    xdiff = np.roll(xs,1,axis=0)-np.roll(xs,2,axis=0)
    mid = xs**2+ys**2-rs**2
    denom = np.sum(xs*ydiff,axis=0)
    xmul = np.sum(-rs*ydiff,axis=0)/denom
    xadd = np.sum(mid*ydiff,axis=0)/(2*denom)
    ymul = np.sum(rs*xdiff,axis=0)/denom
    yadd = np.sum(-mid*xdiff,axis=0)/(2*denom)
    quada = 3*(xmul**2+ymul**2-1)
    quadb = 2*(xmul*(3*xadd-np.sum(xs,axis=0))+ymul*(3*yadd-np.sum(ys,axis=0))-np.sum(rs,axis=0))
    quadc = xadd*(3*xadd-2*np.sum(xs,axis=0))+yadd*(3*yadd-2*np.sum(ys,axis=0))+np.sum(mid,axis=0)
    r = (-quadb-np.sqrt(quadb**2-4*quada*quadc))/(2*quada)
    x = xmul*r+xadd
    y = ymul*r+yadd
    result = np.array((x,y,r))
    if useexpand:
        result = np.transpose(result)
    if debug:
        for name in ('xs','ys','rs','xdiff','ydiff','mid','denom','xmul','xadd','ymul','yadd','quada','quadb','quadc','r','x','y'):
            print(name,'=',locals()[name])
    return result
