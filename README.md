# TibNorm
Normalising Tibetan Text

<!-- TODOs -->
<!-- 1. explain how to use it -->
<!-- 2. explain columns of each table -->

## How to use
```
python ...
```

## Tables
- The following tables contains signs or their combinations that are to be operated (e.g., replaced with other signs, reduced to one sign, etc.)
### Table1
- Simple replacement.
- e.g., ༠ &rarr; 0.
- This table also contains [abbreviations](http://www.rkts.org/abb/list.php).
### Table2
- Reduce repeated multiple signs to one sign.
- e.g., ་་་་་་་་་་ &rarr; ་ (Multiple _tsheg_ is reduced to one _tsheg_)
### Table3
- Completely delete specific signs in the corpus.
- e.g., དོན་ བྱེད་ &rarr; དོན་བྱེད་
### Table4
- Combinations of more than two signs that are to be put together in every case.
- e.g., ང and _tsheg_ (་) &rarr; ང་
### Table5
- Combinations of more than two signs that are not allowed to come together.
- e.g., ག། &rarr; ག
### Table6
- Combinations of more than two signs that are not allowed to come together, but with an(/some) exception(s).
- e.g., _tsheg_ (་) and _shad_ (།) ; ་། &rarr; །, but when it is preceded by ང, it is not the case.
- This table could be merged with Table5.