from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
import imapclient
import pyzmail
import poplib
import email

app = Flask(__name__)
app.secret_key = 'secret_key'

# Настройки SMTP (пример: Gmail)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='test14042004@gmail.com',
    MAIL_PASSWORD='ghtmxouobgtkvlqp'
)

mail = Mail(app)

tasks = ["Задача 1", "Задача 2", "Задача 3"]

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/send_email', methods=['POST'])
def send_email():
    recipient = request.form['email']
    task = request.form['task']
    msg = Message("Задача", sender=app.config['MAIL_USERNAME'], recipients=[recipient])
    msg.body = f"Вот задача: {task}"
    mail.send(msg)
    flash('Письмо отправлено!')
    return redirect('/')

# Чтение почты через IMAP
@app.route('/check_imap')
def check_imap():
    imap = imapclient.IMAPClient('imap.gmail.com', ssl=True)
    imap.login('your_email@gmail.com', 'your_app_password')
    imap.select_folder('INBOX', readonly=True)
    UIDs = imap.search(['ALL'])
    raw = imap.fetch(UIDs[-1], ['BODY[]'])
    message = pyzmail.PyzMessage.factory(raw[UIDs[-1]][b'BODY[]'])
    subject = message.get_subject()
    imap.logout()
    return f"Последнее письмо (IMAP): {subject}"

# Чтение почты через POP3
@app.route('/check_pop3')
def check_pop3():
    pop = poplib.POP3_SSL('pop.gmail.com', 995)
    pop.user('test14042004@gmail.com')
    pop.pass_('ghtmxouobgtkvlqp')
    num_messages = len(pop.list()[1])
    response, lines, octets = pop.retr(num_messages)
    msg_content = b'\r\n'.join(lines)
    message = email.message_from_bytes(msg_content)
    subject = message['subject']

    pop.quit()
    return f"Последнее письмо (POP3): {subject}"

if __name__ == '__main__':
    app.run(debug=True)
