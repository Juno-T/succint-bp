# A toy python implementation of Succint Balanced Parentheses datastructure

This implementation simplified many components but it is also organized so that it could be easily improved. For example, improving `TableLookup` component or replacing `rank` and `select` in `PioneerFamily` with succint sparse bit vector.   

## Usage
```
git clone https://github.com/Juno-T/succint-bp.git
cd succint-bp
export PYTHONPATH=$PWD:$PYTHONPATH
```

## Tests
```
python3 test/interactive.py         # test interactively
python3 test/test_correctness.py    # test with random testcases
```

## Reference
- [A simple optimal representation for balanced parentheses](https://www.sciencedirect.com/science/article/pii/S0304397506006189)