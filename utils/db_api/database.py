import datetime
import sqlite3


class Database:
    def __init__(self, db_path):
        self.db_path = db_path

    async def connect(self):
        return sqlite3.connect(self.db_path)

    async def get_active_image_url(self, name='post'):
        conn = await self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT image_url FROM images WHERE active = ? and name = ?",
                       [True, name])
        row = cursor.fetchone()
        if row:
            image_url = row[0]
        else:
            image_url = None
        conn.close()
        return image_url

    async def deactivate_images(self, name='post'):
        conn = await self.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE images SET active = ? WHERE active = ? and name = ?",
                       [False, True, name])
        conn.commit()
        conn.close()

    async def add_image_url(self, new_image_url, name='post'):
        conn = await self.connect()
        cursor = conn.cursor()
        await self.deactivate_images(name)
        cursor.execute("INSERT INTO images (name, image_url, active, created_time) VALUES (?, ?, ?, ?)",
                       [name, new_image_url, True, datetime.datetime.now()])
        conn.commit()
        conn.close()

    async def get_lid(self, tg_id):
        conn = await self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, tg_id, fullname, phone, school, pinfl, invitation, class_num, created_time, "
                       "update_time FROM lids WHERE tg_id = ?", [tg_id])
        lid = cursor.fetchone()
        conn.close()
        return lid

    async def add_or_update_lid(self, tg_id, fullname, phone, school, pinfl, invitation=None, class_num=None):
        conn = await self.connect()
        cursor = conn.cursor()
        now = datetime.datetime.now().date()
        try:
            cursor.execute(
                "INSERT OR REPLACE INTO lids (tg_id, fullname, phone, school, pinfl, class_num, invitation, "
                "created_time, update_time) VALUES (:tg_id, :fullname, :phone, :school, :pinfl, :class_num, "
                ":invitation, :created_time, :update_time)",
                {
                    'tg_id': tg_id,
                    'fullname': fullname,
                    'phone': phone,
                    'school': school,
                    'pinfl': pinfl,
                    'class_num': class_num,
                    'invitation': invitation,
                    'created_time': now,
                    'update_time': now
                }
            )
            conn.commit()
        except sqlite3.IntegrityError:
            cursor.execute(
                "UPDATE lids SET fullname = :fullname, phone = :phone, school = :school, pinfl = :pinfl, "
                "class_num = :class_num, invitation = :invitation, update_time = :update_time WHERE tg_id = :tg_id",
                {
                    'tg_id': tg_id,
                    'fullname': fullname,
                    'phone': phone,
                    'school': school,
                    'pinfl': pinfl,
                    'class_num': class_num,
                    'invitation': invitation,
                    'update_time': now
                }
            )
            conn.commit()
        finally:
            conn.close()

    async def get_lid_invitation_image(self, tg_id):
        conn = await self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT invitation, fullname FROM lids WHERE tg_id = ?", [tg_id])
        lid = cursor.fetchone()
        conn.close()
        return lid
