import discord
from discord.ext import commands
import clashroyale
import config

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cr = clashroyale.RoyaleAPI(config.CR_API_TOKEN)

    @commands.command()
    async def profil(self, ctx, tag: str):
        """Oyuncu profilini getirir"""
        if not tag.startswith("#"):
            tag = "#" + tag

        try:
            player = await self.cr.get_player(tag)
        except clashroyale.RequestError:
            await ctx.send("API'ye ulaşılamıyor.")
            return
        except clashroyale.NotFoundError:
            await ctx.send("Oyuncu bulunamadı.")
            return

        embed = discord.Embed(title=f"{player.name} ({player.tag})", color=0x00ff00)
        embed.add_field(name="Kupa", value=player.trophies)
        embed.add_field(name="Seviye", value=player.expLevel)
        embed.add_field(name="Klan", value=player.clan.name if player.clan else "Yok")
        embed.set_footer(text="Clash Royale API")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Profile(bot))
