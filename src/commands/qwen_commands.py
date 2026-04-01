"""Comandos para interactuar con Qwen Code."""

import discord
from discord.ext import commands
from discord import app_commands

from ..qwen.executor import QwenExecutor
from ..qwen.parser import ResponseParser
from ..security.auth import is_authorized
from ..utils.logger import setup_logger

logger = setup_logger("QwenCommands")


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
        await confirm_msg.delete()
        
        # Discord tiene límite de 2000 caracteres por mensaje
        if len(response) > 2000:
            chunks = [response[i:i+2000] for i in range(0, len(response), 2000)]
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
