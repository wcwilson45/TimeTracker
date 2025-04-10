import sqlite3
from datetime import datetime
import pathlib
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
import sys
import os
from .utils import get_writable_db_path

class TaskHistoryDB:
    def __init__(self):
        # Use resource_path to locate the database file
        self.task_list_db = get_writable_db_path('app/ui/Databases/task_list.db')
        
        # Create the history table with proper indexing
        conn = sqlite3.connect(self.task_list_db)
        c = conn.cursor()
        
        try:
            # Create task_history table if it doesn't exist
            c.execute("""CREATE TABLE IF NOT EXISTS task_history (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                change_date TEXT,
                field_changed TEXT,
                old_value TEXT,
                new_value TEXT,
                FOREIGN KEY (task_id) REFERENCES TaskList(task_id)
            )""")
            
            # Create index for task_id for better performance if it doesn't exist
            c.execute("CREATE INDEX IF NOT EXISTS idx_task_history_task_id ON task_history(task_id)")
            
            # Create index for change_date for better sorting and searching
            c.execute("CREATE INDEX IF NOT EXISTS idx_task_history_change_date ON task_history(change_date)")
            
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error when initializing task history: {e}")
            conn.rollback()
        finally:
            conn.close()

    def record_change(self, task_id, field_changed, old_value, new_value, existing_conn=None):
        """Record a change in the task history with improved error handling
        
        Args:
            task_id: The ID of the task
            field_changed: Name of the field that changed
            old_value: Previous value
            new_value: New value
            existing_conn: Optional existing database connection to use
        """
        # Skip recording if old and new values are the same
        if str(old_value) == str(new_value):
            return
            
        should_close_conn = False
        conn = None
        
        try:
            if existing_conn:
                conn = existing_conn
            else:
                conn = sqlite3.connect(self.task_list_db)
                should_close_conn = True
                
            c = conn.cursor()
            
            # Ensure task_id is an integer
            try:
                task_id = int(task_id)
            except (ValueError, TypeError):
                print(f"Invalid task_id: {task_id}, must be an integer")
                return
            
            # Format field name
            field_changed = str(field_changed).strip()
            
            # Add timestamp
            change_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Truncate excessively long values if necessary (SQLite has a limit)
            # Use a reasonable size limit (e.g., 10000 characters)
            max_length = 10000
            if old_value and len(str(old_value)) > max_length:
                old_value = str(old_value)[:max_length] + "... (truncated)"
            if new_value and len(str(new_value)) > max_length:
                new_value = str(new_value)[:max_length] + "... (truncated)"
            
            # Insert the record
            c.execute("""
                INSERT INTO task_history 
                (task_id, change_date, field_changed, old_value, new_value)
                VALUES (?, ?, ?, ?, ?)
            """, (task_id, change_date, field_changed, str(old_value), str(new_value)))
            
            if should_close_conn:
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database error when recording change: {e}")
            if should_close_conn and conn:
                conn.rollback()
        except Exception as e:
            print(f"Error recording task history: {e}")
            if should_close_conn and conn:
                conn.rollback()
        finally:
            if should_close_conn and conn:
                conn.close()

    def get_task_history(self, task_id, limit=100, offset=0):
        """Get task history with pagination support
        
        Args:
            task_id: The ID of the task
            limit: Maximum number of records to retrieve
            offset: Number of records to skip
            
        Returns:
            List of (change_date, field_changed, old_value, new_value) tuples
        """
        conn = None
        try:
            conn = sqlite3.connect(self.task_list_db)
            c = conn.cursor()
            
            # Ensure task_id is an integer
            try:
                task_id = int(task_id)
            except (ValueError, TypeError):
                print(f"Invalid task_id: {task_id}, must be an integer")
                return []
            
            # Query with pagination
            c.execute("""
                SELECT change_date, field_changed, old_value, new_value
                FROM task_history
                WHERE task_id = ?
                ORDER BY change_date DESC
                LIMIT ? OFFSET ?
            """, (task_id, limit, offset))
            
            return c.fetchall()
        except sqlite3.Error as e:
            print(f"Database error when getting task history: {e}")
            return []
        except Exception as e:
            print(f"Error getting task history: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def get_task_history_count(self, task_id):
        """Get the total number of history records for a task
        
        Args:
            task_id: The ID of the task
            
        Returns:
            Integer count of history records
        """
        conn = None
        try:
            conn = sqlite3.connect(self.task_list_db)
            c = conn.cursor()
            
            # Ensure task_id is an integer
            try:
                task_id = int(task_id)
            except (ValueError, TypeError):
                print(f"Invalid task_id: {task_id}, must be an integer")
                return 0
            
            # Get count
            c.execute("SELECT COUNT(*) FROM task_history WHERE task_id = ?", (task_id,))
            return c.fetchone()[0]
        except sqlite3.Error as e:
            print(f"Database error when getting history count: {e}")
            return 0
        except Exception as e:
            print(f"Error getting history count: {e}")
            return 0
        finally:
            if conn:
                conn.close()

    def get_change_dates(self, task_id):
        """Get unique dates when changes were made to a task"""
        conn = None
        try:
            conn = sqlite3.connect(self.task_list_db)
            c = conn.cursor()
            
            # Ensure task_id is an integer
            try:
                task_id = int(task_id)
            except (ValueError, TypeError):
                print(f"Invalid task_id: {task_id}, must be an integer")
                return []
            
            # Get distinct dates
            c.execute("""
                SELECT DISTINCT change_date
                FROM task_history
                WHERE task_id = ?
                ORDER BY change_date DESC
            """, (task_id,))
            
            return [date[0] for date in c.fetchall()]
        except sqlite3.Error as e:
            print(f"Database error when getting change dates: {e}")
            return []
        except Exception as e:
            print(f"Error getting change dates: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def get_changes_by_date(self, task_id, date):
        """Get all changes for a task on a specific date"""
        conn = None
        try:
            conn = sqlite3.connect(self.task_list_db)
            c = conn.cursor()
            
            # Ensure task_id is an integer
            try:
                task_id = int(task_id)
            except (ValueError, TypeError):
                print(f"Invalid task_id: {task_id}, must be an integer")
                return []
            
            # Get changes for the specific date
            c.execute("""
                SELECT field_changed, old_value, new_value
                FROM task_history
                WHERE task_id = ? AND change_date = ?
                ORDER BY history_id
            """, (task_id, date))
            
            return c.fetchall()
        except sqlite3.Error as e:
            print(f"Database error when getting changes by date: {e}")
            return []
        except Exception as e:
            print(f"Error getting changes by date: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def delete_task_history(self, task_id):
        """Delete all history records for a task
        
        Args:
            task_id: The ID of the task
            
        Returns:
            Number of records deleted
        """
        conn = None
        try:
            conn = sqlite3.connect(self.task_list_db)
            c = conn.cursor()
            
            # Ensure task_id is an integer
            try:
                task_id = int(task_id)
            except (ValueError, TypeError):
                print(f"Invalid task_id: {task_id}, must be an integer")
                return 0
            
            # Get count before deletion for return value
            c.execute("SELECT COUNT(*) FROM task_history WHERE task_id = ?", (task_id,))
            count = c.fetchone()[0]
            
            # Delete records
            c.execute("DELETE FROM task_history WHERE task_id = ?", (task_id,))
            conn.commit()
            
            return count
        except sqlite3.Error as e:
            print(f"Database error when deleting task history: {e}")
            if conn:
                conn.rollback()
            return 0
        except Exception as e:
            print(f"Error deleting task history: {e}")
            if conn:
                conn.rollback()
            return 0
        finally:
            if conn:
                conn.close()

    def cleanup_old_history(self, days_to_keep=90):
        """Clean up history records older than the specified number of days
        
        Args:
            days_to_keep: Number of days of history to keep
            
        Returns:
            Number of records deleted
        """
        conn = None
        try:
            conn = sqlite3.connect(self.task_list_db)
            c = conn.cursor()
            
            # Calculate cutoff date
            cutoff_date = (datetime.now() - datetime.timedelta(days=days_to_keep)).strftime("%Y-%m-%d")
            
            # Get count before deletion for return value
            c.execute("SELECT COUNT(*) FROM task_history WHERE change_date < ?", (cutoff_date,))
            count = c.fetchone()[0]
            
            # Delete old records
            c.execute("DELETE FROM task_history WHERE change_date < ?", (cutoff_date,))
            conn.commit()
            
            return count
        except sqlite3.Error as e:
            print(f"Database error when cleaning up old history: {e}")
            if conn:
                conn.rollback()
            return 0
        except Exception as e:
            print(f"Error cleaning up old history: {e}")
            if conn:
                conn.rollback()
            return 0
        finally:
            if conn:
                conn.close()
