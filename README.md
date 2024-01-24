# TibNorm
Normalising Tibetan Text

<!-- TODOs -->
<!-- 1. explain how to use it -->
<!-- 2. explain columns of each table -->

## How to use
1. Change your path in _config.ini_

```
python ...
```

## Tables
### Description of tables
- The following tables contains signs or their combinations that are to be operated (e.g., replaced with other signs, reduced to one sign, etc.)
- The columns of the tables are separated by a tab.
#### Table1
- Simple replacement: e.g., ༠ &rarr; 0.
- This table also contains [abbreviations](http://www.rkts.org/abb/list.php).
- This table also contains combinations of more than two signs that are not allowed to come together: e.g., ག། &rarr; ག
#### Table2
- Replacement using regular expressions: e.g., \\n། &rarr; \\n; ་་་་་་་་་་ &rarr; ་ (Multiple _tsheg_ is reduced to one _tsheg_)
- This replacement is done by _re.sub_ function, but it is slower than the simple replacement function (_replace_), which is used to normalise characters in table1 Therefore, whenever it is possible to normalise a character without using a regular expression, it is advisable to include it in table1.
#### Table3
- Repalcement with some exceptions: e.g., whitespace ( ) &rarr; _tsheg_ (་), but spaces before and after numbers, alphabetic characters, Chinese characters and ༄ should remain.
#### Table4
- Characters or combinations of the characters, which are to be put together: e.g., ང and tsheg (་) &rarr; ང་.

### The order of norminalisation.
The replacement is done in the following order:
- ...
### Things to pay attention to, when adding a new line to a table.
- If a tab is to added as a value of a table, you should type \\\t. The tab itself is \t and the additional backslash (\) is the escape character.
- If a line break is to added as a value of a table, you should type \\\n.
- Even if a value in a column should remain empty, at the empty position a tab should be insereted by the tab key, not by the regular expression (\t).