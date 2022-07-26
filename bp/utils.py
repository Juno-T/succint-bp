from typing import List
import math

from . import parser
from .bracket_types import OPEN,CLOSE

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


def constructBP(P: List[bool], min_length = None):
  """
    Construct succint BP data structure recursively.
  """
  from bp.bp import BP, PioneerFamily

  if min_length == None:
    min_length =  int(math.ceil(len(P)/math.log(len(P))/math.log(len(P))))
  if len(P)<=min_length:
    return P
  block_size = int(math.log(len(P))/2)
  R, P_prime = getPioneerFamily(P, block_size)
  BP_prime = constructBP(P_prime, min_length)
  R = PioneerFamily(R, BP_prime)
  return BP(P, R, block_size)


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
  def enclose_inblock(P_block, x, block_offset):
    """
      Also used with smallest P' which is O(n/log^2 n).
    """
    x-=block_offset
    x-=block_offset
    stk = []
    look_for_close=False
    for i,p in enumerate(P_block):
      if p==OPEN:
        if i==x:
          if len(stk)>0:
            return stk[-1]+block_offset
          look_for_close = True
        stk.append(i)
      else:
        close_i=i
        if close_i==x:
          look_for_close = True
        if len(stk)==0:
          if look_for_close and close_i!=x:
            return close_i+block_offset
          continue
        open_i = stk.pop()
        if close_i==x and len(stk)>0:
          return stk[-1]+block_offset
    return -1 # Not found

  @staticmethod
  def find_rightmost_faropen_precede_q_inblock(P_block, q, block_offset):
    stk = []
    for i,p in enumerate(P_block):
      if p==OPEN:
        stk.append(i)
      else:
        close_i=i
        if len(stk)==0:
          continue
        open_i = stk.pop()
    # what's left in the stack is all far open, sorted.
    for open_i in stk[::-1]:
      if open_i+block_offset<q:
        return open_i+block_offset
    raise("No far open preceding q")

  @staticmethod
  def findclose(P, x):
    """
      Meant to be used with small sized P. 
      In BP, it was used with P' with the size of S(O(n/log n).
    """
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
  def findopen(P, x):
    """
      Meant to be used with small sized P. 
      In BP, it was used with P' with the size of S(O(n/log n).
    """
    stk = []
    for i,p in enumerate(P):
      if p==OPEN:
        stk.append(i)
      else:
        close_i=i
        open_i = stk.pop()
        if close_i==x:
          return open_i
    raise("Open not found")


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
