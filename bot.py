import ssl
import socket
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Função para obter a data de expiração do certificado SSL
def get_ssl_expiry(domain):
    context = ssl.create_default_context()
    with socket.create_connection((domain, 443), timeout=10) as sock:
        with context.wrap_socket(sock, server_hostname=domain) as ssock:
            ssl_info = ssock.getpeercert()
            expiry_date_str = ssl_info['notAfter']
            expiry_date = datetime.strptime(expiry_date_str, '%b %d %H:%M:%S %Y %Z')
            return expiry_date

# Função para enviar o e-mail
def send_email(expiring_domains):
    sender_email = ""
    receiver_email = ""
    subject = "Aviso Diário: Certificados SSL Próximos a Expirar"
    
    # Corpo do e-mail
    body = f"Os certificados SSL dos seguintes domínios estão próximos do vencimento (até 10 dias):\n\n" + "\n".join(expiring_domains)

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL(') as server:
            server.login(sender_email, '')  # Use uma senha segura aqui.
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("E-mail enviado com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

# Domínios a serem verificados
domains = [
    
]

# Função principal para verificar os domínios
def check_domains():
    expiring_domains = []
    for domain in domains:
        try:
            expiry_date = get_ssl_expiry(domain)
            days_to_expiry = (expiry_date - datetime.utcnow()).days
            print(f"Domínio: {domain}, expira em {days_to_expiry} dias ({expiry_date})")
            
            # Verifica se o certificado expira em 10 dias ou menos
            if 0 < days_to_expiry <= 10:
                expiring_domains.append(f"{domain} - Expira em {days_to_expiry} dias ({expiry_date.strftime('%d/%m/%Y')})")
        except Exception as e:
            print(f"Erro ao verificar o domínio {domain}: {e}")

    # Envia o e-mail apenas se houver domínios com certificados expirando
    if expiring_domains:
        send_email(expiring_domains)
    else:
        print("Nenhum domínio com certificado próximo a expirar.")

# Programa principal que executa a verificação a cada 1 hora
if __name__ == "__main__":
    while True:
        try:
            print(f"Verificação iniciada em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            check_domains()
            print(f"Próxima verificação em 1 hora...\n")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

        # Espera 1 hora (3600 segundos) até a próxima verificação
        time.sleep(3600)
