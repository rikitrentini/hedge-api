from main import app, db  # sostituisci `your_main_file` con il nome esatto, es. `main`
with app.app_context():
    db.create_all()
    print("Database e tabelle create.")
