from PyQt5.QtGui import *                         #من هنا
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
import sys
import mysql.connector
import datetime
from xlsxwriter import *
from xlrd import *


MainUI,_=loadUiType('main.ui')

class Main(QMainWindow,MainUI):
    def __init__(self,perant=None):
        super(Main,self).__init__(perant)
        QMainWindow.__init__(self)
        self.setupUi(self)                          # الى هنا كود مكرر
        self.UI_changes()
        self.Db_connect()
        self.Handel_Button()
        self.open_daily_movment_tap()
        self.Handel_to_Day_Work()
        self.show_All_categorys()
        self.show_Branch()
        self.show_publisher()
        self.show_Auther()
        self.show_employee()
        self.show_all_books()
        self.show_all_Clients()
        ##
        #self.Rrtreive_Day_work()




    def UI_changes(self):
        #UI change in the logen
        self.tabWidget.tabBar().setVisible(False)

    def Db_connect(self):
        #coonect database
        self.db=mysql.connector.connect(host='localhost',user='root',password='20112019',database='lb2')
        self.cur = self.db.cursor()


    def Handel_Button(self):
        self.pushButton.clicked.connect(self.open_daily_movment_tap)
        self.pushButton_2.clicked.connect(self.open_Books)
        self.pushButton_3.clicked.connect(self.open_Client)
        self.pushButton_4.clicked.connect(self.open_Control)
        self.pushButton_5.clicked.connect(self.open_Sitteng)
        self.pushButton_6.clicked.connect(self.open_History )
        self.pushButton_7.clicked.connect(self.open_Repots)


        self.pushButton_21.clicked.connect(self.Add_Branch)
        self.pushButton_22.clicked.connect(self.Add_Publisher)
        self.pushButton_23.clicked.connect(self.Add_Author)
        self.pushButton_25.clicked.connect(self.Add_Category)
        self.pushButton_27.clicked.connect(self.Add_Employee)

        self.pushButton_11.clicked.connect(self.Add_new_Book)
        self.pushButton_37.clicked.connect(self.Edit_Book_search)
        self.pushButton_13.clicked.connect(self.Edet_book)
        self.pushButton_12.clicked.connect(self.Delete_Book)
        self.pushButton_9.clicked.connect(self.All_books_filer)
        self.pushButton_34.clicked.connect(self.Books_Export_Report)

        self.pushButton_16.clicked.connect(self.Add_new_Client)
        self.pushButton_20.clicked.connect(self.Edit_Client_search)
        self.pushButton_19.clicked.connect(self.Edit_Client)
        self.pushButton_24.clicked.connect(self.Delete_Client)
        self.pushButton_44.clicked.connect(self.Clients_Export_Report)

        #self.pushButton_8.clicked.connect(self.Handel_to_Day_Work)

        self.pushButton_29.clicked.connect(self.check_employee)
        self.pushButton_28.clicked.connect(self.Edit_Employee_Informatain)
        self.pushButton_30.clicked.connect(self.Add_User_Permissions)



    def Handel_Ligen(self):
        #Handel logen
        pass

    def Handel_Rest_Password(self):
        #rest password
        pass

    def Handel_to_Day_Work(self):

        #Function work of day
        Book_title =self.lineEdit.text()
        type = self.comboBox.currentIndex()
        client_national_id =1

        from_date =datetime.datetime.now()
        to_date =datetime.datetime.now()
        branch = 1
        #employee =1
        date = datetime.datetime.now()

        self.cur.execute('''
        insert into daily_movements(book_id , client_id , type , date ,branch_id, book_from , book_to)values(%s,%s,%s,%s,%s,%s,%s)'''
                ,(Book_title,client_national_id,type,date,branch,from_date,to_date))
        self.db.commit()
        print('done')
        self.Rrtreive_Day_work()


    def Rrtreive_Day_work(self):
       self.cur.execute('''select book_id,type,client_id,book_from, book_to from daily_movements ''')
       data = self.cur.fetchall()

       self.tableWidget.setRowCount(0)
       self.tableWidget.insertRow(0)
       for row , form in enumerate(data):
           for column , item in enumerate(form):
               if column==1:
                   if row ==0 :
                       self.tableWidget.setItem(row, column, QTableWidgetItem(str('Rent')))
                   else:
                       self.tableWidget.setItem(row, column, QTableWidgetItem(str('Retrieve')))
               elif column==2:
                   sql ='''select name from clients where national_id=%s'''
                   self.cur.execute(sql,[(item)])
                   clent_name = self.cur.fetchone()
                   self.tableWidget.setItem(row, column, QTableWidgetItem(str(clent_name)))
               else:
                   self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))

               column +=1
           row_pisation =self.tableWidget.rowCount()
           self.tableWidget.insertRow(row_pisation)



