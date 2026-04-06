"""Ejecutor de comandos de Qwen Code."""

import asyncio
from pathlib import Path
from typing import Optional, Tuple

from ..config import QWEN_COMMAND, QWEN_TIMEOUT, BASE_DIR
from ..utils.logger import setup_logger

logger = setup_logger("QwenExecutor")

_SUCCESS_MSG = "Comando ejecutado correctamente"
_ERROR_MSG = "Error desconocido"


class QwenExecutor:
    """Ejecuta comandos de Qwen Code de forma segura."""

    def __init__(self, working_dir: Optional[Path] = None):
        """
        Inicializa el ejecutor.

        Args:
            working_dir: Directorio de trabajo (por defecto, BASE_DIR)
        """
        self.working_dir = working_dir or BASE_DIR
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

            process = await asyncio.create_subprocess_exec(
                QWEN_COMMAND, "exec", "qwen", "--", command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.working_dir),
            )

            return await self._wait_for_result(process)

        except FileNotFoundError:
            msg = f"Comando '{QWEN_COMMAND}' no encontrado. ¿Está instalado Qwen Code?"
            logger.error(msg)
            return False, msg
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            return False, f"Error: {str(e)}"

    async def _wait_for_result(self, process: asyncio.subprocess.Process) -> Tuple[bool, str]:
        """
        Espera el resultado del proceso con timeout.

        Args:
            process: Proceso en ejecución

        Returns:
            Tuple[success, output]: Resultado de la ejecución
        """
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=self.timeout,
            )

            output = stdout.decode("utf-8") if stdout else ""
            error = stderr.decode("utf-8") if stderr else ""

            if process.returncode == 0:
                logger.info("Comando ejecutado exitosamente")
                return True, output or _SUCCESS_MSG

            logger.error(f"Error en comando: {error}")
            return False, error or _ERROR_MSG

        except asyncio.TimeoutError:
            process.kill()
            await process.communicate()
            logger.error(f"Timeout después de {self.timeout}s")
            return False, f"Timeout: El comando tardó más de {self.timeout}s"

    def execute_sync(self, command: str) -> Tuple[bool, str]:
        """
        Ejecuta un comando de forma síncrona (bloqueante).

        Args:
            command: Comando a ejecutar

        Returns:
            Tuple[success, output]: Resultado de la ejecución
        """
        return asyncio.run(self.execute(command))