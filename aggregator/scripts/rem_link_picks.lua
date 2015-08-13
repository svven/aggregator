-- KEYS[1] = link_id
local link_id = KEYS[1]

local pickers_key = '{{ link_pickers }}' .. link_id
local pickers = redis.call('zrange', pickers_key, 0, -1)
if #pickers > 0 then
	for i = 1, #pickers do
		redis.call('zrem', '{{ reader_picks }}' .. pickers[i], link_id)
	end
	redis.call('del', pickers_key)
end