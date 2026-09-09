#!/usr/bin/env python3
"""A deliberately vulnerable note-taking application."""

import os
import sqlite3
import sys

from pathlib import Path

DB_FILE = "notes.db"


def init_db():
    """Create the notes table if it does not exist."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS notes "
        "(id INTEGER PRIMARY KEY, title TEXT, body TEXT)"
    )
    conn.execute(
        "INSERT OR IGNORE INTO notes (id, title, body) VALUES "
        "(1, 'Welcome', 'This is your first note.'), "
        "(2, 'Reminder', 'Submit the SSI lab report on time.'), "
        "(3, 'Secret', 'The admin password is hunter2.')"
    )
    conn.commit()
    conn.close()


def search_notes(query):
    """Search notes by title: SAFE version."""
    conn = sqlite3.connect(DB_FILE)

    sql = "SELECT id, title, body FROM notes WHERE title LIKE ?"

    try:
        cursor = conn.execute(sql, ("%" + query + "%",))
        results = cursor.fetchall()

        if results:
            for row in results:
                print(f"  [{row[0]}] {row[1]}: {row[2]}")
        else:
            print("  No notes found.")

    except sqlite3.Error as e:
        print(f"  SQL error: {e}")

    conn.close()


def export_note(note_id):
    conn = sqlite3.connect(DB_FILE)

    cursor = conn.execute(
        "SELECT title, body FROM notes WHERE id = ?",
        (note_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        print("  Note not found.")
        return

    filename = input("  Enter filename to export to: ").strip()

    if "/" in filename or ".." in filename:
        print("  Invalid filename.")
        return

    with open(Path(filename), "w", encoding="utf-8") as f:
        f.write(f"Title: {row[0]}\n")
        f.write(f"Body: {row[1]}\n")

    print(f"  Note exported to {filename}")


def main():
    init_db()
    while True:
        print("\n=== Note App ===")
        print("1. Search notes")
        print("2. Export note")
        print("3. Quit")
        choice = input("Choice: ").strip()

        if choice == "1":
            query = input("  Search query: ")
            search_notes(query)
        elif choice == "2":
            try:
                note_id = int(input("  Note ID: "))
            except ValueError:
                print("  Invalid ID.")
                continue
            export_note(note_id)
        elif choice == "3":
            break
        else:
            print("  Invalid choice.")


if __name__ == "__main__":
    main()
