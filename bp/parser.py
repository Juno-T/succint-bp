from typing import List

from bracket_types import OPEN, CLOSE

str_prefix = " "
str_block_sep = " | "

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
