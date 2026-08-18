import sqlite3
from datetime import datetime
import config


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(
            config.DATABASE_NAME
        )

        self.cursor = self.connection.cursor()

        # Enable foreign key support
        self.cursor.execute(
            "PRAGMA foreign_keys = ON"
        )

    # ==========================================================
    # CREATE TABLES
    # ==========================================================

    def create_tables(self):

        # ------------------------------------------------------
        # USERS TABLE
        # ------------------------------------------------------

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT NOT NULL,

                department TEXT,

                phone TEXT,

                email TEXT,

                created_at
                    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ------------------------------------------------------
        # ATTENDANCE TABLE
        # ------------------------------------------------------

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                date TEXT NOT NULL,

                time TEXT NOT NULL,

                status TEXT,

                FOREIGN KEY(user_id)
                    REFERENCES users(id)
            )
        """)

        # ------------------------------------------------------
        # VISITORS TABLE
        # ------------------------------------------------------

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS visitors (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                visitor_name TEXT NOT NULL,

                purpose TEXT,

                host TEXT,

                entry_time TEXT,

                exit_time TEXT
            )
        """)

        # ------------------------------------------------------
        # ADMINS TABLE
        # ------------------------------------------------------

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                username TEXT UNIQUE NOT NULL,

                password TEXT NOT NULL
            )
        """)

        self.connection.commit()

    # ==========================================================
    # USER FUNCTIONS
    # ==========================================================

    def add_user(
        self,
        name,
        department,
        phone,
        email
    ):

        self.cursor.execute("""
            INSERT INTO users (
                name,
                department,
                phone,
                email
            )
            VALUES (?, ?, ?, ?)
        """, (
            name,
            department,
            phone,
            email
        ))

        self.connection.commit()

        return self.cursor.lastrowid

    # ----------------------------------------------------------
    # GET USER
    # ----------------------------------------------------------

    def get_user(self, user_id):

        self.cursor.execute("""
            SELECT
                id,
                name,
                department
            FROM users
            WHERE id = ?
        """, (user_id,))

        return self.cursor.fetchone()

    # ----------------------------------------------------------
    # GET ALL USERS
    # ----------------------------------------------------------

    def get_users(self):

        self.cursor.execute("""
            SELECT
                id,
                name,
                department,
                phone,
                email,
                created_at
            FROM users
            ORDER BY id DESC
        """)

        return self.cursor.fetchall()

    # ==========================================================
    # ATTENDANCE FUNCTIONS
    # ==========================================================

    def mark_attendance(self, user_id):

        today = datetime.now().strftime(
            "%Y-%m-%d"
        )

        current_time = datetime.now().strftime(
            "%H:%M:%S"
        )

        # ------------------------------------------------------
        # Check whether attendance is already marked today
        # ------------------------------------------------------

        self.cursor.execute("""
            SELECT id
            FROM attendance
            WHERE user_id = ?
            AND date = ?
        """, (
            user_id,
            today
        ))

        existing_record = self.cursor.fetchone()

        # Already marked
        if existing_record is not None:

            return False

        # ------------------------------------------------------
        # Insert attendance
        # ------------------------------------------------------

        self.cursor.execute("""
            INSERT INTO attendance (
                user_id,
                date,
                time,
                status
            )
            VALUES (?, ?, ?, ?)
        """, (
            user_id,
            today,
            current_time,
            "Present"
        ))

        self.connection.commit()

        return True

    # ----------------------------------------------------------
    # GET ALL ATTENDANCE
    # ----------------------------------------------------------

    def get_attendance(self):

        self.cursor.execute("""
            SELECT
                attendance.id,
                users.id,
                users.name,
                users.department,
                attendance.date,
                attendance.time,
                attendance.status

            FROM attendance

            INNER JOIN users
                ON attendance.user_id = users.id

            ORDER BY
                attendance.date DESC,
                attendance.time DESC
        """)

        return self.cursor.fetchall()

    # ----------------------------------------------------------
    # GET TODAY'S ATTENDANCE
    # ----------------------------------------------------------

    def get_today_attendance(self):

        today = datetime.now().strftime(
            "%Y-%m-%d"
        )

        self.cursor.execute("""
            SELECT
                attendance.id,
                users.id,
                users.name,
                users.department,
                attendance.date,
                attendance.time,
                attendance.status

            FROM attendance

            INNER JOIN users
                ON attendance.user_id = users.id

            WHERE attendance.date = ?

            ORDER BY attendance.time DESC
        """, (today,))

        return self.cursor.fetchall()

    # ----------------------------------------------------------
    # GET ATTENDANCE FOR A USER
    # ----------------------------------------------------------

    def get_user_attendance(self, user_id):

        self.cursor.execute("""
            SELECT
                id,
                user_id,
                date,
                time,
                status

            FROM attendance

            WHERE user_id = ?

            ORDER BY
                date DESC,
                time DESC
        """, (user_id,))

        return self.cursor.fetchall()

    # ==========================================================
    # VISITOR FUNCTIONS
    # ==========================================================

    def add_visitor(
        self,
        visitor_name,
        purpose,
        host,
        entry_time=None
    ):

        # ------------------------------------------------------
        # Automatically create entry time if not supplied
        # ------------------------------------------------------

        if entry_time is None:

            entry_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        # ------------------------------------------------------
        # Insert visitor
        # ------------------------------------------------------

        self.cursor.execute("""
            INSERT INTO visitors (
                visitor_name,
                purpose,
                host,
                entry_time,
                exit_time
            )
            VALUES (?, ?, ?, ?, NULL)
        """, (
            visitor_name,
            purpose,
            host,
            entry_time
        ))

        self.connection.commit()

        return self.cursor.lastrowid

    # ----------------------------------------------------------
    # GET ACTIVE VISITORS
    # ----------------------------------------------------------

    def get_active_visitors(self):

        self.cursor.execute("""
            SELECT
                id,
                visitor_name,
                purpose,
                host,
                entry_time

            FROM visitors

            WHERE exit_time IS NULL

            ORDER BY entry_time DESC
        """)

        return self.cursor.fetchall()

    # ----------------------------------------------------------
    # EXIT VISITOR
    # ----------------------------------------------------------

    def exit_visitor(self, visitor_id):

        exit_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self.cursor.execute("""
            UPDATE visitors

            SET exit_time = ?

            WHERE id = ?

            AND exit_time IS NULL
        """, (
            exit_time,
            visitor_id
        ))

        self.connection.commit()

        if self.cursor.rowcount > 0:

            return True

        return False

    # ----------------------------------------------------------
    # GET ALL VISITORS
    # ----------------------------------------------------------

    def get_visitors(self):

        self.cursor.execute("""
            SELECT
                id,
                visitor_name,
                purpose,
                host,
                entry_time,
                exit_time

            FROM visitors

            ORDER BY entry_time DESC
        """)

        return self.cursor.fetchall()

    # ----------------------------------------------------------
    # GET VISITOR BY ID
    # ----------------------------------------------------------

    def get_visitor(self, visitor_id):

        self.cursor.execute("""
            SELECT
                id,
                visitor_name,
                purpose,
                host,
                entry_time,
                exit_time

            FROM visitors

            WHERE id = ?
        """, (visitor_id,))

        return self.cursor.fetchone()

    # ==========================================================
    # ADMIN FUNCTIONS
    # ==========================================================

    def add_admin(
        self,
        username,
        password
    ):

        try:

            self.cursor.execute("""
                INSERT INTO admins (
                    username,
                    password
                )
                VALUES (?, ?)
            """, (
                username,
                password
            ))

            self.connection.commit()

            return True

        except sqlite3.IntegrityError:

            return False

    # ----------------------------------------------------------
    # VERIFY ADMIN
    # ----------------------------------------------------------

    def verify_admin(
        self,
        username,
        password
    ):

        self.cursor.execute("""
            SELECT id
            FROM admins
            WHERE username = ?
            AND password = ?
        """, (
            username,
            password
        ))

        result = self.cursor.fetchone()

        if result:

            return True

        return False

    # ----------------------------------------------------------
    # CHECK WHETHER ADMIN EXISTS
    # ----------------------------------------------------------

    def admin_exists(self):

        self.cursor.execute("""
            SELECT id
            FROM admins
            LIMIT 1
        """)

        result = self.cursor.fetchone()

        return result is not None

    # ==========================================================
    # STATISTICS
    # ==========================================================

    def get_total_users(self):

        self.cursor.execute("""
            SELECT COUNT(*)
            FROM users
        """)

        result = self.cursor.fetchone()

        return result[0]

    # ----------------------------------------------------------

    def get_total_visitors(self):

        self.cursor.execute("""
            SELECT COUNT(*)
            FROM visitors
        """)

        result = self.cursor.fetchone()

        return result[0]

    # ----------------------------------------------------------

    def get_active_visitor_count(self):

        self.cursor.execute("""
            SELECT COUNT(*)
            FROM visitors
            WHERE exit_time IS NULL
        """)

        result = self.cursor.fetchone()

        return result[0]

    # ----------------------------------------------------------

    def get_today_attendance_count(self):

        today = datetime.now().strftime(
            "%Y-%m-%d"
        )

        self.cursor.execute("""
            SELECT COUNT(*)
            FROM attendance
            WHERE date = ?
        """, (today,))

        result = self.cursor.fetchone()

        return result[0]

    # ==========================================================
    # CLOSE DATABASE
    # ==========================================================

    def close(self):

        if self.connection:

            self.connection.close()
