from Application import db,app
from Application.model import Role,User


def create_professor_user():
    with app.app_context():
        # Check if Admin role exists
        professor_role = Role.query.filter_by(name='Professor').first()
        if not professor_role:
            print("Error: professor role not found. Run the role creation script first.")
            return


        # Create the admin user
        professor_user = User(
            name='Professor User',
            username='professor1',
            email='professor1@gmail.com',
            about='This is Professor',
            role=professor_role
        )
        professor_user.set_password('123456')  # Securely set the password
        db.session.add(professor_user)
        db.session.commit()

        print("professor user created successfully.")

if __name__ == '__main__':
    create_professor_user()