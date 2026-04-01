# 🤖 QwenLM Mobile Bot

Bot de Discord que permite controlar **Qwen Code** desde cualquier dispositivo (móvil, tablet, otra PC) sin necesidad de estar frente a tu computador.

## 📋 Requisitos

- Python 3.8 o superior
- Qwen Code instalado y configurado
- Token de bot de Discord

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git --clone https://github.com/Gleizits/QwenLM_mobile.git
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
```

### 3. Activar entorno virtual (Windows)

```bash
.venv\Scripts\activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno

1. Copia el archivo de ejemplo:
   ```bash
   copy .env.example .env
   ```

2. Edita `.env` y agrega tus credenciales:
   ```env
   DISCORD_TOKEN=tu_token_de_discord
   DISCORD_CLIENT_ID=tu_client_id
   ADMIN_USER_ID=tu_user_id_de_discord
   ```

## 🔑 Cómo obtener el Token de Discord

1. Ve a [Discord Developer Portal](https://discord.com/developers/applications)
2. Crea una nueva aplicación
3. Ve a la sección "Bot"
4. Haz clic en "Add Bot"
5. Copia el token (haz clic en "Reset Token" si es necesario)
6. En "OAuth2" → "URL Generator", selecciona el scope `bot` y los permisos necesarios
7. Usa la URL generada para invitar el bot a tu servidor

## ▶️ Ejecución

### Opción 1: Usar script batch (Windows)

```bash
run.bat
```

### Opción 2: Manual

```bash
.venv\Scripts\activate
python src\bot.py
```

## 📱 Comandos disponibles

### Comandos Generales

| Comando | Descripción |
|---------|-------------|
| `!ping` | Verifica la latencia del bot |
| `!help` | Muestra la ayuda completa |
| `!status` | Muestra el estado del bot |

### Comandos Qwen Code

| Comando | Descripción |
|---------|-------------|
| `!qwen <comando>` | Ejecuta un comando en Qwen Code |
| `!qwen-status` | Verifica si Qwen Code está disponible |

**Ejemplos:**
```
!qwen crea un archivo llamado test.py
!qwen explica cómo funciona la función main
!qwen-status
```

### Comandos de Administración (Solo Admin)

| Comando | Descripción |
|---------|-------------|
| `!whitelist add @usuario` | Agrega usuario a la lista blanca |
| `!whitelist remove @usuario` | Remueve usuario de la lista blanca |
| `!whitelist list` | Lista usuarios autorizados |

## 🔒 Seguridad

- **Whitelist**: Solo usuarios autorizados pueden usar los comandos de Qwen Code
- **Admin único**: Solo el ADMIN_USER_ID puede gestionar la whitelist
- **Logs**: Todas las acciones quedan registradas en `logs/bot.log`

## 📁 Estructura del proyecto

```
QwenLM_mobile/
├── src/
│   ├── bot.py              # Entry point
│   ├── config.py           # Configuración
│   ├── commands/           # Comandos de Discord
│   ├── qwen/               # Integración con Qwen Code
│   ├── security/           # Autenticación y whitelist
│   └── utils/              # Utilidades (logger)
├── data/                   # Datos persistentes
├── logs/                   # Logs del bot
├── .env                    # Variables de entorno (NO commitear)
├── .env.example            # Ejemplo de configuración
├── requirements.txt        # Dependencias
└── run.bat                 # Script de inicio
```

## 🔧 Configuración avanzada

### Cambiar timeout de comandos

En `.env`, modifica:
```env
QWEN_TIMEOUT=600  # 10 minutos
```

### Cambiar directorio de trabajo

El bot usa por defecto el directorio padre del proyecto. Para cambiarlo, modifica `BASE_DIR` en `src/config.py`.

## 🐛 Solución de problemas

### "Comando 'qwen' no encontrado"

Asegúrate de que Qwen Code esté instalado y en el PATH del sistema.

### "DISCORD_TOKEN no encontrado"

Verifica que el archivo `.env` exista y contenga el token correctamente.

### El bot no responde en Discord

1. Verifica que el bot esté en línea (mensaje "✅ [Bot] está en línea!")
2. Asegúrate de que el usuario esté en la whitelist
3. Revisa los logs en `logs/bot.log`

## 📝 Notas

- El bot debe estar ejecutándose continuamente para recibir comandos
- Los comandos de Qwen Code tienen un timeout de 5 minutos por defecto
- Las respuestas muy largas se dividen automáticamente en múltiples mensajes

## 📄 Licencia

MIT License

---

**Desarrollado para controlar Qwen Code desde Discord 🚀**
