"""
Frontend solver: give it a cnf file or a formula

Examples:
$ python solver.py ex/simple_v3_c2.cnf
$ python solver.py "[[-1,2],[-2,-3],[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]"
"""

from dimacs import solve_dimacs_file, solve_dimacs_formula, is_well_formed
import sys
import json

def main(argv=None):
  pp = True
  trace = True

  if argv is None: argv = sys.argv
  if len(argv) != 2:
    print "Usage: %s <cnf_file>|<cnf_formula>" % argv[0]
    return 1
  try: # as file input
    filename = argv[1]
    solve_dimacs_file(filename,pp,trace)
  except IOError: # try as formula
    try:
      f = json.loads(argv[1])
      assert is_well_formed(f)
      solve_dimacs_formula(f,pp,trace)
    except ValueError:
      print "Could not interpret '%s' as file or formula" % argv[1]
      return 1
  return 0

if __name__ == "__main__":
  sys.exit(main())
