# X（@1mai_ikura）のプロフィール画像

| ファイル | 用途 | サイズ |
|---|---|---|
| `x_avatar.png` | アイコン（LINE公式アカウントのアイコンと同じデザイン） | 800×800 |
| `x_header.png` | ヘッダー | 1500×500 |

作り直すときは、スクリプトを書き換えて実行します（Pillow と Windows の BIZ UDゴシックを使います）。

```
python marketing/x/make_icon.py
python marketing/x/make_header.py
```

色は LP（`index.html`）と同じです。黄色 `#ffd84d`、文字 `#1d2433` / `#3a2e00`。
