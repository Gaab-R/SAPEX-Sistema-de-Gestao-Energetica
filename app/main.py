import random
import time
import json
import requests
import pandas as pd
from flask import Flask, render_template
import threading
import mysql.connector
from transformers import pipeline

gerador_ia = pipeline('text-generation', model='gpt2')

# Configuração MySQL
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Você coloca sua senha aqui",
        database="sistema_energia"
    )
    print("[INFO] Conectado ao MySQL.")
except mysql.connector.Error as err:
    print(f"[ERRO] Falha na conexão MySQL: {err}. Usando apenas simulação.")
    db = None

# Variável global
ultimo_dado = None
dispositivos_permitidos = ['lampada', 'tv']

def simular_sensores():
    temperatura = random.uniform(20.0, 30.0)
    umidade = random.uniform(40.0, 60.0)
    consumo_energia = random.uniform(100.0, 200.0)
    presenca = random.choice([True, False])
    dispositivos = ['lampada', 'tv', 'ar_condicionado']
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    return {
        'temperatura': temperatura,
        'umidade': umidade,
        'consumo_energia': consumo_energia,
        'presenca': presenca,
        'dispositivos': dispositivos,
        'timestamp': timestamp
    }

def simular_nuvem(dados, usar_nuvem=True, api_key='Você coloca sua api key aqui'):
    if usar_nuvem:
        url = 'https://api.thingspeak.com/update'
        payload = {
            'api_key': api_key,
            'field1': dados['temperatura'],
            'field2': dados['umidade'],
            'field3': dados['consumo_energia']
        }
        print(f"[DEBUG] Enviando: {payload}")
        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200 and response.text.strip() != '0':
                print(f"[INFO] ThingSpeak OK: Update {response.text.strip()}")
            else:
                print(f"[ERRO] ThingSpeak falhou.")
        except Exception as e:
            print(f"[ERRO] Conexão falhou.")
    else:
        salvar_local(dados)

def salvar_local(dados):
    with open('dados_simulados.json', 'a') as arquivo:
        json.dump(dados, arquivo)
        arquivo.write('\n')
    print("[INFO] Salvo localmente.")

def salvar_no_mysql(dados, usuario_id=1):
    if db is None:
        print("[INFO] MySQL não conectado, pulando salvamento.")
        return
    if not dados:
        print("[ERRO] Dados None, não salvou no MySQL.")
        return
    try:
        cursor = db.cursor()
        sql = "INSERT INTO dados_sensores (usuario_id, timestamp, temperatura, umidade, consumo) VALUES (%s, %s, %s, %s, %s)"
        val = (usuario_id, dados['timestamp'], dados['temperatura'], dados['umidade'], dados['consumo_energia'])
        cursor.execute(sql, val)
        db.commit()
        print("[INFO] Salvo no MySQL.")
    except Exception as e:
        print(f"[ERRO] Falha ao salvar no MySQL: {e}")

def calcular_conta_luz(mes, usuario_id=1):
    if db is None:
        return 0, 0
    try:
        cursor = db.cursor()
        sql = "SELECT SUM(consumo) FROM dados_sensores WHERE usuario_id = %s AND MONTH(timestamp) = %s"
        cursor.execute(sql, (usuario_id, mes))
        consumo_total = cursor.fetchone()[0] or 0
        valor_estimado = consumo_total * 0.5
        return consumo_total, valor_estimado
    except Exception as e:
        print(f"[ERRO] Falha ao calcular conta: {e}")
        return 0, 0

def analisar_com_ia(dados):
    if not dados:
        return "Sem dados para análise."
    
    dispositivos = dados.get('dispositivos', [])
    sugestao = None
    for dispositivo in dispositivos:
        if pode_desligar(dispositivo, dados):
            sugestao = f"{dispositivo} desligado para reduzir consumo."
            break
    
    if not sugestao:
        sugestao = "Nenhum dispositivo seguro para desligar no momento."
    
    try:
        resultado = gerador_ia('text-generation', model='gpt2')
        prompt = f"Análise: Consumo {dados['consumo_energia']}W, temperatura {dados['temperatura']}°C. Sugira em português qual dispositivo desligar para economizar energia. Responda em 1 frase curta, baseada em: {sugestao}"
        resultado = gerador(prompt, max_length=50, num_return_sequences=1, temperature=0.7, do_sample=True, truncation=True)
        resposta = resultado[0]['generated_text'].replace(prompt, '').strip()
        if any(word in resposta.lower() for word in ['desligar', 'reduzir', 'economizar']):
            return resposta[:100]
        else:
            return sugestao
    except Exception as e:
        return sugestao

