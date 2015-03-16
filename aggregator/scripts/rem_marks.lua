-- KEYS[1] = reader_id
-- ARGV[1] = keep
local reader_id = KEYS[1]
local keep = ARGV[1]

local marks_key = '{{ reader_marks }}' .. reader_id
local marks = redis.call('zrange', marks_key, 0, -keep-1)
if #marks > 0 then
	for i = 1, #marks do
		redis.call('zrem', '{{ link_markers }}' .. marks[i], reader_id)
	end
	redis.call('zremrangebyrank', marks_key, 0 , -keep-1)
end