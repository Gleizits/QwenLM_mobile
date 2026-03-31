"""Gestión de la lista blanca de usuarios autorizados."""

import json
from pathlib import Path
from typing import List

from ..config import WHITELIST_FILE


class WhitelistManager:
    """Gestiona la lista de usuarios autorizados para usar el bot."""
    
    def __init__(self):
        self.whitelist_file = WHITELIST_FILE
        self._ensure_file_exists()
    
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
        data = self._load_data()
        if user_id not in data:
            data.append(user_id)
            self._save_data(data)
            return True
        return False
    
    def remove_user(self, user_id: str) -> bool:
        """
        Remueve un usuario de la whitelist.
        
        Args:
            user_id: ID del usuario de Discord
            
        Returns:
            True si se removió, False si no existía
        """
        data = self._load_data()
        if user_id in data:
            data.remove(user_id)
            self._save_data(data)
            return True
        return False
    
    def is_whitelisted(self, user_id: str) -> bool:
        """
        Verifica si un usuario está en la whitelist.
        
        Args:
            user_id: ID del usuario de Discord
            
        Returns:
            True si está autorizado, False si no
        """
        data = self._load_data()
        return user_id in data
    
    def get_all_users(self) -> List[str]:
        """Retorna la lista completa de usuarios autorizados."""
        return self._load_data()
