# TibNorm
Normalising Tibetan Text

<!-- TODOs -->

## How to use
1. Change your path in _src/config.ini_
   - Set to _table_path_ the absolute path where the folder _tables_ is located.
   - Set to _text_path_ the absolute path where texts to be processed are located, but note that the project does not contain it.
   - Set to _output_path_ the absolute path where the folder _output_ is located.
2. Open your terminal and navigate the directory under Tibnorm.
3. Execute the following command.
```
python src/main.py
```
4. You can find the results in _output_.

## Tables
### Description of tables
- The tables below contain signs or combinations to be processed (e.g., replaced with other signs, reduced to one sign, etc.)
- The columns of the tables are separated by a tab.
#### Table1
- Simple replacement: e.g., ༠ &rarr; 0.
- This table also contains [abbreviations](http://www.rkts.org/abb/list.php).
- This table also contains combinations of more than two signs that are not allowed to come together: e.g., ག། &rarr; ག
- Columns:
  1. _transcription_: character(s) to be replaced with others.
  2. _normalisation_: character(s) with which the character(s) in _transcription_ are to be replaced.
#### Table2
- Replacement using regular expressions: e.g., \\n། &rarr; \\n; ་་་་་་་་་་ &rarr; ་ (Multiple _tsheg_ is reduced to one _tsheg_)
- This replacement is done by _re.sub_ function, but it is slower than the simple replacement function (_replace_), which is used to normalise characters in table1 Therefore, whenever it is possible to normalise a character without using a regular expression, it is advisable to include it in table1.
- Columns:
    1. _transcription_: character(s) to be replaced with others. Regular expressions are applicable.
    2. _normalisation_: character(s) with which the character(s) in _transcription_ are to be replaced. Regular expressions are applicable.
#### Table3
- Replacement with some exceptions: e.g., whitespace ( ) &rarr; _tsheg_ (་), but spaces before and after numbers, alphabetic characters and ༄ should remain; ་། &rarr; །, but not when ་། is preceded by ང.
- Columns:
    1. _transcription_: character(s) to be replaced with others.
    2. _normalisation_: character(s) with which the character(s) in _transcription_ are to be replaced.
    3. _exception_: If the character(s) in _transcription_ appears before or after the character(s) in _exception_, the replacement is canceled.

### Things to pay attention to, when adding a new line to a table.
- Some regular expressions should be escaped by adding a backslash before them, e.g., \\\n (\ + \n)
- It is assumed that the order of normalisation does not affect the final result, nevertheless for safety you place a new normalisation in the bottom of the table.
- When adding a new line to a table, it's recommended to verify the success of the replacement and ensure that it doesn't impact other replacements, and to visualise the differences before and after adding the line for confirmation.