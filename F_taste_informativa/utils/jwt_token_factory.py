from flask_jwt_extended import create_access_token, create_refresh_token




class JWTTokenFactory:

    
    def create_access_token(self, identity, role):
        return create_access_token(identity=identity, additional_claims={"role": role})

    def create_refresh_token(self, identity, role):
        return create_refresh_token(identity=identity, additional_claims={"role": role})
    
    def create_forgotten_password_token(self, identity, role):
        return create_access_token(identity=identity, additional_claims={"role": role, "is_forgotten_password_token": True})
