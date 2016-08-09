#!/usr/bin/python
from math import floor, sqrt
from random import randint
import sys

# given floats x and y, generate noise values from -1.0 to 1.0.
# 
# coordinate.

# based on code at:
# http://webstaff.itn.liu.se/~stegu/simplexnoise/SimplexNoise.java
# bare-bones python port by Erik Osheim

# TODO:
# 2. measure performance of Gradient object vs tuple
# 3. measure performance of math.floor vs manual floor
# 4. clean up formatting/comments
# 5. test performance
# 6. consider generalizing to N dimensions

class Grad(object):
    def __init__(self, x, y, z, w=0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
    def dot2(self, x, y):
        return self.x * x + self.y * y
    def dot3(self, x, y, z):
        return self.x * x + self.y * y + self.z * z
    def dot4(self, x, y, z, w):
        return self.x * x + self.y * y + self.z * z + self.w * w

class SimplexNoise(object):
    # 2D/3D gradients
    grad3 = [
        Grad(1,1,0),Grad(-1,1,0),Grad(1,-1,0),Grad(-1,-1,0),
        Grad(1,0,1),Grad(-1,0,1),Grad(1,0,-1),Grad(-1,0,-1),
        Grad(0,1,1),Grad(0,-1,1),Grad(0,1,-1),Grad(0,-1,-1),
    ]

    # 4D gradients
    grad4= [
        Grad(0,1,1,1),Grad(0,1,1,-1),Grad(0,1,-1,1),Grad(0,1,-1,-1),
        Grad(0,-1,1,1),Grad(0,-1,1,-1),Grad(0,-1,-1,1),Grad(0,-1,-1,-1),
        Grad(1,0,1,1),Grad(1,0,1,-1),Grad(1,0,-1,1),Grad(1,0,-1,-1),
        Grad(-1,0,1,1),Grad(-1,0,1,-1),Grad(-1,0,-1,1),Grad(-1,0,-1,-1),
        Grad(1,1,0,1),Grad(1,1,0,-1),Grad(1,-1,0,1),Grad(1,-1,0,-1),
        Grad(-1,1,0,1),Grad(-1,1,0,-1),Grad(-1,-1,0,1),Grad(-1,-1,0,-1),
        Grad(1,1,1,0),Grad(1,1,-1,0),Grad(1,-1,1,0),Grad(1,-1,-1,0),
        Grad(-1,1,1,0),Grad(-1,1,-1,0),Grad(-1,-1,1,0),Grad(-1,-1,-1,0),
    ]

    # Skewing and unskewing factors for 2, 3, and 4 dimensions
    F2 = 0.5*(sqrt(3.0)-1.0);
    G2 = (3.0-sqrt(3.0))/6.0;
    F3 = 1.0/3.0;
    G3 = 1.0/6.0;
    F4 = (sqrt(5.0)-1.0)/4.0;
    G4 = (5.0-sqrt(5.0))/20.0;

    def __init__(self):
        self.reseed()

    def reseed(self):
        # 256 values from 0-255
        p = [randint(0, 255) for x in xrange(0, 256)]
    
        # To remove the need for index wrapping, double the permutation table length
        self.perm = [p[i & 255] for i in range(0, 512)]
        self.permMod12 = [p[i & 255] % 12 for i in range(0, 512)]

    # 2D simplex noise
    def noise2d(self, xin, yin):
        n0 = n1 = n2 = 0.0 # Noise contributions from the three corners
        # Skew the input space to determine which simplex cell we're in
        s = (xin + yin) * self.F2; # Hairy factor for 2D
        i = int(floor(xin + s))
        j = int(floor(yin + s))
        t = (i+j)*self.G2;
        X0 = i-t; # Unskew the cell origin back to (x,y) space
        Y0 = j-t;
        x0 = xin-X0; # The x,y distances from the cell origin
        y0 = yin-Y0;

        # For the 2D case, the simplex shape is an equilateral triangle.
        # Determine which simplex we are in.

        # Offsets for second (middle) corner of simplex in (i,j) coords
        if(x0>y0):
            # lower triangle, XY order: (0,0)->(1,0)->(1,1)
            i1=1
            j1=0
        else:
            # upper triangle, YX order: (0,0)->(0,1)->(1,1)
            i1=0
            j1=1      

        # A step of (1,0) in (i,j) means a step of (1-c,-c) in (x,y), and
        # a step of (0,1) in (i,j) means a step of (-c,1-c) in (x,y), where
        # c = (3-sqrt(3))/6
        x1 = x0 - i1 + self.G2; # Offsets for middle corner in (x,y) unskewed coords
        y1 = y0 - j1 + self.G2;
        x2 = x0 - 1.0 + 2.0 * self.G2; # Offsets for last corner in (x,y) unskewed coords
        y2 = y0 - 1.0 + 2.0 * self.G2;
        # Work out the hashed gradient indices of the three simplex corners
        ii = i & 255;
        jj = j & 255;
        gi0 = self.permMod12[ii+self.perm[jj]];
        gi1 = self.permMod12[ii+i1+self.perm[jj+j1]];
        gi2 = self.permMod12[ii+1+self.perm[jj+1]];
        # Calculate the contribution from the three corners
        t0 = 0.5 - x0*x0-y0*y0;
        if(t0 >= 0):
            # (x,y) of grad3 used for 2D gradient
            t0 *= t0;
            n0 = t0 * t0 * self.grad3[gi0].dot2(x0, y0)

        t1 = 0.5 - x1*x1-y1*y1;
        if(t1 >= 0):
            t1 *= t1;
            n1 = t1 * t1 * self.grad3[gi1].dot2(x1, y1)

        t2 = 0.5 - x2*x2-y2*y2;
        if(t2 >= 0):
            t2 *= t2;
            n2 = t2 * t2 * self.grad3[gi2].dot2(x2, y2)

        # Add contributions from each corner to get the final noise value.
        # The result is scaled to return values in the interval [-1,1].
        return 70.0 * (n0 + n1 + n2);

    # 3D simplex noise
    def noise3d(self, xin, yin, zin):
        n0 = n1 = n2 = n3 = 0.0; # Noise contributions from the four corners
        # Skew the input space to determine which simplex cell we're in
        s = (xin+yin+zin)*self.F3; # Very nice and simple skew factor for 3D
        i = floor(xin+s);
        j = floor(yin+s);
        k = floor(zin+s);
        t = (i+j+k)*self.G3;
        X0 = i-t; # Unskew the cell origin back to (x,y,z) space
        Y0 = j-t;
        Z0 = k-t;
        x0 = xin-X0; # The x,y,z distances from the cell origin
        y0 = yin-Y0;
        z0 = zin-Z0;
        # For the 3D case, the simplex shape is a slightly irregular tetrahedron.
        # Determine which simplex we are in.
        i1, j1, k1; # Offsets for second corner of simplex in (i,j,k) coords
        i2, j2, k2; # Offsets for third corner of simplex in (i,j,k) coords
        if(x0>=y0):
            if(y0>=z0):
                i1=1; j1=0; k1=0; i2=1; j2=1; k2=0; # X Y Z order
            elif(x0>=z0):
                i1=1; j1=0; k1=0; i2=1; j2=0; k2=1; # X Z Y order
            else:
                i1=0; j1=0; k1=1; i2=1; j2=0; k2=1; # Z X Y order
      
        else:
            # x0<y0
            if(y0<z0):
                i1=0; j1=0; k1=1; i2=0; j2=1; k2=1; # Z Y X order
            elif(x0<z0):
                i1=0; j1=1; k1=0; i2=0; j2=1; k2=1; # Y Z X order
            else:
                i1=0; j1=1; k1=0; i2=1; j2=1; k2=0; # Y X Z order

        # A step of (1,0,0) in (i,j,k) means a step of (1-c,-c,-c) in (x,y,z),
        # a step of (0,1,0) in (i,j,k) means a step of (-c,1-c,-c) in (x,y,z), and
        # a step of (0,0,1) in (i,j,k) means a step of (-c,-c,1-c) in (x,y,z), where
        # c = 1/6.
        x1 = x0 - i1 + self.G3; # Offsets for second corner in (x,y,z) coords
        y1 = y0 - j1 + self.G3;
        z1 = z0 - k1 + self.G3;
        x2 = x0 - i2 + 2.0*self.G3; # Offsets for third corner in (x,y,z) coords
        y2 = y0 - j2 + 2.0*self.G3;
        z2 = z0 - k2 + 2.0*self.G3;
        x3 = x0 - 1.0 + 3.0*self.G3; # Offsets for last corner in (x,y,z) coords
        y3 = y0 - 1.0 + 3.0*self.G3;
        z3 = z0 - 1.0 + 3.0*self.G3;
        # Work out the hashed gradient indices of the four simplex corners
        ii = i & 255;
        jj = j & 255;
        kk = k & 255;
        gi0 = self.permMod12[ii+self.perm[jj+self.perm[kk]]];
        gi1 = self.permMod12[ii+i1+self.perm[jj+j1+self.perm[kk+k1]]];
        gi2 = self.permMod12[ii+i2+self.perm[jj+j2+self.perm[kk+k2]]];
        gi3 = self.permMod12[ii+1+self.perm[jj+1+self.perm[kk+1]]];
        # Calculate the contribution from the four corners
        t0 = 0.6 - x0*x0 - y0*y0 - z0*z0;
        if(t0 >= 0):
            t0 *= t0;
            n0 = t0 * t0 * self.grad3[gi0].dot3(x0, y0, z0)

        t1 = 0.6 - x1*x1 - y1*y1 - z1*z1;
        if(t1 >= 0):
            t1 *= t1;
            n1 = t1 * t1 * self.grad3[gi1].dot3(x1, y1, z1)

        t2 = 0.6 - x2*x2 - y2*y2 - z2*z2;
        if(t2 >= 0):
            t2 *= t2;
            n2 = t2 * t2 * self.grad3[gi2].dot3(x2, y2, z2)

        t3 = 0.6 - x3*x3 - y3*y3 - z3*z3;
        if(t3 >= 0):
            t3 *= t3;
            n3 = t3 * t3 * self.grad3[gi3].dot3(x3, y3, z3)

        # Add contributions from each corner to get the final noise value.
        # The result is scaled to stay just inside [-1,1]
        return 32.0*(n0 + n1 + n2 + n3);

    # 4D simplex noise, better simplex rank ordering method 2012-03-09
    def noise4d(self, x, y, z, w):
    
        n0 = n1 = n2 = n3 = n4 = 0.0; # Noise contributions from the five corners
        # Skew the (x,y,z,w) space to determine which cell of 24 simplices we're in
        s = (x + y + z + w) * self.F4; # Factor for 4D skewing
        i = floor(x + s);
        j = floor(y + s);
        k = floor(z + s);
        l = floor(w + s);
        t = (i + j + k + l) * self.G4; # Factor for 4D unskewing
        X0 = i - t; # Unskew the cell origin back to (x,y,z,w) space
        Y0 = j - t;
        Z0 = k - t;
        W0 = l - t;
        x0 = x - X0;  # The x,y,z,w distances from the cell origin
        y0 = y - Y0;
        z0 = z - Z0;
        w0 = w - W0;
        # For the 4D case, the simplex is a 4D shape I won't even try to describe.
        # To find out which of the 24 possible simplices we're in, we need to
        # determine the magnitude ordering of x0, y0, z0 and w0.
        # Six pair-wise comparisons are performed between each possible pair
        # of the four coordinates, and the results are used to rank the numbers.
        rankx = 0;
        ranky = 0;
        rankz = 0;
        rankw = 0;
        if(x0 > y0):
            rankx += 1
        else:
            ranky += 1;
        if(x0 > z0):
            rankx += 1
        else:
            rankz += 1;
        if(x0 > w0):
            rankx += 1
        else:
            rankw += 1;
        if(y0 > z0):
            ranky += 1
        else:
            rankz += 1;
        if(y0 > w0):
            ranky += 1
        else:
            rankw += 1;
        if(z0 > w0):
            rankz += 1
        else:
            rankw += 1;
    
        i1 = j1 = k1 = l1 = 0; # The integer offsets for the second simplex corner
        i2 = j2 = k2 = l2 = 0 # The integer offsets for the third simplex corner
        i3 = j3 = k3 = l3 = 0 # The integer offsets for the fourth simplex corner
        # simplex[c] is a 4-vector with the numbers 0, 1, 2 and 3 in some order.
        # Many values of c will never occur, since e.g. x>y>z>w makes x<z, y<w and x<w
        # impossible. Only the 24 indices which have non-zero entries make any sense.
        # We use a thresholding to set the coordinates in turn from the largest magnitude.
        # Rank 3 denotes the largest coordinate.
        i1 = 1 if rankx >= 3 else 0;
        j1 = 1 if ranky >= 3 else 0;
        k1 = 1 if rankz >= 3 else 0;
        l1 = 1 if rankw >= 3 else 0;
        # Rank 2 denotes the second largest coordinate.
        i2 = 1 if rankx >= 2 else 0;
        j2 = 1 if ranky >= 2 else 0;
        k2 = 1 if rankz >= 2 else 0;
        l2 = 1 if rankw >= 2 else 0;
        # Rank 1 denotes the second smallest coordinate.
        i3 = 1 if rankx >= 1 else 0;
        j3 = 1 if ranky >= 1 else 0;
        k3 = 1 if rankz >= 1 else 0;
        l3 = 1 if rankw >= 1 else 0;
        # The fifth corner has all coordinate offsets = 1, so no need to compute that.
        x1 = x0 - i1 + self.G4; # Offsets for second corner in (x,y,z,w) coords
        y1 = y0 - j1 + self.G4;
        z1 = z0 - k1 + self.G4;
        w1 = w0 - l1 + self.G4;
        x2 = x0 - i2 + 2.0*self.G4; # Offsets for third corner in (x,y,z,w) coords
        y2 = y0 - j2 + 2.0*self.G4;
        z2 = z0 - k2 + 2.0*self.G4;
        w2 = w0 - l2 + 2.0*self.G4;
        x3 = x0 - i3 + 3.0*self.G4; # Offsets for fourth corner in (x,y,z,w) coords
        y3 = y0 - j3 + 3.0*self.G4;
        z3 = z0 - k3 + 3.0*self.G4;
        w3 = w0 - l3 + 3.0*self.G4;
        x4 = x0 - 1.0 + 4.0*self.G4; # Offsets for last corner in (x,y,z,w) coords
        y4 = y0 - 1.0 + 4.0*self.G4;
        z4 = z0 - 1.0 + 4.0*self.G4;
        w4 = w0 - 1.0 + 4.0*self.G4;
        # Work out the hashed gradient indices of the five simplex corners
        ii = i & 255;
        jj = j & 255;
        kk = k & 255;
        ll = l & 255;
        gi0 = self.perm[ii+self.perm[jj+self.perm[kk+self.perm[ll]]]] % 32;
        gi1 = self.perm[ii+i1+self.perm[jj+j1+self.perm[kk+k1+self.perm[ll+l1]]]] % 32;
        gi2 = self.perm[ii+i2+self.perm[jj+j2+self.perm[kk+k2+self.perm[ll+l2]]]] % 32;
        gi3 = self.perm[ii+i3+self.perm[jj+j3+self.perm[kk+k3+self.perm[ll+l3]]]] % 32;
        gi4 = self.perm[ii+1+self.perm[jj+1+self.perm[kk+1+self.perm[ll+1]]]] % 32;
        # Calculate the contribution from the five corners
        t0 = 0.6 - x0*x0 - y0*y0 - z0*z0 - w0*w0;
        if(t0 >= 0):
            t0 *= t0;
            n0 = t0 * t0 * self.grad4[gi0].dot4(x0, y0, z0, w0)
    
        t1 = 0.6 - x1*x1 - y1*y1 - z1*z1 - w1*w1;
        if(t1 >= 0):
            t1 *= t1;
            n1 = t1 * t1 * self.grad4[gi1].dot4(x1, y1, z1, w1)
    
        t2 = 0.6 - x2*x2 - y2*y2 - z2*z2 - w2*w2;
        if(t2 >= 0):
            t2 *= t2;
            n2 = t2 * t2 * self.grad4[gi2].dot4(x2, y2, z2, w2)
    
        t3 = 0.6 - x3*x3 - y3*y3 - z3*z3 - w3*w3;
        if(t3 >= 0):
            t3 *= t3;
            n3 = t3 * t3 * self.grad4[gi3].dot4(x3, y3, z3, w3)
    
        t4 = 0.6 - x4*x4 - y4*y4 - z4*z4 - w4*w4;
        if(t4 >= 0):
            t4 *= t4;
            n4 = t4 * t4 * self.grad4[gi4].dot4(x4, y4, z4, w4)
    
        # Sum up and scale the result to cover the range [-1,1]
        return 27.0 * (n0 + n1 + n2 + n3 + n4);

if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        x1 = float(args[0])
        x2 = float(args[1])
        nx = int(args[2])
        y1 = float(args[3])
        y2 = float(args[4])
        ny = int(args[5])
    except:
        print "usage: %s x1 x2 nx y1 y2 ny" % sys.argv[0]
        print ""
        print "  generate noise values for a 2D grid"
        print "  y ranges from [y1, y2] sliced into ny values"
        print "  x ranges from [x1, x2] sliced into nx values"
        print ""
        print "  e.g. 3 4 2 6 7 2 specifies a 2x2 square x~[3,4] y~[6,7]"
        print ""
        sys.exit(1)

    dx = x2 - x1
    dy = y2 - y1

    n = SimplexNoise()
    i = 0
    while i < ny:
        y = y1 + i * dy / (ny - 1)
        rs = []
        j = 0
        while j < nx:
            x = x1 + j * dx / (nx - 1)
            rs.append(n.noise2d(x, y))
            j += 1

        print ' '.join(["%+.3f" % r for r in rs])
        i += 1
