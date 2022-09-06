# Change Log

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