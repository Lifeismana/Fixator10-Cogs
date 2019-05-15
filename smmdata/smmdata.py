import aiohttp
from discord import Embed
from redbot.core import commands
from redbot.core.i18n import Translator, cog_i18n

from .smmbookmark import Level, SMMB_BASE_URL

_ = Translator("SMMData", __file__)

BOOKMARKS_ICON_URL = (
    f"{SMMB_BASE_URL}/assets/favicon/icon76-08f927f066250b84f628e92e0b94f58d.png"
)


@cog_i18n(_)
class SMMData(commands.Cog):
    """Super Mario Maker-related data"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

    @commands.group(autohelp=True)
    async def smm(self, ctx):
        """Get Super Mario Maker-related data"""
        pass

    @smm.command(usage="<level ID>")
    async def level(self, ctx, lvl: Level):
        """Get info about SMM level"""
        embed = Embed(
            title=lvl.title,
            color=lvl.difficulty_color,
            description=lvl.difficulty,
            timestamp=lvl.created_at,
        )
        embed.add_field(name="\N{White Medium Star} " + _("Stars"), value=lvl.stars)
        embed.add_field(name="\N{Footprints} " + _("Unique Players"), value=lvl.players)
        embed.add_field(name=_("Share count"), value=lvl.shares)
        embed.add_field(
            name=_("Clears"), value=f"{lvl.clears}/{lvl.attempts} ({lvl.clear_rate}%)"
        )
        if lvl.first_clear_name:
            embed.add_field(
                name=_("First clear"),
                value=f"[{lvl.first_clear_name}]({lvl.first_clear_url})",
            )
        if lvl.best_player_name:
            embed.add_field(
                name=_("World record"),
                value=_("{time} by [{player}]({url})").format(
                    time=lvl.best_player_time,
                    player=lvl.best_player_name,
                    url=lvl.best_player_url,
                ),
            )
        embed.set_thumbnail(url=lvl.preview)
        embed.set_image(url=lvl.map)
        embed.set_author(
            name=lvl.creator, url=lvl.creator_url, icon_url=lvl.creator_img
        )
        embed.set_footer(text=lvl.tag or Embed.Empty, icon_url=BOOKMARKS_ICON_URL)
        await ctx.send(embed=embed)