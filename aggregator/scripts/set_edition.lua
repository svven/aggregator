-- KEYS[1] = reader_id
-- ARGV = [min_moment, max_moment, fellows_count, news_limit]
local reader_id = KEYS[1]
local moment_min, moment_max, fellows_count, news_limit = unpack(ARGV)
if moment_min == 'None' then moment_min = '-inf' end
if moment_max == 'None' then moment_max = '+inf' end

local edition_key = '{{ reader_edition }}' .. reader_id
redis.call('del', edition_key)

local fellows_key = '{{ reader_fellows }}' .. reader_id
local fellows_kvkv = redis.call('zrevrange', fellows_key, 0, fellows_count-1, 
	'withscores')
local fellows_no = #fellows_kvkv/2

if #fellows_kvkv > 0 then
	if moment_min == '-inf' and moment_max == '+inf' then
		local fellows_kkwvv = {}
		for i = 1, fellows_no do
			fellows_kkwvv[i] = '{{ reader_picks }}' .. fellows_kvkv[2*i-1]
			fellows_kkwvv[fellows_no+i+1] = fellows_kvkv[2*i]
		end
		fellows_kkwvv[fellows_no+1] = 'weights'
		redis.call('zunionstore', edition_key, fellows_no, unpack(fellows_kkwvv))
	else
		for i = 1, fellows_no do
			local picks_key = '{{ reader_picks }}' .. fellows_kvkv[2*i-1]
			local fellowship = fellows_kvkv[2*i]
			local range = redis.call('zrangebyscore', 
				picks_key, moment_min, moment_max, 'withscores')
			if #range > 0 then
				for j = 1, #range, 2 do
					redis.call('zincrby', edition_key, fellowship*range[j+1], range[j])
				end
			end
		end
	end
	local picks_key = '{{ reader_picks }}' .. reader_id
	local picks = redis.call('zrevrange', picks_key, 0, -1)
	redis.call('zrem', edition_key, unpack(picks))
	redis.call('zremrangebyrank', edition_key, 0 , -news_limit-1)
	redis.call('expire', edition_key, 60)
	-- return redis.call('zrevrange', edition_key, 0, -1, 'withscores')
	
	local find = function(e, t)
		for _, e_ in ipairs(t) do if e_ == e then return true end end
	end
	local intersection = function(t1, t2)
		local ret = {}
		for _, e in ipairs(t2) do
			if find(e, t1) then table.insert(ret, e) end
		end
		return ret
	end

	local fellows = {}
	for i = 1, fellows_no do
		fellows[i] = fellows_kvkv[2*i-1]
	end
	local edition = redis.call('zrevrange', edition_key, 0, -1)
	local no_links_by_fellows = {}
	local edition_fellows_key = '{{ edition_fellows }}' .. reader_id
	redis.call('del', edition_fellows_key)
	
	for i = 1, #edition do
		local link_id = edition[i]
		local pickers_key = '{{ link_pickers }}' .. link_id
		local pickers = redis.call('zrevrange', pickers_key, 0, -1)

		local link_fellows = intersection(pickers, fellows)
		table.sort(link_fellows)
		local link_fellows_key = table.concat(link_fellows, ",")
		no_links_by_fellows[link_fellows_key] = (no_links_by_fellows[link_fellows_key] or 0) + 1

		if no_links_by_fellows[link_fellows_key] > 3 then
			redis.call('zrem', edition_key, link_id)
		else
			redis.call('hset', edition_fellows_key, link_id, link_fellows_key)
		end
	end
end
