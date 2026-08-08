# Relatório da Verificação de Vulnerabilidades — Etapa 5

## 1. Identificação da sessão

| Item | Valor |
| :--- | :--- |
| **Ambiente testado** | OWASP Juice Shop `20.1.1` executado localmente em contêiner Docker |
| **Ferramenta** | OWASP ZAP `2.17.0`, imagem estável oficial |
| **Modalidade** | ZAP Baseline Scan: spider tradicional seguido de análise passiva |
| **Início** | 08/08/2026 às 12:16:27 (`America/Sao_Paulo`, UTC−03:00) |
| **Término** | 08/08/2026 às 12:17:30 (`America/Sao_Paulo`, UTC−03:00) |
| **Duração aproximada** | 1 minuto e 3 segundos |
| **Alvo interno** | `http://es-seguro-juice-shop:3000` |
| **Acesso pelo host** | `http://127.0.0.1:3000` |
| **Autorização** | Aplicação deliberadamente vulnerável, executada localmente para treinamento |

O teste permaneceu restrito à instância local do OWASP Juice Shop. Nenhum sistema de terceiros foi incluído no escopo.

## 2. Ambiente e rastreabilidade

| Componente | Versão ou identificação |
| :--- | :--- |
| Docker Engine | `29.4.3` |
| OWASP Juice Shop | `20.1.1` |
| Imagem Juice Shop | `bkimminich/juice-shop@sha256:e68144772ebaaca0ec117b38d44903af92416793230288ef7c5437fc4f26850a` |
| OWASP ZAP | `2.17.0` |
| Imagem ZAP | `ghcr.io/zaproxy/zaproxy@sha256:781a2bdaea47324e7bab583e2263f21d257b0aee61ed51521a5be45f5f5081ef` |
| Rede Docker dedicada | `es-seguro-e5` |
| Contêiner do alvo | `es-seguro-juice-shop` |

Antes da sessão, o alvo retornou `HTTP 200` pelo host e a partir de um contêiner conectado à rede `es-seguro-e5`. Essa dupla verificação confirmou que o serviço estava disponível e que o ZAP alcançaria somente o alias interno autorizado.

## 3. Configuração e execução

O Juice Shop foi publicado apenas na interface de loopback do computador:

```powershell
docker network create es-seguro-e5
docker run --detach `
  --name es-seguro-juice-shop `
  --network es-seguro-e5 `
  --publish 127.0.0.1:3000:3000 `
  bkimminich/juice-shop:latest
```

A sessão válida utilizou o script oficial `zap-baseline.py`, com um minuto de spider tradicional e até dez minutos para inicialização e conclusão da análise passiva:

```powershell
$evidencePath = (Resolve-Path "evidencias\etapa-5\relatorios").Path
docker run --rm `
  --network es-seguro-e5 `
  --volume "${evidencePath}:/zap/wrk/:rw" `
  ghcr.io/zaproxy/zaproxy:stable `
  zap-baseline.py `
  -t http://es-seguro-juice-shop:3000 `
  -m 1 -T 10 `
  -r relatorio-zap.html `
  -J relatorio-zap.json
```

Segundo a documentação oficial do ZAP, o Baseline Scan rastreia o alvo pelo tempo configurado e aguarda a conclusão das regras passivas, sem executar ataques ativos. Essa modalidade foi suficiente para observar cabeçalhos e configurações inseguras no ambiente educacional.

## 4. Resultado geral da execução

A sessão definitiva apresentou:

- `158` URLs observadas;
- `59` regras sem alerta (`PASS`);
- `8` identificadores de regra com novos avisos (`WARN-NEW`);
- `0` regras configuradas como falha (`FAIL-NEW`);
- código de saída `2`, que na convenção do script indica ao menos um `WARN` e nenhum `FAIL`.

O JSON contém dez entradas nomeadas de alerta porque os identificadores `90004` e `10049` aparecem com duas variações de nome cada. A saída resumida agrupa essas variações pelo identificador da regra.

## 5. Evidências preservadas

- [Relatório HTML original do ZAP](relatorios/relatorio-zap.html)
- [Relatório JSON original do ZAP](relatorios/relatorio-zap.json)
- [Log integral da sessão definitiva](relatorios/log-da-execucao.txt)

Os três arquivos foram gerados pela mesma sessão, possuem conteúdo não vazio e o JSON foi validado por desserialização antes da análise.

## 6. Limitações e tentativas descartadas

Duas tentativas anteriores de executar o ZAP Full Scan foram descartadas e não foram usadas como evidência. A primeira, com Client Spider, tornou a API do Docker indisponível; a segunda, sem o navegador, foi encerrada por falta de memória. Os eventos do Docker registraram `oom` para o contêiner do ZAP. A máquina disponibilizava aproximadamente `3,69 GiB` à VM do Docker, valor insuficiente para concluir o active scan com a imagem utilizada.

Por essa restrição comprovada, a sessão definitiva utilizou o Baseline Scan oficial. Consequentemente:

- não foram enviados payloads de exploração ativa;
- a navegação foi feita sem autenticação;
- fluxos protegidos por login não foram cobertos;
- aplicações de página única podem expor rotas que o spider tradicional não alcança;
- alertas passivos apontam condições que exigem interpretação e não comprovam, isoladamente, exploração ou impacto;
- a ausência de um alerta não comprova ausência de vulnerabilidade.

## 7. Referências da metodologia

- [ZAP Baseline Scan](https://www.zaproxy.org/docs/docker/baseline-scan/)
- [Documentação das imagens Docker do ZAP](https://www.zaproxy.org/docs/docker/)
- [Execução local do OWASP Juice Shop](https://pwning.owasp-juice.shop/companion-guide/local/part1/running.html)
