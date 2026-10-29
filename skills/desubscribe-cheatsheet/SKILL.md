---
name: desubscribe-cheatsheet
description: 'Use when the user wants to cancel paid SaaS subscriptions and switch to free self-hosted open-source alternatives: Notion, Slack, Figma, Dropbox, 1Password, Airtable and more, each with a one-command Docker install and the yearly saving per swap.'
---

# Desubscribe 💸 一页速查：SaaS 免费/自托管替代品

> 你每个月交的订阅费，有一半是在交"冤枉钱"。
> 下面 10 组替代，全部开源、全部可自托管，**每人每年省约 $1,260**。

| # | 你在交钱的 SaaS | 约多少钱/年 | 免费替代品 | 一条命令跑起来 | 每年省 |
|---|---|---|---|---|---|
| 1 | Notion Plus | $120 | [AppFlowy](https://appflowy.com) / [Anytype](https://anytype.io) | `git clone https://github.com/AppFlowy-IO/AppFlowy-SelfHost-Commercial && cd AppFlowy-SelfHost-Commercial && cp deploy.env .env && docker compose up -d` | **$120** |
| 2 | Slack Pro | $87 | [Mattermost](https://mattermost.com) | `git clone https://github.com/mattermost/docker && cd docker && docker compose -f docker-compose.yml -f docker-compose.without-nginx.yml up -d` | **$87** |
| 3 | Figma Professional | $144 | [Penpot](https://penpot.app) | `curl -o docker-compose.yaml https://raw.githubusercontent.com/penpot/penpot/main/docker/images/docker-compose.yaml && docker compose -p penpot -f docker-compose.yaml up -d` | **$144** |
| 4 | Google One 2TB | $100 | [Immich](https://immich.app) | `wget -O docker-compose.yml https://github.com/immich-app/immich/releases/latest/download/docker-compose.yml && wget -O .env https://github.com/immich-app/immich/releases/latest/download/example.env && docker compose up -d` | **$100** |
| 5 | 1Password 个人版 | $48 | [Vaultwarden](https://github.com/dani-garcia/vaultwarden) | `docker run -d --name vaultwarden -v /vw-data/:/data/ --restart unless-stopped -p 80:80 vaultwarden/server:latest` | **$48** |
| 6 | Dropbox Plus | $120 | [Nextcloud](https://nextcloud.com) | `docker run -d --name nextcloud -p 8080:80 -v nextcloud-data:/var/www/html --restart unless-stopped nextcloud` | **$120** |
| 7 | Airtable Team | $240 | [NocoDB](https://nocodb.com) | `docker run -d --name noco -v "$(pwd)"/nocodb:/usr/app/data/ -p 8080:8080 --restart unless-stopped nocodb/nocodb:latest` | **$240** |
| 8 | Trello Premium | $120 | [Wekan](https://wekan.github.io) | 见下方两条命令（需 MongoDB） | **$120** |
| 9 | Zoom Pro | $150 | [Jitsi Meet](https://jitsi.org) | `git clone https://github.com/jitsi/docker-jitsi-meet && cd docker-jitsi-meet && cp env.example .env && docker compose up -d` | **$150** |
| 10 | Evernote Personal | $130 | [Joplin](https://joplinapp.org) | `docker run -d --name joplin -p 22300:22300 -e APP_PORT=22300 -e APP_BASE_URL=http://localhost:22300 --restart unless-stopped joplin/server:latest` | **$130** |

**合计：约 $1,260 /人/年** —— 一台 $5/月的小 VPS（$60/年）全装下，净省 $1,200。

## Wekan 安装（两条命令）

```bash
docker network create wekan-net
docker run -d --name wekan-db --network wekan-net --restart=always mongo:5
docker run -d --name wekan --network wekan-net --restart=always \
  -e MONGO_URL=mongodb://wekan-db:27017/wekan \
  -e ROOT_URL=http://localhost:8080 -p 8080:8080 wekanteam/wekan
```

## 说明

- 价格为 2026 年 10 月核实的官方定价（年付口径），标"约"；订阅价格会变，动手前请以官网为准。
- 自托管需要一台服务器（旧电脑、树莓派或云 VPS 都行），数据归你自己。
- AppFlowy 自托管新版走 `AppFlowy-SelfHost-Commercial` 仓库（含免费层）；Anytype 是本地优先、P2P 同步，连服务器都不用。
- Joplin 一条命令默认用 SQLite，正式用建议换 Postgres（见 Joplin 官方文档）。

## 链接

- 完整中文版 → [README.md](README.md) ｜ 西班牙语 → [README.es.md](README.es.md) ｜ 葡萄牙语 → [README.pt.md](README.pt.md)

MIT License © 2026 Guangyi Zhao
