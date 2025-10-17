video de apresentação https://youtu.be/DOuDFw4q8YE
aplicação wokwi https://wokwi.com/projects/444280653137120257


Objetivo do Código

Monitorar condições simuladas (umidade, pH, nutrientes).
Acionar irrigação ou drenagem automaticamente.
Planejar ações futuras com base em previsão de chuva.
Exibir relatórios no Serial Monitor.
 
Estrutura de Dados

Para efeito de simulação, utilizamos uma estrutura de dados de vetores com valores inseridos manualmente.

 prob_chuva[]: Probabilidade de chuva para 15 dias (em %).
nivel_chuva_original[]: Nível esperado de chuva (Seco, Fraca, Moderada, Forte).
data_ref[]: Datas de referência (15/out a 29/out).
Arrays para programação de ações: data_programacao, tipo_acao, nivel_chuva_programada.
2. Sensores e Atuadores

 Utilização de 7 LEDs atuando como representação de características da plantação

LEDs: Indicadores para alarmes e ações:
ledPin1 → Umidade
ledPin2 → pH
ledPin3 → Nitrogênio
ledPin4 → Fósforo
ledPin5 → Potássio
ledPin6 → Irrigação
ledPin7 → Drenagem
Botões: Cada botão simula uma leitura ou alterna estado:
Botão 1 → Umidade (simula sensor DHT22)
Botão 2 → pH (simula sensor LDR)
Botões 3, 4, 5 → Nitrogênio, Fósforo, Potássio (alternam falta/normal).
3. Lógica Principal (loop)

Botão 1 (Umidade):
Gera valor aleatório (1 a 100).
Se ≤15%: Umidade baixa → liga irrigação, verifica nutrientes.
Se ≤13%: Programa irrigação para dias com baixa probabilidade de chuva.
Se ≥50%: Umidade alta → liga drenagem.
Programa drenagem para dias com chuva moderada ou forte.
Caso contrário: Umidade normal → tudo desligado.
Exibe programação no Serial Monitor.
A programação de irrigação e drenagem no código funciona com base em dois fatores principais:

Valor de umidade simulada (sensor DHT22)
Previsão de chuva (probabilidade e nível)
 

 

Botão 2 (pH):
Simula pH (0 a 14).
Liga alarme se pH ≤4 (ácido) ou ≥10 (básico).
Botões 3, 4, 5 (Nutrientes):
Alternam estado (falta ou normal) e ligam/desligam LEDs.
