from F_taste_informativa.repositories.informativa_repository import InformativaRepository
from F_taste_informativa.models.informativa_breve import InformativaBreveModel
from F_taste_informativa.db import get_session

class InformativaService:
    
    @staticmethod
    def caricamento(informativa,tipo_informativa,link):
        # Se il testo o il link sono vuoti viene segnalato
        if informativa == "":
            return {"message": "Campo del testo vuoto. Inserire una informativa e riprovare."}, 422
        if link == "":
            return {"message": "Campo del link vuoto. Inserire una link e riprovare."}, 422 

        # Gestiamo il caso
        if tipo_informativa == "nutrizionista" or tipo_informativa == "paziente":
            # Inseriamo nel db l'informativa
            return InformativaService.addInformativaInDB(tipologia = tipo_informativa, link = link, testo = informativa)
        else:
            return {'message': f'Errore nell invio del tipo informativa. Inviata: {tipo_informativa}. Possibili: nutrizionista, paziente'}, 404
        

        # Questo metodo serve ad inserire l'informativa all'interno del db
    def addInformativaInDB(tipologia, testo, link):
        
        # Reference alla sessione
        session = get_session('admin')

        # Nuovo elemento da inserire
        informativa = InformativaBreveModel(tipologia, link, testo)

        try:
            # Operazioni di inserimento nel DB
            InformativaRepository.add(informativa)
            session.close()
            # Ritorniamo messaggi di successo se è andato a buon fine
            return {"message" : "Informativa salvata con successo."}, 200
        
        except Exception:
            return {"message" : "Errore durante il caricamento della informativa"}, 404
        

    staticmethod
    def get_for_paziente():
        # Reference alla sessione del DB
        session = get_session("patient")
        
        # Estraiamo la normativa del nutrizionista
        informativa = InformativaRepository.get_last_privacy_policy_by_type(("paziente", session))
        # Gestiamo gli errori
        if informativa is None:
            session.close()
            return {"message" : ""}, 204
        
        testo=informativa.testo_informativa
        link=informativa.link_inf_estesa
        session.close()
        
        # Ritorniamo il model
        return {
                'informativa': testo, 
                'link_informativa': link
                }, 200
    
    @staticmethod
    def get_for_nutrizionista():
        # Reference alla sessione del DB
        session = get_session("dietitian")
        
        # Estraiamo la normativa del nutrizionista
        informativa = InformativaRepository.get_last_privacy_policy_by_type(("nutrizionista", session))
        # Gestiamo gli errori
        if informativa is None:
            session.close()
            return {"message" : ""}, 204
        
        testo=informativa.testo_informativa
        link=informativa.link_inf_estesa
        session.close()
        
        # Ritorniamo il model
        return {
                'informativa': testo, 
                'link_informativa': link
                }, 200
    
    @staticmethod
    def add_link_nutrizionista(email_nutrizionista,s_informativa):
        # Reference alla sessione
        session = get_session('dietitian')
        #tramite kafka cerca nutrizionista per email e se c'è aggiorna il campo link_informativa 
        #in base allo status code capisce che output fare(messaggio positivo o negativo)