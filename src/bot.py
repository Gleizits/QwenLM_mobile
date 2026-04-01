"""Bot de Discord para controlar Qwen Code remotamente."""

import discord
from discord.ext import commands
from discord.app_commands import AppCommandError

# Cambiamos los '.' por 'src.'
from src.config import DISCORD_TOKEN, ADMIN_USER_ID
from src.commands.general import setup as setup_general
from src.commands.qwen_commands import setup as setup_qwen
from src.security.auth import is_authorized, add_authorized_user
from src.utils.logger import setup_logger

logger = setup_logger("DiscordBot")

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Crear bot
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    """Se ejecuta cuando el bot está listo."""
    try:
        logger.info(f"Bot conectado como {bot.user}")
        logger.info(f"ID: {bot.user.id}")
        
        # Sincronizar slash commands
        try:
            synced = await bot.tree.sync()
            logger.info(f"Sincronizados {len(synced)} slash commands")
        except Exception as e:
            logger.error(f"Error sincronizando slash commands: {e}")
        
        print(f"✅ {bot.user} está en línea!")
        print(f"   ID: {bot.user.id}")
        print("-" * 50)
        print(f"   Usa !help para ver comandos")
        print("-" * 50)
    except Exception as e:
        logger.error(f"Error en on_ready: {e}")
        print(f"❌ Error en on_ready: {e}")
        import traceback
        traceback.print_exc()


@bot.event
async def on_command_error(ctx: commands.Context, error):
    """Maneja errores de comandos."""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Comando no encontrado. Usa `!help` para ver la lista.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Falta un argumento: {error.param.name}")
    else:
        logger.error(f"Error en comando {ctx.command}: {error}")
        await ctx.send(f"❌ Error: {str(error)}")


@bot.event
async def on_message(message):
    """Procesa los mensajes."""
    # Ignorar mensajes del propio bot
    if message.author == bot.user:
        return
    
    # Ignorar mensajes directos de usuarios no autorizados
    if isinstance(message.channel, discord.DMChannel):
        if not is_authorized(str(message.author.id)):
            await message.channel.send("❌ No estás autorizado para usar este bot.")
            logger.warning(f"Mensaje DM no autorizado de {message.author}")
            return
    
    await bot.process_commands(message)


# Cargar comandos
setup_general(bot)
setup_qwen(bot)


# Comandos de administración de whitelist
@bot.command(name="whitelist")
async def whitelist_command(ctx: commands.Context, action: str, member: discord.Member = None):
    """
    Gestiona la whitelist de usuarios.
    
    Uso:
    !whitelist add @usuario - Agrega usuario
    !whitelist remove @usuario - Remueve usuario
    !whitelist list - Lista usuarios
    """
    # Solo el admin puede usar este comando
    if str(ctx.author.id) != ADMIN_USER_ID:
        await ctx.send("❌ Solo el administrador puede usar este comando.")
        return
    
    if action.lower() == "add":
        if member is None:
            await ctx.send("❌ Debes mencionar a un usuario.")
            return
        
        user_id = str(member.id)
        if add_authorized_user(user_id):
            await ctx.send(f"✅ {member.mention} agregado a la whitelist.")
            logger.info(f"Usuario {member} agregado a whitelist por {ctx.author}")
        else:
            await ctx.send(f"⚠️ {member.mention} ya está en la whitelist.")
    
    elif action.lower() == "remove":
        if member is None:
            await ctx.send("❌ Debes mencionar a un usuario.")
            return
        
        from .security.auth import remove_authorized_user
        user_id = str(member.id)
        if remove_authorized_user(user_id):
            await ctx.send(f"✅ {member.mention} removido de la whitelist.")
            logger.info(f"Usuario {member} removido de whitelist por {ctx.author}")
        else:
            await ctx.send(f"⚠️ {member.mention} no está en la whitelist.")
    
    elif action.lower() == "list":
        from .security.auth import get_authorized_users
        users = get_authorized_users()
        
        if not users:
            await ctx.send("📋 No hay usuarios en la whitelist.")
        else:
            # Convertir IDs a menciones si es posible
            user_mentions = []
            for user_id in users:
                try:
                    user = await bot.fetch_user(int(user_id))
                    user_mentions.append(user.mention)
                except:
                    user_mentions.append(f"`{user_id}`")
            
            await ctx.send(f"📋 **Usuarios autorizados:**\n" + "\n".join(user_mentions))
    
    else:
        await ctx.send("❌ Uso: `!whitelist <add|remove|list> [@usuario]`")


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
        print(f"✅ Iniciando bot...")
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
