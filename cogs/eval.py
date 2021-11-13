from time import time
from disnake.ext import commands
import sys
import os
from inspect import getsource
import disnake as discord

class EvalCommand(commands.Cog):
    def __init__(self, Yui):
        self.Yui = Yui

    class QuitButton(disnake.ui.View):
        def __init__(
            self,
            ctx: Union[Context, ApplicationCommandInteraction],
            *,
            timeout: float = 180.0,
            delete_after: bool = False
        ):
            super().__init__(timeout=timeout)
            self.ctx = ctx
            self.delete_after = delete_after
            self.message = None
  
  
      @commands.command(name='eval', aliases=['e'])
        async def _eval(self, ctx: Context, *, content=None):
            """Evaluate code."""

            if content is None:
                return await ctx.send("Please give code that you want to evaluate!")

            code = clean_code(content)

            local_variables = {
                "disnake": disnake,
                "commands": commands,
                "_bot": self.bot,
                "_ctx": ctx,
                "_channel": ctx.channel,
                "_author": ctx.author,
                "_guild": ctx.guild,
                "_message": ctx.message,
                "colours": Colours
            }
            start = time.perf_counter()

            stdout = io.StringIO()
            try:
                 with contextlib.redirect_stdout(stdout):
                     exec(
                        f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
                    )

                    obj = await local_variables["func"]()
                    result = f"{stdout.getvalue()}\n-- {obj}\n"
            except Exception as e:
                result = "".join(format_exception(e, e, e.__traceback__))

            end = time.perf_counter()
            took = f"{end-start:.3f}"
            if took == "0.000":
                took = f"{end-start:.7f}"

            if len(result) >= 4000:
                pager = TextPage(
                    ctx,
                    [result[i: i + 4000] for i in range(0, len(result), 4000)],
                    footer=f'Took {took}s',
                    quit_delete=True
                )
                return await pager.start()
            em = disnake.Embed(description=f'```py\n{result}\n```')
            em.set_footer(text=f'Took {took}s')
            view = QuitButton(ctx)
            view.message = await ctx.send(embed=em, view=view)

        
def setup(Yui):
  Yui.add_cog(EvalCommand(Yui))
