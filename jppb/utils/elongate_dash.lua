if PANDOC_VERSION and PANDOC_VERSION.must_be_at_least then
    PANDOC_VERSION:must_be_at_least("2.17")
else
    error("pandoc version >=2.17 is required")
end

local run=false

-- only runs with Str inline, not compatible with RawInline
-- thus this must be called before convert_ruby

-- only works in html/epub environment
if FORMAT == 'html5' then run=true
elseif FORMAT == 'html4' then  run=true
elseif FORMAT == 'html' then  run=true
elseif FORMAT == 'epub' then  run=true
elseif FORMAT == 'epub3' then run=true
end

if run==false then return {}
end


function elongate_dash(strelem)
  inputstr = strelem.text
  
  if (inputstr:find("――") == nil) then
    return nil -- do nothing, remain unchanged
  end

  inline_split = {}
  -- split str by "――"
  -- insert span inline element (dash)
  
  local span_dashline = pandoc.Span('―', {class = 'dashline'}) 
  -- equivalent to <span class="dashline">―</span>
  local span_dash = pandoc.Span({span_dashline, pandoc.Str('　')}, {class = 'dash'}) 
  -- equivalent to <span class="dash"><span class="dashline">―</span>　</span>
  
  inputstr = inputstr .. '――'
  for matchstring in inputstr:gmatch("(.-)――") do
    if #matchstring>0 then
      table.insert(inline_split, matchstring)
    end
    table.insert(inline_split, span_dash)
  end
  inline_split[#inline_split] = nil -- remove last element
    
  return inline_split
end

return {
  { Str = elongate_dash }
}