import pyodbc

class ms_sql:
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=KOMPLAENCE-7304;DATABASE=CRM-DB;uid=sa;pwd=111', timeout=30)

    def addvalues(self, bin, param, value, uid):
        cursor = self.conn.cursor()
        sqlstr = "insert into GoszakupCopy(bin, parameter, value, parentuid) values (N'" + bin + "',N'" + param+ "',N'" + value + "',N'" + uid +"')"
        cursor.execute(sqlstr)
        cursor.commit()

    def addlink(self, link, bin, page, uid):
        cursor = self.conn.cursor()
        sqlstr = "insert into GoszakupLinksCopy(page, link, bin, uid) values (N'" + str(page) + "',N'" + link + "',N'" + bin+ "',N'" + uid +"')"
        print(sqlstr)
        cursor.execute(sqlstr)
        cursor.commit()
