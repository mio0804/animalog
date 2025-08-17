<samp>
<div align="center">

# AnimaLog

<img width="4666" height="3147" alt="Image" src="https://github.com/user-attachments/assets/15e053cf-f86c-4d7c-a513-29b05b534b04" />

## アプリURL情報

</div>

**▼ URL**  
[https://animalog-nabinemu.com](https://animalog-nabinemu.com)

**▼ テストユーザー情報**  
Email：`test@example.com`  
Password：`Password-01`  

✅ 新規ユーザー登録も可能です。

<br>

<div align="center">

## 概要

</div>

AWS上に構築した、高可用性とコンテナ化による柔軟な構成を備えたWebアプリケーションのインフラポートフォリオです。  
ECS(Fargate)によるコンテナオーケストレーション、RDSによるデータ永続化など、AWSのベストプラクティスを取り入れた堅牢かつコスト効率の高い構成を実現しています。

### 主なアプリ機能

- **ユーザー認証**  
  Amazon Cognitoを利用した安全なログイン・ログアウト機能
- **ペット管理**  
  ペットの登録・編集・削除で複数匹を管理可能
- **日記投稿**  
  テキストと画像を添えてペットの日常を記録
- **画像アップロード**  
  投稿画像をAmazon S3に安全に保存
- **日記一覧**  
  ペット別、または全体で日記を一覧表示

<br>

<div align="center">

## 作成の背景

</div>

インフラエンジニアとして、AWS主要サービスを組み合わせたシステム構築を実践するために開始したプロジェクトです。  
座学で得た知識を実際の構築に落とし込み、サービスのライフサイクル全体を深く理解することを目的としました。

<br>

<div align="center">

## 技術スタック

</div>

### フロントエンド
| 技術名 | 用途 |
|--------|------|
| React | UIフレームワーク |
| TypeScript | 型安全なJavaScript開発 |
| Vite | モダンビルドツール・開発サーバー |
| React Router DOM | クライアントサイドルーティング |
| Bootstrap | CSSフレームワーク |
| React Bootstrap | React用Bootstrapコンポーネント |
| Axios | HTTP通信ライブラリ |
| AWS Amplify | AWS連携・Cognito認証 |

### バックエンド
| 技術名 | 用途 |
|--------|------|
| Python | サーバーサイド言語 |
| Flask | Webフレームワーク |
| Flask-SQLAlchemy | ORM |
| Flask-CORS | クロスオリジン対応 |
| PostgreSQL | RDBMS |
| Gunicorn | WSGI HTTPサーバー |
| python-jose | JWT(ジョット)認証・暗号化 |
| boto3 | AWS SDK |

### インフラ・AWS
| 技術名 | 用途 |
|--------|------|
| Amazon ECS Fargate | コンテナオーケストレーション |
| Amazon RDS | マネージドPostgreSQL |
| Amazon S3 | 画像ファイルストレージ |
| Amazon EC2 | 踏み台サーバー |
| AWS Cognito | ユーザー認証・管理 |
| AWS Secrets Manager | 認証情報の安全管理 |
| AWS Certificate Manager | SSL証明書管理 |
| Application Load Balancer | ロードバランサー |
| Amazon Route 53 | DNS管理 |
| CloudWatch Logs | ログ管理・監視 |
| Amazon ECR | コンテナレジストリ |

### 開発環境・ツール
| 技術名 | 用途 |
|--------|------|
| Claude Code | AI開発アシスタント |
| GitHub Codespaces | クラウド開発環境 |
| VS Code DevContainer | 一貫した開発環境 |
| Docker | コンテナ化 |
| Docker Compose | ローカルオーケストレーション |
| Nginx | リバースプロキシ |

<br>

<div align="center">

## インフラ構成図

<img width="1151" height="941" alt="Image" src="https://github.com/user-attachments/assets/57b7bbe5-2ad7-4d4b-b5f0-19065abf046a" />

</div>

<br>

<div align="center">

## 構築・デプロイ手順
</div>

### 1. 開発環境構築
- Devcontainerで環境設定
- GitHubリポジトリ作成
- GitHub Codespacesで開発環境をビルド

### 2. Webアプリケーション構築
- Claude Codeでアプリケーションを作成
- S3・Cognito構築、接続確認
- 本番用Dockerfile作成

### 3. 本番環境構築

- ネットワーク基盤の作成  
   - VPC を新規作成し、パブリック/プライベートサブネットを用途別に分割  
   - インターネットゲートウェイとルートテーブルを設定し、外部通信経路を確保  

- データベース構築  
   - Amazon RDS for PostgreSQL を作成  
   - 接続情報は AWS Secrets Manager で安全に管理  

- ドメイン・証明書設定  
   - Route 53 で独自ドメインを設定  
   - ACM で SSL/TLS 証明書を発行し、HTTPS対応  

- 認証設定  
   - Cognito ユーザープールのリダイレクトURLを本番環境に変更  

- アプリケーション公開基盤の構築  
   - ALB とターゲットグループを作成し、HTTPSでリクエストを振り分け  
   - ALBとECSタスク間のポートマッピングを設定  

- コンテナデプロイ準備  
   - ECR にアプリのDockerイメージをPush  
   - ECSタスク定義を作成  

- デプロイと検証  
   - ECSサービスを作成して本番タスクを起動  
   - CloudWatch Logs でエラー解析・動作確認

- ECR への push を自動化  
   - GitHub Actions で OIDC を使用して AWS 認証設定  
   - GitHub への push をトリガーにビルドを実行し、Docker を使ってコンテナイメージを作成
   - イメージを ECR に push する

<br>

<div align="center">

## こだわりポイント

</div>

- AWS CLI ではなく AWS コンソールを使い、構造を直感的に理解
- フロントエンドとバックエンドを別タスクにし疎結合化
- Cloud Map を利用して、コンテナ間通信にService Connectを採用  
  **メリット**:
   - シンプルなURLで通信可能 (`http://backend:5000`)
   - 自動負荷分散
   - 独立したスケーリング
   - 障害分離
- コストを抑えつつ幅広くAWSサービスを活用
- 開発環境にDevcontainer、Codespacesを採用  
環境構築の自動化により、端末に依存しない開発環境を確立し、開発スピードの向上を図った
- ECR への push を自動化することで、CI/CD の知識も学習できた

<br>

<div align="center">

## 苦労したところ

</div>

### ECS構築・デプロイ
- ALBがECSタスクを自動登録せず、原因調査に時間を要した  
  **自動登録条件**:
  - タスクがRUNNINGであること
  - `essential: true`コンテナが起動していること
  - ポートマッピングが正しいこと 
→ フロントエンドの起動条件設定が原因で削除することで解決したが、  
疎結合を実現するため Cloud Map を利用して、フロントエンド/バックエンドをタスク分離でデプロイ

### 接続設定の不足
- VPCエンドポイント不足  
  - S3 のみしか作成できていなかったため、エンドポイントを追加  
  - アーキテクチャ図で再整理
- Cognito JWKSはインターネット接続必須  
  - コスト効率を考え NAT ゲートウェイの代替としてパブリック IP 付与
- S3 の CORS 設定忘れ  
  - 本番 URL を追加設定  
  - パブリックに公開していないものにはセキュリティを考慮した設定があることを意識する

<br>
<div align="center">

## 今後の課題

</div>

- CI/CD
  - ビルド時にテスト実行
  - ECS サービスを自動デプロイ
- IaC管理
- CloudFront導入
- ECS Auto Scaling設定
- コンテナ内部の仕組み学習
- 全体構成を意識した構築順序の見直し
- アプリケーションを自作する
- チーム開発を意識したGit運用（ブランチ・プルリク）

</samp>