import discord
from discord import app_commands
from discord.ext import tasks, commands
import json
import os
import shlex  
from datetime import datetime, timezone

SETTINGS_FILE = "settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "target_role_id": None, 
        "wait_days": 30, 
        "notice_channel_id": None,
        "template_mode": "all",
        "keywords": []
    }

def save_settings(data):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        self.check_inactive_members.start()
        await self.tree.sync()

    @tasks.loop(hours=24)
    async def check_inactive_members(self):
        settings = load_settings()
        role_id = settings.get("target_role_id")
        wait_days = settings.get("wait_days")
        channel_id = settings.get("notice_channel_id")
        keywords = settings.get("keywords", [])
        mode = settings.get("template_mode", "all")

        if not (role_id and channel_id): return

        channel = self.get_channel(channel_id)
        if not channel: return
        
        
        
        valid_intro_users = set()
        async for msg in channel.history(limit=2000):
            if not msg.author.bot:
                content = msg.content
                if not keywords:
                    valid_intro_users.add(msg.author.id)
                    continue
                
                
                matches = [k for k in keywords if k in content]
                if mode == "all" and len(matches) == len(keywords):
                    valid_intro_users.add(msg.author.id)
                elif mode == "any" and len(matches) > 0:
                    valid_intro_users.add(msg.author.id)

        guild = channel.guild
        now = datetime.now(timezone.utc)
        targets = []

        for member in guild.members:
            if member.bot: continue
            has_role = any(r.id == role_id for r in member.roles)
            
            
            if not has_role and member.id not in valid_intro_users:
                if (now - member.joined_at).days >= wait_days:
                    targets.append(member.mention)

        if targets:
            await channel.send(f"リマインド：自己紹介が未完了、または形式が不完全な方がいます：\n" + " ".join(targets))

bot = MyBot()



@bot.tree.command(name="set_config", description="基本設定（ロール・日数・通知先）")
async def set_config(interaction: discord.Interaction, role: discord.Role, days: int, channel: discord.TextChannel):
    settings = load_settings()
    settings.update({"target_role_id": role.id, "wait_days": days, "notice_channel_id": channel.id})
    save_settings(settings)
    await interaction.response.send_message("基本設定を保存しました。", ephemeral=True)

@bot.tree.command(name="template", description="自己紹介の判定基準（テンプレ項目）を設定します")
@app_commands.describe(
    mode="all: 全項目必須, any: いずれか1つでOK",
    items='項目をスペース区切りで入力（例: 趣味 年齢 "一言メッセージ"）'
)
@app_commands.choices(mode=[
    app_commands.Choice(name="すべての項目が含まれる (all)", value="all"),
    app_commands.Choice(name="一つ以上の項目が含まれる (any)", value="any"),
])
async def set_template(interaction: discord.Interaction, mode: str, items: str):
    try:
        
        keyword_list = shlex.split(items)
    except Exception:
        await interaction.response.send_message("入力形式が正しくありません。\"\" の閉じ忘れ等を確認してください。", ephemeral=True)
        return

    settings = load_settings()
    settings["template_mode"] = mode
    settings["keywords"] = keyword_list
    save_settings(settings)

    msg = f"判定モード: {mode}\n設定キーワード: " + ", ".join([f"`{k}`" for k in keyword_list])
    await interaction.response.send_message(f"テンプレ設定を更新しました！\n{msg}", ephemeral=True)

bot.run("YOUR_TOKEN")
