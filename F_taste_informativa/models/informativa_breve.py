from F_taste_informativa.db import Base
from sqlalchemy import Column, String, Integer, TIMESTAMP
from datetime import datetime
from sqlalchemy.orm import scoped_session


class InformativaBreveModel(Base):

    __tablename__ = "informativa_breve"

    id_informativa = Column(Integer, primary_key = True)
    tipologia_informativa = Column(String(50), nullable = False)
    link_inf_estesa = Column(String(50), nullable = False)
    testo_informativa = Column(String(3000), nullable = False)
    data_inserimento = Column(TIMESTAMP, nullable = False)

    def __init__(self, tipologia, link_inf, testo_informativa, data = datetime.now()):
        self.tipologia_informativa = tipologia
        self.link_inf_estesa = link_inf
        self.testo_informativa = testo_informativa
        self.data_inserimento = data
        
    def __repr__(self):
        return 'InformativaBreveModel(tipologia_informativa=%s, link_inf_estesa=%s, testo_informativa=%s, data_inserimento=%s)' % (self.tipologia_informativa, self.link_inf_estesa, self.testo_informativa, self.data_inserimento)

    def __json__(self):
        return { 'tiplogia_informativa' : self.tipologia_informativa, 
                 'link_inf_estesa' : self.link_inf_estesa, 
                 'testo_informativa' : self.testo_informativa, 
                 'data_inserimento': self.data_inserimento }