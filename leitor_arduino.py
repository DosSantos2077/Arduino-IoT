import serial
import serial.tools.list_ports
import time

def listar_portas():
    """Lista todas as portas COM detectadas pelo sistema."""
    portas = serial.tools.list_ports.comports()
    print("---- PORTAS ENCONTRADAS ----")

    if not portas:
        print("Nenhuma porta encontrada!")
        print("Verifique o cabo USB e os drivers.\n")
        return []

    for p in portas:
        print(f"{p.device} | {p.description}")

    print("-----------------------------\n")
    return portas


def encontrar_arduino():
    """Detecta automaticamente a porta em que o Arduino está conectado."""
    portas = serial.tools.list_ports.comports()

    for p in portas:
        device = p.device.lower()
        descricao = p.description.lower()

        # Critérios para identificar automaticamente
        if ("arduino" in descricao or
            "ch340" in descricao or
            "usb serial" in descricao or
            "usb" in device or
            "acm" in device or
            "ttyusb" in device):

            print(f"Arduino detectado automaticamente na porta: {p.device}")
            return p.device

    return None


# -------------------- PROGRAMA PRINCIPAL --------------------

# Primeiro lista as portas para debug
listar_portas()

porta = encontrar_arduino()

if porta is None:
    print("Nenhum Arduino detectado automaticamente.")
    print("Conecte o Arduino e tente novamente.\n")
    exit()

# Conecta na porta encontrada
print(f"Conectando ao Arduino em {porta}...")
try:
    ser = serial.Serial(porta, 9600, timeout=1)
except serial.SerialException as e:
    print("Erro ao abrir porta serial:", e)
    exit()

# Aguarda inicialização da ligação USB
time.sleep(2)
print("Conexão estabelecida! Lendo mensagens...\n")

while True:
    try:
        # Lê linha enviada pelo Arduino
        linha = ser.readline().decode("utf-8", errors="ignore").strip()
        if linha:
            print("Arduino:", linha)

    except KeyboardInterrupt:
        print("\nPrograma encerrado pelo usuário.")
        break
    except Exception as e:
        print("\nErro inesperado:", e)
        break
