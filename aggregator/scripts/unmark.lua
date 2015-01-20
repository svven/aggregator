-- KEYS[1] = reader_id
-- ARGV[1] = link_id
local reader_id = KEYS[1]
local link_id = ARGV[1]
redis.call('zrem', '{{ link_markers }}' .. link_id, reader_id)
redis.call('zrem', '{{ reader_marks }}' .. reader_id, link_id)