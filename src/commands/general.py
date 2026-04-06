"""Comandos generales del bot."""

import discord
from discord.ext import commands

from ..utils.logger import setup_logger

logger = setup_logger("GeneralCommands")

_HELP_FIELDS = [
    (
        "Comandos Generales",
        (
            "`!ping` - Verifica latencia del bot\n"
            "`!help` - Muestra esta ayuda\n"
            "`!status` - Estado del bot"
        ),
    ),
    (
        "Comandos Qwen Code",
        (
            "`!qwen <comando>` - Ejecuta un comando en Qwen Code\n"
            "`!qwen-status` - Verifica si Qwen Code está disponible"
        ),
    ),
    (
        "Comandos de Administración",
        (
            "`!whitelist add @usuario` - Agrega usuario a whitelist\n"
            "`!whitelist remove @usuario` - Remueve usuario de whitelist\n"
            "`!whitelist list` - Lista usuarios autorizados"
        ),
    ),
]


def _build_help_embed() -> discord.Embed:
    """Construye el embed de ayuda."""
    embed = discord.Embed(title="🤖 QwenLM Mobile Bot - Ayuda", color=discord.Color.blue())
    for name, value in _HELP_FIELDS:
        embed.add_field(name=name, value=value, inline=False)
    embed.set_footer(text="Usa !help para más información")
    return embed


def _build_status_embed(bot: commands.Bot) -> discord.Embed:
    """Construye el embed de estado del bot."""
    embed = discord.Embed(title="📊 Estado del Bot", color=discord.Color.green())
    latency = round(bot.latency * 1000)
    total_members = sum(len(g.members) for g in bot.guilds)

    embed.add_field(name="Bot", value=f"✅ En línea\nLatencia: {latency}ms", inline=False)
    embed.add_field(name="Servidores", value=str(len(bot.guilds)), inline=True)
    embed.add_field(name="Usuarios", value=str(total_members), inline=True)
    return embed


def setup(bot: commands.Bot):
    """Registra los comandos generales en el bot."""

    @bot.command(name="ping")
    async def ping(ctx: commands.Context):
        """Verifica si el bot está respondiendo."""
        latency = round(bot.latency * 1000)
        await ctx.send(f"🏓 Pong! Latencia: {latency}ms")
        logger.info(f"Comando ping ejecutado por {ctx.author}")

    @bot.command(name="help")
    async def help_command(ctx: commands.Context):
        """Muestra la ayuda del bot."""
        await ctx.send(embed=_build_help_embed())
        logger.info(f"Comando help ejecutado por {ctx.author}")

    @bot.command(name="status")
    async def status(ctx: commands.Context):
        """Muestra el estado del bot."""
        await ctx.send(embed=_build_status_embed(bot))
        logger.info(f"Comando status ejecutado por {ctx.author}")