############################################
############Books##############
    def show_all_books(self):
        #show all books
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)
        self.cur.execute('''select  code ,title ,category_id ,auther_id,price from books ''')
        data = self.cur.fetchall()
        for row ,form in enumerate(data):
            for col, item in enumerate(form):
                if col == 2:
                    sql = '''select cetgory_name  from category where id=%s'''
                    self.cur.execute(sql, [(item+1)])
                    category_name = self.cur.fetchone()
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(category_name[0])))

                elif col == 3:
                        sql = '''select Name  from auther where id=%s'''
                        self.cur.execute(sql, [(item + 1)])
                        auther_name = self.cur.fetchone()
                        self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(auther_name[0])))
                else:
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(item)))

                col += 1

            row_pisation =self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_pisation)

    def All_books_filer(self):
        title_book =self.lineEdit_2.text()
        #category = self.comboBox_2.currentIndex()

        sql = '''
            select  code,title , category_id,auther_id, price  from books where title= %s
        '''
        self.cur.execute(sql,[title_book])
        data = self.cur.fetchall()
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)

        print(data)
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                if col == 2:
                    sql = '''select cetgory_name  from category where id=%s'''
                    self.cur.execute(sql, [(item + 1)])
                    category_name = self.cur.fetchone()
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(category_name[0])))

                elif col == 3:
                    sql = '''select Name  from auther where id=%s'''
                    self.cur.execute(sql, [(item + 1)])
                    auther_name = self.cur.fetchone()
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(auther_name[0])))
                else:
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(item)))

                col += 1

            row_pisation =self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_pisation)




    def Add_new_Book(self):
        #add new book
        Book_title = self.lineEdit_4.text()
        Book_category = self.comboBox_4.currentIndex()
        Book_Description = self.textEdit.toPlainText()
        Book_price = self.lineEdit_8.text()
        Book_code = self.lineEdit_6.text()
        Book_barcode = self.lineEdit_50.text()
        publisher = self.comboBox_5.currentIndex()
        auther = self.comboBox_6.currentIndex()
        status = self.comboBox_7.currentIndex()
        part_Order = self.lineEdit_7.text()

        date = datetime.datetime.now()
        self.cur.execute('''
                    insert into books(title,description,code, barcode,part_order,price,publisher_id,auther_id ,status,date,category_id)
                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ''', (Book_title, Book_Description, Book_code, Book_barcode, part_Order, Book_price, publisher, auther,
        status, date, Book_category))##وقفت عند مشكلة id المربوط بشكل مشكلة سوف اقوم بحذف السجلات المرتبطه واجيب بدلها من غيرربط
        self.db.commit()
        self.show_all_books()




    def Edit_Book_search(self):
        #Edit Book
        book_code = self.lineEdit_12.text()
        sql = ('''select * from books where code =%s''')
        self.cur.execute(sql, [(book_code)])
        data = self.cur.fetchone()

        self.lineEdit_5.setText(data[1])
        self.plainTextEdit_2.setPlainText(data[2])
        self.comboBox_9.setCurrentIndex(int(data[3]))
        self.lineEdit_10.setText(str(data[7]))
        self.lineEdit_9.setText(data[4])
        self.comboBox_10.setCurrentIndex(int(data[8]))
        self.comboBox_24.setCurrentIndex(int(data[11]))
        self.lineEdit_11.setText(data[6])

        self.show_all_books()


    def Edet_book(self):
        Book_title = self.lineEdit_5.text()
        Book_category = self.comboBox_9.currentIndex()
        Book_Description = self.plainTextEdit_2.toPlainText()
        Book_price = self.lineEdit_10.text()
        Book_code = self.lineEdit_12.text()

        publisher = self.comboBox_10.currentIndex()
        auther = self.comboBox_8.currentIndex()
        status = self.comboBox_24.currentIndex()
        part_Order = self.lineEdit_11.text()

        self.cur.execute('''
            UPDATE books SET title = %s , description=%s , code =%s ,part_order=%s ,price=%s , status =%s ,category_id = %s ,publisher_id = %s , auther_id = %s  WHERE code = %s
        ''',(Book_title,Book_Description,Book_code,part_Order,Book_price,status,Book_category,publisher,auther,Book_code))
        self.db.commit()

        self.statusBar().showMessage('تم تعديل الكتاب بنجاح')
        self.show_all_Clients()

    def Delete_Book(self):
        #delete book
        Book_code = self.lineEdit_12.text()
        delet_message = QMessageBox.warning(self,'مسح معلومات','هل انت متأكد من مسح الكتاب ', QMessageBox.Yes | QMessageBox.No)
        if delet_message.QMessageBox.Yes :
            sql= (''' DELETE FROM books WHERE code =%s''')
            self.cur.execute(sql,[(Book_code)])
            self.db.commit()
            self.statusBar().showMessage('تم حذف الكتاب بنجاح')
            self.show_all_books()



