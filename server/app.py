
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_marshmallow import Marshmallow
from models import db, User, Skill, Swap, SkillUser
from config import Config
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import logging

# Set up logging for better error tracking
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database and marshmallow
db.init_app(app)
ma = Marshmallow(app)

# CORS setup - Only allow requests from the frontend at localhost:3000
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

api = Api(app)

# Marshmallow schemas
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

class SkillSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Skill
        load_instance = True

class SwapSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Swap
        load_instance = True

class SkillUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SkillUser
        load_instance = True

# User Resources (CRUD)
class UserListResource(Resource):
    def get(self):
        try:
            users = User.query.all()
            user_schema = UserSchema(many=True)
            return user_schema.dump(users)
        except Exception as e:
            app.logger.error(f"Error fetching users: {str(e)}")
            return jsonify({"message": f"Error fetching users: {str(e)}"}), 500
    
    def post(self):
        try:
            data = request.get_json()
            if 'username' not in data or 'email' not in data or 'password' not in data:
                return jsonify({"message": "Missing required fields: username, email, and password are required."}), 400
            
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                return jsonify({"message": "Email already in use."}), 409

            new_user = User(username=data['username'], email=data['email'])
            new_user.set_password(data['password'])  # Hash password before storing
            
            db.session.add(new_user)
            db.session.commit()
            
            user_schema = UserSchema()
            return user_schema.dump(new_user), 201
        except Exception as e:
            app.logger.error(f"Error creating user: {str(e)}")
            return jsonify({"message": f"Error creating user: {str(e)}"}), 500

class LoginResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            if not data or 'email' not in data or 'password' not in data:
                return jsonify({"message": "Email and password are required."}), 400

            user = User.query.filter_by(email=data['email']).first()
            if user and user.check_password(data['password']):
                user_schema = UserSchema()
                return user_schema.dump(user)
            return jsonify({"message": "Invalid email or password"}), 401
        except Exception as e:
            app.logger.error(f"Error logging in: {str(e)}")
            return jsonify({"message": f"Error logging in: {str(e)}"}), 500

class UserResource(Resource):
    def get(self, user_id):
        try:
            user = User.query.get(user_id)
            if user:
                user_schema = UserSchema()
                return user_schema.dump(user)
            return jsonify({"message": "User not found"}), 404
        except Exception as e:
            app.logger.error(f"Error fetching user: {str(e)}")
            return jsonify({"message": f"Error fetching user: {str(e)}"}), 500

    def put(self, user_id):
        try:
            data = request.get_json()
            user = User.query.get(user_id)
            if user:
                if 'username' in data:
                    user.username = data['username']
                if 'email' in data:
                    user.email = data['email']
                if 'password' in data:  # Allow password update
                    user.set_password(data['password'])
                db.session.commit()
                
                user_schema = UserSchema()
                return user_schema.dump(user)
            return jsonify({"message": "User not found"}), 404
        except Exception as e:
            app.logger.error(f"Error updating user: {str(e)}")
            return jsonify({"message": f"Error updating user: {str(e)}"}), 500

    def delete(self, user_id):
        try:
            user = User.query.get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return jsonify({"message": "User deleted"})
            return jsonify({"message": "User not found"}), 404
        except Exception as e:
            app.logger.error(f"Error deleting user: {str(e)}")
            return jsonify({"message": f"Error deleting user: {str(e)}"}), 500

# Skill Resources (CRUD)
class SkillListResource(Resource):
    def get(self):
        try:
            skills = Skill.query.all()
            skill_schema = SkillSchema(many=True)
            return skill_schema.dump(skills)
        except Exception as e:
            app.logger.error(f"Error fetching skills: {str(e)}")
            return jsonify({"message": f"Error fetching skills: {str(e)}"}), 500

    def post(self):
        try:
            data = request.get_json()
            new_skill = Skill(skill_name=data['skill_name'], description=data.get('description', ''))
            db.session.add(new_skill)
            db.session.commit()
            
            skill_schema = SkillSchema()
            return skill_schema.dump(new_skill), 201
        except Exception as e:
            app.logger.error(f"Error creating skill: {str(e)}")
            return jsonify({"message": f"Error creating skill: {str(e)}"}), 500

class SkillResource(Resource):
    def get(self, skill_id):
        try:
            skill = Skill.query.get(skill_id)
            if skill:
                skill_schema = SkillSchema()
                return skill_schema.dump(skill)
            return jsonify({"message": "Skill not found"}), 404
        except Exception as e:
            app.logger.error(f"Error fetching skill: {str(e)}")
            return jsonify({"message": f"Error fetching skill: {str(e)}"}), 500

    def put(self, skill_id):
        try:
            data = request.get_json()
            skill = Skill.query.get(skill_id)
            if skill:
                if 'skill_name' in data:
                    skill.skill_name = data['skill_name']
                if 'description' in data:
                    skill.description = data['description']
                db.session.commit()

                app.logger.info(f"Skill {skill_id} updated successfully")
                skill_schema = SkillSchema()
                return skill_schema.dump(skill)
            return jsonify({"message": "Skill not found"}), 404
        except Exception as e:
            app.logger.error(f"Error updating skill: {str(e)}")
            return jsonify({"message": f"Error updating skill: {str(e)}"}), 500

    def delete(self, skill_id):
        try:
            skill = Skill.query.get(skill_id)
            if skill:
                db.session.delete(skill)
                db.session.commit()
                return jsonify({"message": "Skill deleted"})
            return jsonify({"message": "Skill not found"}), 404
        except Exception as e:
            app.logger.error(f"Error deleting skill: {str(e)}")
            return jsonify({"message": f"Error deleting skill: {str(e)}"}), 500

# SkillUser Resources (CRUD)
class SkillUserListResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            skill_user = SkillUser(user_id=data['user_id'], skill_id=data['skill_id'], proficiency=data['proficiency'])
            db.session.add(skill_user)
            db.session.commit()
            
            skill_user_schema = SkillUserSchema()
            return skill_user_schema.dump(skill_user), 201
        except Exception as e:
            app.logger.error(f"Error creating skill-user relationship: {str(e)}")
            return jsonify({"message": f"Error creating skill-user relationship: {str(e)}"}), 500

# Add the resources to the API
api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(LoginResource, '/login')  # New login route
api.add_resource(SkillListResource, '/skills')
api.add_resource(SkillResource, '/skills/<int:skill_id>')  # For individual skill CRUD
api.add_resource(SkillUserListResource, '/skill-user')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)