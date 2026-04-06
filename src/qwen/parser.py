"""Parser de respuestas de Qwen Code."""

from typing import Optional

_CODE_KEYWORDS = ("def ", "class ", "import ", "function ")


class ResponseParser:
    """Procesa y formatea las respuestas de Qwen Code."""

    MAX_MESSAGE_LENGTH = 2000  # Límite de Discord
    _TRUNCATE_RESERVE = 50

    @staticmethod
    def truncate(text: str, max_length: int = MAX_MESSAGE_LENGTH) -> str:
        """
        Trunca un texto si excede el límite.

        Args:
            text: Texto a truncar
            max_length: Longitud máxima

        Returns:
            Texto truncado con indicador si fue cortado
        """
        if len(text) <= max_length:
            return text

        truncated = text[:max_length - ResponseParser._TRUNCATE_RESERVE]
        return f"{truncated}\n\n... [Mensaje truncado, excede {max_length} caracteres]"

    @staticmethod
    def format_code_block(code: str, language: Optional[str] = None) -> str:
        """
        Formatea código en un bloque de markdown.

        Args:
            code: Código a formatear
            language: Lenguaje para syntax highlighting

        Returns:
            Código formateado para Discord
        """
        lang = language or ""
        return f"```{lang}\n{code}\n```"

    @staticmethod
    def _looks_like_code(output: str) -> bool:
        """Determina si el output parece ser código."""
        return output.startswith("```") or any(kw in output for kw in _CODE_KEYWORDS)

    @staticmethod
    def format_response(success: bool, output: str) -> str:
        """
        Formatea una respuesta completa para Discord.

        Args:
            success: Si el comando fue exitoso
            output: Salida del comando

        Returns:
            Mensaje formateado
        """
        emoji = "✅" if success else "❌"
        prefix = "Éxito" if success else "Error"
        header = f"{emoji} **{prefix}**\n\n"

        body = (
            ResponseParser.format_code_block(output)
            if ResponseParser._looks_like_code(output)
            else ResponseParser.truncate(output)
        )

        return header + body