import discord
from discord.ext import commands
import clashroyale

# Config dosyasından tokenları alacağız, önce oluşturacağız.
from config import DISCORD_TOKEN, CR_API_TOKEN

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='.', intents=intents)

# Clash Royale API bağlantısı
cr = clashroyale.RoyaleAPI(CR_API_TOKEN)

@bot.event
async def on_ready():
    print(f"{bot.user} olarak giriş yapıldı!")

@bot.command()
async def profil(ctx, tag):
    try:
        # Clash Royale oyuncu bilgisi çekiliyor
        player = cr.get_player(tag)
        embed = discord.Embed(title=f"{player.name} Profili", color=discord.Color.blue())
        embed.add_field(name="Kupa", value=player.trophies)
        embed.add_field(name="Level", value=player.expLevel)
        embed.add_field(name="Klan", value=player.clan.name if player.clan else "Yok")
        await ctx.send(embed=embed)
    except clashroyale.RequestError as e:
        await ctx.send(f"API hatası: {e}")
    except Exception as e:
        await ctx.send(f"Hata oluştu: {e}")

bot.run(DISCORD_TOKEN)
