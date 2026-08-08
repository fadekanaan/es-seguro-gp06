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
  bkimminich/juice-shop@sha256:e68144772ebaaca0ec117b38d44903af92416793230288ef7c5437fc4f26850a
```

A sessão válida utilizou o script oficial `zap-baseline.py`, com um minuto de spider tradicional e até dez minutos para inicialização e conclusão da análise passiva:

```powershell
$evidencePath = (Resolve-Path "evidencias\etapa-5\relatorios").Path
docker run --rm `
  --network es-seguro-e5 `
  --volume "${evidencePath}:/zap/wrk/:rw" `
  ghcr.io/zaproxy/zaproxy@sha256:781a2bdaea47324e7bab583e2263f21d257b0aee61ed51521a5be45f5f5081ef `
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

Tentativas preparatórias de Full Scan não foram concluídas e foram descartadas. Como os diagnósticos dessas tentativas não foram preservados no repositório, nenhuma causa ou métrica de recursos é apresentada como evidência. Todas as conclusões deste relatório derivam exclusivamente da sessão Baseline concluída e versionada.

Consequentemente:

- não foram enviados payloads de exploração ativa;
- a navegação foi feita sem autenticação;
- fluxos protegidos por login não foram cobertos;
- aplicações de página única podem expor rotas que o spider tradicional não alcança;
- alertas passivos apontam condições que exigem interpretação e não comprovam, isoladamente, exploração ou impacto;
- a ausência de um alerta não comprova ausência de vulnerabilidade.

## 7. Achados selecionados

| ID | Alerta | Risco / confiança | Evidência observada | Classificação | Correção proposta |
| :---: | :--- | :---: | :--- | :--- | :--- |
| `A01` | `Content Security Policy (CSP) Header Not Set` | Médio / alta | Plugin `10038`, 4 instâncias sem CSP | OWASP A02:2025 e CWE-693 | Implantar CSP restritiva, inicialmente em modo `Report-Only` |
| `A02` | `Cross-Domain Misconfiguration` | Médio / média | Plugin `10098`, uma resposta com `Access-Control-Allow-Origin: *` | OWASP A02:2025 e CWE-942 | Restringir CORS às origens e aos recursos necessários |
| `A03` | `Deprecated Feature Policy Header Set` | Baixo / média | Plugin `10063`, 5 instâncias exclusivamente em arquivos `chunk-*.js` | OWASP A02:2025 e CWE-16 | Remover o cabeçalho dos subrecursos; se a política for necessária, enviar `Permissions-Policy` na resposta do documento HTML principal |

A interpretação completa, o impacto contextual e os critérios de priorização estão na [Seção 15 do documento acadêmico](../../docs/etapas/etapa-5/sec15-verificacao-vulnerabilidades.md).

## 8. Capturas de tela

1. [OWASP Juice Shop em execução](capturas-de-tela/01-juice-shop-em-execucao.jpg)
2. [Resumo dos alertas do ZAP](capturas-de-tela/02-resumo-alertas-zap.jpg)
3. [Detalhe do A01 — CSP ausente](capturas-de-tela/03-achado-a01.jpg)
4. [Detalhe do A02 — CORS permissivo](capturas-de-tela/04-achado-a02.jpg)
5. [Detalhe do A03 — Feature Policy obsoleta](capturas-de-tela/05-achado-a03.jpg)

## 9. Interpretação e ressalvas

Os achados não foram tratados como prova automática de exploração. O A01 confirma a ausência de uma camada de defesa, não a existência de XSS. O A02 apareceu em um recurso JavaScript público e sem credenciais; por isso, não comprova exposição de dados sensíveis, embora indique uma configuração que deve ser restrita antes de ser reutilizada em APIs. No A03, o cabeçalho apareceu apenas em subrecursos JavaScript e não governa as permissões do documento principal; nesse contexto, o alerta foi classificado como configuração sem impacto efetivo demonstrado.

A priorização recomendada é `A01` → `A02` → `A03`. Uma nova sessão deve ser executada depois das correções para verificar a remoção dos alertas e possíveis regressões.

## 10. Referências

- [ZAP Baseline Scan](https://www.zaproxy.org/docs/docker/baseline-scan/)
- [Documentação das imagens Docker do ZAP](https://www.zaproxy.org/docs/docker/)
- [Execução local do OWASP Juice Shop](https://pwning.owasp-juice.shop/companion-guide/local/part1/running.html)
- [ZAP — Content Security Policy Header Not Set](https://www.zaproxy.org/docs/alerts/10038/)
- [ZAP — Cross-Domain Misconfiguration](https://www.zaproxy.org/docs/alerts/10098/)
- [ZAP — Permissions Policy Header Not Set](https://www.zaproxy.org/docs/alerts/10063/)
- [OWASP Top 10:2025 — A02 Security Misconfiguration](https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/)
- [CWE-693](https://cwe.mitre.org/data/definitions/693.html), [CWE-942](https://cwe.mitre.org/data/definitions/942.html) e [CWE-16](https://cwe.mitre.org/data/definitions/16.html)
