import subprocess
import shutil
from src.interfaces.base import InterfazLLM
from src.utils.exceptions import console

class AdaptadorQwen(InterfazLLM):
    """Adaptador para Qwen CLI (NPM). Corregido para Windows."""

    def __init__(self, binary_name: str = "qwen"):
        self.binary_name = binary_name
        self._validar_instalacion()

    def _validar_instalacion(self) -> None:
        """Verifica si qwen está disponible en el sistema."""
        # En Windows, shutil.which puede no encontrar .cmd si no se especifica
        if not shutil.which(self.binary_name) and not shutil.which(f"{self.binary_name}.cmd"):
            console.print(f"[bold red]⚠ Alerta:[/bold red] '{self.binary_name}' no se encontró en el PATH.")
            console.print("[italic]Intentando ejecutar de todos modos con shell=True...[/italic]")

    def preguntar(self, prompt: str) -> str:
        with console.status("[bold cyan]Qwen procesando solicitud...", spinner="bouncingBar"):
            try:
                # Ejecutamos con shell=True para resolver archivos .cmd o .ps1 de npm
                # Usamos una lista de argumentos para mayor seguridad
                proceso = subprocess.run(
                    [self.binary_name, prompt],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    shell=True,
                    check=True
                )
                return proceso.stdout.strip()
            except subprocess.CalledProcessError as e:
                # Capturamos el error específico del CLI de Qwen
                error_output = e.stderr.strip() if e.stderr else e.stdout.strip()
                console.print(f"[bold red]❌ Error de Qwen:[/bold red] {error_output}")
                return f"Qwen devolvió un error: {error_output}"
            except Exception as e:
                console.print(f"[bold red]❌ Error de Sistema:[/bold red] {str(e)}")
                return "No se pudo conectar con el servicio Qwen."
