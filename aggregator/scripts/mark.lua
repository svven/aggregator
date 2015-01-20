-- KEYS[1] = reader_id
-- ARGV = [moment, link_id, ..]
local reader_id = KEYS[1]
for i = 1, #ARGV, 2 do
	-- local moment = ARGV[i]
	-- local link_id = ARGV[i+1]
	redis.call('zadd', '{{ link_markers }}' .. ARGV[i+1], ARGV[i], reader_id)
end
local marks_key = '{{ reader_marks }}' .. reader_id
redis.call('zadd', marks_key, unpack(ARGV))