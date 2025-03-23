from F_taste_informativa.models.informativa_breve import InformativaBreveModel
from F_taste_informativa.db import get_session
from sqlalchemy.exc import SQLAlchemyError

class InformativaRepository:

    @staticmethod
    def get_last_privacy_policy_by_type(tipologia, session=None):
        session = session or get_session('dietitian')
        return session.query(InformativaBreveModel).filter_by(tipologia_informativa=tipologia).order_by(InformativaBreveModel.data_inserimento.desc()).first()
    
    @staticmethod
    def add(informativa, session=None):
        session = session or get_session('admin')
        session.add(informativa)
        session.commit()
