import sqlite3
def connect():
    try:
        con = sqlite3.connect("users.db")
        cursor = con.cursor()
    
        cursor.execute("""CREATE TABLE IF NOT EXISTS subscribes(
                user_id int,
                category_id int,
                FOREIGN KEY (user_id) REFERENCES users (ID),                                             FOREIGN KEY (category_id) REFERENCES category (ID),
                primary key(user_id, category_id));""")
        con.commit()
    
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL, 
                name TEXT NOT NULL,
                password TEXT NOT NULL);""")
        con.commit()

        cursor.execute("""CREATE TABLE IF NOT EXISTS category(
                ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT NOT NULL);""")
        con.commit()

        print("Вы успешно подключились")

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

    finally:
        con.close()
  
    
def reg(user_id, login, password):
        print("Авторизация")
        try:
                con = sqlite3.connect("users.db")
                cursor = con.cursor()
                cursor.execute(""" INSERT INTO users(user_id, name, password) VALUES (?, ?, ?);                 """, (user_id, login, password))
                con.commit()
                print("Вы зарегистрированы")
                return "Вы зарегистрированы"       
        except:
                print ('ошибка при регистрации')
        finally:
                con.close()


        
def auth(user_id, password):
        print("Вход в систему")
        con = sqlite3.connect("users.db")
        cursor = con.cursor()
        info = cursor.execute("""SELECT * FROM users WHERE user_id = ? AND password = ?""",                               (user_id, password,)).fetchall()
        print("Вы вошли в систему")


def checkUser(user_id):
        try:
                con = sqlite3.connect("users.db")
                cursor = con.cursor()
                user = cursor.execute("""SELECT user_id FROM users""").fetchall()
                if not user:
                        return 0
                else:
                        return 1
                
        except:
                print ('не достал пароль')
                return 'что-то пошло не так'
        finally:
                con.close()


def news(user_id):
        try:
                con = sqlite3.connect("users.db")
                cursor = con.cursor()
                info = cursor.execute(""" SELECT category.name FROM subscribes        
                                        INNER JOIN category ON subscribes.category_id = category.ID
                                        where user_id = ?
                                        """, (user_id,)).fetchall()

                return info
                        
        except sqlite3.Error as err:
                print(err)
                return "false"
        finally:
                con.close()



def addSub(user_id, category_id):
        try:
                con = sqlite3.connect("users.db")
                cursor = con.cursor()

                catName = cursor.execute("""SELECT name FROM category where ID = ? """, (category_id,)).fetchall()
                print(catName[0][0])

                subscrs = cursor.execute(""" SELECT * FROM subscribes 
                                        where user_id = ? and
                                         category_id=?""", (user_id,category_id)).fetchone()

                if subscrs == None:
                        info = cursor.execute(""" INSERT INTO subscribes (user_id, category_id) values (?, ?)""", (user_id,category_id))
                        con.commit()
                        print(f"Вы подписались на категорию {catName[0][0]}")
                        return f"Вы подписались на категорию {catName[0][0]}"
                else:
                        print(f"Вы уже подписаны на категорию {catName[0][0]}")
                        return f"Вы уже подписаны на категорию {catName[0][0]}"


                      

        except sqlite3.Error as err:
                print(err)
                return "false"
        finally:
                con.close()


def delSub(user_id, category_id):
        try:
                con = sqlite3.connect("users.db")
                cursor = con.cursor()

                catName = cursor.execute("""SELECT name FROM category where ID = ? """, (category_id,)).fetchone()

                subscrs = cursor.execute(""" SELECT category_id FROM subscribes 
                                        where user_id = ? and
                                        category_id=?""", (user_id,category_id)).fetchone()

                if not subscrs:
                        print(f"Вы не подписаны на категорию {catName}")
                        return f"Вы не подписаны на категорию {catName}"
                else:
                        delSub = cursor.execute(""" DELETE FROM subscribes 
                                        where category_id = ?""", (category_id,))
                        con.commit()
                        
                        print(f"Вы отписались от категории {catName}")
                        return f"Вы отписались от категории {catName}"
                
        except sqlite3.Error as err:
                print(err)
                return "false"
        finally:
                con.close()

try:
        con = sqlite3.connect("users.db")
        cursor = con.cursor()
       

except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

finally:
        con.close()