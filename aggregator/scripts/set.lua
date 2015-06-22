-- Set operations
-- http://www.phailed.me/2011/02/common-set-operations-in-lua/

local function find(a, tbl)
	for _,a_ in ipairs(tbl) do if a_==a then return true end end
end

function union(a, b)
	a = {unpack(a)}
	for _,b_ in ipairs(b) do
		if not find(b_, a) then table.insert(a, b_) end
	end
	return a
end

function intersection(a, b)
	local ret = {}
	for _,b_ in ipairs(b) do
		if find(b_,a) then table.insert(ret, b_) end
	end
	return ret
end

function difference(a, b)
	local ret = {}
	for _,a_ in ipairs(a) do
		if not find(a_,b) then table.insert(ret, a_) end
	end
	return ret
end

function symmetric(a, b)
	return difference(union(a,b), intersection(a,b))
end