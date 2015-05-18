-- KEYS[1] = reader_id
-- ARGV[1] = link_id
local reader_id = KEYS[1]
local link_id = ARGV[1]
redis.call('zrem', '{{ link_pickers }}' .. link_id, reader_id)
redis.call('zrem', '{{ reader_picks }}' .. reader_id, link_id)