from typing import List, Union

str_prefix = " "
str_block_sep = " | "

OPEN=True
CLOSE=False

def str2P(P_str: str):
  P = [OPEN if c=="(" else CLOSE for c in P_str]
  return P

def P2str(P: List[bool], block_size=None):
  num=""
  s = ""
  for i, p in enumerate(P):
    s+=str_prefix+"(" if p==OPEN else str_prefix+")"
    if block_size!=None:
      if (i+1)%block_size==0:
        s+=str_block_sep
  return s

def R2str(R: List[bool], block_size=None):
  s = ""
  for i, r in enumerate(R):
    s+=str_prefix+"1" if r else str_prefix+"0"
    if block_size!=None:
      if (i+1)%block_size==0:
        s+=str_block_sep
  return s

def pos_str(pos: List[int], block_size=None):
  s = ""
  count =0
  pos = sorted(pos)
  for p in pos:
    while count<p:
      s+=str_prefix+" "
      count+=1
      if block_size!=None:
        if count%block_size==0:
          s+=" "*len(str_block_sep)
    s+=str_prefix+"^"
    count+=1
    if block_size!=None:
      if count%block_size==0:
        s+=" "*len(str_block_sep)
  return s

def getPioneerFamily(P: List[bool], block_size: int):
  def b(i):
    return i//block_size
  R=[False for _ in P]
  P_prime = []
  stk = []
  length = len(P)
  potential_pioneer = None
  for i,p in enumerate(P):
    if p==OPEN:
      open_i = i
      stk.append(open_i)
    else:
      close_i=i
      open_i=stk.pop()
      if open_i==0 or close_i==length-1:
        R[open_i]=True
        R[close_i]=True
      if potential_pioneer is not None:
        pp_open_i, pp_close_i = potential_pioneer
        if (b(open_i)!=b(pp_open_i) or b(close_i)!=b(pp_close_i)):
          R[pp_open_i]=True
          R[pp_close_i]=True
      if b(open_i)==b(close_i):
        potential_pioneer=None
      else:
        potential_pioneer=(open_i, close_i)
  P_prime = [P[i] for i in range(len(P)) if R[i]]
  assert(len(P_prime)==sum(R))
  assert(len(stk)==0)

  return R, P_prime

def constructBP(P: List[bool]):
  block_size1 = 3
  print("P   ", P2str(P, block_size1))
  R1, P_prime1 = getPioneerFamily(P, block_size1)
  print("R1  ", R2str(R1,block_size1))
  block_size2 = 2
  print("P'1 ", P2str(P_prime1, block_size2))
  R2, P_prime2 = getPioneerFamily(P_prime1, block_size2)
  print("R2  ", R2str(R2,block_size2))
  print("P'2 ", P2str(P_prime2))
  R2 = PioneerFamily(R2, P_prime2)
  BP2 = BP(P_prime2, R2, block_size2)
  R1 = PioneerFamily(R1, BP2)
  BP1 = BP(P, R1, block_size1)
  return BP1

class BP:
  def __init__(self, P: List[bool], R:"PioneerFamily", block_size):
    self.P = P
    self.R = R
    self.block_size=block_size

  def b(self, p: int):
    return p//self.block_size

  def get_block(self, p: int):
    block_start =self.b(p)*self.block_size
    return self.P[block_start:block_start+self.block_size]

  def findclose(self, p: int):
    block_offset = self.b(p)*self.block_size
    close_i = TableLookup.findmatching_inblock(self.get_block(p), p, block_offset)
    if close_i!=-1:
      return close_i
    p_star = self.R.pred(p+1)
    q_star = self.R.findclose(p_star)
    if p==p_star:
      return q_star
    # now q must be in the same block as q_star because p isn't an open pioneer.
    # p is also inside the same block as p_star because p isn't a close pioneer.
    p_block_offset = self.b(p)*self.block_size
    q_block_offset = self.b(q_star)*self.block_size
    q_depth = TableLookup.depth_open(self.get_block(p), p_star, p, p_block_offset)
    q = TableLookup.finddepthclose_inblock(self.get_block(q_star), q_depth, q_star, q_block_offset)
    return q

  def findopen():
    pass
  
  def enclose():
    pass

