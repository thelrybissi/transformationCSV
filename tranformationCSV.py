import time
from datetime import datetime
import pandas as pd
import random

# Gera CPF valido de forma aleatória
def generate_cpf():
    # Função para gerar CPF válido
    def generate_cpf_digits(digits):
        sum_of_products = sum(a * b for a, b in zip(digits, range(len(digits) + 1, 1, -1)))
        mod = sum_of_products % 11
        return 11 - mod if mod > 1 else 0

    # Geração dos primeiros 9 dígitos
    digits = [random.randint(0, 9) for _ in range(9)]

    # Cálculo dos dois dígitos verificadores
    digits.append(generate_cpf_digits(digits))
    digits.append(generate_cpf_digits(digits))

    # Formatação do CPF com máscara
    return f"{digits[0]}{digits[1]}{digits[2]}.{digits[3]}{digits[4]}{digits[5]}.{digits[6]}{digits[7]}{digits[8]}-{digits[9]}{digits[10]}"

# Calcula a idade a partir da data de nascimento
def calculate_age(birthdate):
    today = datetime.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

start_time = time.time() # Inicia o timer antes do carregamento do .csv

input_file_path = 'C:\dev\example\inputCSV\pessoas.csv' # Carregar o CSV exportado

df = pd.read_csv(input_file_path, sep=";") # Aqui passamos o caminho do csv e tambem definimos qual separador de colunas é o do arquivo(por padrão é ",")
df["hobby"] = df["hobby"].str.upper() # Transformo todos os valores da coluna hobby em Maiúscula
df["Cpf"] = [generate_cpf() for _ in range(len(df))] # Chamo a função generate_cpf que gera os CPFs, crio a coluna Cpf no .csv e populo ela com CPFs gerados
df["gender"] = df["gender"].replace({"Masculino": "M","Feminino": "F"}) # Transformo Masculino para o M, caso valor da coluna Feminino passará a ser F
df["birthdate"] = pd.to_datetime(df["birthdate"], format='%d/%m/%Y') # Converto para formato data e formato para padrão dd/mm/AAAA
df['age'] = df['birthdate'].apply(calculate_age) #Chamo a calculate_age que a partir da data de nascimento calcula a idade da pessoa

# Salvar o dataframe transformado em um novo CSV
current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file_path = f'C:\dev\example\outputCSV\pessoas_convertidas{current_datetime}.csv'

# Salvo um novo arquivo já transformado, com separador ";" e o encoding no formato que os caracteres especiais não quebrem
df.to_csv(output_file_path, index=False, sep=";", encoding="latin1")

print("Arquivo gerado com sucesso na pasta de output!")

end_time = time.time()
duration = end_time - start_time

# Mostro no console o tempo que levou o arquivo csv para ser transformado.
print(f"Tempo para converter o arquivo CSV: {duration:.2f} segundos")


