# 🤖 QwenLM Mobile Bot

Bot de Discord que permite controlar **Qwen Code** desde cualquier dispositivo (móvil, tablet, otra PC) sin necesidad de estar frente a tu computador.

## 📋 Requisitos

- Python 3.8 o superior
- Qwen Code instalado via npm (`npm install -g qwen-code`)
- Token de bot de Discord

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/Gleizits/QwenLM_mobile.git
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
   QWEN_COMMAND=npx
   QWEN_TIMEOUT=300
```

## 🔑 Cómo obtener el Token de Discord

1. Ve a [Discord Developer Portal](https://discord.com/developers/applications)
2. Crea una nueva aplicación
3. Ve a la sección **Bot**
4. Haz clic en **Add Bot**
5. Copia el token (haz clic en **Reset Token** si es necesario)
6. En **Bot** → **Privileged Gateway Intents**, activa:
   - ✅ Server Members Intent
   - ✅ Message Content Intent
7. En **OAuth2** → **URL Generator**, selecciona el scope `bot` y los permisos necesarios
8. Usa la URL generada para invitar el bot a tu servidor

## ▶️ Ejecución

### Opción 1: Usar script batch (Windows)
```bash
run.bat
```

### Opción 2: Manual
```bash
.venv\Scripts\activate
python main.py
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
