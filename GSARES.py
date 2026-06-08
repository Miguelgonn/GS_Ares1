# ============================================================
# ARES-1 — Sistema Inteligente de Monitoramento
#          de uma Base Autônoma em Marte
# Global Solution — FIAP 2026
# ============================================================
 
import csv
import os
import random
from datetime import datetime
 
# ============================================================
# 0. GERADOR DE DADOS ALEATÓRIOS REALISTAS
# ============================================================
 
def gerar_dados_csv(caminho_csv):
    """
    Gera um arquivo dados.csv com telemetria aleatória realista
    a cada execução do sistema ARES-1.
    """
 
    # --- Módulos: maior chance de operacional, pequena chance de falha ---
    def status_modulo(prob_falha=0.2):
        return 0 if random.random() < prob_falha else 1
 
    modulos = {
        "suporte_vida":  status_modulo(0.15),
        "energia":       status_modulo(0.15),
        "comunicacao":   status_modulo(0.4),   # falha mais comum
        "habitat":       status_modulo(0.1),
        "laboratorio":   status_modulo(0.3),
        "armazenamento": status_modulo(0.1),
    }
 
    # --- Energia: simula queda solar ao longo do dia (tempestade de poeira) ---
    horarios = ["06:00", "08:00", "10:00", "12:00", "14:00", "16:00"]
    geracao_base = [
        round(random.uniform(8, 15), 1),
        round(random.uniform(25, 40), 1),
        round(random.uniform(35, 55), 1),
        round(random.uniform(30, 50), 1),
        round(random.uniform(10, 25), 1),
        round(random.uniform(5, 12), 1),
    ]
    consumo_base = [
        round(random.uniform(40, 50), 1),
        round(random.uniform(45, 55), 1),
        round(random.uniform(50, 60), 1),
        round(random.uniform(55, 65), 1),
        round(random.uniform(58, 70), 1),
        round(random.uniform(60, 72), 1),
    ]
 
    reserva = round(random.uniform(75, 90), 1)
    energia_rows = []
    for i in range(6):
        delta = geracao_base[i] - consumo_base[i]
        reserva = max(0, min(100, reserva + delta * 0.5))
        energia_rows.append((horarios[i], geracao_base[i], consumo_base[i], round(reserva, 1)))
 
    # --- Variáveis ambientais ---
    temp_interna  = round(random.uniform(18, 26), 1)
    temp_externa  = round(random.uniform(-80, -40), 1)
    radiacao      = round(random.uniform(0.5, 6.0), 2)
    qualidade_com = random.randint(5, 95)
    vento         = round(random.uniform(20, 130), 1)
    pressao       = random.randint(100800, 101800)
 
    def status_rad(v):
        return "critico" if v > 3.0 else "alerta" if v > 2.0 else "normal"
    def status_com(v):
        return "critico" if v < 20 else "alerta" if v < 50 else "normal"
    def status_vento(v):
        return "critico" if v > 120 else "alerta" if v > 60 else "normal"
 
    # --- Sensor defeituoso: valor impossível aleatório ---
    valor_sensor_defeituoso = random.randint(400, 999)
 
    # --- Eventos: gerados conforme o estado dos módulos ---
    eventos = [
        (1, "06:15", "INFO",
         "Sistema ARES-1 inicializado com sucesso", "normal"),
        (2, "07:30", "ALERTA",
         f"Tempestade de poeira detectada a {random.randint(80, 200)}km — reducao solar prevista", "alerta"),
    ]
    eid = 3
    if not modulos["comunicacao"]:
        eventos.append((eid, "08:45", "FALHA",
                        "Modulo de comunicacao desligado — antena primaria danificada", "critico"))
        eid += 1
    if radiacao > 3.0:
        eventos.append((eid, "09:30", "ALERTA",
                        f"Nivel de radiacao elevado: {radiacao} mSv/h — tempestade solar", "critico"))
        eid += 1
    eventos.append((eid, "11:20", "ERRO",
                    f"Sensor TI-04 retornou valor invalido ({valor_sensor_defeituoso}C)", "critico"))
    eid += 1
    if not modulos["laboratorio"]:
        eventos.append((eid, "13:00", "ACAO",
                        "Laboratorio entrou em standby — economia de energia", "alerta"))
        eid += 1
    if energia_rows[-1][3] < 40:
        eventos.append((eid, "15:30", "ALERTA",
                        f"Reserva em {energia_rows[-1][3]}% — consumo supera geracao", "critico"))
        eid += 1
    eventos.append((eid, "16:45", "INFO",
                    "Reinicializacao do modulo de comunicacao via antena de emergencia", "alerta"))
 
    # --- Escreve o CSV ---
    os.makedirs(os.path.dirname(caminho_csv), exist_ok=True)
    with open(caminho_csv, "w", encoding="utf-8") as f:
        f.write("# ============================================================\n")
        f.write("# ARES-1 — Base Marciana Autônoma\n")
        f.write(f"# Telemetria gerada em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("# ============================================================\n\n")
 
        f.write("# --- MODULOS CRITICOS (1 = operacional, 0 = falha) ---\n")
        f.write("modulo,status\n")
        for nome, val in modulos.items():
            f.write(f"{nome},{val}\n")
 
        f.write("\n# --- ENERGIA POR HORARIO (kWh) ---\n")
        f.write("hora,geracao_solar,consumo,reserva\n")
        for h, g, c, rv in energia_rows:
            f.write(f"{h},{g},{c},{rv}\n")
 
        f.write("\n# --- VARIAVEIS AMBIENTAIS ---\n")
        f.write("variavel,valor,unidade,status\n")
        f.write(f"temperatura_interna,{temp_interna},celsius,normal\n")
        f.write(f"temperatura_externa,{temp_externa},celsius,normal\n")
        f.write(f"nivel_radiacao,{radiacao},mSv/h,{status_rad(radiacao)}\n")
        f.write(f"qualidade_comunicacao,{qualidade_com},percentual,{status_com(qualidade_com)}\n")
        f.write(f"velocidade_vento,{vento},km/h,{status_vento(vento)}\n")
        f.write(f"pressao_interna,{pressao},pascal,normal\n")
 
        f.write("\n# --- INCONSISTENCIA PROPOSITAL ---\n")
        f.write("# Sensor TI-04 com leitura impossível para habitat habitado\n")
        f.write(f"temperatura_interna_sensor_defeituoso,{valor_sensor_defeituoso},celsius,ERRO_SENSOR\n")
 
        f.write("\n# --- LOG DE EVENTOS (ordem cronologica) ---\n")
        f.write("id,timestamp,tipo,descricao,severidade\n")
        for ev in eventos:
            f.write(",".join(str(x) for x in ev) + "\n")
 
    print(f"  Telemetria gerada: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
 
 
# ============================================================
# 1. LEITURA DOS DADOS DO ARQUIVO CSV
# ============================================================
 
def carregar_dados(caminho_arquivo):
    """
    Lê o arquivo dados.csv e organiza as seções em dicionários.
    Retorna: modulos, energia, ambiente, eventos, inconsistencia
    """
    modulos = {}
    energia = []
    ambiente = []
    eventos = []
    inconsistencia = {}
 
    secao_atual = None
 
    with open(caminho_arquivo, encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
 
            if not linha or (linha.startswith("#") and "---" not in linha):
                continue
 
            if "MODULOS CRITICOS" in linha:
                secao_atual = "modulos"
                continue
            elif "ENERGIA POR HORARIO" in linha:
                secao_atual = "energia"
                continue
            elif "VARIAVEIS AMBIENTAIS" in linha:
                secao_atual = "ambiente"
                continue
            elif "INCONSISTENCIA" in linha:
                secao_atual = "inconsistencia"
                continue
            elif "LOG DE EVENTOS" in linha:
                secao_atual = "eventos"
                continue
            elif linha.startswith("#"):
                continue
 
            if linha.startswith("modulo,") or linha.startswith("hora,") or \
               linha.startswith("variavel,") or linha.startswith("id,") or \
               linha.startswith("temperatura_interna_sensor"):
                partes = linha.split(",")
                if partes[0] == "temperatura_interna_sensor_defeituoso":
                    try:
                        inconsistencia = {
                            "sensor": partes[0],
                            "valor": float(partes[1]),
                            "unidade": partes[2],
                            "status": partes[3]
                        }
                    except (IndexError, ValueError):
                        pass
                continue
 
            partes = linha.split(",")
 
            if secao_atual == "modulos" and len(partes) >= 2:
                modulos[partes[0]] = int(partes[1])
 
            elif secao_atual == "energia" and len(partes) >= 4:
                energia.append({
                    "hora": partes[0],
                    "geracao": float(partes[1]),
                    "consumo": float(partes[2]),
                    "reserva": float(partes[3])
                })
 
            elif secao_atual == "ambiente" and len(partes) >= 4:
                ambiente.append({
                    "variavel": partes[0],
                    "valor": float(partes[1]),
                    "unidade": partes[2],
                    "status": partes[3]
                })
 
            elif secao_atual == "eventos" and len(partes) >= 5:
                eventos.append({
                    "id": int(partes[0]),
                    "timestamp": partes[1],
                    "tipo": partes[2],
                    "descricao": partes[3],
                    "severidade": partes[4]
                })
 
    return modulos, energia, ambiente, eventos, inconsistencia
 
 
# ============================================================
# 2. ESTRUTURAS DE DADOS
# ============================================================
 
def montar_estruturas(modulos, energia, ambiente, eventos):
    lista_geracao  = [e["geracao"]  for e in energia]
    lista_consumo  = [e["consumo"]  for e in energia]
    lista_reserva  = [e["reserva"]  for e in energia]
    lista_horarios = [e["hora"]     for e in energia]
 
    fila_alertas = []
    for ev in eventos:
        if ev["severidade"] in ("alerta", "critico"):
            fila_alertas.append(ev)
 
    pilha_criticos = []
    for ev in eventos:
        if ev["tipo"] in ("FALHA", "ERRO"):
            pilha_criticos.append(ev)
 
    dicionario_modulos = modulos.copy()
 
    hierarquia_missao = {
        "ARES-1": {
            "Energia": {
                "Solar":   lista_geracao,
                "Bateria": lista_reserva
            },
            "Habitat": {
                "Oxigenio":    "suporte_vida",
                "Temperatura": "habitat",
                "Comunicacao": "comunicacao"
            },
            "Ciencia": {
                "Laboratorio":   "laboratorio",
                "Armazenamento": "armazenamento"
            }
        }
    }
 
    matriz_energia = []
    for e in energia:
        matriz_energia.append([e["hora"], e["geracao"], e["consumo"], e["reserva"]])
 
    return (lista_geracao, lista_consumo, lista_reserva, lista_horarios,
            fila_alertas, pilha_criticos, dicionario_modulos,
            hierarquia_missao, matriz_energia)
 
 
# ============================================================
# 3. REGRAS LÓGICAS — DIAGNÓSTICO DO SISTEMA
# ============================================================
 
def diagnosticar(modulos, ambiente, reserva_atual):
    amb = {a["variavel"]: a["valor"] for a in ambiente}
 
    suporte_vida  = modulos.get("suporte_vida", 0)
    energia_mod   = modulos.get("energia", 0)
    comunicacao   = modulos.get("comunicacao", 0)
    laboratorio   = modulos.get("laboratorio", 0)
 
    radiacao      = amb.get("nivel_radiacao", 0)
    qualidade_com = amb.get("qualidade_comunicacao", 100)
 
    alertas_gerados = []
 
    if not suporte_vida and not energia_mod:
        alertas_gerados.append(("CRITICO", "Falha simultânea em suporte à vida e energia — missão em risco imediato"))
    elif not suporte_vida:
        alertas_gerados.append(("CRITICO", "Falha no módulo de suporte à vida — tripulação em perigo"))
    elif not energia_mod:
        alertas_gerados.append(("CRITICO", "Falha no módulo de energia — sistemas críticos desligando"))
 
    if reserva_atual < 25 and reserva_atual >= 0:
        alertas_gerados.append(("CRITICO", f"Reserva de energia em {reserva_atual}% — abaixo do limiar mínimo de sobrevivência (25%)"))
    elif reserva_atual < 50:
        alertas_gerados.append(("ALERTA", f"Reserva de energia em {reserva_atual}% — monitorar consumo"))
 
    if radiacao > 3.0 and not comunicacao:
        alertas_gerados.append(("CRITICO", f"Radiação em {radiacao} mSv/h + comunicação falha — tripulação isolada sob radiação perigosa"))
    elif radiacao > 3.0:
        alertas_gerados.append(("ALERTA", f"Nível de radiação elevado: {radiacao} mSv/h (limite seguro: 3.0 mSv/h)"))
 
    if not comunicacao or qualidade_com < 20:
        alertas_gerados.append(("CRITICO", f"Comunicação com a Terra comprometida — qualidade: {qualidade_com}%, módulo: {'ON' if comunicacao else 'OFF'}"))
 
    if not laboratorio:
        alertas_gerados.append(("ALERTA", "Laboratório científico offline — pesquisas interrompidas"))
 
    severidades = [a[0] for a in alertas_gerados]
    if "CRITICO" in severidades:
        status_geral = "CRITICO"
    elif "ALERTA" in severidades:
        status_geral = "ALERTA"
    else:
        status_geral = "NORMAL"
 
    return status_geral, alertas_gerados
 
 
# ============================================================
# 4. DETECÇÃO DE INCONSISTÊNCIA
# ============================================================
 
def detectar_inconsistencia(inconsistencia):
    if not inconsistencia:
        return None
 
    valor = inconsistencia.get("valor", 0)
 
    if "temperatura_interna" in inconsistencia.get("sensor", "") and valor > 100:
        return {
            "sensor": inconsistencia["sensor"],
            "valor_lido": valor,
            "diagnostico": f"ERRO: Temperatura interna de {valor}°C é fisicamente impossível em habitat habitado.",
            "acao": "Sensor TI-04 marcado como DEFEITUOSO. Usando última leitura válida (22°C)."
        }
    return None
 
 
# ============================================================
# 5. ANÁLISE E PREVISÃO — REGRESSÃO LINEAR SIMPLES
# ============================================================
 
def prever_reserva(lista_reserva, lista_horarios):
    n = len(lista_reserva)
    x = list(range(n))
    y = lista_reserva
 
    media_x = sum(x) / n
    media_y = sum(y) / n
 
    numerador   = sum((x[i] - media_x) * (y[i] - media_y) for i in range(n))
    denominador = sum((x[i] - media_x) ** 2 for i in range(n))
 
    b = numerador / denominador if denominador != 0 else 0
    a = media_y - b * media_x
 
    reserva_proximo = a + b * n
    reserva_proximo = max(0, round(reserva_proximo, 1))
 
    if b < 0:
        ciclos_ate_zero = -a / b - n
        ciclos_ate_zero = max(0, round(ciclos_ate_zero, 1))
    else:
        ciclos_ate_zero = None
 
    return reserva_proximo, ciclos_ate_zero, round(b, 2)
 
 
# ============================================================
# 6. GERAÇÃO DE RECOMENDAÇÕES
# ============================================================
 
def gerar_recomendacoes(status_geral, alertas, reserva_proximo, modulos):
    recomendacoes = []
 
    if status_geral == "CRITICO":
        recomendacoes.append(("CRITICA", "Manter suporte à vida e comunicação de emergência ativos a qualquer custo"))
        recomendacoes.append(("CRITICA", "Ativar protocolo de tempestade solar — tripulação para abrigo blindado"))
 
    for severidade, mensagem in alertas:
        if "Reserva" in mensagem and "25%" in mensagem:
            recomendacoes.append(("ALTA", "Desligar laboratório e sistemas não essenciais imediatamente"))
            recomendacoes.append(("ALTA", "Redirecionar energia para habitat e carregamento de baterias"))
        if "Radiação" in mensagem:
            recomendacoes.append(("ALTA", "Tripulação deve permanecer no interior blindado do habitat"))
        if "Comunicação" in mensagem:
            recomendacoes.append(("ALTA", "Ativar antena de emergência de baixo consumo para contato mínimo com Terra"))
 
    if reserva_proximo < 15:
        recomendacoes.append(("ALTA", f"Previsão indica reserva em {reserva_proximo}% no próximo ciclo — iniciar modo de hibernação"))
    elif reserva_proximo < 30:
        recomendacoes.append(("MEDIA", f"Reserva prevista em {reserva_proximo}% — reduzir consumo em 30%"))
 
    recomendacoes.append(("MEDIA", "Registrar todos os eventos no log para análise pós-tempestade"))
    recomendacoes.append(("BAIXA", "Verificar integridade do sensor TI-04 após normalização"))
 
    return recomendacoes
 
 
# ============================================================
# 7. EXIBIÇÃO — SAÍDA FORMATADA NO TERMINAL
# ============================================================
 
def linha(char="=", tamanho=60):
    print(char * tamanho)
 
def exibir_cabecalho():
    linha()
    print("  ARES-1 — SISTEMA INTELIGENTE DE MONITORAMENTO")
    print("  Base Autônoma em Marte | FIAP Global Solution 2026")
    linha()
 
def exibir_modulos(dicionario_modulos):
    print("\n[ MÓDULOS CRÍTICOS ]")
    linha("-")
    print(f"{'Módulo':<20} {'Status':<12} {'Estado'}")
    linha("-")
    for nome, status in dicionario_modulos.items():
        estado = "✔ OPERACIONAL" if status == 1 else "✘ FALHA"
        print(f"{nome:<20} {status:<12} {estado}")
 
def exibir_matriz_energia(matriz_energia):
    print("\n[ LEITURAS DE ENERGIA POR HORÁRIO ]")
    linha("-")
    print(f"{'Hora':<8} {'Geração (kWh)':<16} {'Consumo (kWh)':<16} {'Reserva (%)'}")
    linha("-")
    for row in matriz_energia:
        print(f"{row[0]:<8} {row[1]:<16} {row[2]:<16} {row[3]}")
 
def exibir_fila_alertas(fila_alertas):
    print("\n[ FILA DE ALERTAS PENDENTES — por ordem de chegada ]")
    linha("-")
    if not fila_alertas:
        print("  Nenhum alerta pendente.")
    for i, ev in enumerate(fila_alertas):
        print(f"  [{i+1}] {ev['timestamp']} | {ev['tipo']:<6} | {ev['descricao']}")
 
def exibir_pilha_criticos(pilha_criticos):
    print("\n[ PILHA DE EVENTOS CRÍTICOS — mais recente primeiro ]")
    linha("-")
    if not pilha_criticos:
        print("  Nenhum evento crítico registrado.")
    for ev in reversed(pilha_criticos):
        print(f"  ▲ {ev['timestamp']} | {ev['tipo']:<6} | {ev['descricao']}")
 
def exibir_inconsistencia(resultado_inconsistencia):
    print("\n[ DETECÇÃO DE INCONSISTÊNCIA ]")
    linha("-")
    if resultado_inconsistencia:
        print(f"  Sensor : {resultado_inconsistencia['sensor']}")
        print(f"  Valor  : {resultado_inconsistencia['valor_lido']}°C")
        print(f"  {resultado_inconsistencia['diagnostico']}")
        print(f"  Ação   : {resultado_inconsistencia['acao']}")
    else:
        print("  Nenhuma inconsistência detectada.")
 
def exibir_diagnostico(status_geral, alertas_gerados):
    print("\n[ DIAGNÓSTICO DO SISTEMA ]")
    linha("-")
    cores = {"CRITICO": "!!! CRÍTICO", "ALERTA": ">>  ALERTA ", "NORMAL": "--- NORMAL "}
    print(f"\n  STATUS GERAL DA MISSÃO: {cores.get(status_geral, status_geral)}\n")
    for severidade, mensagem in alertas_gerados:
        prefixo = "🔴" if severidade == "CRITICO" else "🟡"
        print(f"  {prefixo} [{severidade}] {mensagem}")
 
def exibir_previsao(reserva_proximo, ciclos_ate_zero, taxa_queda, lista_horarios):
    print("\n[ ANÁLISE E PREVISÃO — Regressão Linear ]")
    linha("-")
    print(f"  Método        : Regressão linear simples (sem bibliotecas externas)")
    print(f"  Variável      : Reserva de energia (%)")
    print(f"  Taxa de queda : {taxa_queda}% por ciclo de 2h")
    print(f"  Reserva atual : {lista_horarios[-1]} → última leitura registrada")
    print(f"  Previsão 18h  : {reserva_proximo}% no próximo ciclo")
    if ciclos_ate_zero:
        print(f"  ⚠ Esgotamento : reserva chega a 0% em ~{ciclos_ate_zero} ciclos")
        print(f"    → Decisão   : iniciar modo de hibernação imediatamente")
    else:
        print(f"  Reserva estável — sem previsão de esgotamento.")
 
def exibir_recomendacoes(recomendacoes):
    print("\n[ RECOMENDAÇÕES PRIORIZADAS ]")
    linha("-")
    ordem = {"CRITICA": 0, "ALTA": 1, "MEDIA": 2, "BAIXA": 3}
    recomendacoes_ord = sorted(recomendacoes, key=lambda r: ordem.get(r[0], 9))
    for i, (prioridade, texto) in enumerate(recomendacoes_ord, 1):
        print(f"  {i}. [{prioridade:<7}] {texto}")
 
def exibir_hierarquia(hierarquia_missao):
    print("\n[ HIERARQUIA DA MISSÃO ]")
    linha("-")
    for missao, subsistemas in hierarquia_missao.items():
        print(f"  {missao}")
        for sub, componentes in subsistemas.items():
            print(f"  ├── {sub}")
            if isinstance(componentes, dict):
                items = list(componentes.items())
                for j, (comp, val) in enumerate(items):
                    prefixo = "└──" if j == len(items) - 1 else "├──"
                    print(f"  │   {prefixo} {comp}")
 
 
# ============================================================
# 8. FUNÇÃO PRINCIPAL
# ============================================================
 
def main():
    caminho_base = os.path.dirname(os.path.abspath(__file__))
    caminho_csv  = os.path.join(caminho_base, "data", "dados.csv")
 
    exibir_cabecalho()
 
    # --- Gera telemetria aleatória realista a cada execução ---
    print("\n  Gerando telemetria da missão ARES-1...")
    gerar_dados_csv(caminho_csv)
 
    # --- Leitura dos dados ---
    print("  Carregando telemetria da missão ARES-1...")
    modulos, energia, ambiente, eventos, inconsistencia = carregar_dados(caminho_csv)
    print("  Dados carregados com sucesso.\n")
 
    # --- Montagem das estruturas ---
    (lista_geracao, lista_consumo, lista_reserva, lista_horarios,
     fila_alertas, pilha_criticos, dicionario_modulos,
     hierarquia_missao, matriz_energia) = montar_estruturas(modulos, energia, ambiente, eventos)
 
    # --- Exibições ---
    exibir_modulos(dicionario_modulos)
    exibir_hierarquia(hierarquia_missao)
    exibir_matriz_energia(matriz_energia)
    exibir_fila_alertas(fila_alertas)
    exibir_pilha_criticos(pilha_criticos)
 
    # --- Inconsistência ---
    resultado_inconsistencia = detectar_inconsistencia(inconsistencia)
    exibir_inconsistencia(resultado_inconsistencia)
 
    # --- Diagnóstico ---
    reserva_atual = lista_reserva[-1]
    status_geral, alertas_gerados = diagnosticar(modulos, ambiente, reserva_atual)
    exibir_diagnostico(status_geral, alertas_gerados)
 
    # --- Previsão ---
    reserva_proximo, ciclos_ate_zero, taxa_queda = prever_reserva(lista_reserva, lista_horarios)
    exibir_previsao(reserva_proximo, ciclos_ate_zero, taxa_queda, lista_horarios)
 
    # --- Recomendações ---
    recomendacoes = gerar_recomendacoes(status_geral, alertas_gerados, reserva_proximo, modulos)
    exibir_recomendacoes(recomendacoes)
 
    linha()
    print("  FIM DO RELATÓRIO ARES-1")
    linha()
 
 
if __name__ == "__main__":
    main()
