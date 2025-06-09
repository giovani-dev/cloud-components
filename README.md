# Cloud Components

**Cloud Components** é um conjunto de bibliotecas que abstraem operações de serviços em provedores de nuvem. O projeto oferece uma interface unificada para interação com recursos da AWS e GCP, além de implementações de log e carregamento de variáveis de ambiente.

## Docs

A documentação oficial encontra-se em construção e será disponibilizada em breve. Enquanto isso, consulte os exemplos deste README e o código-fonte para entender o funcionamento dos componentes.

## Visão Geral

- **AWSFacade**: acesso simplificado a SNS, Lambda, SQS e S3.
- **GCSFacade**: implementação inicial para o Cloud Storage do Google Cloud.
- **Interfaces comuns**: definidas em `cloud_components/common` para padronizar eventos, filas, funções e armazenamento.
- **Libs**: wrappers para carregar arquivos `.env` (Dotenv) e para o logger Loguru.

## Instalação

```bash
pip install cloud-components
# ou com poetry
poetry add cloud-components
```

Para desenvolvimento local, instale as dependências de teste e lint:

```bash
make install_pkg
```

## Uso Básico

```python
from cloud_components.libs.env.env import Dotenv
from cloud_components.libs.log.log import Loguru
from cloud_components.cloud.aws.facade import AWSFacade

logger = Loguru().load()
env = Dotenv(logger)
env.load()

aws = AWSFacade(logger=logger, env=env)

# Trabalhando com S3
s3 = aws.storage()
s3.bucket = env.get("BUCKET_NAME")
s3.save_file(b"Hello", "path/arquivo.txt", "text/plain")

# Enviando mensagem para SNS
sns = aws.event()
sns.source = env.get("SNS_TOPIC")
sns.send({"message": "Hello"})
```

Para uso com GCP:

```python
from cloud_components.cloud.gcp.facade import GCSFacade

gcs = GCSFacade(logger=logger, env=env)
storage = gcs.storage()
storage.bucket = env.get("BUCKET_NAME")
storage.save_file("conteúdo", "hello.txt", "text/plain", is_public=True)
```

## Ambiente de Desenvolvimento

O projeto fornece um `docker-compose` com [LocalStack](https://github.com/localstack/localstack) e um emulador de Cloud Storage para facilitar testes locais.

```bash
# subir serviços
make run_docker
# criar bucket e recursos
make create_bucket
```

Scripts auxiliares estão disponíveis em `docker/aws` para criar recursos fictícios (SNS, SQS e Lambda) no LocalStack.

## Testes e Lint

```bash
# executar testes unitários
make test

# executar pylint
make lint LINT_PATH=cloud_components
```

## CI/CD

O repositório utiliza GitHub Actions com os seguintes jobs principais:

- **lint**: executa o Pylint.
- **test**: executa a suíte de testes.
- **deploy**: publica o pacote no PyPI para tags iniciadas com `v-`.

Os detalhes de configuração estão em `.github/workflows/python-app.yml`.

## Licença

Distribuído sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais informações.
