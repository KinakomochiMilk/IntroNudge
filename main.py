import discord
from discord import app_commands
from discord.ext import tasks, commands
import json
import os
import shlex
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()  

TOKEN = os.getenv("DISCORD_TOKEN") or "ここにトークンを直接入力"

SETTINGS_FILE = "settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
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

class IntroNudge(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        self.check_loop.start()
        await self.tree.sync()

    @tasks.loop(hours=24)
    async def check_loop(self):
        s = load_settings()
        if not (s["target_role_id"] and s["notice_channel_id"]):
            return
        
        channel = self.get_channel(s["notice_channel_id"])
        if not channel:
            return

        valid_users = set()
        
        async for msg in channel.history(limit=2000):
            if not msg.author.bot:
                content = msg.content
                keywords = s.get("keywords", [])
                mode = s.get("template_mode", "all")
                
                if not keywords:
                    valid_users.add(msg.author.id)
                    continue

                matches = [k for k in keywords if k in content]
                if (mode == "all" and len(matches) == len(keywords)) or \
                   (mode == "any" and len(matches) > 0):
                    valid_users.add(msg.author.id)

        now = datetime.now(timezone.utc)
        remind_list = []
        
        for m in channel.guild.members:
            if m.bot: continue
            
            
            has_role = any(r.id == s["target_role_id"] for r in m.roles)
            
            
            if not has_role and m.id not in valid_users:
                days_elapsed = (now - m.joined_at).days
                if days_elapsed >= s["wait_days"]:
                    remind_list.append(m.mention)

        if remind_list:
            await channel.send(
                f"【IntroNudge】サーバー参加から{s['wait_days']}日以上経過していますが、"
                f"自己紹介（または規定のロール付与）が確認できていない方へリマインドです：\n"
                + " ".join(remind_list)
            )

bot = IntroNudge()

@bot.tree.command(name="intro_config", description="基本設定（ロール・日数・通知先）を行います")
@app_commands.describe(role="判定基準ロール", days="猶予日数", channel="通知先チャンネル")
async def intro_config(interaction: discord.Interaction, role: discord.Role, days: int, channel: discord.TextChannel):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("管理者権限が必要です。", ephemeral=True)
        return
    
    s = load_settings()
    s.update({"target_role_id": role.id, "wait_days": days, "notice_channel_id": channel.id})
    save_settings(s)
    await interaction.response.send_message(f"設定を保存しました。\nロール: {role.name} / 日数: {days}日", ephemeral=True)

@bot.tree.command(name="intro_template", description="自己紹介の判定基準（テンプレ項目）を設定します")
@app_commands.choices(mode=[
    app_commands.Choice(name="すべて必須 (all)", value="all"),
    app_commands.Choice(name="いずれか必須 (any)", value="any"),
])
async def intro_template(interaction: discord.Interaction, mode: str, items: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("管理者権限が必要です。", ephemeral=True)
        return

    try:
        k_list = shlex.split(items)
        s = load_settings()
        s.update({"template_mode": mode, "keywords": k_list})
        save_settings(s)
        await interaction.response.send_message(f"テンプレ更新完了！\nモード: {mode}\n項目: {', '.join(k_list)}", ephemeral=True)
    except:
        await interaction.response.send_message("パースエラーが発生しました。引用符の閉じ忘れがないか確認してください。", ephemeral=True)

if __name__ == "__main__":
    if TOKEN == "ここにトークンを直接入力":
        print("エラー: トークンが設定されていません。main.pyを書き換えるか、.envファイルを作成してください。")
    else:
        bot.run(TOKEN)
