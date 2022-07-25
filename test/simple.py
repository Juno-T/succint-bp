from bp import parser, utils

if __name__=="__main__":
  paren = "(((())()())(()()))"
  block_size = 3
  P = parser.str2P(paren)
  R, P_prime = utils.getPioneerFamily(P, block_size)
  myBP = utils.constructBP(P)
  print(myBP)
  while True:
    p = int(input())
    if paren[p]!="(":
      print("not open!")
      continue
    q = myBP.findclose(p)
    str_P_prefix = "P  "
    print(str_P_prefix, parser.P2str(P, block_size))
    print(" "*len(str_P_prefix), parser.pos_str([p,q], block_size))
