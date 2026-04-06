"""Gestión de la lista blanca de usuarios autorizados."""

import json
from typing import List

from ..config import WHITELIST_FILE


class WhitelistManager:
    """Gestiona la lista de usuarios autorizados para usar el bot."""

    def __init__(self):
        self.whitelist_file = WHITELIST_FILE
        self._ensure_file_exists()
        self._cache: set[str] = set(self._load_data())

    def _ensure_file_exists(self):
        """Crea el archivo de whitelist si no existe."""
        self.whitelist_file.parent.mkdir(exist_ok=True)
        if not self.whitelist_file.exists():
            self._save_data([])

    def _load_data(self) -> List[str]:
        """Carga los datos del archivo JSON."""
        try:
            with open(self.whitelist_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_data(self, data: List[str]):
        """Guarda los datos en el archivo JSON."""
        with open(self.whitelist_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_user(self, user_id: str) -> bool:
        """
        Agrega un usuario a la whitelist.

        Args:
            user_id: ID del usuario de Discord

        Returns:
            True si se agregó, False si ya existía
        """
        if user_id in self._cache:
            return False
        self._cache.add(user_id)
        self._save_data(list(self._cache))
        return True

    def remove_user(self, user_id: str) -> bool:
        """
        Remueve un usuario de la whitelist.

        Args:
            user_id: ID del usuario de Discord

        Returns:
            True si se removió, False si no existía
        """
        if user_id not in self._cache:
            return False
        self._cache.discard(user_id)
        self._save_data(list(self._cache))
        return True

    def is_whitelisted(self, user_id: str) -> bool:
        """
        Verifica si un usuario está en la whitelist.

        Args:
            user_id: ID del usuario de Discord

        Returns:
            True si está autorizado, False si no
        """
        return user_id in self._cache

    def get_all_users(self) -> List[str]:
        """Retorna la lista completa de usuarios autorizados."""
        return list(self._cache)