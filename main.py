import sqlalchemy as sq
import json
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime


Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40))

class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40))
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref="book")

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), nullable=False)

    stock = relationship("Stock", back_populates="shop")
class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    count = sq.Column(sq.Integer)

    book = relationship(Book, backref="stock")
    shop = relationship(Shop, back_populates="stock")

class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.DateTime)
    count = sq.Column(sq.Integer)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)

    stock = relationship(Stock, backref="sale")


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

user_name = ''
password = ''
data_base = ''
DSN = f'postgresql://{user_name}:{password}@localhost:5432/{data_base}'
engine = sq.create_engine(DSN)


Session = sessionmaker(bind=engine)
session = Session()

create_tables(engine)

autor_1 = Publisher(name='Пушкин')
autor_2 = Publisher(name='Толстой')
session.add_all([autor_1, autor_2])
session.commit()

book_1 = Book(title='Капитанская дочка', publisher=autor_1)
book_2 = Book(title='Евгений Онегин', publisher=autor_1)
book_3 = Book(title='Война и мир', publisher=autor_2)
book_4 = Book(title='Анна Каренина', publisher=autor_2)
session.add_all([book_1, book_2, book_3, book_4])
session.commit()

shop_1 = Shop(name='Читатель')
shop_2 = Shop(name='Мир книг')
session.add_all([shop_1, shop_2])
session.commit()

stock_1 = Stock(count=10, book=book_1, shop=shop_1)
stock_2 = Stock(count=8, book=book_2, shop=shop_1)
stock_3 = Stock(count=15, book=book_3, shop=shop_1)
stock_4 = Stock(count=10, book=book_4, shop=shop_1)
stock_5 = Stock(count=12, book=book_1, shop=shop_2)
stock_6 = Stock(count=10, book=book_2, shop=shop_2)
stock_7 = Stock(count=10, book=book_3, shop=shop_2)
session.add_all([stock_1, stock_2, stock_3, stock_4, stock_5, stock_6, stock_7])
session.commit()

sale_1 = Sale(price=300, date_sale='2023-10-10 20:00:32', count=1, stock=stock_1)
sale_2 = Sale(price=250, date_sale='2023-10-14 12:00:00', count=1, stock=stock_2)
sale_3 = Sale(price=600, date_sale='2023-11-01 14:00:00', count=1, stock=stock_3)
sale_4 = Sale(price=500, date_sale='2023-11-04 17:00:00', count=1, stock=stock_4)
sale_5 = Sale(price=300, date_sale='2023-11-06 15:00:00', count=1, stock=stock_5)
sale_6 = Sale(price=300, date_sale='2023-11-08 18:00:00', count=1, stock=stock_6)
sale_7 = Sale(price=700, date_sale='2023-11-17 11:00:00', count=1, stock=stock_7)
session.add_all([sale_1, sale_2, sale_3, sale_4, sale_5, sale_6, sale_7])
session.commit()



def get_sale(autor_or_id):
    query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)\
        .select_from(Shop)\
        .join(Stock)\
        .join(Book)\
        .join(Publisher)\
        .join(Sale)
    if autor_or_id.isdigit():
        result = query.filter(Publisher.id == autor_or_id).all()
    else:
        result = query.filter(Publisher.name == autor_or_id).all()
    for title, shop, sale, data_of_sale in result:
        print(f'{title} | {shop} | {sale} | {data_of_sale}')

if __name__ == '__main__':
    autor_or_id = input()
    get_sale(autor_or_id)
    session.close()




