# auth/database.py
# This is a VERY simple example.  Use a real database for production!
import os

users = {
    "user1": "password123",
    "user2": "securepass",
}

def get_user(username):
  """Retrieves user data (e.g., hashed password) from the database."""
  if username in users:
    return users[username]
  else:
    return None

def create_user(username, password):
  """Creates a new user in the database.  Hash the password before saving!"""
  users[username] = password #In a real app, hash the password first!
  return True # Or return the user object