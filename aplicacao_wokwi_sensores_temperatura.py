int prob_chuva[] = {0, 20, 100, 100, 0, 0, 30, 25, 50, 0, 0, 40, 50, 100, 0};
String nivel_chuva_original[] = {"Seco", "Forte", "Fraca", "Fraca", "Seco", "Seco", "Moderada", "Moderada", "Forte", "Seco", "Seco", "Fraca", "Moderada", "Fraca", "Seca"};
String data_ref[] = {"15/out", "16/out", "17/out", "18/out", "19/out", "20/out", "21/out", "22/out", "23/out", "24/out", "25/out", "26/out", "27/out", "28/out", "29/out"};

String data_programacao[15];
String tipo_acao[15];
String nivel_chuva_programada[15];
int programacao_index = 0;

int ledPin1 = 19;       // Alarme Umidade
int buttonPin1 = 34;
int valorDHT22 = 0;
bool lastButtonState1 = HIGH;

int ledPin2 = 18;       // Alarme pH
int buttonPin2 = 35;
int valorLDR = 0;
bool lastButtonState2 = HIGH;

int ledPin3 = 5;        // Alarme Nitrogênio
int buttonPin3 = 32;
bool lastButtonState3 = HIGH;
bool ledState3 = LOW;

int ledPin4 = 17;       // Alarme Fósforo
int buttonPin4 = 33;
bool lastButtonState4 = HIGH;
bool ledState4 = LOW;

int ledPin5 = 16;       // Alarme Potássio
int buttonPin5 = 25;
bool lastButtonState5 = HIGH;
bool ledState5 = LOW;

int ledPin6 = 4;        // Irrigação
int ledPin7 = 2;        // Drenagem

String Nitrogenio = "";
String Potassio = "";
String Fosforo = "";

void setup() {
  pinMode(ledPin1, OUTPUT);
  pinMode(buttonPin1, INPUT_PULLUP);

  pinMode(ledPin2, OUTPUT);
  pinMode(buttonPin2, INPUT_PULLUP);

  pinMode(ledPin3, OUTPUT);
  pinMode(buttonPin3, INPUT_PULLUP);

  pinMode(ledPin4, OUTPUT);
  pinMode(buttonPin4, INPUT_PULLUP);

  pinMode(ledPin5, OUTPUT);
  pinMode(buttonPin5, INPUT_PULLUP);

  pinMode(ledPin6, OUTPUT);
  pinMode(ledPin7, OUTPUT);

  Serial.begin(115200);
  randomSeed(analogRead(0));
}

void loop() {
  bool currentButtonState1 = digitalRead(buttonPin1);
  bool currentButtonState2 = digitalRead(buttonPin2);
  bool currentButtonState3 = digitalRead(buttonPin3);
  bool currentButtonState4 = digitalRead(buttonPin4);
  bool currentButtonState5 = digitalRead(buttonPin5);

  // Botão 1 - Umidade
  if (lastButtonState1 == HIGH && currentButtonState1 == LOW) {
    valorDHT22 = random(1, 100);
    Serial.print("Botão 1 - Umidade simulada: ");
    Serial.println(valorDHT22);

    programacao_index = 0;

    if (valorDHT22 <= 15) {
      digitalWrite(ledPin1, HIGH);
      digitalWrite(ledPin6, HIGH);
      digitalWrite(ledPin7, LOW);

      Nitrogenio = (ledState3 == HIGH) ? "Adicionar Nitrogênio" : "Nitrogênio OK";
      Potassio = (ledState5 == HIGH) ? "Adicionar Potássio" : "Potássio OK";
      Fosforo = (ledState4 == HIGH) ? "Adicionar Fósforo" : "Fósforo OK";

      Serial.println("Umidade Baixa <= 15% - Acionar Irrigação");
      Serial.println(Nitrogenio);
      Serial.println(Potassio);
      Serial.println(Fosforo);

      if (valorDHT22 <= 13) {
        for (int i = 0; i < 15; i++) {
          if (prob_chuva[i] <= 20) {
            data_programacao[programacao_index] = data_ref[i];
            tipo_acao[programacao_index] = "programar_irrigacao";
            nivel_chuva_programada[programacao_index] = nivel_chuva_original[i];
            programacao_index++;
          }
        }
      }

    } else if (valorDHT22 >= 50) {
      digitalWrite(ledPin1, HIGH);
      digitalWrite(ledPin6, LOW);
      digitalWrite(ledPin7, HIGH);
      Serial.println("Umidade Alta >= 50% - Acionar Drenagem");

      for (int i = 0; i < 15; i++) {
        if (prob_chuva[i] >= 20 && (nivel_chuva_original[i] == "Moderada" || nivel_chuva_original[i] == "Forte")) {
          data_programacao[programacao_index] = data_ref[i];
          tipo_acao[programacao_index] = "programar_drenagem";
          nivel_chuva_programada[programacao_index] = nivel_chuva_original[i];
          programacao_index++;
        }
      }

    } else {
      digitalWrite(ledPin1, LOW);
      digitalWrite(ledPin6, LOW);
      digitalWrite(ledPin7, LOW);
      Serial.println("Umidade Normal > 15% e < 50%");
    }

    // Exibir programação
    Serial.println("Datas programadas:");
    for (int i = 0; i < programacao_index; i++) {
      Serial.print("Data: ");
      Serial.println(data_programacao[i]);
      Serial.print("Ação: ");
      Serial.println(tipo_acao[i]);
      Serial.print("Nível de chuva: ");
      Serial.println(nivel_chuva_programada[i]);
      Serial.println("------");
    }

    delay(200);
  }

  // Botão 2 - pH
  if (lastButtonState2 == HIGH && currentButtonState2 == LOW) {
    valorLDR = random(0, 14);
    Serial.print("Botão 2 - pH simulado: ");
    Serial.println(valorLDR);

    if (valorLDR <= 4) {
      digitalWrite(ledPin2, HIGH);
      Serial.println("pH abaixo do limite <= 4");
    } else if (valorLDR >= 10) {
      digitalWrite(ledPin2, HIGH);
      Serial.println("pH acima do limite >= 10");
    } else {
      digitalWrite(ledPin2, LOW);
      Serial.println("pH Normal > 4 e < 10");
    }
    delay(200);
  }

  // Botão 3 - Nitrogênio
  if (lastButtonState3 == HIGH && currentButtonState3 == LOW) {
    ledState3 = !ledState3;
    digitalWrite(ledPin3, ledState3);
    Serial.print("Análise Nitrogênio: ");
    Serial.println(ledState3 ? "Falta" : "Normal");
    delay(200);
  }

  // Botão 4 - Fósforo
  if (lastButtonState4 == HIGH && currentButtonState4 == LOW) {
    ledState4 = !ledState4;
    digitalWrite(ledPin4, ledState4);
    Serial.print("Análise Fósforo: ");
    Serial.println(ledState4 ? "Falta" : "Normal");
    delay(200);
  }

  // Botão 5 - Potássio
  if (lastButtonState5 == HIGH && currentButtonState5 == LOW) {
    ledState5 = !ledState5;
    digitalWrite(ledPin5, ledState5);
    Serial.print("Análise Potássio: ");
    Serial.println(ledState5 ? "Falta" : "Normal");
    delay(200);
  }

  // Atualizar estados
  lastButtonState1 = currentButtonState1;
  lastButtonState2 = currentButtonState2;
  lastButtonState3 = currentButtonState3;
  lastButtonState4 = currentButtonState4;
  lastButtonState5 = currentButtonState5;
}