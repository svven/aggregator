-- KEYS[1] = reader_id
-- ARGV = [min_moment, max_moment, marks_count]
local reader_id = KEYS[1]
local moment_min, moment_max, marks_count = unpack(ARGV)
if moment_min == 'None' then moment_min = '-inf' end
if moment_max == 'None' then moment_max = '+inf' end

local marks_key = '{{ reader_marks }}' .. reader_id
local marks = redis.call('zrevrange', marks_key, 0, marks_count)
if #marks > 0 then
	local fellows_key = '{{ reader_fellows }}' .. reader_id
	if moment_min == '-inf' and moment_max == '+inf' then
		for i = 1, #marks do
			marks[i] = '{{ link_markers }}' .. marks[i]
		end
		redis.call('zunionstore', fellows_key, #marks, unpack(marks))
	else
		redis.call('del', fellows_key)
		for i = 1, #marks do
			marks[i] = '{{ link_markers }}' .. marks[i]
			local range = redis.call('zrangebyscore', 
				marks[i], moment_min, moment_max, 'withscores')
			if #range > 0 then
				for j = 1, #range, 2 do
					redis.call('zincrby', fellows_key, range[j+1], range[j])
				end
			end
		end
	end
	redis.call('zrem', fellows_key, reader_id)
	-- return redis.call('zrevrange', fellows_key, 0, -1, 'withscores')
end