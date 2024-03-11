# TibNorm

        TibNorm is a utility for producing normalised versions of Tibetan texts to make them easier for contemporary users to search and read, in line with current Tibetan writing conventions. As part of the normalisation process, TibNorm:

        -        changes Tibetan numbers into Arabic numerals
        -        changes Tibetan brackets and quotation marks into the standard western equivalents
        -        changes non-standard “illegal” stacks into standard ones
        -        deletes a ། if found at the beginning of a line
        -        removes a ། if found after a ཀ, ག or ཤ, with or without a vowel
        -        adds a ་ between ང  and །
        -        reduces two or more ་  to a single one
        -        changes ཌ་ or ཊ་ to གས་ unless preceded by a white space, tab, or new line.

        TibNorm also expands abbreviations so that they are shown in their full form. For abbreviations in classical Tibetan, TibNorm draws from the list of over 6,000 classical Tibetan abbreviations compiled by Bruno Lainé of the Tibetan Manuscript Project Vienna (TMPV) as part of the project’s Resources for Kanjur and Tanjur Studies. In TibNorm, the user can manually change the flag in the abbreviations table to exclude any abbreviation that they don’t want to expand.
        
        Tibnorm was developed for the Divergent Discourses project by YUki Kyogoku of Leipzig University.

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
#### Abbreviations
- Simple replacement of [abbreviations](http://www.rkts.org/abb/list.php), just as in table1.
- Columns:
  1. _transcription_: an abbreviated form.
  2. _normalisation_: a full-form.
  3. _flag_: 0 means that the replacement is cancelled, while 1 means that it is valid. You can modify this parameter in _src/config.ini_.
#### Table1
- Simple replacement except for abbreviations: e.g., ༠ &rarr; 0.
- This table contains combinations of more than two characters that are not allowed to come together: e.g., ག། &rarr; ག
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
    4. _exc_len_: This parameter signifies the maximum length of characters in _exception_. For instance, characters in [A-Za-z0-9\u4e00-\u9fff༄] represent individually a single character, thus having a maximum length of 1 (This is equivalent to [A-Za-z0-9\u4e00-\u9fff༄]{1}, though the Python code itself does not explicitly specify the length). Conversely, characters in (?:ང|ངི|ངུ|ངེ|ངོ) have lengths: ང is treated as a single character, while the others, combined with a vowel, are considered as two characters. Thus, the maximal length in this case is 2.
    5. _scope_: This parameter defines the scope within which exceptions are searched. When set to _left_, it means that the characters located on the left side of the target character within the range of _exc_len_ are checked for exceptions. Conversely, _right_ means the opposite, and when set to _both_ sides are searched. 
    6. _flag_: 0 means that the replacement is cancelled, while 1 means that it is valid. You can modify this parameter in _src/config.ini_.

### Things to pay attention to, when adding a new entry to a table.
- Consider whether the entry you want to add is part of other words. If it is, you will need to use regular expressions to define exceptions.
- Some regular expressions should be escaped by adding a backslash before them, e.g., \\\n (\ + \n)
- It is assumed that the order of normalisation does not affect the final result, nevertheless for safety you place a new normalisation in the bottom of the table.
- When adding a new entry to a table, it's recommended to verify the success of the replacement and ensure that it doesn't impact other replacements, and to visualise the differences before and after adding the line for confirmation using a [diff-tool](https://www.site24x7.com/tools/diff-checker.html).
- A character with a vowel, e.g., ཏེ (length=2), or a ligature, e.g., བཀྲམས (length=5), are computationally regarded as multiple characters. Thus, for example, if you refer to ཏ as a consonant, you should use regular expression, so that ཏ with any vowel is also included.
- When adding an abbreviated form and its full form in table1, it is advisable to use tsheg both before and after the abbreviated and full forms. This helps avoid mistaken replacements of the same form appearing in the middle of a syllable. However, a drawback is that an abbreviated form at the beginning of the sentence remains unreplaced (See [issue](https://github.com/orgs/Divergent-Discourses/projects/1/views/1?pane=issue&itemId=50262100)).
