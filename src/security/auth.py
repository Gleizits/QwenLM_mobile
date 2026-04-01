"""Módulo de autenticación y autorización."""

from ..config import ADMIN_USER_ID
from .whitelist import WhitelistManager

_whitelist_manager = WhitelistManager()


def is_authorized(user_id: str) -> bool:
    """
    Verifica si un usuario está autorizado para usar el bot.
    
    Args:
        user_id: ID del usuario de Discord
        
    Returns:
        True si está autorizado, False si no
    """
    # El admin siempre está autorizado
    if user_id == ADMIN_USER_ID:
        return True
    
    # Verificar whitelist
    return _whitelist_manager.is_whitelisted(user_id)


def add_authorized_user(user_id: str) -> bool:
    """
    Agrega un usuario autorizado.
    
    Args:
        user_id: ID del usuario de Discord
        
    Returns:
        True si se agregó, False si ya existía
    """
    return _whitelist_manager.add_user(user_id)


def remove_authorized_user(user_id: str) -> bool:
    """
    Remueve un usuario autorizado.
    
    Args:
        user_id: ID del usuario de Discord
        
    Returns:
        True si se removió, False si no existía
    """
    return _whitelist_manager.remove_user(user_id)


def get_authorized_users() -> list:
    """Retorna la lista de usuarios autorizados."""
    return _whitelist_manager.get_all_users()
