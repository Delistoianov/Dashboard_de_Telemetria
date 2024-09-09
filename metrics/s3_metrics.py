import os
import boto3
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Variáveis de ambiente para acessar o S3
BUCKET_NAME = os.getenv('BUCKET_NAME')
AWS_REGION = os.getenv('AWS_REGION')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN')

# Função para inicializar o cliente S3
def get_s3_client():
    return boto3.client(
        's3',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN
    )

# Função para obter métricas do S3
def get_s3_metrics():
    s3_client = get_s3_client()

    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)

        if 'Contents' not in response:
            print(f"O bucket '{BUCKET_NAME}' está vazio.")
            return {
                'total_size': 0,
                'total_objects': 0,
                'last_modified': None
            }

        total_size = 0
        total_objects = 0
        last_modified = None

        for obj in response['Contents']:
            total_size += obj['Size']  
            total_objects += 1  

            # Atualiza a última modificação se for mais recente
            if not last_modified or obj['LastModified'] > last_modified:
                last_modified = obj['LastModified']

        metrics = {
            'total_size': total_size,  # Tamanho total dos objetos no bucket
            'total_objects': total_objects,  # Quantidade de objetos no bucket
            'last_modified': last_modified  # Data da última modificação
        }

        return metrics

    except Exception as e:
        print(f"Erro ao coletar métricas do S3: {e}")
        return None

# Testar a função de coleta de métricas
if __name__ == "__main__":
    metrics = get_s3_metrics()
    if metrics:
        print(f"Métricas do S3 para o bucket '{BUCKET_NAME}':")
        print(f"Tamanho total (em bytes): {metrics['total_size']}")
        print(f"Total de objetos: {metrics['total_objects']}")
        print(f"Última modificação: {metrics['last_modified']}")
