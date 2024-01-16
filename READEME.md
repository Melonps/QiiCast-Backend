# FastAPI Qiita 記事評価予測

## コンテナ設定
このプロジェクトでは、VSCodeの `.devcontainer` を使用しています。開発環境を簡単にセットアップするために、VSCodeを使用している場合は `コンテナーを再度開く` を選択してください。

## 必要なモデルと設定

`qiicast_backend/model` ディレクトリには以下の二つのモデルファイルが必要です。
- `ik_model.pkl`
- `nobo_model.pkl`

`qiicast_backend/conf` ディレクトリには、Qiitaからレスポンスを受け取るための設定ファイルが必要です。
- `secret.yml`

## APIの立ち上げ
以下のコマンドを使用して、FastAPIのサーバーを起動できます。

```sh
uvicorn app:app --port 8000 --reload
```

サーバーが起動したら、ブラウザで [http://localhost:8000/docs](http://localhost:8000/docs) にアクセスしてAPIドキュメントを確認してください。