#############################Client
    def show_all_Clients(self):
        #show all Clients
        self.tableWidget_4.setRowCount(0)
        self.tableWidget_4.insertRow(0)
        self.cur.execute('''select  name ,mail ,phone ,national_id,date from clients ''')
        data = self.cur.fetchall()
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_4.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1

            row_pisation = self.tableWidget_4.rowCount()
            self.tableWidget_4.insertRow(row_pisation)

    def Add_new_Client(self):
        #add new Client
        Add_name = self.lineEdit_14.text()
        Add_mail = self.lineEdit_15.text()
        Add_phone = self.lineEdit_16.text()
        Add_national_id = self.lineEdit_17.text()
        date =datetime.datetime.now()
        self.cur.execute(''' insert into clients(name,mail,phone,date,national_id)
            values(%s,%s,%s,%s,%s)        
        ''',(Add_name,Add_mail,Add_phone,date,Add_national_id))
        self.db.commit()
        self.show_all_Clients()
        print('Addint')

    def Edit_Client_search(self):
        #Edit Client
        client_data = self.lineEdit_27.text()
        if self.comboBox_14.currentIndex() ==0:
            sql = ('''select * from clients where name =%s''')
            self.cur.execute(sql, [(client_data)])
            data = self.cur.fetchone()

        if self.comboBox_14.currentIndex() ==1:
            sql = ('''select * from clients where mail =%s''')
            self.cur.execute(sql, [(client_data)])
            data = self.cur.fetchone()

        if self.comboBox_14.currentIndex() ==2:
            sql = ('''select * from clients where phone =%s''')
            self.cur.execute(sql, [(client_data)])
            data = self.cur.fetchone()

        if self.comboBox_14.currentIndex() ==3:
            sql = ('''select * from clients where national_id =%s''')
            self.cur.execute(sql, [(client_data)])
            data = self.cur.fetchone()

        self.lineEdit_25.setText(data[1])
        self.lineEdit_23.setText(data[2])
        self.lineEdit_26.setText(str(data[4]))
        self.lineEdit_24.setText(str(data[5]))






    def Edit_Client(self):
        clientname = self.lineEdit_25.text()
        clientmail =self.lineEdit_23.text()
        clientphone =self.lineEdit_26.text()
        clientnational_id =self.lineEdit_24.text()

        self.cur.execute(''' UPDATE clients SET name = %s , mail=%s , phone =%s ,national_id=%s 
                    ''', (clientname, clientmail, clientphone, clientnational_id))
        self.db.commit()

        self.statusBar().showMessage('تم تعديل العميل بنجاح')

    def Delete_Client(self):
        #delete Client
        client_data = self.lineEdit_27.text()
        #delet_message = QMessageBox.warning(self, 'مسح معلومات', 'هل انت متأكد من مسح الكتاب ',QMessageBox.Yes | QMessageBox.No)
        #if delet_message.QMessageBox.Yes:

        if self.comboBox_14.currentIndex() ==0:
            sql = ('''delete from clients where name =%s''')
            self.cur.execute(sql, [(client_data)])



        if self.comboBox_14.currentIndex() ==1:
            sql = ('''delete from clients where mail =%s''')
            self.cur.execute(sql, [(client_data)])


        if self.comboBox_14.currentIndex() ==2:
            sql = ('''delete from clients where phone =%s''')
            self.cur.execute(sql, [(client_data)])


        if self.comboBox_14.currentIndex() ==3:
            sql = ('''delete from clients where national_id =%s''')
            self.cur.execute(sql, [(client_data)])

        self.db.commit()
        self.statusBar().showMessage('تم حذف العميل بنجاح')
        self.show_all_Clients()

