# vivliostyle-jppb-test-print
- [DockerによるPDFビルド](https://qiita.com/suzuki_sh/items/03bd86909a47323cbfa3)を[vivliostyle-jppb](https://github.com/ayhy/vivliostyle-jppb)でやってみたテストリポジトリです。このリポジトリをforkまたはclone(共にprivate推奨)し、自分が作った本の中身をjppb/以下に置くいた状態でmasterブランチにpushすることで、[github actions](../../actions/)でpdfをビルドします。




### 導入
```
npm i -g @vivliostyle-cli
git clone https://github.com/ayhy/vivliostyle-jppb-test-print
cd vivliostyle-jppb-test-print
```

## Push前本文確認
```
python generate_publication.py jppb/src.json
vivliostyle preview jppb/publication.json
```
## Known Issues
* ubuntu上のplaywrightではchromiumのverが異なるため`.inline-footnote`の挿入位置がずれるほか、意図しない文字溢れが発生しています。さしあたりwindows serverを作って試験します。

## Licence
[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author
[ayhy](https://github.com/ayhy)