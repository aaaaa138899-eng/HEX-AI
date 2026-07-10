import discord
from discord.ext import commands
import google.generativeai as genai
import os

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ai(ctx, *, question):
    await ctx.typing()

    response = model.generate_content(
        f"""
أنت المساعد الرسمي لسيرفر HEX.

قوانينك:
- رد بالعربية إلا إذا طلب المستخدم غير ذلك.
- كن مختصرًا.
- لا تسب.
- لا تخرج عن الآداب.
- إذا كان السؤال عن السيرفر فأجب كمساعد رسمي.
- إذا كان السؤال عام فأجب كذكاء اصطناعي.

السؤال:
{question}
"""
    )

    await ctx.reply(response.text)

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author

    embed = discord.Embed(
        title=f"معلومات {member}",
        color=0x5865F2
    )

    embed.add_field(
        name="تاريخ إنشاء الحساب",
        value=member.created_at.strftime("%Y-%m-%d"),
        inline=False
    )

    embed.add_field(
        name="دخول السيرفر",
        value=member.joined_at.strftime("%Y-%m-%d"),
        inline=False
    )

    embed.add_field(
        name="الرتبة الأعلى",
        value=member.top_role.name,
        inline=False
    )

    await ctx.send(embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"))
