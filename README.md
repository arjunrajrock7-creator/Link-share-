# <p align="center">🌈 ✨ 𝗦𝗨𝗣𝗘𝗥 𝗟𝗜𝗡𝗞 𝗦𝗛𝗔𝗥𝗘 𝗕𝗢𝗧 ✨ 🌈</p>

<p align="center">
  <img src="https://img.shields.io/badge/Speed-LightSpeed-red?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/UI-Anime%20Themed-orange?style=for-the-badge&logo=appveyor" />
  <img src="https://img.shields.io/badge/Python-3.10+-yellow?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Database-MongoDB-green?style=for-the-badge&logo=mongodb" />
  <img src="https://img.shields.io/badge/Security-Auto%20Revoke-blue?style=for-the-badge&logo=shield" />
  <img src="https://img.shields.io/badge/Status-Ultra%20Stable-indigo?style=for-the-badge&logo=render" />
</p>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<p align="center"><b>🔥 𝗨𝗹𝘁𝗿𝗮 𝗙𝗮𝘀𝘁, 𝗭𝗲𝗿𝗼 𝗟𝗮𝗴, 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗔𝗻𝗶𝗺𝗲 𝗘𝘅𝗽𝗲𝗿𝗶𝗲𝗻𝗰𝗲 🔥</b></p>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🎋 𝗙𝗘𝗔𝗧𝗨𝗥𝗘𝗦
- ⚡ **Light Speed Response**: Powered by Pyrogram + Motor for millisecond execution.
- 📡 **Unlimited Channels**: Manage as many channels as you need with ease.
- 🔗 **Smart Link Generator**: Generate Normal and Join Request links instantly.
- ⏱️ **Auto Revoke system**: Links expire automatically after 5 minutes for copyright safety.
- 📦 **Bulk Generation**: Interactive checkbox-style UI for generating multiple links.
- 🔐 **Force Subscription**: Integrated FSub system to grow your audience.
- 👨‍💻 **Dynamic Admin Panel**: Add/Remove admins on the fly via commands.
- 📢 **Robust Broadcast**: Send messages to all users with real-time progress tracking.
- 📊 **Detailed Stats**: Monitor user count, channel count, and link generation history.
- 🦊 **Anime Themed UI**: Beautiful Unicode styling and anime-themed messages everywhere.

---

## 🛠️ 𝗗𝗘𝗣𝗟𝗢𝗬𝗠𝗘𝗡𝗧 𝗩𝗔𝗥𝗜𝗔𝗕𝗟𝗘𝗦 (𝗘𝗡𝗩)

| Variable | Description | Default |
|:---|:---|:---|
| `API_ID` | 🔴 **REQUIRED**: Your Telegram API ID | - |
| `API_HASH` | 🟠 **REQUIRED**: Your Telegram API Hash | - |
| `BOT_TOKEN` | 🟡 **REQUIRED**: Your Telegram Bot Token | - |
| `MONGO_DB_URI` | 🟢 **REQUIRED**: MongoDB Connection URI | - |
| `OWNER_ID` | 🔵 **REQUIRED**: Your Telegram User ID | - |
| `DB_NAME` | 🟣 Database Name | `SuperLinkShareBot` |
| `ADMINS` | ⚪ Space-separated Admin IDs | - |
| `FSUB_ENABLED` | 🔐 Enable Force Sub (`True`/`False`) | `True` |
| `PORT` | 🌐 Port for health checks | `8080` |

---

## 🚀 𝗗𝗘𝗣𝗟𝗢𝗬𝗠𝗘𝗡𝗧 𝗚𝗨𝗜𝗗𝗘 (𝟭𝟬𝟬% 𝗦𝗨𝗖𝗖𝗘𝗦𝗦)

### 🐳 𝗗𝗲𝗽𝗹𝗼𝘆 𝘄𝗶𝘁𝗵 𝗗𝗼𝗰𝗸𝗲𝗿 (𝗥𝗲𝗰𝗼𝗺𝗺𝗲𝗻𝗱𝗲𝗱)
```bash
# Clone the repository
git clone https://github.com/abhinai2244/LINK-SHAREBOT.git
cd LINK-SHAREBOT

# Edit .env file
nano .env

# Build and Start
docker-compose up -d --build
```

### ☁️ 𝗗𝗲𝗽𝗹𝗼𝘆 𝘁𝗼 𝗥𝗲𝗻𝗱𝗲𝗿.𝗰𝗼𝗺
1. **Fork** this repository.
2. Create a new **Web Service** on Render.
3. Connect your fork.
4. **Environment**: `Docker` (Select Docker for 100% success rate with TgCrypto).
5. **Advanced**: Add all variables from the table above.
6. **Deploy!** 🚀

### 🚂 𝗗𝗲𝗽𝗹𝗼𝘆 𝘁𝗼 𝗛𝗲𝗿𝗼𝗸𝘂
1. Click **Deploy to Heroku**.
2. Fill in the variables.
3. Enable `worker` dyno.

---

## 🎮 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦 𝗟𝗜𝗦𝗧

### 👤 **User Commands**
- `/start` ➻ Start the anime journey.
- `/help` ➻ View commands and usage.
- `/channels` ➻ See your authorized channels.
- `/genlink <url>` ➻ Securely encode any external URL.

### 👨‍💻 **Admin Commands**
- `/addchannel` ➻ Add new channel (-100xxxx).
- `/removechannel` ➻ Remove channel from DB.
- `/bulkgen` ➻ Start bulk generation flow.
- `/requeston`/`off` ➻ Toggle join request approval.
- `/fsub_add`/`remove` ➻ Manage force sub channels.
- `/addadmin`/`rmadmin` ➻ Manage bot admins.
- `/broadcast` ➻ Send global announcements.
- `/stats` / `/status` ➻ System health & metrics.

---

## 🏮 𝗖𝗥𝗘𝗗𝗜𝗧𝗦
- ⚡ **Owner**: **⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛⚡**
- 🛠️ **Developer**: **[Sahil](https://github.com/abhinai2244)**
- 🎋 **Contributors**: Obito, Yato, RexBots

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<p align="center"><b>ᴍᴀᴅᴇ ᴡɪᴛʜ ❤️ ʙʏ ⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛⚡</b></p>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
