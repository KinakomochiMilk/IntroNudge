# 日本語バージョン

# IntroNudge

Discordサーバーにおける「自己紹介ルール」の定着をサポートする、自動リマインドBotです。  
新規参加者が自己紹介を忘れてしまう問題をやさしく解決し、運営の負担を軽減します。

---

## 🧩 概要

IntroNudgeは、サーバーに参加したユーザーが一定期間内に自己紹介を行っているかを確認し、未実施の場合にリマインドを送信するBotです。

ロールの付与状況と、自己紹介内容に含まれるキーワードを組み合わせて判定するため、単純なチェックよりも柔軟かつ実用的に運用できます。

---

## ✨ 特徴

- **ゼロ・セットアップ設計**  
  既存のロールやチャンネルをそのまま利用可能。複雑な初期設定は不要です。

- **柔軟な判定ロジック**  
  - 指定ロールの有無（例：`member`）  
  - 自己紹介内の必須キーワード  
  の両方をチェックし、正確に判定します。

- **スラッシュコマンドで完結**  
  すべての設定はDiscord上で完結します。外部ファイルの編集は不要です。

- **運営に優しい設計**  
  自動リマインドにより、手動での声かけや確認作業を削減できます。

---

## 🚀 セットアップ手順

1. `main.py` を実行してBotを起動します  
2. Botを対象のDiscordサーバーに招待します  
3. 以下のコマンドで設定を行います：

### `/set_config`

以下の基本設定を行います：

- 対象ロール（例：member）
- 猶予日数（例：3日）
- 通知先チャンネル

### `/template`

自己紹介に含めるべき必須項目（キーワード）を設定します  

例：
- 年齢  
- 趣味  
- 一言  

---

## 🛠 動作イメージ

- 新規ユーザーが参加  
- 指定期間内に自己紹介を投稿  
  → 条件を満たしていれば何も起きません  
- 未投稿、または内容不十分  
  → Botが自動でリマインド  

---

## 📌 想定ユースケース

- 新規参加者の定着率向上  
- 自己紹介文化の定着  
- モデレーション負担の軽減  

---

## 📄 ライセンス

MIT License

---

# English Version

# IntroNudge

A Discord bot that automatically reminds new members to complete their self-introduction, helping server admins maintain community standards with minimal effort.

---

## 🧩 Overview

IntroNudge checks whether new members have completed their self-introduction within a specified time frame.  
If not, it sends a gentle reminder automatically.

It uses both role-based checks and keyword validation, making it more flexible and reliable than simple message detection.

---

## ✨ Features

- **Zero-setup design**  
  Works with your existing roles and channels—no complicated setup required.

- **Flexible validation logic**  
  Combines:
  - Role presence (e.g., `member`)
  - Required keywords in introduction

- **Fully configurable via slash commands**  
  No need to edit config files manually.

- **Admin-friendly automation**  
  Reduces manual moderation and follow-ups.

---

## 🚀 Setup Guide

1. Run `main.py` to start the bot  
2. Invite the bot to your Discord server  
3. Configure it using the following commands:

### `/set_config`

Set:

- Target role (e.g., member)
- Grace period (in days)
- Notification channel

### `/template`

Define required keywords for self-introductions  

Example:
- Age  
- Hobbies  
- Short message  

---

## 🛠 How It Works

- A new user joins the server  
- The bot waits for the configured period  
- If the user:
  - Has the required role  
  - AND includes required keywords  
  → No action is taken  
- Otherwise  
  → A reminder is sent automatically  

---

## 📌 Use Cases

- Improving onboarding experience  
- Encouraging community engagement  
- Reducing moderation workload  

---

## 📄 License

MIT License
