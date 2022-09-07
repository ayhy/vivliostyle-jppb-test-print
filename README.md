# vivliostyle-jppb-test-print
- [DockerによるPDFビルド](https://qiita.com/suzuki_sh/items/03bd86909a47323cbfa3)を[vivliostyle-jppb](https://github.com/ayhy/vivliostyle-jppb)でやってみた自動pdfビルドリポジトリです。`serverbuild`ブランチ(ここにpushするとwindows serverによるビルドを行う)、`dockerbuild`(ここにpushするとubuntuによるビルドを行う)があります。
- 特に理由がない限り、速くて安い方の`dockerbuild`へのpushを推奨します。


### 使い方
1. gitとしてリポジトリをforkまたはcloneします。
2. `dockerbuild`ブランチまたは`serverbuild`ブランチに切り替え、`publication.json`で定義される本の中身をjppb/以下に置きます。
3. 変更分をpushします。
4. しばらくしたら、[github actions](../../actions/)からビルドしたpdfにアクセスできます。

* コンソールからやる場合は

```
git clone https://github.com/ayhy/vivliostyle-jppb-test-print
```
* ここでjppb内部に`publicacion.json`をはじめとした本の情報(html, css, 画像、フォントファイル等）をコピー

```
git add .
git commit -m "changed book content"
```

* Push前に本文がちゃんとできているか確認(任意)
```
vivliostyle preview publication.json
```

（推奨）Ubuntuのdockerコンテナの場合は`dockerbuild`でビルドされるので
```
git push origin serverbuild
```

Windows serverでpdfが必要な場合は`serverbuild`でビルドされるので
```
git push origin serverbuild
```

## Licence
[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author
[ayhy](https://github.com/ayhy)