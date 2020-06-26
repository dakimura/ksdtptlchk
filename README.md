# ksdtptlchk

https://koto-kosodate-portal.jp/smf/mizube/general/refresh_cal.php?center_cd=60
に空きが出たらメールで通知する

## usage
```bash
$ make build
$ docker run ksdtptlchk:latest python ksdtptlchk/app.py \
--from_email=[あなたのメールアドレス] \
--password=[あなたのメールアカウントのパスワード. gmailアカウントのパスワードなど。gmailで２段階認証などを設定している場合はApplication Specific Passwordが必要なことに注意)] \
--to_email=[結果を通知するメールアドレス] \
--smtp_addr=[smtpサーバのホスト名(e.g. smtp.gmail.com)] \
--smtp_port=[smtpサーバのポート番号(e.g. 465)] \
```