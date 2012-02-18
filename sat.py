"""
Pretty naive implementations of DFS and DPLL sat solver.
"""

from listpred import *

# f is a formula in CNF (in dimacs format)
# c is a clause in f
# l is a literal in c
# v is a valuation

# all literals appearing inside f
def symbols_of(f):
  return uniquify([ abs(l) for l in flatten(f) ])

# c is satisfied by v
# if c contains at least one literal which is true
def clause_satisfied(c,v):
  return exists(c, lambda l: l in v)

# f is satisfied by v
# if every clause of f is satisfied by v
def satisfied(f,v):
  return forall(f, lambda c: clause_satisfied(c,v))

# f is unsatisfiable
# if there exists a clause of f that is false (all literals are false)
def unsatisfiable(f,v):
  return exists(f, lambda c: forall(c, lambda l: -l in v))

# solve using only dfs search
def solve_dfs(f):
  def dfs(sym,v):
    if satisfied(f,v): return v
    elif unsatisfiable(f,v): return False
    else:
      l, s = sym[0], sym[1:]
      return dfs(s, v+[l]) or dfs(s, v+[-l])
  return dfs(symbols_of(f), [])

# a unit clause contains only one unassigned literal
def find_unit_clause(f,v):
  def unassigned_literals(c):
    return [ l for l in c if l not in v and -l not in v ]
  for c in f:
    unassigned = unassigned_literals(c)
    if len(unassigned) == 1:
      return unassigned[0]
  return None

# a pure literal appears with only one polarity in f
def find_pure_literal(f):
  literals = flatten(f)
  for l in literals:
    if -l not in literals: return l, [ c for c in f if l not in c ]
  return None, None

# dpll = dfs search + two other tactics (unit clause and pure literals)
def solve_dpll(f, trace=False):
  def remove(sym,l): # non-destructive removal of literal
    x = sym.index(l)
    return sym[0:x] + sym[x+1:]
  def dfs(f,sym,v):
    if satisfied(f,v): return v
    elif unsatisfiable(f,v): return False
    else:
      l = find_unit_clause(f,v)
      if l:
        if trace: print "[trace] Found unit clause ", l
        return dfs(f, remove(sym,abs(l)), v+[l])
      l, g = find_pure_literal(f)
      if l:
        if trace: print "[trace] Found pure literal ", l
        return dfs(g, remove(sym,abs(l)), v+[l])
      l, s = sym[0], sym[1:]
      if trace: print "[trace] Splitting on ", l
      return dfs(f, s, v+[l]) or dfs(f, s, v+[-l])
  return dfs(f, symbols_of(f), [])
