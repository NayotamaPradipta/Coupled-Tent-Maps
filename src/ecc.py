# ECC Library to be used in ECDH
def mod_inverse(k, p):
    if k == 0:
        raise ValueError('Division by zero')
    if k < 0:
        return p - mod_inverse(-k, p)

    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = p, k
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    return old_s % p

def point_addition(P, Q, p, a):
    if P[0] is None:
        return Q
    if Q[0] is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and y1 == (p - y2) % p:
        return (None, None)
    if x1 == x2 and y1 == y2:
        # Point doubling
        m = ((3 * x1**2 + a) * mod_inverse(2 * y1, p)) % p
    else:
        # Point addition
        m = ((y2 - y1) * mod_inverse(x2 - x1, p)) % p
    x3 = (m**2 - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    return (x3, y3)

def scalar_multiplication(k, P, p, a):
    R = (None, None)
    Q = P
    while k > 0:
        if k % 2 == 1:
            R = point_addition(R, Q, p, a)
        Q = point_addition(Q, Q, p, a)
        k //= 2
    return R

if __name__ == '__main__':
    p = 23
    a = 1  
    P = (3, 10) 
    k = 2  
    result = scalar_multiplication(k, P, p, a)
    print("Result of scalar multiplication kP:", result)
