# Instalar pacotes necessários (se ainda não estiverem instalados)
# install.packages(c("httr", "jsonlite", "dplyr", "lubridate", "purrr"))

library(httr)
library(jsonlite)
library(dplyr)
library(lubridate)
library(purrr)

# Conexão com API Open Weather Map
API_KEY <- "e6d1c279f1c8e066b58bd6e7dab3129f"
BASE_URL <- "http://api.openweathermap.org/data/2.5/forecast"
city_name <- "Osasco"

# Requisição à API
response <- try(GET(BASE_URL, query = list(q = city_name, appid = API_KEY, units = "metric")), silent = TRUE)

# Verificar se a requisição foi bem-sucedida
if (inherits(response, "response") && status_code(response) == 200) {
  
  data <- content(response, as = "parsed", simplifyVector = FALSE)
  previsoes <- data$list
  
  # Construção do data.frame
  df <- tibble(
    DATA = as_datetime(map_dbl(previsoes, "dt")),
    TEMPERATURA = map_dbl(previsoes, ~ .x$main$temp),
    DESCRICAO = map_chr(previsoes, ~ .x$weather[[1]]$description),
    CHUVA = map_dbl(previsoes, ~ if (!is.null(.x$rain)) .x$rain$`3h` else 0.0),
    PRECIPITACAO = map_dbl(previsoes, ~ if (!is.null(.x$pop)) .x$pop else NA_real_)
  )
  
  df <- df %>%
    mutate(
      CIDADE = city_name,
      DATA_REF = format(DATA, "%Y-%m-%d"),
      DIA = date(DATA)
    )
  
  print(head(df))  # Exibe as primeiras linhas
  
  # Estatísticas por dia
  resumo_diario <- df %>%
    group_by(DIA) %>%
    summarise(
      TEMP_MEDIA = mean(TEMPERATURA, na.rm = TRUE),
      TEMP_MAX = max(TEMPERATURA, na.rm = TRUE),
      TEMP_MIN = min(TEMPERATURA, na.rm = TRUE),
      CHUVA_TOTAL = sum(CHUVA, na.rm = TRUE),
      PROB_MEDIA_PRECIP = mean(PRECIPITACAO, na.rm = TRUE)
    )
  
  print(resumo_diario)
  
  # Dia mais chuvoso
  dia_chuvoso <- resumo_diario %>%
    filter(CHUVA_TOTAL == max(CHUVA_TOTAL)) %>%
    select(DIA, CHUVA_TOTAL)
  
  cat("\n🌧️ Dia mais chuvoso previsto:\n")
  print(dia_chuvoso)
  
  # Dia mais quente
  dia_quente <- resumo_diario %>%
    filter(TEMP_MAX == max(TEMP_MAX)) %>%
    select(DIA, TEMP_MAX)
  
  cat("\n🔥 Dia mais quente previsto:\n")
  print(dia_quente)
  
} else {
  print("Erro na requisição. Verifique sua conexão ou a chave da API.")
}


