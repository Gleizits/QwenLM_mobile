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


def _split_message(text: str, chunk_size: int = ResponseParser.MAX_MESSAGE_LENGTH) -> List[str]:
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def setup(bot: commands.Bot):
    """Registra los comandos de Qwen Code en el bot."""
    
    @bot.command(name="qwen")
    async def qwen_command(ctx: commands.Context, *, command: str):
        """
        Ejecuta un comando en Qwen Code.
        
        Uso: !qwen <tu comando>
        Ejemplo: !qwen crea un archivo llamado test.py
        """
        # Verificar autorización
        if not is_authorized(str(ctx.author.id)):
            await ctx.send("❌ No estás autorizado para usar este comando.")
            logger.warning(f"Usuario no autorizado intentó usar qwen: {ctx.author}")
            return
        
        # Confirmar recepción
        confirm_msg = await ctx.send(f"⏳ Procesando comando...")
        
        # Ejecutar comando
        executor = QwenExecutor()
        success, output = await executor.execute(command)
        
        # Formatear respuesta
        parser = ResponseParser()
        response = parser.format_response(success, output)
        
        # Enviar respuesta (posiblemente en múltiples mensajes si es muy largo)
        with suppress(discord.HTTPException):
            await confirm_msg.delete()
        
        if len(response) > ResponseParser.MAX_MESSAGE_LENGTH:
            chunks = _split_message(response)
            for chunk in chunks:
                await ctx.send(chunk)
        else:
            await ctx.send(response)
        
        logger.info(f"Comando qwen ejecutado por {ctx.author}: {command[:50]}...")
    
    @bot.command(name="qwen-status")
    async def qwen_status(ctx: commands.Context):
        """Verifica si Qwen Code está disponible."""
        if not is_authorized(str(ctx.author.id)):
            await ctx.send("❌ No estás autorizado para usar este comando.")
            return
        
        executor = QwenExecutor()
        
        # Intentar ejecutar un comando simple de versión
        success, output = await executor.execute("--version")
        
        if success:
            embed = discord.Embed(
                title="✅ Qwen Code Disponible",
                description=output.strip(),
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="❌ Qwen Code No Disponible",
                description=output.strip(),
                color=discord.Color.red()
            )
        
        await ctx.send(embed=embed)
        logger.info(f"qwen-status ejecutado por {ctx.author}")
