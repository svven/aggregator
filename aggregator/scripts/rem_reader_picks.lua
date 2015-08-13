-- KEYS[1] = reader_id
-- ARGV[1] = keep
local reader_id = KEYS[1]
local keep = ARGV[1]

local picks_key = '{{ reader_picks }}' .. reader_id
local picks = redis.call('zrange', picks_key, 0, -keep-1)
if #picks > 0 then
	for i = 1, #picks do
		redis.call('zrem', '{{ link_pickers }}' .. picks[i], reader_id)
	end
	redis.call('zremrangebyrank', picks_key, 0 , -keep-1)
end