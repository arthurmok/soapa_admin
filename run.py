from create_app import create_app, db


app = create_app()
app.app_context().push()
# db.create_all(app=create_app())

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8092, debug=True)