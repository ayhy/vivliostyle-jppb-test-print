if PANDOC_VERSION and PANDOC_VERSION.must_be_at_least then
    PANDOC_VERSION:must_be_at_least("2.17")
else
    error("pandoc version >=2.17 is required")
end

local run=false

local ruby_starter = {"|","｜"}
local ruby_delimiter= "《"
local ruby_closer = "》"

-- ここを書き換えることで任意のルビ記法を使用できます。
-- デフォルトは青空文庫形式の|漢字《読み仮名》 です。
-- それぞれの、半角スペースでない互いに異なる文字（記号）である必要があります。

-- lpeg.reの範囲に2バイト文字を用いると特定文字のみ検出できないなど動作が不安定になるため、
-- 一度1バイト文字の連続に一旦変換して後から戻しています。
-- 内部的には ~~漢字$$ふりがな``という形式に一度変更して処理しています。
-- そのため、ルビをふる本文およびふりがなに半角の~（チルダ）、$（ドル記号）、`（グレイヴ・アクセント）を使うことはできません。
-- また、副作用で記号として半角|を使っている場合出力テキストは全角｜に変換されます。

-- only works in html/epub environment
if FORMAT == 'html5' then run=true
elseif FORMAT == 'html4' then  run=true
elseif FORMAT == 'html' then  run=true
elseif FORMAT == 'epub' then  run=true
elseif FORMAT == 'epub3' then run=true
end

-- 内部的にpandocのStrはspace区切りで分割された一単語レベルの粒度を持ちます。
-- 日本語の文章の場合大きな問題にはなりませんが、|iPad Pro《タブレット》のような半角スペースを含むテキストは
-- 文字列が分割されてしまうため、検出できなくなります。そのため一旦結合してルビにかける必要があります。

function ruby_with_concatedStrings(inlines)
  local elem_newinlines = {}
  local lastelemTag=""
  local secondlastelemtype=""
  local currentelemhasText=false
  local secondlastelemhasText=false
  -- concat inline strings if split by space
  -- only concats [Str or Rawline]-Space-[Str or Rawline] to [Str or Rawline] case
  for i, elem_inside in ipairs(inlines) do
    local concatText=false
    if (elem_inside.tag == "Str" or elem_inside.tag == "RawInline") then
      if lastelemTag == "Space" then
        if (secondlastelemTag == "Str" or secondlastelemTag == "RawInline") then  concatText = true end
      end
    end
    local inlineType = "Str"
    if elem_inside.tag == "RawInline" then inlineType ="RawInline" end
    if secondlastelemTag == "RawInline" then inlineType ="RawInline" end

    local joinedInline = pandoc.Str("test")
    if concatText == true then
      local joinedInline = pandoc.RawInline( "html", elem_newinlines[#elem_newinlines-1].text .. " " .. elem_inside.text)
      if (inlineType == "Str") then
         joinedInline = pandoc.Str( elem_newinlines[#elem_newinlines-1].text .. " " .. elem_inside.text)
      end
      elem_newinlines[#elem_newinlines] = nil --delete last 'Space' inline
      elem_newinlines[#elem_newinlines] = joinedInline -- changed to joined inline
    else
      table.insert(elem_newinlines, elem_inside);
    end
    secondlastelemTag = lastelemTag
    lastelemTag = elem_inside.tag
  end
  -- convert str to rubied rawinline (html)
  for i, elem_inside in ipairs(elem_newinlines) do
    if (elem_inside.tag == "Rawline") or (elem_inside.tag == "Str") then
        elem_newinlines[i] = convert_ruby(elem_inside)
    end
  end
    return elem_newinlines
end

function convert_ruby(inline_str)
  local inputstr = inline_str.text
  if inputstr:match(ruby_delimiter)==nil then --no need for search
    return inline_str
  end

-- 前処理
  inputstr=string.gsub(inputstr, '\n', "==nl==")
  inputstr=string.gsub(inputstr, ' ', "@@ws@@")
-- ルビや文字の間に半角 (whitespace)が含まれていると認識されないので予め繋いでおく

  for i, ruby_letter in ipairs(ruby_starter) do
    inputstr = string.gsub(inputstr, ruby_letter, "~~")
  end
  inputstr = string.gsub(inputstr, ruby_delimiter,"##")
  inputstr = string.gsub(inputstr, ruby_closer,"``")

  pattern = re.compile ("{~ (( '~~' ({ [^~`#]+}) '##' ({[^~`#]+}) '``' ) -> ruby / .)* ~}",
                      { ruby = function (a, b) return '<ruby><rb>' .. a .. '</rb><rt>' .. b .. '</rt></ruby>' end } )
  inputstr = pattern:match(inputstr)

--復元
  inputstr = string.gsub(inputstr, "~~","｜")
  inputstr = string.gsub(inputstr, "##","《")
  inputstr = string.gsub(inputstr, "``","》")
  inputstr=string.gsub(inputstr, '@@ws@@', " ")
  inputstr=string.gsub(inputstr, '==nl==', "\n")

  return pandoc.RawInline('html', inputstr)
end

return {
  { Inlines = ruby_with_concatedStrings }
}

