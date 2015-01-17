-- KEYS[1] = reader_id
-- ARGV[1] = marks_no (optional)
local reader_id = KEYS[1]
local marks_no = -1
if #ARGV > 0 then
	marks_no = ARGV[1] -- 30
end
local marks_key = '{{ reader_marks }}' .. reader_id
local marks = redis.call('zrevrange', marks_key, 0, marks_no)
if #marks > 0 then
	for i = 1, #marks do
		marks[i] = '{{ link_markers }}' .. marks[i]
	end
	local fellows_key = '{{ reader_fellows }}' .. reader_id
	redis.call('zunionstore', fellows_key, #marks, unpack(marks))
	redis.call('zrem', fellows_key, reader_id)
	-- return redis.call('zrevrange', fellows_key, 0, -1, 'withscores')
end