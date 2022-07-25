from typing import List

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


def constructBP(P: List[bool]):
  from bp.bp import BP, PioneerFamily

  block_size1 = 3
  R1, P_prime1 = getPioneerFamily(P, block_size1)
  block_size2 = 2
  R2, P_prime2 = getPioneerFamily(P_prime1, block_size2)
  R2 = PioneerFamily(R2, P_prime2)
  BP2 = BP(P_prime1, R2, block_size2)
  R1 = PioneerFamily(R1, BP2)
  BP1 = BP(P, R1, block_size1)
  return BP1


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
