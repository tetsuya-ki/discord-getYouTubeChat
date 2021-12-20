
# このBotについて

- YouTubeの動画IDを`.env`の`VIDEO_ID`に設定しBotを起動すると、ギルドの指定したチャンネルに内容を投稿します。
  - 設定されていない場合、何もしません($setでvideo_idを設定してください)

## 機能について

### コマンド

#### $skip: チャットをリセットし、読み込む

- チャットが早すぎて読み込みが遅れた場合に使います
  - 一気に投稿するように変更したので、多分使う機会はないはず

#### $set <video_id>: 読み込み先を別のVideoIDに変更

- 指定されたvideo_idを読み込みます
- (非同期処理のため、前回まで実行していた処理は急には止まれません。時間をおいて止まります)

#### $stop: 処理を停止

- 処理を停止します

## 環境構築について

### 前提

1. pythonの3系がインストールされていること
2. git, poetryがインストールされていること
3. Discordの管理者（もしくは、Webhookを作成してもらえる立場）であること
4. Botに紐づくギルドは1である必要があります(複数あった場合の対応をしていないため)

### 前準備

1. GitHubから`git clone`する
   1. `git clone https://github.com/tetsuya-ki/discord-getyoutubechat.git`
   2. `cd discord-getyoutubechat`し、実行ディレクトリにカレントディレクトリを変更しておく
2. discordの開発者サイトに行き、Botを作成する
   1. こちらのサイトを参照: <https://discordpy.readthedocs.io/ja/latest/discord.html>
   2. 権限は`send messages`のみでOK
3. DiscordのギルドにBotを登録する
   1. 招待リンクを作成し、それをクリックすると招待画面に行くので目的のギルドに登録する
   2. Botの追加はサーバー管理者ロールを保持している必要アリ(権限がない場合、ダイアログにギルドが表示されない、かも)

### 準備

#### 共通手順

1. 必要な情報を保管する、`.env`ファイルを作成
   1. `.env.sample`をコピーし、名前を`.env`にする
   2. `.env`の「YOUR_DISCORD_TOKEN_IS_HERE」に、**Botのトークンを入力する**
   3. `.env`の「DISCORD_CHANNEL_ID_IS_HERE」に**送信先のDiscordのチャンネルIDを入力する**
   4. `.env`の「YOUR_YOUTUBE_VIDEO_ID_IS_HERE」に、**YouTubeの動画IDを入力**し、保存する
      1. たとえば、「<https://www.youtube.com/watch?v=dVjfdgGygo0>」の場合、`dVjfdgGygo0`が動画ID
   5. (オプション)`.env`の「CSV_OUTPUT_FLAG」に、csvとして保存したくない場合、`FALSE`を記載(環境変数が存在しない場合もFALSE扱い)

#### venvを使う手順

1. pythonの仮想環境を作成
   1. `python3 -m venv venv`
2. 必要なパッケージを`requirements.txt`からインストール
   1. `pip install -r requirements.txt`

3. Botの起動/停止

- `python discord-getYoutubeChat.py`で起動する(`INFO:Test:bot ready.`と記載されたら起動成功)

```sh
(venv) mac-mini:discord-getYoutubeChat mac_mini$ python discord-getYoutubeChat.py WARNING:discord.client:PyNaCl is not installed, voice will NOT be supported
INFO:discord.client:logging in using static token
...（中略）...
INFO:discord-getYouTubeChat:We have logged in as xxxxxxx
```

- `Ctrl + C`: 停止(YouTubeでコメントを拾ったタイミングで、Discordに投稿せず終了される)

#### poetryを使う手順

1. poetryでモジュールのインストール(poetry.lockのものをインストール)
   1. `poetry install`
2. Botの起動/停止

- `poetry run python discord-getYoutubeChat.py`で起動する(`INFO:Test:bot ready.`と記載されたら起動成功)

```sh
(venv) mac-mini:discord-getYouTubeChat mac_mini$ poetry run python discord-getYouTubeChat.py 
WARNING:discord.client:PyNaCl is not installed, voice will NOT be supported
INFO:discord-getYouTubeChat:cogを読むぞ！
INFO:cogs.getYouTubeChatCog:GetYouTubeChatCogを読み込む！
INFO:discord.client:logging in using static token
...（中略）...
INFO:discord-getYouTubeChat:We have logged in as xxxxxxx
```

- `Ctrl + C`: 停止(YouTubeでコメントを拾ったタイミングで、Discordに投稿せず終了される)