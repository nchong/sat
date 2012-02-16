"""
dimacs file reader
"""

from listpred import *
from sat import solve_dfs, solve_dpll

# solve a dimacs formula [f] (given as a list of list of literals)
# pp    = pretty-print formula and valuation
# trace = show dpll tactics trace
#
# > solve_dimacs_formula([[1,-3],[2,3,-1]], True, True)
#   (A \/ !C) /\ (B \/ C \/ !A)
#   SAT
#   B, A = True
def solve_dimacs_formula(f, pp=False, trace=False):
  if pp: print pp_dimacs_formula(f)
  v = solve_dpll(f, trace)
  if v:
    print "SAT"
    if pp: print pp_valuation(v)
  else:
    print "UNSAT"
  return v

# parse and solve a dimacs cnf file [filename]
def solve_dimacs_file(filename, pp=False, trace=False):
  f = read_dimacs(filename)
  return solve_dimacs_formula(f, pp, trace)

# parse a dimacs file into a formula
def read_dimacs(filename):
  formula = []
  f = open(filename, 'r')
  v,c = -1,-1
  for line in f:
    if line.startswith('c'): # comment
      continue
    elif line.startswith('p'): # problem statement
      x = line.split(" ")
      v,c = int(x[2]), int(x[3])
      if x[1] != "cnf": raise Exception("Not a CNF problem file")
    else: #clause
      clause = [ int(x) for x in line.split(" ") ]
      if clause[-1] != 0:
        raise Exception("Clause line does not end in 0 [%s]" % line)
      formula.append(clause[:-1])
  nclauses = len(formula)
  if c != nclauses:
    raise Exception("Expected [%d] clauses; found [%d]" % (c, nclauses))
  nvars = len(set([ abs(l) for clause in formula for l in clause ]))
  if v != nvars:
    raise Exception("Expected [%d] vars; found [%d]" % (v, nvars))
  return formula

# sanity check a formula to see if it is okay for us to process
# f must be a list of list of ints
# which must not contain 0
def is_well_formed(f):
  assert isinstance(f,list)
  for c in f: assert isinstance(c, list)
  sym = uniquify([ l for l in flatten(f) ])
  for l in sym: assert isinstance(l,int)
  assert (0 not in sym)
  return True

# ascii representation of a literal
def string_of_literal(l):
  assert l > 0
  if l < 27: return chr(64+l)
  else: return chr(64+(l%26))+str(l/26)

# pretty print a dimacs formula
def pp_dimacs_formula(f):
  sym = uniquify([ abs(l) for l in flatten(f) ]) # all literals inside f
  mapping = dict(zip(sym, [ string_of_literal(l) for l in sym ]))
  def pp_literal(l):
    assert l != 0
    if l > 0: return     mapping[    l ]
    else:     return "!"+mapping[abs(l)]
  def pp_clause(c):
    return "(" + " \\/ ".join([ pp_literal(l) for l in c ]) + ")"
  return " /\\ ".join([ pp_clause(c) for c in f ])

# pretty print a valuation
def pp_valuation(v):
  sym = [ abs(l) for l in v ]
  mapping = dict(zip(sym, [ string_of_literal(l) for l in sym ]))
  true =  [ l for l in v if l > 0 ]
  false = [ l for l in v if l < 0 ]
  result = []
  if len(true) > 0:
    result.append(", ".join([ mapping[l]      for l in true  ]) + " = True")
  if len(false) > 0:
    result.append(", ".join([ mapping[abs(l)] for l in false ]) + " = False")
  return "\n".join(result)
