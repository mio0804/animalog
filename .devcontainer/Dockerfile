# Python 3.11の公式イメージ
FROM python:3.11

# 作業ディレクトリを指定
WORKDIR /workspace

# 必要なパッケージをコピー
COPY requirements.txt .

# Pythonライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリのコードをコピー（VSCodeからはマウントされるが、buildでも必要）
COPY . .

# ポート解放（Flask用）
EXPOSE 5000

## 開発中のため CMD は使わず、VSCode から起動する
# Flask アプリを Gunicorn 経由で自動的に起動
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