class PioneerFamily:
  def __init__(self, R: List[bool], P_prime: Union["BP", List[bool]]):
    self.R = R
    self.P_prime = P_prime

  def rank(self, p):
    """
      SIMPLIFIED
    """
    return sum(self.R[:p+1])

  def select(self, x):
    """
      SIMPLIFIED
    """
    p=x-1
    rank = self.rank(p)
    while rank<x:
      p+=1
      rank+=self.R[p]
      if p>=len(self.R):
        raise("Out of bound")
    return p

  def pred(self, p):
    return self.select(self.rank(p-1)) # p-1?

  def succ(self, p):
    return self.select(self.rank(p)+1)

  def findclose(self, p):
    assert(self.R[p]), "p is not in pioneer family"
    if isinstance(self.P_prime, BP):
      rank = self.P_prime.findclose(self.rank(p)-1)
    else:
      rank = TableLookup.findclose(self.P_prime, self.rank(p)-1)
    return self.select(rank+1)

class TableLookup:
  """
    SIMPLIFIED
    Functions that could have been implemented using table look up with O(1).
  """
  @staticmethod
  def findmatching_inblock(P_block, x, block_offset):
    x-=block_offset
    stk = []
    for i,p in enumerate(P_block):
      if p==OPEN:
        stk.append(i)
      else:
        if len(stk)==0:
          continue
        close_i=i
        open_i = stk.pop()
        if open_i==x:
          return close_i+block_offset
        if close_i==x:
          return open_i+block_offset
    return -1 # Not found
  
  @staticmethod
  def findclose(P, x):
    stk = []
    for i,p in enumerate(P):
      if p==OPEN:
        stk.append(i)
      else:
        close_i=i
        open_i = stk.pop()
        if open_i==x:
          return close_i
    raise("Close not found")

  @staticmethod
  def depth_open(P_block, p_star, p, block_offset):
    """
      return 0 means p==p_star
    """
    dist = p-p_star
    num_open = sum(P_block[p_star-block_offset:p-block_offset])
    num_close = dist-num_open
    return num_open-num_close

  @staticmethod
  def depth_close(P_block, q_star, q, block_offset):
    dist = q_star - q
    num_open = sum(P_block[q-block_offset:q_star-block_offset])
    num_close = dist-num_open
    return num_close-num_open

  @staticmethod
  def finddepthclose_inblock(P_block, depth, q_star, block_offset):
    for i,p in enumerate(P_block):
      if i+block_offset>q_star:
        break
      if p==CLOSE:
        i_depth = TableLookup.depth_close(P_block, q_star, i+block_offset, block_offset)
        if i_depth == depth:
          return i+block_offset
    raise(f"CANT FIND CLOSE WITH DEPTH={depth}.")

  @staticmethod
  def findedepthopen_inblock(P_block, depth, p_star, block_offset):
    for i in range(len(P_block)-1, -1, -1):
      if i+block_offset<p_star:
        break
      p = P_block[i]
      if p==OPEN:
        i_depth = TableLookup.depth_open(P_block, p_star, i+block_offset, block_offset)
        if i_depth == depth:
          return i+block_offset
    raise(f"CANT FIND CLOSE WITH DEPTH={depth}.")



if __name__=="__main__":
  paren = "(((())()())(()()))"
  block_size = 3
  P = str2P(paren)
  R, P_prime = getPioneerFamily(P, block_size)
  bp = constructBP(P)
  while True:
    p = int(input())
    if paren[p]!="(":
      print("not open!")
      continue
    q = bp.findclose(p)
    str_P_prefix = "P  "
    print(str_P_prefix, P2str(P, block_size))
    print(" "*len(str_P_prefix), pos_str([p,q], block_size))
