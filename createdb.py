#!/usr/bin/python3
import sqlite3


def main():
    conn = sqlite3.connect('lntitles.db')
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS titles
                 (datetime integer, title text)''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
