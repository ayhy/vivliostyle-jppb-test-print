if PANDOC_VERSION and PANDOC_VERSION.must_be_at_least then
    PANDOC_VERSION:must_be_at_least("2.17")
else
    error("pandoc version >=2.17 is required")
end

local run=false

-- only works in html/epub environment
if FORMAT == 'html5' then run=true
elseif FORMAT == 'html4' then  run=true
elseif FORMAT == 'html' then  run=true
elseif FORMAT == 'epub' then  run=true
elseif FORMAT == 'epub3' then run=true
end

if run==false then return {}
end

-- "-- "を行頭につけてコメントアウトして調整してください

function convert_exchar(inputstr)


-- 全角感嘆符疑問符の連続 -> 単独文字
--  inputstr = inputstr:gsub("！！！","")
--  inputstr = inputstr:gsub("？？","⁇")
--  inputstr = inputstr:gsub("？！","⁈")
--  inputstr = inputstr:gsub("！？","⁉")
--  inputstr = inputstr:gsub("！！","‼")

-- ひらがな、カタカナの濁音・半濁音
  inputstr = inputstr:gsub("あ゛","")
  inputstr = inputstr:gsub("い゛", "")
  inputstr = inputstr:gsub("う゛","ゔ")
  inputstr = inputstr:gsub("え゛","")
  inputstr = inputstr:gsub("お゛","")
  inputstr = inputstr:gsub("ん゛","")
  inputstr = inputstr:gsub("ア゛","")
  inputstr = inputstr:gsub("イ゛","")
  inputstr = inputstr:gsub("エ゛","")
  inputstr = inputstr:gsub("オ゛","")
  inputstr = inputstr:gsub("ン゛","")
  inputstr = inputstr:gsub("が゜","")
  inputstr = inputstr:gsub("き゜","")
  inputstr = inputstr:gsub("く゜","")
  inputstr = inputstr:gsub("け゜","")
  inputstr = inputstr:gsub("こ゜","")
  inputstr = inputstr:gsub("カ゜","")
  inputstr = inputstr:gsub("キ゜","")
  inputstr = inputstr:gsub("ク゜","")
  inputstr = inputstr:gsub("ケ゜","")
  inputstr = inputstr:gsub("コ゜","")
  inputstr = inputstr:gsub("セ゜","")
  inputstr = inputstr:gsub("ツ゜","")
  inputstr = inputstr:gsub("ト゜","")
  inputstr = inputstr:gsub("フ゜","")
  inputstr = inputstr:gsub("な゛","")
  inputstr = inputstr:gsub("に゛","")
  inputstr = inputstr:gsub("ぬ゛","")
  inputstr = inputstr:gsub("ね゛","")
  inputstr = inputstr:gsub("の゛","")
  inputstr = inputstr:gsub("ま゛","")
  inputstr = inputstr:gsub("み゛","")
  inputstr = inputstr:gsub("む゛","")
  inputstr = inputstr:gsub("め゛","")
  inputstr = inputstr:gsub("も゛","")
  inputstr = inputstr:gsub("や゛","")
  inputstr = inputstr:gsub("ゆ゛","")
  inputstr = inputstr:gsub("よ゛","")
  inputstr = inputstr:gsub("ら゛","")
  inputstr = inputstr:gsub("り゛","")
  inputstr = inputstr:gsub("る゛","")
  inputstr = inputstr:gsub("れ゛","")
  inputstr = inputstr:gsub("ろ゛","")
  inputstr = inputstr:gsub("わ゛","")
  inputstr = inputstr:gsub("ゐ゛","")
  inputstr = inputstr:gsub("ゑ゛","")
  inputstr = inputstr:gsub("を゛","")
  inputstr = inputstr:gsub("ぁ゛","")
  inputstr = inputstr:gsub("ぃ゛","")
  inputstr = inputstr:gsub("ぅ゛","")
  inputstr = inputstr:gsub("ぇ゛","")
  inputstr = inputstr:gsub("ぉ゛","")
  inputstr = inputstr:gsub("が゛","")
  inputstr = inputstr:gsub("げ゛","")
  inputstr = inputstr:gsub("っ゛","")
  inputstr = inputstr:gsub("ゃ゛","")
  inputstr = inputstr:gsub("ゅ゛","")
  inputstr = inputstr:gsub("ょ゛","")
  inputstr = inputstr:gsub("ゎ゛","")
  inputstr = inputstr:gsub("ナ゛","")
  inputstr = inputstr:gsub("ニ゛","")
  inputstr = inputstr:gsub("ヌ゛","")
  inputstr = inputstr:gsub("ネ゛","")
  inputstr = inputstr:gsub("ノ゛","")
  inputstr = inputstr:gsub("マ゛","")
  inputstr = inputstr:gsub("ミ゛","")
  inputstr = inputstr:gsub("ム゛","")
  inputstr = inputstr:gsub("メ゛","")
  inputstr = inputstr:gsub("モ゛","")
  inputstr = inputstr:gsub("ヤ゛","")
  inputstr = inputstr:gsub("ユ゛","")
  inputstr = inputstr:gsub("ヨ゛","")
  inputstr = inputstr:gsub("ラ゛","")
  inputstr = inputstr:gsub("リ゛","")
  inputstr = inputstr:gsub("ル゛","")
  inputstr = inputstr:gsub("レ゛","")
  inputstr = inputstr:gsub("ロ゛","")
  inputstr = inputstr:gsub("ァ゛","")
  inputstr = inputstr:gsub("ィ゛","")
  inputstr = inputstr:gsub("ゥ゛","")
  inputstr = inputstr:gsub("ェ゛","")
  inputstr = inputstr:gsub("ォ゛","")
  inputstr = inputstr:gsub("ヵ゛","")
  inputstr = inputstr:gsub("ヶ゛","")
  inputstr = inputstr:gsub("ッ゛","")
  inputstr = inputstr:gsub("ャ゛","")
  inputstr = inputstr:gsub("ュ゛","")
  inputstr = inputstr:gsub("ョ゛","")
  inputstr = inputstr:gsub("ヮ゛","")
  inputstr = inputstr:gsub("・゛","")
  inputstr = inputstr:gsub("ー゛","")
  return inputstr
end
 
function Str(elem)
  elem.text = convert_exchar(elem.text)
  return elem
end