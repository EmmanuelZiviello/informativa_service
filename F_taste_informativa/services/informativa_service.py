from F_taste_informativa.repositories.informativa_repository import InformativaRepository
from F_taste_informativa.models.informativa_breve import InformativaBreveModel
from F_taste_informativa.db import get_session
from F_taste_informativa.kafka.kafka_producer import send_kafka_message
from F_taste_informativa.utils.kafka_helpers import wait_for_kafka_response

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
    def add_link_nutrizionista(email_nutrizionista,link):
        #tramite kafka cerca nutrizionista per email e se c'è aggiorna il campo link_informativa 
        #in base allo status code capisce che output fare(messaggio positivo o negativo)
        message={"email_nutrizionista":email_nutrizionista,"link":link}
        send_kafka_message("dietitian.addLink.request",message)
        response=wait_for_kafka_response(["dietitian.addLink.success", "dietitian.addLink.failed"])
        if response.get("status_code") == "201":
            # Ritorniamo infine un messaggio di buona riuscita
            return {"message" : "Associazione link informativa all'account eseguito con successo."}, 201
        elif response.get("status_code") == "404":
            return {"message": "Nutrizionista non valido. Riprovare."}, 204
        elif response.get("status_code") == "400":
            return {"message":"Dati mancanti per l'aggiornamento del link"}, 400
        else:
            return {"message":"Errore nell'aggiornamento del link"}, 500

        