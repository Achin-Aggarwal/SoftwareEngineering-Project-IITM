from Application import db, app
from Application.model import Role


def create_roles():
    roles = ['Admin', 'Student', 'Professor', 'Instructor', 'Support Staff']
    
    for role_name in roles:
        if not Role.query.filter_by(name=role_name).first():  # Avoid duplicates
            role = Role(name=role_name)
            db.session.add(role)
    
    db.session.commit()
    print("Roles created successfully.")

if __name__ == '__main__':
    with app.app_context():
        create_roles()