#######################################
###############
    def Show_History(self):
        #show history
        pass
#######################################
################report
    def All_Book_Report(self):
        #all book report
        pass


    def Books_Fild_Report(self):
        #book fild report
        pass

    def Books_Export_Report(self):
        # book Export report
        self.cur.execute('''select  code ,title ,category_id ,auther_id,price from books ''')
        data = self.cur.fetchall()

        excel_file = Workbook('book_report.xlsx')
        sheet1 = excel_file.add_worksheet()
        sheet1.write(0,0,'Book Code')
        sheet1.write(0,1,'Book Title')
        sheet1.write(0,2,'Category')
        sheet1.write(0,3,'Auther')
        sheet1.write(0,4,'Price')

        row_number =1
        for row in data:
            coulam_number =0
            for itme in row:
                sheet1.write(row_number,coulam_number,str(itme))
                coulam_number+=1
            row_number +=1
        excel_file.close()
        self.statusBar().showMessage('تم رفع التقرير بنجاح')

####################################client
    def All_Clients_Report(self):
        #all Clients report
        pass

    def Clients_Fild_Report(self):
        #Clients fild report
        pass

    def Clients_Export_Report(self):
        # Clients Export report
        self.cur.execute('''select  name ,mail ,phone ,national_id from clients ''')
        data = self.cur.fetchall()

        excel_file = Workbook('Clients_report.xlsx')
        sheet1 = excel_file.add_worksheet()
        sheet1.write(0, 0, 'Clients name')
        sheet1.write(0, 1, 'Client Mail')
        sheet1.write(0, 2, 'Client phone')
        sheet1.write(0, 3, 'Client National id')

        row_number = 1
        for row in data:
            coulam_number = 0
            for itme in row:
                sheet1.write(row_number, coulam_number, str(itme))
                coulam_number += 1
            row_number += 1
        excel_file.close()
        self.statusBar().showMessage('تم رفع تقريرالعملاء بنجاح')

##########################################
    def Monthly_Report(self):
        #monthly report
        pass
    def Monthly_Report_Export(self):
        #monthly report Export
        pass
