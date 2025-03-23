from flask_restx import Namespace

paziente_ns = Namespace('paziente', description='paziente operations')
nutrizionista_ns = Namespace('nutrizionista', description='nutrizionista operations')
admin_ns = Namespace('admin', description='admin operations')