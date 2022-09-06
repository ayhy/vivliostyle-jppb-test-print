# vivliostyle-jppb
- vivliostyle japanese-paperback or japanese python-pandoc book
- vertical 2-row  novel layout (typical for Japanese shinsho / paperback) vivliostyle example. This repo uses pandoc and python to compile html and generate publication.json for display, also  offers utilty wrapper to create front matter (w/ toc) and back matter.
- 新書二段レイアウトのvivliostyle-cli使用例です。vivliostyle.config.jsではなく、src.jsonからpython+pandocでhtmlとpublication.jsonを生成します。前付に表題紙、目次（本文ファイルから自動生成）、中扉、本文、奥付というフォーマットで出力します。→[デフォルトのレイアウト例](https://vivliostyle.org/viewer/#src=https://raw.githubusercontent.com/ayhy/vivliostyle-jppb/master/publication.json&bookMode=true)

## 前提
* python3.8 or higher
* pandoc2.17 or higher

## 簡易導入ガイド
1. [vivliostyle-cliの導入ガイド](https://docs.vivliostyle.org/#/ja/vivliostyle-cli)に従って、node.jsとvivliostyle-cliを導入します。
2. 下記のコマンドで当リポジトリをダウンロードします。gitがないなら[zipファイル](https://github.com/vivliostyle/vivliostyle-cli/archive/refs/heads/main.zip)とかでもいいです。
3. 適当なフォルダにダウンロードしたリポジトリを展開して、コマンドラインから`python generate_publication.py`を打ちます。
4. さっきほどのコマンドが`publication.json`ファイルを更新するので、`vivliostyle build publication.json`をやるとPDFが出力されます。
  * `vivliostyle preview publication.json`だとブラウザで確認できます。

* コマンドまとめ：
```
npm i -g @vivliostyle-cli
git clone https://github.com/ayhy/vivliostyle-jppb
cd vivliostyle-jppb
python generate_publication.py
vivliostyle build publication.json
```

### 補足
* `generate_publication.py`はそれだけだとスクリプトのあるフォルダ内のsrc.jsonを読んで処理を行います。それ以外の名前のjsonファイルや、別フォルダでにあるjsonファイルを指定して`python generate_publication.py book1/src2.json`のように実行することもできます。
* publication.jsonは指定したjsonファイルと同一のフォルダ内に生成され、既に存在している場合は`src.json`で指定した`author`、`name`および`readingOrder`の内容を上書きします。


## 簡易制作ガイド
* 基本的には、必要なファイル（おもにsrc.jsonとsource/以下のファイル、レイアウトをいじるならtheme/以下のファイルやfont以下のファイルも）を書き換えて、プレビューを観ながら満足するまでいじりましょう。
```
python generate_publication.py
vivliostyle preview publication.json
```
* 満足したらpdfにpreviewウィンドウからPDFプリンターで印刷するか、以下のコマンドで直にPDF出力できます。
```
vivliostyle build publication.json
```

* このレイアウトは行間設定がやや詰まっているので、そのままの設定でchromeに出すとルビがある行の行間が多少不規則になります（2022年7月現在）。さしあたりはFirefoxブラウザを指定してプレビューし、そこからPDFプリンターへ印刷することで回避できます。
```
vivliostyle preview publication.json -browser firefox

```

### 補足：本文内容の変更
 * デフォルトではsource/以下のファイルを読み込むようになっているため、ファイルの中身を変更するか、`src.json`で読み込むファイルを指定して出力htmlが参照する元テキストを変更できます。
 * `__frontmatter1.md`、`__frontmatter2.md`、`__backmatter.md`については中身の書き換えが必要な箇所のみを変更するのを推奨します。
 * 本文はmarkdown記法で書かれるため、二回以上の連続改行は単一の改行へ変換され、無視されます。複数行に渡って空白行を連続させる方法はいくつかありますが、`　`（全角スペース+改行）を行うのが一番楽です。

### 補足：フォントの変更
* [Google Fonts](https://fonts.google.com/)や[Bunny Fonts](https://fonts.bunny.net/)が提供する外部フォントは、それぞれのサイトが提供する`<link>`形式のタグを `/fonts/externalfont.md`に転記することで、css/sassファイルにで当該フォントを`font-family`で指定可能になります。
  * `<link href=...`形式のファイルはエラーがあって読み込めないことがあります。その場合はダウンロードしてローカルに`@font-face`を指定してください。
* webフォントとして提供されていない（ttf形式でダウンロードできるフォント）は、`./fonts/localfont.css`に`@font-face`を指定することで、設定したフォントを使用可能です。
* fonf-face云々の詳細はwebフォント cssとかで解説が沢山あると思うのでここではしません。

### 補足：レイアウトのカスタマイズ
* 基礎的なsass(scss)とcssの知識が必要です。
* 基本的にレイアウトに影響するものは以下の三つです。
  * `theme-shinho/_param.scss`  -本文全体に影響するページサイズ、天地小口ノド、タチキリの設定
  * `theme-shinho/make_multi_column.scss` - n段組および段組内の字数行数の設定
  * `theme-shinho/theme_common.scss` - デフォルトのスタイル
* を変更してcssに変換してください。
  * このテンプレートとはフォルダ構造が違いますが、scssファイル→cssファイルへの変換は[チュートリアル - 既存のテーマのカスタマイズ](https://vivliostyle.org/ja/tutorials/customize/)で解説されているほか、[vscodeのリアルタイムコンパイラ](https://marketplace.visualstudio.com/items?itemName=glenn2223.live-sass)など様々な選択肢があります。
* ファイル名を変更した場合はsrc.jsonの下の方に読み込むスタイルシート名の設定があるのでそちらも変更してください。


## Licence
[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)
* vivliostyle-jppbへの表記をどこかに入れておいてください。

## Author
[ayhy](https://github.com/ayhy)