#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import datetime
from datetime import datetime, date, time

# VARIABLES: ID, FirstAppear, Descriptor, Name, IGname, VKname, FBname, OKname

class Isheyka_DB:
    
    def __init__(self, database):
        """Conecting to DB and saving connection cursor"""
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

#     def get_Phones(self):
#         """Obtaining all face descriptors"""
#         with self.connection:
#             return self.cursor.execute("SELECT StartPhone, EndPhone, PhoneLink FROM Isheyka").fetchall()
# #            return self.cursor.execute("SELECT ID, Descriptor, Name FROM FoundFaces").fetchall()

    def get_URL(self, phone):
        """Obtaining all names"""
        with self.connection:
            return self.cursor.execute("SELECT PhoneLink FROM Isheyka WHERE (StartPhone <= ? AND EndPhone >= ?)", (phone,phone)).fetchone()

    def add_Phone(self, PhoneCode, StartPhone, EndPhone, PhoneLink, OnURL):
        """Adding new descriptor into DB"""
        with self.connection:
            return self.cursor.execute("INSERT INTO Isheyka (PhoneCode, StartPhone, EndPhone, PhoneLink, OnURL) VALUES(?,?,?,?,?)", (PhoneCode, StartPhone, EndPhone, PhoneLink, OnURL))

    # def get_id(self):
    #     """Obtaining last created row ID"""
    #     with self.connection:
    #         row_id = self.cursor.execute("SELECT id FROM Isheyka WHERE rowid=last_insert_rowid()").fetchall()
    #         return int((row_id[0])[0])

    # def upd_face(self, id, Descriptor, Name, IGname, VKname, FBname, OKname):
    #     """Whenever needed updating user data"""
    #     with self.connection:
    #         return self.cursor.execute("UPDATE Isheyka SET Descriptor = ?, Name = ?, IGname = ?, VKname = ?, FBname = ?, OKname = ? WHERE id = ?", (Descriptor, Name, IGname, VKname, FBname, OKname, id))
    
    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()

    # def close(self):
    #     """Закрываем соединение с БД"""
    #     self.connection.close()