from app import app, db, Task


with app.app_context():
    db.create_all()
    db.session.add(Task(title="Clean your room"))
    db.session.add(Task(title="Take out the trash"))
    db.session.commit()
