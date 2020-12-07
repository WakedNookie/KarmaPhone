#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import datetime
from datetime import datetime, date, time

class PK_DB:
    
    def __init__(self, database):
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_URL(self, phone):
        with self.connection:
            return self.cursor.execute("SELECT PhoneLink FROM Ish WHERE (StartPhone <= ? AND EndPhone >= ?)", (phone,phone)).fetchone()

    def add_Phone(self, PhoneCode, StartPhone, EndPhone, PhoneLink, OnURL):
        with self.connection:
            return self.cursor.execute("INSERT INTO Ish (PhoneCode, StartPhone, EndPhone, PhoneLink, OnURL) VALUES(?,?,?,?,?)", (PhoneCode, StartPhone, EndPhone, PhoneLink, OnURL))

       def close(self):
        self.connection.close()
