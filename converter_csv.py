# converter_csv.py
import pandas as pd

# Lê o CSV com encoding problemático
df = pd.read_csv('data/obras.csv', encoding='latin1')

# Limpa os nomes das colunas
df.columns = df.columns.str.strip()

# Renomeia colunas problemáticas
colunas_renomear = {}
for col in df.columns:
    if 'regi' in col.lower():
        colunas_renomear[col] = 'Região'
    if 'obra' in col.lower():
        colunas_renomear[col] = 'Obras'

df = df.rename(columns=colunas_renomear)

# Salva com encoding correto
df.to_csv('data/obras.csv', index=False, encoding='utf-8-sig')
print("✅ Arquivo convertido com sucesso!")
print("Colunas:", df.columns.tolist())