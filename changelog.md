# Change Log

## 0.0.6 - 2022-09-04

### Added
 - `src.json` now specifies `name` and `author` under `pubinfo`. In default style, `name` string is copied to `publication.json` and appears along with  page number in body section.
 - `name`と`author`を`src.json`の`pubinfo`内から指定するように。`name`のテキストはデフォルト状態では本文左ページのページ番号の隣に題名として表示されます。

## 0.0.5 - 2022-09-02

### Added
- New footnotes style that can be set at the end of the column in multi-column area, as opposed to the end of the page. 
  - usage: `[_footnote text_]{.incolumn_footnote}` in multi-column text.
  - Please note this is a __workaround implelentation as noted in [vivliostyle issue](https://github.com/vivliostyle/vivliostyle.js/issues/981)__, in future all usage will be moved back to `footnote` class.

- 多段組のページで、段落をぶち抜かずに段落内末尾につけられる脚注を追加。
  - `[_脚注内テキスト_]{.incolumn_footnote}`で使えます。
  - 今回の実装は __[Vivliostyleのissue](https://github.com/vivliostyle/vivliostyle.js/issues/981)にあるとおり、@footnoteがサポートされるまでの暫定的なもの__ です。`@footnote`がサポートされた後は段落内脚注も`footnote`に一本化されます。


## 0.0.4 - 2022-09-01

### Changed
- decoupled `h1`- `h6` tag and display style as class to allow flexible hiearchical structure.
  - header element now requires class `title`. e.g.  `# chaptertitle {.title}`. `subtitle`, `author` class can be also set added under `shortstory` class.
  - ToC can now be generated as hiearchical lists.
- 階層構造を持った章立てが作れるように。行頭 `#` の個数が`src.json`中の`section_depth`より大きいものは見出しに反映されます。
  - これにより、第一部-第一章といった階層構造のある章立てをつくることができます。
  - 表示上の情報は `# 見出し名{.クラス}`の`.クラス`で定義され、現在は本文中は`title`、`subtitle`、`author`などを指定できます。本文要素内中扉は`single_element_page`で指定できます。

## 0.0.3 - 2022-08-15

### Added
- Added footnotes style as `inline-notes` class. Now `[string of inline elements]{.footenote}` shows up at a footnote section.
- 脚注クラス（.footnote）を追加。`[脚注本文]{.footnote}`または`<span class="footnote">脚注本文</span>`の形で脚注が記述できるように。

- Added "title" specification in src.json for body-text. If empty, it will use first header element name as title.
- 本文htmlの<title>をsrc.jsonで指定できるように。この指定が存在しない場合はファイルの最初の見出し要素をタイトルとして使うように。


## 0.0.2 - 2022-08-06

### Added
- In-book illustration support class. Sample is available in ch6.
- Added bleed param to _param.scss and related parameters in theme_common.scss.

- 挿絵クラス(.illustration)を追加。記法のサンプルはch6.mdで確認できます。
- 塗り足し・断ちきりに関する指定を_param.scssで行えるように。

### Changed
- Display control of page conter has switched from css-overwrite to named page rule. Removed hade_pagenum.css.
- named page mediaを指定してセクションごとにページ番号を表示するか、スタイルの雛形を作れるように。

## 0.0.1 - 2022-07-11

- Initial alpha release.
- 初版発行。