Aggregator
==========

Description
-----------
Reader class performs the aggregations on demand 
and provides the marks, fellows and news edition for the reader.


Note: [Moment](https://www.google.com/search?q=define+moment) may refer to:

  1. a very brief period of time.
  synonyms: bit, minute, instant, second, split second;
  2. importance.
  synonyms: importance, significance, weight;

Redis Keys
----------
  * `link_markers:link_id` - zset of (reader_id, moment) that marked link_id
  * `reader_marks:reader_id` - zset of (link_id, moment) marked by reader_id
  * `reader_fellows:reader_id` - zset of (fellow_id, moment)
  * `reader_edition:reader_id` - zset of (link_id, moment) aka the 
  relavant news edition
