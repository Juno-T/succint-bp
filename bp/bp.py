from typing import List, Union

from .bracket_types import OPEN, CLOSE
from .utils import TableLookup
from . import parser

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

  def findopen(self, q:int):
    block_offset = self.b(q)*self.block_size
    open_i = TableLookup.findmatching_inblock(self.get_block(q), q, block_offset)
    if open_i!=-1:
      return open_i
    q_star = self.R.succ(q-1)
    p_star = self.R.findopen(q_star)
    if q==q_star:
      return p_star
    p_block_offset = self.b(p_star)*self.block_size
    q_block_offset = self.b(q)*self.block_size
    p_depth = TableLookup.depth_close(self.getblock(q), q_star, q_block_offset)
    p = TableLookup.findedepthopen_inblock(self.get_block(p_star), p_depth, p_star, p_block_offset)
    return p
    ##???
  
  def enclose():
    pass

  def __len__(self):
    return len(self.P)

  def __repr__(self) -> str:
    s=""
    s+="P   "+parser.P2str(self.P, self.block_size)+"\n"
    s+="R   "+parser.R2str(self.R.R, self.block_size)+"\n"
    s+="-"*10+"\n"
    if isinstance(self.R.P_prime, BP):
      s+=str(self.R.P_prime)
    else:
      s+="P'  "+parser.P2str(self.R.P_prime)+"\n"
    return s

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

  def findopen(self, q):
    assert(self.R[q]), "q is not in pioneer family"
    if isinstance(self.P_prime, BP):
      rank = self.P_prime.findopen(self.rank(q)-1)
    else:
      rank = TableLookup.findopen(self.P_prime, self.rank(q)-1)
    return self.select(rank+1)

