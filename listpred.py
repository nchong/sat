# list predicates

# test if a predicate [p] holds for all elements of [l]
def forall(l,p):
  return len([x for x in l if p(x)]) == len(l)

# test if a predicate [p] holds for some element of [l]
def exists(l,p):
  return len([x for x in l if p(x)]) > 0

# flatten list of lists
def flatten(l):
  return [x for xs in l for x in xs]

# remove duplicates from [l]
# nb: does not guarantee order
def uniquify(l):
  return list(set(l))
