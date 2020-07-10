from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class test(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(20000), nullable=False)
    created_at = db.Column(db.DateTime)
    types = db.Column(db.String(10), nullable=False)
    author = db.Column(db.String(20))
    view_count = db.Column(db.Integer)
    is_valid = db.Column(db.Boolean)

    def __init__(self, title, content, types, created_at, author='', is_valid=1):
        self.title = title
        self.content = content
        self.types = types
        self.created_at = created_at
        self.author = author
        self.is_valid = is_valid

    def __repr__(self):
        return '%s, %s, %s' % (self.id, self.title, self.content)

# 建表语句
db.create_all()

# 添加一条数据
obj = test(
    title='新闻标题',
    content='新闻内容',
    types='百家',
    created_at=datetime.datetime.now(),
)
db.session.add(obj)
db.session.commit()

# 查询数据
text = test.query.all()
print(text)
admin = test.query.filter_by(types='百家').first()
print(admin)

# 删除数据
text = test.query.filter_by(is_valid=1).first()
db.session.delete(text)
db.session.commit()

# 修改数据
text = test.query.filter_by(types='百家').first()
text.types = '体育'
db.session.commit()




if __name__ == '__main__':
    app.run(debug=True)