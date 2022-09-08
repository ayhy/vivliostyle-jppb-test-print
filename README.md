# vivliostyle-jppb-test-print
- vivliostyleファイルをgithub actionsで自動PDF化するリポジトリです。[vivliostyle-jppb](https://github.com/ayhy/vivliostyle-jppb)で作ったデータを使うことを念頭にしていますが、`publication.json`で規定されていれば何でも使えます。
- `serverbuild`ブランチと`dockerbuildブランチ`へのpushに対応しており、それぞれwindows serverとubuntuのdockerでのビルドを行います。
- 特に理由がない限り、速くて安い方の`dockerbuild`へのpushを推奨します。


### 使い方
1. gitとしてリポジトリをforkまたはcloneします。Web上だと`use this tempalte`が楽です。
2. `dockerbuild`ブランチまたは`serverbuild`ブランチに切り替え、`publication.json`で定義される本の中身をjppb/以下に置きます。
3. 変更分をpushします。
4. しばらくしたら、[github actions](../../actions/)からビルドしたpdfにアクセスできます。

* コンソールからやる場合は

```
gh repo create <new-repo-name> --template="ayhy/vivliostyle-jppb-test-print"  --private
cd <new-repo-name>
```
多分新しい本を作るのでしょうし`--private`はあったほうがよいでしょう。


* ここでjppb/フォルダ内部に`publicacion.json`をはじめとした本の中身(html, css, 画像、フォントファイル等）をコピーし
* Push前に本文がちゃんとできているか確認(任意)
```
vivliostyle preview jppb/publication.json
```

ステージして `dockerbuild`（推奨）または`serverbuild`にpush、元々コミットが残っていた場合は上書きします。
```
git add .
git push origin dockerbuild --force
```


## Reference
* [DockerによるPDFビルド](https://qiita.com/suzuki_sh/items/03bd86909a47323cbfa3)

## Licence
[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author
[ayhy](https://github.com/ayhy)