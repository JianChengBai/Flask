from flask import flash

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 设置连接数据
app.config['SQLALCHEMY_DATABASE_URI'] = '*********'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.secret_key = 'sdfjsdfdsdfsdg'
# 实例化SQLAlchemy对象
db = SQLAlchemy(app)


# 定义模型类-作者
class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    books = db.relationship('Book', backref='author')


# 定义模型类-书名
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        author_name = request.form.get('author')
        book_name = request.form.get('book')
        if not all([author_name, book_name]):
            flash('没有参数')
        author = Author.query.filter_by(name=author_name).first()
        if not author:
            try:
                # 添加作者
                author = Author(name=author_name)
                db.session.add(author)
                db.session.commit()
                # 添加书
                book = Book(name=book_name, au_book=author.id)
                db.session.add(book)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)
                flash('数据添加错误')
        else:
            book_names = [book.name for book in author.books]
            if book_name in book_names:
                flash('该作者已经添加过相应的书籍')
            else:
                try:
                    book = Book(name=book_name, author_id=author.id)
                    db.session.add(book)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(e)
                    flash('参数错误')

    authors = Author.query.all()
    books = Book.query.all()
    return render_template('index.html', authors=authors, books=books)


if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    # 生成数据
    au1 = Author(name='老王')
    au2 = Author(name='老尹')
    au3 = Author(name='老刘')
    # 把数据提交给用户会话
    db.session.add_all([au1, au2, au3])
    # 提交会话
    db.session.commit()
    bk1 = Book(name='老王回忆录', author_id=au1.id)
    bk2 = Book(name='我读书少，你别骗我', author_id=au1.id)
    bk3 = Book(name='如何才能让自己更骚', author_id=au2.id)
    bk4 = Book(name='怎样征服美丽少女', author_id=au3.id)
    bk5 = Book(name='如何征服英俊少男', author_id=au3.id)
    # 把数据提交给用户会话
    db.session.add_all([bk1, bk2, bk3, bk4, bk5])
    # 提交会话
    db.session.commit()
    app.run(debug=True)

