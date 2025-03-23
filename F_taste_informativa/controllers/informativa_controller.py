from flask import request
from flask_restx import Resource, fields
from flask_jwt_extended import get_jwt_identity
from F_taste_informativa.namespaces import nutrizionista_ns,paziente_ns,admin_ns
from F_taste_informativa.services.informativa_service import InformativaService
from F_taste_informativa.utils.jwt_custom_decorators import nutrizionista_required,paziente_required,admin_required





informativa_json = admin_ns.model('post_informativa_model', {
    'informativa': fields.String(required = True),
    'tipo_informativa': fields.String(enum=["nutrizionista", "paziente"], required=True),
    'link_informativa' : fields.String(required = True)
}, strict = True)


post_link_informativa = nutrizionista_ns.model('post_link_informativa', {
    'link_informativa': fields.String(required = True),
}, strict = True)

class AdminInformativaPrivacy(Resource):

    #da provare
    @admin_required()
    @admin_ns.expect(informativa_json, validate = True)
    @admin_ns.doc(description = "caricamento informativa aired")
    # In questa post eseguita da un admin vi troviamo la possibilità di gestire i contenuti dei testi della privacy
    # La sua logica interna permette i gestire l'informativa privacy Aired e quella dei nutrizionisti
    def post(self):
        # Estraiamo il testo dell'informativa
        informativa = request.json['informativa']
        # Estraiamo il valore corrispondente alla chiave del tipo di informativa
        tipo_informativa = request.json["tipo_informativa"]
        #Estraiamo il link
        link = request.json["link_informativa"]
        return InformativaService.caricamento(informativa,tipo_informativa,link)
    


class PazienteInformativaPrivacy(Resource):

    #da provare
    @paziente_ns.doc(description="informativa privacy di Aired e del nutrizionista, se specificato", 
                     params = {'email_nutrizionista': 'optional'})
    # La funzione get di questa risorsa gestisce il ritorno di una informativa privacy in base 
    # al tipo di richiesta fatta dall'utente
    def get(self):

        return InformativaService.get_for_paziente()




class NutrizionistaInformativaPrivacy(Resource):

    #da provare
    @nutrizionista_ns.doc(description="This GET method returns the privacy policy for the Nutritionists")
    def get(self):

        return InformativaService.get_for_nutrizionista()

    #da provare    
    
    # Con il metodo post possiamo eseguire un'inserimento nel campo del link_informativa estesa
    # Di proprietà esclusiva del nutrizionista
    @nutrizionista_required()
    def post(self):

        # Json della richeista
        json = request.get_json()

        # Gestiamo la validazione
        validation_errors = post_link_informativa.validate(json)
        if validation_errors:
            return validation_errors, 404
        
        # Identità del nutrizionista
        email_nutrizionista= get_jwt_identity()
        link=json["link_informativa"]
        
        return InformativaService.add_link_nutrizionista(email_nutrizionista,link)
        

        

    
   