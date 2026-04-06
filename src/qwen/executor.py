"""Ejecutor de comandos de Qwen Code."""

import asyncio
from typing import Optional, Tuple
from pathlib import Path

from ..config import QWEN_COMMAND, QWEN_TIMEOUT, BASE_DIR
from ..utils.logger import setup_logger

logger = setup_logger("QwenExecutor")


class QwenExecutor:
    """Ejecuta comandos de Qwen Code de forma segura."""
    
    def __init__(self, working_dir: Optional[Path] = None):
        """
        Inicializa el ejecutor.
        
        Args:
            working_dir: Directorio de trabajo (por defecto, la raíz del proyecto)
        """
        self.working_dir = working_dir or BASE_DIR
        self.command = QWEN_COMMAND
        self.timeout = QWEN_TIMEOUT
    
    async def execute(self, command: str) -> Tuple[bool, str]:
        """
        Ejecuta un comando de Qwen Code.
        
        Args:
            command: Comando a ejecutar
            
        Returns:
            Tuple[success, output]: Resultado de la ejecución
        """
        try:
            logger.info(f"Ejecutando comando Qwen: {command}")
            
            # Ejecutar el comando
            process = await asyncio.create_subprocess_exec(
                self.command,
                "exec",
                "qwen",
                "--",
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.working_dir)
            )
            
            # Esperar con timeout
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=self.timeout
                )
                
                output = stdout.decode("utf-8") if stdout else ""
                error = stderr.decode("utf-8") if stderr else ""
                
                if process.returncode == 0:
                    logger.info(f"Comando ejecutado exitosamente")
                    return True, output or "Comando ejecutado correctamente"
                else:
                    logger.error(f"Error en comando: {error}")
                    return False, error or "Error desconocido"
                    
            except asyncio.TimeoutError:
                process.kill()
                await process.communicate()
                logger.error(f"Timeout después de {self.timeout}s")
                return False, f"Timeout: El comando tardó más de {self.timeout}s"
                
        except FileNotFoundError:
            msg = f"Comando '{self.command}' no encontrado. ¿Está instalado Qwen Code?"
            logger.error(msg)
            return False, msg
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            return False, f"Error: {str(e)}"
    
    def execute_sync(self, command: str) -> Tuple[bool, str]:
        """
        Ejecuta un comando de forma síncrona (bloqueante).
        
        Args:
            command: Comando a ejecutar
            
        Returns:
            Tuple[success, output]: Resultado de la ejecución
        """
        return asyncio.run(self.execute(command))
