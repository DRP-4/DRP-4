from app import app, db
import models.current_session
import models.slot
import models.space
import models.task
import models.in_space

with app.app_context():
    db.create_all()
    db.session.commit()
