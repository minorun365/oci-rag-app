# oci-rag-app

## 事前準備

事前にあなたのOCIアカウントでRAGエージェントを作成ください。

- 参考記事： [30分でOCI Generative AI Agents 爆速RAGってみた 【Object storage編】 - Qiita](https://qiita.com/msasakaw/items/219c58ecdf98b4bfb743)

本リポジトリをローカルにクローンし、必要なPythonライブラリをインストールします。

```zsh
pip install -U streamlit oci
```

その後、本リポジトリ内の `frontend.py` に同エージェントのエンドポイントのOCIDを記載してください。

## 実行方法

ルートディレクトリで以下コマンドを実行してください。

```zsh
streamlit run frontend.py
```
