from sqlite3 import *

class Database:
    def __init__(self, db_file):
        self.connection = connect(db_file)
        self.cursor = self.connection.cursor()
    
    def user_exists(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            s = len(res)
            if s>0:
                return True
            else:
                return False

    def create_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`, `money`) VALUES (?,?)", (user_id,0))

    def user_money(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT `money` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchmany(1)
            return int(res[0][0])

    def set_money(self, user_id, money):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `money` = ? WHERE `user_id` = ?", (money,user_id,))


    
    def add_check(self, user_id,money,bill_id):
        with self.connection:
            self.cursor.execute("INSERT INTO `check` (`user_id`, `money`,`bill_id`) VALUES (?,?,?)", (user_id,money,bill_id,))

    
    def get_check(self, bill_id):
        with self.connection:
            res = self.cursor.execute("SELECT * FROM `check` WHERE `bill_id` = ?", (bill_id,)).fetchmany(1)
            s = len(res)
            if s>0:
                return res[0]
            else:
                return False

    def del_check(self, bill_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `check` WHERE `bill_id` = ?", (bill_id,))


    def account_exists(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT * FROM `account` WHERE `user_id` = ?", (user_id,)).fetchall()
            s = len(res)
            if s>0:
                return True
            else:
                return False


    def add_account(self, user_id,):
        with self.connection:
            self.cursor.execute("INSERT INTO `account` (`user_id`, `money`,`verif`, `trans`,`number`) VALUES (?,?,?,?,?)", (user_id,0,False,0,0,))
    
    def account_money(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT `money` FROM `account` WHERE `user_id` = ?", (user_id,)).fetchmany(1)
            return int(res[0][0])
    
    def account_verif(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT `verif` FROM `account` WHERE `user_id` = ?", (user_id,))
            s = self.cursor.fetchone()[0]
            if s == 0:
                return False
            else:
                return True

    def account_trans(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT `trans` FROM `account` WHERE `user_id` = ?", (user_id,)).fetchmany(1)
            return int(res[0][0])

    def upd_trans(self, user_id, transac):
        with self.connection:
            return self.cursor.execute("UPDATE `account` SET `trans` = ? WHERE `user_id` = ?", (transac,user_id,))

    def upd_money(self, user_id, money):
        with self.connection:
            return self.cursor.execute("UPDATE `account` SET `money` = ? WHERE `user_id` = ?", (money,user_id,))

    def upd_verif(self, user_id, verif):
        with self.connection:
            return self.cursor.execute("UPDATE `account` SET `verif` = ? WHERE `user_id` = ?", (verif,user_id,))

    def get_number(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT `number` FROM `account` WHERE `user_id` = ?", (user_id)).fetchmany(1)
            return int(res[0][0])

    def upd_number(self,user_id,number):
        with self.connection:
            return self.cursor.execute("UPDATE `account` SET `number` = ? WHERE `user_id` = ?", (number, user_id))




    def del_acc_1(self,user_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `check` WHERE `user_id` = ?", (user_id,))
    def del_acc_2(self,chat_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `users` WHERE `user_id` = ?", (chat_id,))
    def del_acc_3(self,chat_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `account` WHERE `user_id` = ?", (chat_id,))

    def all_acc(self):
        with self.connection:
            res = self.cursor.execute("SELECT * FROM `account`").fetchall()
            return res
