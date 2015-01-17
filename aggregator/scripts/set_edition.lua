-- KEYS[1] = reader_id
local reader_id = KEYS[1]
local fellows_key = '{{ reader_fellows }}' .. reader_id
local fellows_kvkv = redis.call('zrevrange', fellows_key, 0, -1, 'withscores')
if #fellows_kvkv > 0 then
	local fellows_kkwvv = {}
	local fellows_no = #fellows_kvkv/2
	for i = 1, fellows_no do
		fellows_kkwvv[i] = '{{ reader_marks }}' .. fellows_kvkv[2*i-1]
		fellows_kkwvv[fellows_no+i+1] = fellows_kvkv[2*i]
	end
	fellows_kkwvv[fellows_no+1] = 'weights'
	local edition_key = '{{ reader_edition }}' .. reader_id
	redis.call('zunionstore', edition_key, fellows_no, unpack(fellows_kkwvv))
	local reads_key = '{{ reader_marks }}' .. reader_id
	local reads = redis.call('zrevrange', reads_key, 0, -1)
	redis.call('zrem', edition_key, unpack(reads))
	-- return redis.call('zrevrange', edition_key, 0, -1, 'withscores')
end