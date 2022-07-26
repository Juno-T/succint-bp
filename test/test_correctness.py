import random
import json

from bp import parser, utils
from bp.bracket_types import OPEN, CLOSE

def genEnclosedParen(n: int):
  assert(n%2==0)
  assert(n>=4)
  n-=2
  s = ""
  stk = []
  while n>0:
    r = random.randint(0,1)
    if r==1:
      s+="("
      n-=2
      stk.append(r)
    else:
      if len(stk)>0:
        s+=")"
        stk.pop()
      else:
        s+="("
        stk.append(1)
        n-=2
  s+=")"*len(stk)
  return "("+s+")"

def verifyParen(paren: str):
  P = parser.str2P(paren)
  stk=[]
  for i,p in enumerate(P):
    if p==OPEN:
      stk.append(i)
    else:
      if len(stk)==0:
        return False
      stk.pop()
  return True

def test_query(paren: str, n: int):
  res = []
  P = parser.str2P(paren)
  myBP = utils.constructBP(P) # Using optimal construct
  for i in range(n):
    q = random.randint(0,2)
    x = random.randint(0, len(myBP)-1)
    if x==0 or x==len(myBP)-1:
      # x don't have enclosed parenthesis
      q=0
    if q==2:
      # test enclose
      query = "en"
      ans = utils.TableLookup.enclose_inblock(P, x, 0)
      cal = myBP.enclose(x)
    else:
      # test find
      if P[x]==OPEN:
        # test find close
        query = "fc"
        ans = utils.TableLookup.findclose(P, x)
        cal = myBP.findclose(x)
      else:
        # test find open
        query = "fo"
        ans = utils.TableLookup.findopen(P, x)
        cal = myBP.findopen(x)
    query+=" "+str(x)
    if cal!=ans:
      res.append({"query": query, "ans": ans, "cal": cal})
  
  return res

def main():
  res = []
  num_incorrect = 0
  num_loop = 100
  num_queries_per_loop = 10
  num_queries = num_loop*num_queries_per_loop
  for i in range(num_loop):
    n = random.randint(20, 100)*2
    paren = genEnclosedParen(n)
    res.append({"P": paren})
    r = test_query(paren, num_queries_per_loop)
    num_correct = num_queries_per_loop-len(r)
    if len(r)>0:
      res[-1]["incorrect_queries"]=r
    res[-1]["score"]=f"{num_correct}/{num_queries_per_loop}"
    num_incorrect+=len(r)
  with open('./test/test_result.json', 'w') as outfile:
    json.dump(res, outfile)
  num_correct=  num_queries-num_incorrect
  print(f"Score: {num_correct}/{num_queries}")

if __name__=="__main__":
  main()