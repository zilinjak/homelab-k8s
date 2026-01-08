"""Database package for storing HTTP results."""

from db.repository import init_db, save_result, get_all_results
from db.config import DB_PATH

__all__ = ["init_db", "save_result", "get_all_results", "DB_PATH"]

