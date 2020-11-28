from playhouse.sqlite_ext import SqliteExtDatabase
from peewee import *
import datetime

sqlite_db = MySQLDatabase('lb2',user='root' , password='20112019',host='localhost',port=3306 )



class Auther(Model):
    Name= CharField(unique=True)
    Location= CharField(null=True)


    class Meta:
        database =sqlite_db


class Publisher(Model):
    name = CharField(unique=True)
    location = CharField(null=True)


    class Meta:
        database =sqlite_db



class Category(Model):
    cetgory_name =CharField(unique=True)
    Perent_category =  IntegerField(null=True)

    class Meta:
        database =sqlite_db



class Branch(Model):
    name = CharField()
    code = CharField(null=True,unique=True)
    location = CharField(null=True)


    class Meta:
        database =sqlite_db





BOOK_STATUS = (
      (1,'new'),
      (2,'used'),
      (3,'dameg')

    )

class Books(Model):
    title = CharField(unique=True)
    description =TextField(null=True)
    category = ForeignKeyField(Category,backref='category' ,null=True)
    code = CharField(null=True)
    barcode =CharField()
    part_order=CharField(null=True)
    #pritc =
    price = DecimalField(null=True)
    publisher =ForeignKeyField(Publisher,backref='publisher',null=True)
    auther =ForeignKeyField(Auther,backref='auther',null=True)
    image = CharField(null=True)
    status =CharField(choices=BOOK_STATUS) #choies
    date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database =sqlite_db



class Clients(Model):
    name = CharField()
    mail = CharField(null=True,unique=True)
    phone = CharField(null=True)
    date = DateTimeField(default=datetime.datetime.now)
    national_id = IntegerField(null=True,unique=True)

    class Meta:
        database =sqlite_db




class Employee(Model):
    name = CharField()
    mail = CharField(null=True, unique=True)
    phone = CharField(null=True)
    date = DateTimeField(default=datetime.datetime.now)
    national_id = IntegerField(null=True, )
    periority = IntegerField(null=True)


    class Meta:
        database =sqlite_db




PROSEC_TYPE =(
        (1,'Rent'),
        (2,'Retrieve')
    )

class Daily_Movements(Model):
    book =ForeignKeyField(Books,backref= 'Daiy_boob' )
    client = ForeignKeyField(Clients,backref='Daily_clien')
    type =CharField(choices= PROSEC_TYPE)
    date =DateTimeField(default=datetime.datetime.now)
    branch = ForeignKeyField(Branch,backref='Daily_branch' ,null=True)
    book_from = DateField(null=True)
    book_to = DateField(null=True)
    employee =ForeignKeyField(Employee,backref='Daily_empolyee' ,null=True)


    class Meta:
        database =sqlite_db



ACTONS =(
    (1,'login'),
    (2,'Updet'),
    (3,'Creat'),
    (4,'Delete')
    )

TABLES =(
    (1,'Books'),
    (2,'Clients'),
    (3,'Employee'),
    (4,'Category'),
    (5,'Branch'),
    (6,'Daily Movements'),
    (7,'Publisher'),
    (8,'Auther')
    )

class History(Model):
    employee = ForeignKeyField(Employee,backref='History_empolyee')
    action = CharField(choices=ACTONS)
    table = CharField(choices=TABLES)
    date =DateTimeField(default=datetime.datetime.now)
    branch =ForeignKeyField(Branch,backref='History_Branch')


    class Meta:
        database =sqlite_db






sqlite_db.connect()
sqlite_db.create_tables([Auther,Publisher,Category,Branch,Books,Clients,Employee,Daily_Movements,History])
