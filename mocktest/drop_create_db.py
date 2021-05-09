from mocktest import db
from mocktest.utils import add_questions_java, add_questions_python

db.drop_all()
db.create_all()

add_questions_java()
add_questions_python()

