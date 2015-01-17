Aggregator
==========

Description
-----------
Reader class performs the aggregations on demand 
and provides the marks, fellows and news edition for the reader.

? Also used to cache reader data.

? Link class to cache link data.

Note: Moment may refer to:

<https://www.google.com/search?q=define+moment>

  1. a very brief period of time.
  synonyms: bit, minute, instant, second, split second;
  2. importance.
  synonyms: importance, significance, weight;

Redis Keys
----------
  * `link_markers:link_id` - set of reader_ids that marked the link_id
  * `reader_marks:reader_id` - zset of (link_id, moment) marked by reader_id
  * `reader_fellows:reader_id` - zset of (fellow_id, moment)
  * `reader_edition:reader_id` - zset of (link_id, moment) aka the 
  relavant news edition
