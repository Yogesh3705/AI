def occurs_check(var, expr):
    if var == expr:
        return True
    if isinstance(expr, tuple): 
        return any(occurs_check(var, sub) for sub in expr)
    return False

def substitute(expr, subst):
    if isinstance(expr, str):
        return subst.get(expr, expr)
    return tuple(substitute(sub, subst) for sub in expr)

def unify(Y1, Y2, subst=None):
    if subst is None:
        subst = {}

    Y1 = substitute(Y1, subst)
    Y2 = substitute(Y2, subst)

    if Y1 == Y2:
        return subst

    if isinstance(Y1, str):
        if occurs_check(Y1, Y2):
            return "FAILURE"
        subst[Y1] = Y2
        return subst

    if isinstance(Y2, str):
        if occurs_check(Y2, Y1):
            return "FAILURE"
        subst[Y2] = Y1
        return subst

    if Y1[0] != Y2[0] or len(Y1) != len(Y2):
        return "FAILURE"

    for a, b in zip(Y1[1:], Y2[1:]):
        subst = unify(a, b, subst)
        if subst == "FAILURE":
            return "FAILURE"

    return subst


expr1 = ('p', 'b', 'X', ('f', ('g', 'Z')))
expr2 = ('p', 'z', ('f', 'Y'), ('f', 'Y'))

result = unify(expr1, expr2)
print("MGU:", result)
