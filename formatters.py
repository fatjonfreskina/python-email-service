def format_to_html_website(subject: str, body: str, sender:str, name: str) -> str:
    return """
    <html>
    <head></head>
    <body>
        <h1>Hai un nuovo messagio di posta dal sito web.</h1>
        <h2>Oggetto: {}</h2>
        <p>Nome: {}</p>
        <p>Email: {}</p>
        <p>Testo: {}</p>
    </body>
    </html>
    """.format(subject, name, sender, body)

def format_to_html_password_reset(reset_link: str) -> str:
    return """
    <html>
    <head></head>
    <body>
        <h1>Richiesta di reset password</h1>
        <p>Per resettare la password clicca sul seguente link: {}</p>
    </body>
    </html>
    """.format(reset_link)
  