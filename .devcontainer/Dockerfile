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

# Node.js（18系）と npm をインストール
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
&& apt-get install -y nodejs

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# vscode ユーザを作成する
RUN if ! id -u ${USERNAME} > /dev/null 2>&1; then \
    groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME; \
    fi
# workspace ディレクトリの設定
RUN mkdir -p /workspace && chown -R $USERNAME:$USERNAME /workspace

# vscode ユーザに切り替える
USER $USERNAME

## 開発中のため CMD は使わず、VSCode から起動する
# Flask アプリを Gunicorn 経由で自動的に起動
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
