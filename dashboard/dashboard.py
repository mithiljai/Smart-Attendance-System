import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os


from database.database import Database


class AdminDashboard:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Smart Attendance & Visitor Management System"
        )

        self.root.geometry(
            "1000x700"
        )

        self.root.resizable(
            False,
            False
        )

        # ==================================================
        # DATABASE
        # ==================================================

        self.db = Database()
        self.db.create_tables()

        # ==================================================
        # ATTENDANCE PROCESS
        # ==================================================

        self.attendance_process = None

        # ==================================================
        # CREATE UI
        # ==================================================

        self.create_header()
        self.create_buttons()
        self.create_statistics()
        self.create_attendance_table()
        self.create_status_bar()

        self.refresh_dashboard()

        self.root.after(
            5000,
            self.auto_refresh
        )

    # ======================================================
    # HEADER
    # ======================================================

    def create_header(self):

        header = tk.Frame(
            self.root
        )

        header.pack(
            fill="x",
            pady=15
        )

        tk.Label(
            header,
            text="SMART ATTENDANCE & VISITOR SYSTEM",
            font=("Arial", 22, "bold")
        ).pack()

        tk.Label(
            header,
            text="Admin Dashboard",
            font=("Arial", 11)
        ).pack(
            pady=5
        )

    # ======================================================
    # BUTTONS
    # ======================================================

    def create_buttons(self):

        button_frame = tk.Frame(
            self.root
        )

        button_frame.pack(
            pady=10
        )

        tk.Button(
            button_frame,
            text="REGISTER NEW FACE",
            width=22,
            height=2,
            command=self.register_face
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.start_button = tk.Button(
            button_frame,
            text="START ATTENDANCE",
            width=22,
            height=2,
            command=self.start_attendance
        )

        self.start_button.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        self.stop_button = tk.Button(
            button_frame,
            text="STOP ATTENDANCE",
            width=22,
            height=2,
            command=self.stop_attendance,
            state=tk.DISABLED
        )

        self.stop_button.grid(
            row=0,
            column=2,
            padx=5,
            pady=5
        )

        tk.Button(
            button_frame,
            text="VISITOR ENTRY",
            width=22,
            height=2,
            command=self.visitor_entry
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

        tk.Button(
            button_frame,
            text="VISITOR EXIT",
            width=22,
            height=2,
            command=self.visitor_exit
        ).grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        tk.Button(
            button_frame,
            text="ATTENDANCE REPORT",
            width=22,
            height=2,
            command=self.attendance_report
        ).grid(
            row=2,
            column=0,
            padx=5,
            pady=5
        )

        tk.Button(
            button_frame,
            text="VISITOR REPORT",
            width=22,
            height=2,
            command=self.visitor_report
        ).grid(
            row=2,
            column=1,
            padx=5,
            pady=5
        )

    # ======================================================
    # STATISTICS
    # ======================================================

    def create_statistics(self):

        frame = tk.Frame(
            self.root
        )

        frame.pack(
            pady=15
        )

        self.users_label = tk.Label(
            frame,
            text="Registered Users: 0",
            font=("Arial", 12, "bold"),
            width=22
        )

        self.users_label.grid(
            row=0,
            column=0,
            padx=5
        )

        self.attendance_label = tk.Label(
            frame,
            text="Present Today: 0",
            font=("Arial", 12, "bold"),
            width=22
        )

        self.attendance_label.grid(
            row=0,
            column=1,
            padx=5
        )

        self.visitors_label = tk.Label(
            frame,
            text="Total Visitors: 0",
            font=("Arial", 12, "bold"),
            width=22
        )

        self.visitors_label.grid(
            row=0,
            column=2,
            padx=5
        )

        self.active_visitors_label = tk.Label(
            frame,
            text="Visitors Inside: 0",
            font=("Arial", 12, "bold"),
            width=22
        )

        self.active_visitors_label.grid(
            row=0,
            column=3,
            padx=5
        )

    # ======================================================
    # TODAY ATTENDANCE TABLE
    # ======================================================

    def create_attendance_table(self):

        frame = tk.Frame(
            self.root
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        tk.Label(
            frame,
            text="TODAY'S ATTENDANCE",
            font=("Arial", 14, "bold")
        ).pack(
            pady=5
        )

        columns = (
            "id",
            "name",
            "department",
            "date",
            "time",
            "status"
        )

        self.attendance_table = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            height=8
        )

        headings = {
            "id": "ID",
            "name": "Name",
            "department": "Department",
            "date": "Date",
            "time": "Time",
            "status": "Status"
        }

        for column, heading in headings.items():

            self.attendance_table.heading(
                column,
                text=heading
            )

        self.attendance_table.column(
            "id",
            width=50
        )

        self.attendance_table.column(
            "name",
            width=180
        )

        self.attendance_table.column(
            "department",
            width=150
        )

        self.attendance_table.column(
            "date",
            width=120
        )

        self.attendance_table.column(
            "time",
            width=100
        )

        self.attendance_table.column(
            "status",
            width=100
        )

        self.attendance_table.pack(
            fill="x"
        )

    # ======================================================
    # STATUS
    # ======================================================

    def create_status_bar(self):

        self.status_label = tk.Label(
            self.root,
            text="Database: CONNECTED | Attendance: STOPPED",
            font=("Arial", 10)
        )

        self.status_label.pack(
            pady=8
        )

    # ======================================================
    # REFRESH DASHBOARD
    # ======================================================

    def refresh_dashboard(self):

        try:

            cursor = self.db.connection.cursor()

            # ----------------------------------------------
            # USERS
            # ----------------------------------------------

            cursor.execute(
                "SELECT COUNT(*) FROM users"
            )

            total_users = cursor.fetchone()[0]

            # ----------------------------------------------
            # TODAY ATTENDANCE
            # ----------------------------------------------

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM attendance
                WHERE date = date('now','localtime')
                """
            )

            today_attendance = cursor.fetchone()[0]

            # ----------------------------------------------
            # VISITORS
            # ----------------------------------------------

            cursor.execute(
                "SELECT COUNT(*) FROM visitors"
            )

            total_visitors = cursor.fetchone()[0]

            # ----------------------------------------------
            # ACTIVE VISITORS
            # ----------------------------------------------

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM visitors
                WHERE exit_time IS NULL
                OR exit_time = ''
                """
            )

            active_visitors = cursor.fetchone()[0]

            # ----------------------------------------------
            # UPDATE LABELS
            # ----------------------------------------------

            self.users_label.config(
                text=f"Registered Users: {total_users}"
            )

            self.attendance_label.config(
                text=f"Present Today: {today_attendance}"
            )

            self.visitors_label.config(
                text=f"Total Visitors: {total_visitors}"
            )

            self.active_visitors_label.config(
                text=f"Visitors Inside: {active_visitors}"
            )

            # ----------------------------------------------
            # CLEAR TODAY TABLE
            # ----------------------------------------------

            for item in self.attendance_table.get_children():

                self.attendance_table.delete(
                    item
                )

            # ----------------------------------------------
            # LOAD TODAY ATTENDANCE
            # ----------------------------------------------

            cursor.execute(
                """
                SELECT
                    attendance.id,
                    users.name,
                    users.department,
                    attendance.date,
                    attendance.time,
                    attendance.status
                FROM attendance
                LEFT JOIN users
                    ON attendance.user_id = users.id
                WHERE attendance.date =
                    date('now','localtime')
                ORDER BY attendance.id DESC
                """
            )

            records = cursor.fetchall()

            for record in records:

                self.attendance_table.insert(
                    "",
                    "end",
                    values=record
                )

            self.status_label.config(
                text=(
                    "Database: CONNECTED | "
                    f"Attendance: {self.get_attendance_status()}"
                )
            )

        except Exception as error:

            print(
                "Dashboard refresh error:",
                error
            )

            self.status_label.config(
                text="Database: ERROR"
            )

    # ======================================================
    # AUTOMATIC REFRESH
    # ======================================================

    def auto_refresh(self):

        self.refresh_dashboard()

        self.root.after(
            5000,
            self.auto_refresh
        )

    # ======================================================
    # ATTENDANCE STATUS
    # ======================================================

    def get_attendance_status(self):

        if (
            self.attendance_process is not None
            and self.attendance_process.poll() is None
        ):

            return "RUNNING"

        return "STOPPED"

    # ======================================================
    # REGISTER FACE
    # ======================================================

    def register_face(self):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Register New Face"
        )

        window.geometry(
            "450x400"
        )

        window.resizable(
            False,
            False
        )

        tk.Label(
            window,
            text="REGISTER NEW FACE",
            font=("Arial", 18, "bold")
        ).pack(
            pady=20
        )

        tk.Label(
            window,
            text="Name"
        ).pack()

        name_entry = tk.Entry(
            window,
            width=35
        )

        name_entry.pack(
            pady=5
        )

        tk.Label(
            window,
            text="Department"
        ).pack()

        department_entry = tk.Entry(
            window,
            width=35
        )

        department_entry.pack(
            pady=5
        )

        tk.Label(
            window,
            text="Phone"
        ).pack()

        phone_entry = tk.Entry(
            window,
            width=35
        )

        phone_entry.pack(
            pady=5
        )

        tk.Label(
            window,
            text="Email"
        ).pack()

        email_entry = tk.Entry(
            window,
            width=35
        )

        email_entry.pack(
            pady=5
        )

        def start_registration():

            name = name_entry.get().strip()

            department = (
                department_entry.get().strip()
            )

            phone = (
                phone_entry.get().strip()
            )

            email = (
                email_entry.get().strip()
            )

            if not name:

                messagebox.showerror(
                    "Error",
                    "Please enter a name."
                )

                return

            user_data = {

                "name": name,

                "department": department,

                "phone": phone,

                "email": email
            }

            window.destroy()

            try:

                from face.register_face import (
                    register_face
                )

                user_id = register_face(
                    user_data
                )

                if user_id:

                    messagebox.showinfo(
                        "Registration Successful",
                        "Face registration completed.\n\n"
                        f"User ID: {user_id}\n\n"
                        "Remember to train the face model "
                        "before recognition."
                    )

                    self.refresh_dashboard()

                else:

                    messagebox.showerror(
                        "Registration Failed",
                        "Face registration failed."
                    )

            except Exception as error:

                print(
                    "Registration error:",
                    error
                )

                messagebox.showerror(
                    "Registration Error",
                    str(error)
                )

        tk.Button(
            window,
            text="START FACE CAPTURE",
            width=25,
            height=2,
            command=start_registration
        ).pack(
            pady=25
        )

    # ======================================================
    # START ATTENDANCE
    # ======================================================

    def start_attendance(self):

        if (
            self.attendance_process is not None
            and self.attendance_process.poll() is None
        ):

            messagebox.showinfo(
                "Attendance",
                "Attendance is already running."
            )

            return

        try:

            project_root = os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )

            self.attendance_process = subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "face.recognize"
                ],
                cwd=project_root
            )

            self.start_button.config(
                state=tk.DISABLED
            )

            self.stop_button.config(
                state=tk.NORMAL
            )

            self.status_label.config(
                text=(
                    "Database: CONNECTED | "
                    "Attendance: RUNNING"
                )
            )

        except Exception as error:

            self.attendance_process = None

            messagebox.showerror(
                "Attendance Error",
                str(error)
            )

    # ======================================================
    # STOP ATTENDANCE
    # ======================================================

    def stop_attendance(self):

        if self.attendance_process is None:

            return

        try:

            if (
                self.attendance_process.poll()
                is None
            ):

                self.attendance_process.terminate()

                try:

                    self.attendance_process.wait(
                        timeout=3
                    )

                except subprocess.TimeoutExpired:

                    self.attendance_process.kill()

            self.attendance_process = None

            self.start_button.config(
                state=tk.NORMAL
            )

            self.stop_button.config(
                state=tk.DISABLED
            )

            self.status_label.config(
                text=(
                    "Database: CONNECTED | "
                    "Attendance: STOPPED"
                )
            )

        except Exception as error:

            print(
                "Stop attendance error:",
                error
            )

    # ======================================================
    # VISITOR ENTRY
    # ======================================================

    def visitor_entry(self):

        try:

            project_root = os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )

            subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "visitor.register_visitor"
                ],
                cwd=project_root
            )

        except Exception as error:

            messagebox.showerror(
                "Visitor Entry Error",
                str(error)
            )

    # ======================================================
    # VISITOR EXIT
    # ======================================================

    def visitor_exit(self):

        try:

            project_root = os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )

            subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "visitor.exit_visitor"
                ],
                cwd=project_root
            )

        except Exception as error:

            messagebox.showerror(
                "Visitor Exit Error",
                str(error)
            )

    # ======================================================
    # ATTENDANCE REPORT
    # ======================================================

    def attendance_report(self):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Attendance Report"
        )

        window.geometry(
            "900x600"
        )

        window.resizable(
            True,
            True
        )

        tk.Label(
            window,
            text="ATTENDANCE REPORT",
            font=("Arial", 18, "bold")
        ).pack(
            pady=15
        )

        # --------------------------------------------------
        # Table frame
        # --------------------------------------------------

        frame = tk.Frame(
            window
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "id",
            "user_id",
            "name",
            "department",
            "date",
            "time",
            "status"
        )

        table = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "Record ID",
            "user_id": "User ID",
            "name": "Name",
            "department": "Department",
            "date": "Date",
            "time": "Time",
            "status": "Status"
        }

        widths = {
            "id": 80,
            "user_id": 80,
            "name": 180,
            "department": 140,
            "date": 120,
            "time": 100,
            "status": 100
        }

        for column in columns:

            table.heading(
                column,
                text=headings[column]
            )

            table.column(
                column,
                width=widths[column]
            )

        # --------------------------------------------------
        # Scrollbars
        # --------------------------------------------------

        vertical_scrollbar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=table.yview
        )

        horizontal_scrollbar = ttk.Scrollbar(
            frame,
            orient="horizontal",
            command=table.xview
        )

        table.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        table.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        vertical_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        horizontal_scrollbar.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        frame.rowconfigure(
            0,
            weight=1
        )

        frame.columnconfigure(
            0,
            weight=1
        )

        # --------------------------------------------------
        # LOAD ALL ATTENDANCE DIRECTLY FROM DATABASE
        # --------------------------------------------------

        try:

            cursor = self.db.connection.cursor()

            cursor.execute(
                """
                SELECT
                    attendance.id,
                    attendance.user_id,
                    users.name,
                    users.department,
                    attendance.date,
                    attendance.time,
                    attendance.status
                FROM attendance
                LEFT JOIN users
                    ON attendance.user_id = users.id
                ORDER BY
                    attendance.date DESC,
                    attendance.time DESC
                """
            )

            records = cursor.fetchall()

            print(
                f"Attendance records found: {len(records)}"
            )

            for record in records:

                table.insert(
                    "",
                    "end",
                    values=record
                )

            # ------------------------------------------------
            # No records
            # ------------------------------------------------

            if len(records) == 0:

                tk.Label(
                    window,
                    text="No attendance records found.",
                    font=("Arial", 12)
                ).pack(
                    pady=10
                )

        except Exception as error:

            print(
                "Attendance report error:",
                error
            )

            messagebox.showerror(
                "Report Error",
                str(error)
            )

    # ======================================================
    # VISITOR REPORT
    # ======================================================

    def visitor_report(self):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Visitor Report"
        )

        window.geometry(
            "900x500"
        )

        tk.Label(
            window,
            text="VISITOR REPORT",
            font=("Arial", 18, "bold")
        ).pack(
            pady=15
        )

        columns = (
            "id",
            "name",
            "purpose",
            "host",
            "entry",
            "exit"
        )

        table = ttk.Treeview(
            window,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "name": "Visitor Name",
            "purpose": "Purpose",
            "host": "Host",
            "entry": "Entry Time",
            "exit": "Exit Time"
        }

        for column in columns:

            table.heading(
                column,
                text=headings[column]
            )

        table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        try:

            cursor = self.db.connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    visitor_name,
                    purpose,
                    host,
                    entry_time,
                    exit_time
                FROM visitors
                ORDER BY id DESC
                """
            )

            records = cursor.fetchall()

            for record in records:

                table.insert(
                    "",
                    "end",
                    values=record
                )

        except Exception as error:

            messagebox.showerror(
                "Visitor Report Error",
                str(error)
            )

    # ======================================================
    # CLOSE
    # ======================================================

    def close(self):

        self.stop_attendance()

        try:

            self.db.close()

        except Exception:
            pass

        self.root.destroy()


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    root = tk.Tk()

    dashboard = AdminDashboard(
        root
    )

    root.protocol(
        "WM_DELETE_WINDOW",
        dashboard.close
    )

    root.mainloop()
