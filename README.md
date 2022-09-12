# vrc_quest_video_url

陣内システム(https://nextnex.com/) のようなシステムを AWS サーバレスで実現しようとした物

## 必要なもの

### yt-dlp

src\lambda\get_quest_url に yt-dlp(https://github.com/yt-dlp/yt-dlp) の配置が必要

### 環境変数

デプロイ時の環境変数に下記が必要

- LAMBDA_IAM
  - Lambda実行用ロールのARN

- DEPLOY_BUCKET
  - ServerlessFrameworkデプロイ先S3バケット


### Use

https://qst.akakitune87.net/q?url=[youtube_url]


### site

https://aki-lua87.github.io/vrc_quest_video_url/docs/