##########################################
#################################SettBing
    def Add_Branch(self):
        #add branch
        branch_name =self.lineEdit_31.text()
        branch_code =self.lineEdit_28.text()
        branch_location = self.lineEdit_32.text()
        self.cur.execute('''insert into branch (name,code,location)values(%s,%s,%s)
             ''',(branch_name,branch_code,branch_location) )
        self.db.commit()
        print('branch add')
        self.show_Branch()


    def Add_Publisher(self):
        #add publisher
        publisher_name = self.lineEdit_29.text()
        publisher_location = self.lineEdit_33.text()
        self.cur.execute('''insert into publisher(name,location)values(%s,%s)
        ''',(publisher_name,publisher_location))
        self.db.commit()
        print('publisher add')
        self.show_publisher()

    def Add_Author(self):
        #add auther
        author_name = self.lineEdit_30.text()
        author_location = self.lineEdit_34.text()
        self.cur.execute('''insert into auther(name,location)values(%s,%s)
                ''', (author_name,author_location))
        self.db.commit()
        print('auther add')
        self.show_Auther()

    def Add_Category(self):
        #add category
        catrgoty_name = self.lineEdit_35.text()
        pearant_category_text = self.comboBox_3.currentText()   #من اجل اختيار القيمة الحالية

        query = '''select id from category where cetgory_name=%s '''     # ال%s عشان يرجع قيمة ال pearant_category_text
        self.cur.execute(query,[(pearant_category_text)])                # مناجل ادخال القيمة
        data=self.cur.fetchone()
        pearant_category =data[0]                    #### ##من اجل اضافة القيمة الى الid يعني القيمة الجديده يكون لها اب مرتبطة ب idحقه###
        print(pearant_category)

        self.cur.execute(''' insert into category(cetgory_name,Perent_category)values(%s,%s)''',(catrgoty_name,pearant_category))
        self.db.commit()
        self.show_All_categorys()

    def Add_Employee(self):
        #add employee
        employee_name = self.lineEdit_38.text()
        employee_mail = self.lineEdit_36.text()
        employee_phone= self.lineEdit_37.text()
        employee_branch= self.comboBox_22.currentIndex()
        employee_national_id= self.lineEdit_39.text()
        periorty= self.lineEdit_48.text()
        password= self.lineEdit_41.text()
        password2= self.lineEdit_40.text()

        date = datetime.datetime.now()

        if password == password2 :
            self.cur.execute(''' insert into employee(name,mail, phone  ,national_id, periority  ,date,branch_id,password)
            values(%s,%s,%s,%s,%s,%s,%s,%s)
            ''',(employee_name,employee_mail,employee_phone,employee_national_id,periorty,date,employee_branch ,password))
            self.db.commit()
            self.statusBar().showMessage('تم اضافة الموظف بنجاح')
        else:
            print('wring password')

        self.lineEdit_38.setText(' ')
        self.lineEdit_36.setText(' ')
        self.lineEdit_37.setText(' ')
        self.lineEdit_39.setText(' ')
        self.lineEdit_48.setText(' ')
        self.lineEdit_41.setText(' ')
        self.lineEdit_40.setText(' ')




    def check_employee(self):
        employee_name =self.lineEdit_42.text()
        employee_password =self.lineEdit_46.text()

        self.cur.execute('''select * from employee''')
        data = self.cur.fetchall()
        print(data)
        for lor in data :
            if lor[1]==employee_name and lor[8  ]== employee_password :
                self.groupBox_7.setEnabled(True)
                print(lor)
                self.lineEdit_44.setText(lor[2])
                self.lineEdit_45.setText(str(lor[3]))
                self.lineEdit_43.setText(str(lor[5]))
                self.lineEdit_49.setText(str(lor[6]))
                self.lineEdit_47.setText(str(lor[8]))
                self.comboBox_23.setCurrentIndex(lor[7])


    def Edit_Employee_Informatain(self):
        #edit employee informatain
        employee_name = self.lineEdit_42.text()
        employee_password = self.lineEdit_46.text()
        employee_mail=self.lineEdit_44.text()
        employee_phone=self.lineEdit_45.text()
        employee_national_id=self.lineEdit_43.text()
        employee_periorty=self.lineEdit_49.text()
        employee_password2=self.lineEdit_47.text()
        employee_branch=self.comboBox_23.currentIndex()

        date =datetime.datetime.now()
        if employee_password == employee_password2 :
            self.cur.execute('''
                UPDATE employee SET mail=%s,phone=%s,national_id=%s,periority=%s,branch_id=%s,password=%s WHERE name=%s
            ''',(employee_mail,employee_phone,employee_national_id,employee_periorty,employee_branch,employee_password2,employee_name ))
        self.db.commit()
        self.lineEdit_42.setText(' ')
        self.lineEdit_46.setText('  ')
        self.lineEdit_45.setText(' ')
        self.lineEdit_44.setText(' ')
        self.lineEdit_45.setText(' ')
        self.lineEdit_43.setText(' ')
        self.lineEdit_49.setText(' ')
        self.lineEdit_47.setText(' ')
        self.comboBox_23.setCurrentIndex(0)
        self.groupBox_7.setEnabled(False)
        self.statusBar().showMessage('تم تعديل معلومات الموظف بنجاح')

    def Add_User_Permissions(self):
        #Add User Permissions
        employee_name =self.comboBox_19.currentText()
        if self.checkBox_23.isChecked() == True:
            self.cur.execute('''
                            INSERT INTO employee_prmission (employee_name,books_tab,clients_tab,dashbord_tab,history_tab,report_tab,setting_tab,
                            Add_book,Edit_book,Delete_book,import_book,export_book,Add_client,Edit_client,Delete_client,import_client,export_client,
                            Add_bransh,Add_publisher,Add_auther,Add_category,Add_employee,Edit_employee,is_admin)        
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                             , ( employee_name, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1,1, 1, 1,1))
            self.db.commit()
            print('addint')
            self.statusBar().showMessage('تم اضافة كـل الصلاحيات للموضف الموظف بنجاح')

        else:
                books_tab = 0
                clients_tab = 0
                dashbord_tab = 0
                hostory_tab = 0
                report_tab = 0
                setting_tab = 0

                Add_book = 0
                EDit_book = 0
                Delete_book = 0
                import_book = 0
                export_book = 0

                Add_client = 0
                EDit_client = 0
                Delete_client = 0
                import_client = 0
                export_client = 0

                Add_bransh = 0
                Add_publisher = 0
                Add_auther = 0
                Add_categpry =0
                Add_employee =0
                Edit_employee =0
                ####################################tabs
                if self.checkBox_6.isChecked() == True:
                    books_tab = 1
                if self.checkBox_7.isChecked() == True:
                    clients_tab = 1
                if self.checkBox_9.isChecked() == True:
                    dashbord_tab = 1
                if self.checkBox_10.isChecked() == True:
                    hostory_tab = 1
                if self.checkBox_3.isChecked() == True:
                    report_tab = 1
                if self.checkBox_12.isChecked() == True:
                    setting_tab = 1
                ##########################books
                if self.checkBox_2.isChecked() == True:
                    Add_book = 1
                if self.checkBox_4.isChecked() == True:
                    EDit_book = 1
                if self.checkBox_5.isChecked() == True:
                    Delete_book = 1
                if self.checkBox_13.isChecked() == True:
                    import_book = 1
                if self.checkBox_14.isChecked() == True:
                    export_book = 1
                ##############################clients
                if self.checkBox_8.isChecked() == True:
                    Add_client = 1
                if self.checkBox_11.isChecked() == True:
                    EDit_client = 1
                if self.checkBox.isChecked() == True:
                    Delete_client = 1
                if self.checkBox_16.isChecked() == True:
                    import_client = 1
                if self.checkBox_15.isChecked() == True:
                    export_client = 1

                #################################sittengs
                if self.checkBox_20.isChecked() == True:
                    Add_bransh = 1
                if self.checkBox_17.isChecked() == True:
                    Add_publisher = 1
                if self.checkBox_19.isChecked() == True:
                    Add_auther = 1
                if self.checkBox_21.isChecked() == True:
                    Add_categpry = 1
                if self.checkBox_18.isChecked() == True:
                    Add_employee = 1
                if self.checkBox_22.isChecked() == True:
                    Edit_employee = 1

                self.cur.execute('''
                    INSERT INTO employee_prmission (employee_name,books_tab,clients_tab,dashbord_tab,history_tab,report_tab,setting_tab,
                    Add_book,Edit_book,Delete_book,import_book,export_book,Add_client,Edit_client,Delete_client,import_client,export_client,
                    Add_bransh,Add_publisher,Add_auther,Add_category,Add_employee,Edit_employee)        
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                ,(employee_name,books_tab,clients_tab,dashbord_tab,hostory_tab,report_tab,setting_tab,Add_book,EDit_book,Delete_book,import_book,export_book,Add_client,EDit_client,Delete_client,import_client,export_client,Add_bransh,Add_publisher,Add_auther,Add_categpry,Add_employee,Edit_employee))
                self.db.commit()
                print('addint')
                self.statusBar().showMessage('تم اضافة الصلاحيات للموضف الموظف بنجاح')


    def Admin_Reports(self):
        #admin reports
        pass

