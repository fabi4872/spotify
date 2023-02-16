import importlib
from flask import Flask
from flask import render_template, request, redirect, url_for, flash, session
from flask_cors import CORS
from web.controllers import spotify_controller



def create_app(env="development", static_folder="static"):
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])
    # CORS(app, supports_credentials=True)
    # configuracion de la bd
    database.init_app(app)
    app.secret_key= "holamundo"
    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    QRcode(app)



    #Operaciones Spotify
    app.add_url_rule('/obtener_enlaces_youtube/', 'obtener_enlaces_youtube', spotify_controller.obtener_enlaces_youtube, methods=["POST", "GET"])
    # app.add_url_rule('/pagar_cuota/<id_c> <monto><id_d> <id_a> ', 'pagar_cuota', cuota_controller.pagar_cuota)



    @app.cli.command(name="resetdb")
    def resetdb():
        database.reset_db()

    @app.cli.command(name="seeds")
    def seedsdb():
        seeds.run()

    @app.shell_context_processor
    def make_shell_context():
        modules = dict(app=app)
        
        modelsmodule = importlib.import_module('src.core.models')
        # import ipdb
        # ipdb.set_trace() #breakpoint
        for modulename in modelsmodule.__dict__:
            modules[modulename] = getattr(modelsmodule, modulename)
        return modules 
    app.jinja_env.globals.update(validar_permisos=validar_permisos)
    app.jinja_env.globals.update(es_admin=es_admin)
    return app
