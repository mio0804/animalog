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

# Create non-root user
ARG USERNAME=codespace
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user if it doesn't exist
RUN if ! id -u ${USERNAME} > /dev/null 2>&1; then \
    groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME; \
    fi
# Set up workspace directory
RUN mkdir -p /workspace && chown -R $USERNAME:$USERNAME /workspace

USER $USERNAME

## 開発中のため CMD は使わず、VSCode から起動する
# Flask アプリを Gunicorn 経由で自動的に起動
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
