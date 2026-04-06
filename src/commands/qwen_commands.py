"""Comandos para interactuar con Qwen Code."""

from contextlib import suppress
from typing import List

import discord
from discord.ext import commands

from ..qwen.executor import QwenExecutor
from ..qwen.parser import ResponseParser
from ..security.auth import is_authorized
from ..utils.logger import setup_logger

logger = setup_logger("QwenCommands")

_UNAUTHORIZED_MSG = "❌ No estás autorizado para usar este comando."


def _split_message(text: str, chunk_size: int = ResponseParser.MAX_MESSAGE_LENGTH) -> List[str]:
    """Divide un mensaje largo en chunks para Discord."""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


async def _send_response(ctx: commands.Context, response: str) -> None:
    """Envía la respuesta, dividiéndola si excede el límite de Discord."""
    if len(response) <= ResponseParser.MAX_MESSAGE_LENGTH:
        await ctx.send(response)
        return
    for chunk in _split_message(response):
        await ctx.send(chunk)


def _build_status_embed(success: bool, output: str) -> discord.Embed:
    """Construye el embed de estado de Qwen Code."""
    if success:
        return discord.Embed(
            title="✅ Qwen Code Disponible",
            description=output.strip(),
            color=discord.Color.green(),
        )
    return discord.Embed(
        title="❌ Qwen Code No Disponible",
        description=output.strip(),
        color=discord.Color.red(),
    )


def setup(bot: commands.Bot):
    """Registra los comandos de Qwen Code en el bot."""
    executor = QwenExecutor()

    @bot.command(name="qwen")
    async def qwen_command(ctx: commands.Context, *, command: str):
        """
        Ejecuta un comando en Qwen Code.

        Uso: !qwen <tu comando>
        Ejemplo: !qwen crea un archivo llamado test.py
        """
        if not is_authorized(str(ctx.author.id)):
            await ctx.send(_UNAUTHORIZED_MSG)
            logger.warning(f"Usuario no autorizado intentó usar qwen: {ctx.author}")
            return

        confirm_msg = await ctx.send("⏳ Procesando comando...")
        success, output = await executor.execute(command)
        response = ResponseParser.format_response(success, output)

        with suppress(discord.HTTPException):
            await confirm_msg.delete()

        await _send_response(ctx, response)
        logger.info(f"Comando qwen ejecutado por {ctx.author}: {command[:50]}...")

    @bot.command(name="qwen-status")
    async def qwen_status(ctx: commands.Context):
        """Verifica si Qwen Code está disponible."""
        if not is_authorized(str(ctx.author.id)):
            await ctx.send(_UNAUTHORIZED_MSG)
            return

        success, output = await executor.execute("--version")
        await ctx.send(embed=_build_status_embed(success, output))
        logger.info(f"qwen-status ejecutado por {ctx.author}")