#############################################################
    def show_Branch(self):
        self.comboBox_22.clear()
        self.comboBox_23.clear()
        self.comboBox_16.clear()
        self.cur.execute(''' select name from branch''')
        branches = self.cur.fetchall()
        for branch in branches :
            self.comboBox_22.addItem(str(branch[0]))
            self.comboBox_23.addItem(str(branch[0]))
            self.comboBox_16.addItem(str(branch[0]))


    def show_publisher(self):
        self.comboBox_5.clear()
        self.cur.execute('''select name from publisher''')
        publishers = self.cur.fetchall()
        for publisher in publishers:
            self.comboBox_5.addItem(publisher[0])
            self.comboBox_10.addItem(publisher[0])

    def show_Auther(self):
        self.comboBox_8.clear()
        self.comboBox_6.clear()
        self.cur.execute('''select Name from auther''')
        Authers = self.cur.fetchall()
        for Auther in Authers:
            self.comboBox_8.addItem(Auther[0])
            self.comboBox_6.addItem(Auther[0])


    def show_All_categorys(self): # دالة اضافة قيمة جديده الحلقه تقوم بتنضيف الراجع من قاعدة البيانات
        self.comboBox_3.clear()
        self.comboBox_2.clear()
        self.comboBox_4.clear()
        self.comboBox_9.clear()
        self.cur.execute(''' select cetgory_name from category''')
        categorys= self.cur.fetchall()
        for category in categorys:
            self.comboBox_3.addItem(str(category[0]))
            self.comboBox_2.addItem(str(category[0]))
            self.comboBox_4.addItem(str(category[0]))
            self.comboBox_9.addItem(str(category[0]))


    def show_employee(self):
        self.cur.execute('select name from employee')
        employees= self.cur.fetchall()
        for employee in employees :
            self.comboBox_19.addItem(employee[0])

#####################################
    #مجموعة دوال الازرار للالنتقال بالصفحات
####################################

    def login (self):
        pass

    def   rest_pasword(self):
        pass

    def open_daily_movment_tap (self):
        self.tabWidget.setCurrentIndex(2)

    def open_Books (self):
        self.tabWidget.setCurrentIndex(3)
        self.tabWidget_2.setCurrentIndex(0)

    def open_Client (self):
        self.tabWidget.setCurrentIndex(4)
        self.tabWidget_3.setCurrentIndex(0)

    def open_Control (self):
        self.tabWidget.setCurrentIndex(5)

    def open_History (self):
        self.tabWidget.setCurrentIndex(6)

    def open_Repots (self):
        self.tabWidget.setCurrentIndex(7)
        self.tabWidget_5.setCurrentIndex(0)

    def open_Sitteng (self):
        self.tabWidget.setCurrentIndex(8)
        self.tabWidget_4.setCurrentIndex(0)






def main():                                           #كود مكرر حفظ
    App = QApplication(sys.argv)
    window = Main()
    window.show()
    App.exec_()
if __name__== '__main__':
    main()




