from redbot.core import commands

from leveler.abc import CompositeMetaClass


class LevelSetBaseCMD(metaclass=CompositeMetaClass):
    @commands.group(name="llvlset")
    async def llvlset(self, ctx):
        """Profile configuration Options."""
        pass
