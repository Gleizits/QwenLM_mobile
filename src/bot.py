"""Bot de Discord para controlar Qwen Code remotamente."""

import traceback

import discord
from discord.ext import commands

from src.config import DISCORD_TOKEN, ADMIN_USER_ID
from src.commands.general import setup as setup_general
from src.commands.qwen_commands import setup as setup_qwen
from src.security.auth import (
    is_authorized,
    add_authorized_user,
    remove_authorized_user,
    get_authorized_users,
)
from src.utils.logger import setup_logger

logger = setup_logger("DiscordBot")

_UNAUTHORIZED_MSG = "❌ No estás autorizado para usar este bot."
_ADMIN_ONLY_MSG = "❌ Solo el administrador puede usar este comando."

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


@bot.event
async def on_ready():
    """Se ejecuta cuando el bot está listo."""
    try:
        logger.info(f"Bot conectado como {bot.user} (ID: {bot.user.id})")

        try:
            synced = await bot.tree.sync()
            logger.info(f"Sincronizados {len(synced)} slash commands")
        except Exception as e:
            logger.error(f"Error sincronizando slash commands: {e}")

        print(f"✅ {bot.user} está en línea!")
        print(f"   ID: {bot.user.id}")
        print("-" * 50)
        print("   Usa !help para ver comandos")
        print("-" * 50)
    except Exception as e:
        logger.error(f"Error en on_ready: {e}")
        traceback.print_exc()


@bot.event
async def on_command_error(ctx: commands.Context, error: Exception):
    """Maneja errores de comandos."""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Comando no encontrado. Usa `!help` para ver la lista.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Falta un argumento: `{error.param.name}`")
    else:
        logger.error(f"Error en comando {ctx.command}: {error}")
        await ctx.send(f"❌ Error: {str(error)}")


@bot.event
async def on_message(message: discord.Message):
    """Procesa los mensajes."""
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        if not is_authorized(str(message.author.id)):
            await message.channel.send(_UNAUTHORIZED_MSG)
            logger.warning(f"Mensaje DM no autorizado de {message.author}")
            return

    await bot.process_commands(message)


async def _handle_whitelist_add(ctx: commands.Context, member: discord.Member) -> None:
    if member is None:
        await ctx.send("❌ Debes mencionar a un usuario.")
        return
    if add_authorized_user(str(member.id)):
        await ctx.send(f"✅ {member.mention} agregado a la whitelist.")
        logger.info(f"Usuario {member} agregado a whitelist por {ctx.author}")
    else:
        await ctx.send(f"⚠️ {member.mention} ya está en la whitelist.")


async def _handle_whitelist_remove(ctx: commands.Context, member: discord.Member) -> None:
    if member is None:
        await ctx.send("❌ Debes mencionar a un usuario.")
        return
    if remove_authorized_user(str(member.id)):
        await ctx.send(f"✅ {member.mention} removido de la whitelist.")
        logger.info(f"Usuario {member} removido de whitelist por {ctx.author}")
    else:
        await ctx.send(f"⚠️ {member.mention} no está en la whitelist.")


async def _handle_whitelist_list(ctx: commands.Context) -> None:
    users = get_authorized_users()
    if not users:
        await ctx.send("📋 No hay usuarios en la whitelist.")
        return

    user_mentions = []
    for user_id in users:
        try:
            user = await bot.fetch_user(int(user_id))
            user_mentions.append(user.mention)
        except (discord.NotFound, discord.HTTPException, ValueError):
            user_mentions.append(f"`{user_id}`")

    await ctx.send("📋 **Usuarios autorizados:**\n" + "\n".join(user_mentions))


@bot.command(name="whitelist")
async def whitelist_command(
    ctx: commands.Context,
    action: str,
    member: discord.Member = None,
):
    """
    Gestiona la whitelist de usuarios.

    Uso:
    !whitelist add @usuario - Agrega usuario
    !whitelist remove @usuario - Remueve usuario
    !whitelist list - Lista usuarios
    """
    if str(ctx.author.id) != ADMIN_USER_ID:
        await ctx.send(_ADMIN_ONLY_MSG)
        return

    handlers = {
        "add": lambda: _handle_whitelist_add(ctx, member),
        "remove": lambda: _handle_whitelist_remove(ctx, member),
        "list": lambda: _handle_whitelist_list(ctx),
    }

    handler = handlers.get(action.lower())
    if handler:
        await handler()
    else:
        await ctx.send("❌ Uso: `!whitelist <add|remove|list> [@usuario]`")


setup_general(bot)
setup_qwen(bot)


def run():
    """Inicia el bot."""
    if not DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN no encontrado en .env")
        print("❌ Error: DISCORD_TOKEN no encontrado en .env")
        print("   Copia .env.example a .env y agrega tu token.")
        input("Presione Enter para salir...")
        return

    try:
        logger.info("Iniciando bot...")
        print("✅ Iniciando bot...")
        bot.run(DISCORD_TOKEN)
    except discord.LoginFailure:
        logger.error("Token de Discord inválido")
        print("❌ Error: Token de Discord inválido")
        print("   Verifica tu token en .env")
        input("Presione Enter para salir...")
    except Exception as e:
        logger.error(f"Error al iniciar: {e}")
        print(f"❌ Error al iniciar: {e}")
        input("Presione Enter para salir...")


if __name__ == "__main__":
    run()