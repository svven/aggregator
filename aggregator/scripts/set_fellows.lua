-- KEYS[1] = reader_id
-- ARGV = [min_moment, max_moment, picks_count, fellows_limit]
local reader_id = KEYS[1]
local moment_min, moment_max, picks_count, fellows_limit = unpack(ARGV)
if moment_min == 'None' then moment_min = '-inf' end
if moment_max == 'None' then moment_max = '+inf' end

local fellows_key = '{{ reader_fellows }}' .. reader_id
redis.call('del', fellows_key)

local picks_key = '{{ reader_picks }}' .. reader_id
local picks = redis.call('zrevrange', picks_key, 0, picks_count-1)

if #picks > 0 then
	if moment_min == '-inf' and moment_max == '+inf' then
		for i = 1, #picks do
			picks[i] = '{{ link_pickers }}' .. picks[i]
		end
		redis.call('zunionstore', fellows_key, #picks, unpack(picks))
	else
		for i = 1, #picks do
			picks[i] = '{{ link_pickers }}' .. picks[i]
			local range = redis.call('zrangebyscore', 
				picks[i], moment_min, moment_max, 'withscores')
			if #range > 0 then
				for j = 1, #range, 2 do
					redis.call('zincrby', fellows_key, range[j+1], range[j])
				end
			end
		end
	end
	redis.call('zrem', fellows_key, reader_id)
	redis.call('zremrangebyrank', fellows_key, 0 , -fellows_limit-1)
	redis.call('expire', fellows_key, 60)
	-- return redis.call('zrevrange', fellows_key, 0, -1, 'withscores')
end