-- KEYS[1] = reader_id
-- ARGV = [moment, link_id, ..]
local reader_id = KEYS[1]
for i = 1, #ARGV, 2 do
	-- local moment = ARGV[i]
	-- local link_id = ARGV[i+1]
	redis.call('zadd', '{{ link_pickers }}' .. ARGV[i+1], ARGV[i], reader_id)
end
local picks_key = '{{ reader_picks }}' .. reader_id
redis.call('zadd', picks_key, unpack(ARGV))