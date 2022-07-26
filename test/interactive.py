import logging

from bp import parser, utils
from bp.bp import BP, PioneerFamily
from bp.bracket_types import OPEN, CLOSE

# MUST export PYTHONPATH=path/to/succint_BP:$PYTHONPATH

# PARENTHESIS = "(((())()())(()()))"
# PARENTHESIS = "(()(())()((()())())())()(()((()())())())"
PARENTHESIS = "((())(())(((((((((((()())(())())))))))))))"

def query_check(command, x, myBP):
  err=""
  if not (command in ["fc", "fo", "en"]):
    err += f"Invalid command \"{command}\".\n"
  
  if not (x>=0 and x<len(myBP)):
    err+=f"Position \"{x}\" out of bound.\n"
  
  if command=="fc" and myBP.P[x]!=OPEN:
    err+=f"Position \"{x}\" is close parenthesis.\n"

  if command=="fo" and myBP.P[x]!=CLOSE:
    err+=f"Position \"{x}\" is open parenthesis.\n"

  if len(err)>0:
    logging.error(err)
    return False
  return True

def print_man():
  s = """
    Query must be input in a form of operation and position separated by single space.
    Operation includes:
    - fc: Find Close
    - fo: Find Open
    - en: Find enclose
    Position must be integer.
    Example queries:
    fc 3
    fo 5
    en 10
  """
  print(s)

def constructManualBP(P: BP):
  block_size1 = 3
  R1, P_prime1 = utils.getPioneerFamily(P, block_size1)
  block_size2 = 2
  R2, P_prime2 = utils.getPioneerFamily(P_prime1, block_size2)
  R2 = PioneerFamily(R2, P_prime2)
  BP2 = BP(P_prime1, R2, block_size2)
  R1 = PioneerFamily(R1, BP2)
  BP1 = BP(P, R1, block_size1)
  return BP1

if __name__=="__main__":
  print_man()
  P = parser.str2P(PARENTHESIS)
  # myBP = constructManualBP(P) # Using manual construct (for visualization)
  myBP = utils.constructBP(P) # Using optimal construct
  print("BP data structure:\n")
  print(" "*3, parser.index_str(myBP))
  print(myBP)
  print("\n"+"-"*15+"\n")

  while True:
    try:
      print("Enter query:")
      command, x = input().split(" ")
      x=int(x)
    except KeyboardInterrupt:
      import sys
      sys.exit()
    except:
      logging.error("Invalid query.")
      continue
    if not query_check(command, x, myBP):
      str_P_prefix = "P  "
      print(" "*len(str_P_prefix), parser.index_str(myBP))
      print(str_P_prefix, parser.P2str(P, myBP.block_size))
      continue
    marker = []
    if command=="fc":
      q = myBP.findclose(x)
      marker = [x, q]
    elif command=="fo":
      p = myBP.findopen(x)
      marker = [x, p]
    elif command=="en":
      p = myBP.enclose(x)
      marker = [x, p]

    str_P_prefix = "P  "
    print(" "*len(str_P_prefix), parser.index_str(myBP))
    print(str_P_prefix, parser.P2str(P, myBP.block_size))
    print(" "*len(str_P_prefix), parser.pos_str(marker, myBP.block_size))
