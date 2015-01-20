-- KEYS[1] = reader_id
-- ARGV = [min_moment, max_moment, fellows_count]
local reader_id = KEYS[1]
local moment_min, moment_max, fellows_count = unpack(ARGV)
if moment_min == 'None' then moment_min = '-inf' end
if moment_max == 'None' then moment_max = '+inf' end

local fellows_key = '{{ reader_fellows }}' .. reader_id
local fellows_kvkv = redis.call('zrevrange', fellows_key, 0, fellows_count, 
	'withscores')
if #fellows_kvkv > 0 then
	local fellows_no = #fellows_kvkv/2
	local edition_key = '{{ reader_edition }}' .. reader_id
	if moment_min == '-inf' and moment_max == '+inf' then
		local fellows_kkwvv = {}
		for i = 1, fellows_no do
			fellows_kkwvv[i] = '{{ reader_marks }}' .. fellows_kvkv[2*i-1]
			fellows_kkwvv[fellows_no+i+1] = fellows_kvkv[2*i]
		end
		fellows_kkwvv[fellows_no+1] = 'weights'
		redis.call('zunionstore', edition_key, fellows_no, unpack(fellows_kkwvv))
	else
		redis.call('del', edition_key)
		for i = 1, fellows_no do
			local marks_key = '{{ reader_marks }}' .. fellows_kvkv[2*i-1]
			local fellows_value = fellows_kvkv[2*i]
			local range = redis.call('zrangebyscore', 
				marks_key, moment_min, moment_max, 'withscores')
			if #range > 0 then
				for j = 1, #range, 2 do
					redis.call('zincrby', edition_key, fellows_value*range[j+1], range[j])
				end
			end
		end
	end
	local marks_key = '{{ reader_marks }}' .. reader_id
	local marks = redis.call('zrevrange', marks_key, 0, -1)
	redis.call('zrem', edition_key, unpack(marks))
	-- return redis.call('zrevrange', edition_key, 0, -1, 'withscores')
end