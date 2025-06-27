# Usa imagem oficial do Python
FROM python:3.11-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante da aplicação
COPY . .

# Expõe a porta padrão do Django
EXPOSE 8000

# Comando padrão (pode ser sobrescrito pelo docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

