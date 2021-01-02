# fn-reflection
python utility scripts for my private projects

## このライブラリの考え方
基本的に個人的なプロジェクトのうち公開可能な部分を共有可能なように公開したものです。

pythonの言語を拡張するイメージでモジュール定義しています。
自分のライブラリを構築するためのリファレンス実装程度に扱ってください。

バージョンは1を超えていますが、semverの規約を理解していない時に作ったものなので、APIのインタフェースはunstableであり、気に入らなくなったら関数ごと消します。

production useは想定していません。(常用しているのでそれなりに動くことは期待できますが、ユニットテストも整備されていません。)

もし万が一利用されるならば、masterブランチで指定するのではなく、ハッシュ指定でバージョンをフリーズして使ってください。


## How to install
poetry(pyproject.tomlに追加)
```toml:pyproject.toml
fn_reflection = { git = "https://github.com/fn-reflection/fn_reflection.git", branch = "master" }
```
pip
```sh
pip install git+https://github.com/fn-reflection/fn-reflection
pip install fn-reflection # deprecated バージョン更新してないので古いです
```
## How to use

```py
import fn-reflection
```