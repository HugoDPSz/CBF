# Usar uma imagem base oficial do Python
FROM python:3.9-slim

# Definir o diretório de trabalho no contentor
WORKDIR /app

# Copiar o ficheiro de dependências e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto do código da aplicação
COPY . .

# Expor a porta que a aplicação Flask usa
EXPOSE 5000

# Comando para executar a aplicação
CMD ["python", "run.py"]