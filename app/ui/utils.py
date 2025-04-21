def show_messagebox(parent_window, messagebox_func, *args, **kwargs):
    """
    Safely show a messagebox by temporarily releasing the parent window's grab
    
    Args:
        parent_window: The Toplevel or Tk window that currently has grab
        messagebox_func: The messagebox function to call (e.g., messagebox.showinfo)
        *args, **kwargs: Arguments to pass to the messagebox function
        
    Returns:
        The result from the messagebox function
    """
    had_grab = False
    
    try:
        # Check if the parent window exists and supports grab operations
        # Don't use winfo_exists() since some objects might not have it
        try:
            parent_window.grab_release()
            had_grab = True
        except Exception as e:
            print(f"Note: Could not release grab: {e}")
                
        # Show the messagebox
        result = messagebox_func(*args, **kwargs)
        
        # Return the result
        return result
        
    finally:
        # Restore grab if it was released
        if had_grab:
            try:
                parent_window.grab_set()
                parent_window.focus_force()
            except Exception as e:
                print(f"Note: Could not restore grab: {e}")
                
    return result