def otimizar_e_automatizar(dados):
    if not dados:
        return "Nenhum dado para otimizar."
    df = pd.DataFrame([dados])
    acao = "Tudo OK, continue monitorando."
    if df['consumo_energia'].mean() > 150 and df['temperatura'].mean() > 25:
        acao = "Reduzir consumo! Desligue dispositivos desnecessários."
    
    for dispositivo in dados.get('dispositivos', []):
        if pode_desligar(dispositivo, dados):
            acao += f" - Desligar {dispositivo} (seguro)."
            simular_automacao(f"Desligar {dispositivo}")
    
    print(f"[INFO] Ação integrada: {acao}")
    return acao

def pode_desligar(dispositivo, dados):
    nao_desligaveis = ['geladeira', 'freezer']
    if dispositivo in nao_desligaveis or dispositivo not in dispositivos_permitidos or dados.get('presenca', True):
        return False
    return True

def simular_automacao(acao):
    if "Desligar" in acao:
        print(f"[INFO] Automação: {acao}")
    else:
        print("[INFO] Automação: Mantendo padrão.")

app = Flask(__name__)

@app.route('/')
def index():
    global ultimo_dado
    ultimo_dado = None
    try:
        with open('dados_simulados.json', 'r') as arquivo:
            linhas = arquivo.readlines()
            if linhas:
                for linha in reversed(linhas):
                    linha = linha.strip()
                    if linha:
                        ultimo_dado = json.loads(linha)
                        print(f"[DEBUG] Último dado carregado: {ultimo_dado}")
                        break
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[ERRO] Falha ao carregar JSON: {e}. Usando simulação.")
        ultimo_dado = simular_sensores()
    
    acao = otimizar_e_automatizar(ultimo_dado) if ultimo_dado else 'Nenhum dado ainda.'
    analise_ia = analisar_com_ia(ultimo_dado) if ultimo_dado else 'Sem dados.'
    
    consumo_atual = round(ultimo_dado.get('consumo_energia', 0), 2) if ultimo_dado else 0
    valor_janeiro = round(calcular_conta_luz(1, usuario_id=1)[1], 2)
    emissoes_co2 = round(consumo_atual * 0.5, 2) if consumo_atual else 0
    consumo_janeiro = round(calcular_conta_luz(1, usuario_id=1)[0], 2)
    consumo_fevereiro = round(calcular_conta_luz(2, usuario_id=1)[0], 2)
    
    # Status dinâmicos
    status_consumo = "Eficiente" if consumo_atual < 150 else "Alto"
    status_custo = "Neutro" if valor_janeiro < 50 else "Alto"
    status_co2 = "Baixo" if emissoes_co2 < 50 else "Alto"
    
    # Cálculos de economia
    baseline_consumo = 200  # kWh baseline
    economia_percentual = round((1 - consumo_atual / baseline_consumo) * 100, 2) if consumo_atual < baseline_consumo else 0
    valor_economizado = round(economia_percentual / 100 * valor_janeiro, 2) if economia_percentual > 0 else 0
    
    print(f"[DEBUG] Consumo Atual: {consumo_atual}, Valor Janeiro: {valor_janeiro}, Emissões: {emissoes_co2}")
    
    return render_template('index.html', 
                           ultimo_dado=ultimo_dado,
                           ultimo_dado_json=json.dumps(ultimo_dado),
                           acao=acao, 
                           analise_ia=analise_ia, 
                           consumo_atual=consumo_atual,
                           valor_janeiro=valor_janeiro,
                           emissoes_co2=emissoes_co2,
                           consumo_janeiro=consumo_janeiro,
                           consumo_fevereiro=consumo_fevereiro,
                           status_consumo=status_consumo,
                           status_custo=status_custo,
                           status_co2=status_co2,
                           economia_percentual=economia_percentual,
                           valor_economizado=valor_economizado,
                           dispositivos=['lampada', 'tv', 'ar_condicionado'])

def iniciar_flask():
    app.run(host='0.0.0.0', debug=False, use_reloader=False, port=5000)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=iniciar_flask)
    flask_thread.start()
    
    print("[INFO] Iniciando loop contínuo.")
    while True:
        ultimo_dado = simular_sensores()
        print(f"[INFO] Dados: {ultimo_dado['timestamp']} - Presença: {ultimo_dado['presenca']}")
        simular_nuvem(ultimo_dado)
        salvar_no_mysql(ultimo_dado)
        otimizar_e_automatizar(ultimo_dado)
        time.sleep(60)
