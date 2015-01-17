-- KEYS[1] = reader_id
-- ARGV = [moment, link_id, ..]
local reader_id = KEYS[1]
if #ARGV > 0 then
	-- local link_ids = {}
	local links_no = #ARGV/2
	for i = 1, links_no do
		-- link_ids[i] = ARGV[2*i]
		redis.call('sadd', '{{ link_markers }}' .. ARGV[2*i], reader_id)
	end
	local reads_key = '{{ reader_marks }}' .. reader_id
	redis.call('zadd', reads_key, unpack(ARGV))
end