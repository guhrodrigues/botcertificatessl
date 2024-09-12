import ssl
import socket
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_ssl_expiry(domain):
    context = ssl.create_default_context()
    with socket.create_connection((domain, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=domain) as ssock:
            ssl_info = ssock.getpeercert()
            expiry_date_str = ssl_info['notAfter']
            expiry_date = datetime.strptime(expiry_date_str, '%b %d %H:%M:%S %Y %Z')
            return expiry_date

def send_email(expiring_domains):
    sender_email = "email que vai enviar as informações de vencimento"
    receiver_email = "email que vai receber as informações de vencimento"
    subject = "Aviso: Certificados SSL Próximos a Expirar"
    body = f"Os certificados SSL dos seguintes domínios estão próximos do vencimento, com expiração prevista para os próximos 4 dias:\n\n" + "\n".join(expiring_domains)

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('servidor smtp', porta) as server:
            server.login(sender_email, 'senha')
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("E-mail enviado com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")


domains = [
    "seudominio.com.br"
]

expiring_domains = []
for domain in domains:
    try:
        expiry_date = get_ssl_expiry(domain)
        days_to_expiry = (expiry_date - datetime.utcnow()).days
        print(f"Domínio: {domain}, expira em {days_to_expiry} dias ({expiry_date})")
        if days_to_expiry <= 4:
            expiring_domains.append(f"{domain} - Expira em {days_to_expiry} dias ({expiry_date})")
    except Exception as e:
        print(f"Erro ao verificar o domínio {domain}: {e}")

if expiring_domains:
    send_email(expiring_domains)
else:
    print("Nenhum domínio com certificado próximo a expirar.")



