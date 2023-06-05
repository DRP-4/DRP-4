from app import app, db, Task


with app.app_context():
    db.create_all()
    db.session.commit()
