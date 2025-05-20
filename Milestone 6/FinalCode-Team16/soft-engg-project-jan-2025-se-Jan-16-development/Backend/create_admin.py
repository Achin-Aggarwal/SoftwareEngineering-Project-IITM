from Application import db,app
from Application.model import Role,User


def create_admin_user():
    with app.app_context():
        # Check if Admin role exists
        admin_role = Role.query.filter_by(name='Admin').first()
        if not admin_role:
            print("Error: Admin role not found. Run the role creation script first.")
            return


        # Create the admin user
        admin_user = User(
            name='Admin User',
            username='admin',
            email='admin@example.com',
            about='This is Admin',
            role=admin_role
        )
        admin_user.set_password('admin123')  # Securely set the password
        db.session.add(admin_user)
        db.session.commit()

        print("Admin user created successfully.")

if __name__ == '__main__':
    create_admin_user()