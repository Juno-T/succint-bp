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
    p_depth = TableLookup.depth_close(self.get_block(q), q_star, q_block_offset)
    p = TableLookup.findedepthopen_inblock(self.get_block(p_star), p_depth, p_star, p_block_offset)
    return p
  
  def enclose(self, c):
    block_offset = self.b(c)*self.block_size
    par_i = TableLookup.enclose_inblock(self.get_block(c), c, block_offset)
    if par_i!=-1:
      if self.P[par_i]==CLOSE:
        par_i = self.findopen(par_i)
        return par_i
    if self.P[c]==OPEN:
      c = self.findclose(c)
    c_prime = self.R.succ(c)
    if self.P[c_prime]==CLOSE:
      p_prime = self.findopen(c_prime)
    else:
      p_prime = self.R.enclose(c_prime) # p' always be open in piofam
    q = self.R.succ(p_prime)
    p_prime_block_offset = self.b(p_prime)*self.block_size
    if self.b(q) == self.b(p_prime):
      #far open in b(p') right before q
      return TableLookup.find_rightmost_faropen_precede_q_inblock(self.get_block(p_prime), q, p_prime_block_offset)
    else:
      #right most far open in b(p') == preceding block's end
      block_end = self.block_size+p_prime_block_offset
      return TableLookup.find_rightmost_faropen_precede_q_inblock(self.get_block(p_prime), block_end, p_prime_block_offset)

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
    return self.select(self.rank(p-1))

  def succ(self, p):
    return self.select(self.rank(p)+1)

  def findclose(self, p):
    assert(self.R[p]), "p is not in pioneer family"
    p_pos = self.rank(p)-1
    if isinstance(self.P_prime, BP):
      q_pos = self.P_prime.findclose(p_pos)
    else:
      q_pos = TableLookup.findclose(self.P_prime, p_pos)
    q_rank = q_pos+1
    return self.select(q_rank)

  def findopen(self, q):
    assert(self.R[q]), "q is not in pioneer family"
    q_pos = self.rank(q)-1
    if isinstance(self.P_prime, BP):
      p_pos = self.P_prime.findopen(q_pos)
    else:
      p_pos = TableLookup.findopen(self.P_prime, q_pos)
    p_rank = p_pos+1
    return self.select(p_rank)

  def enclose(self, c):
    assert(self.R[c]), "c is not in pioneer family"
    c_pos = self.rank(c)-1
    if isinstance(self.P_prime, BP):
      par_pos = self.P_prime.enclose(c_pos)
    else:
      par_pos = TableLookup.enclose_inblock(self.P_prime, c_pos, 0)
    par_rank=par_pos+1
    return self.select(par_rank)


