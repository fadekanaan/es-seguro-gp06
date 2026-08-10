# Relatório da Verificação de Vulnerabilidades — Etapa 5

## 1. Identificação da sessão

| Item | Valor |
| :--- | :--- |
| **Sistema testado** | ThesisFlow, revisão `486219c46ffce643e567a76b737e1f7b4cfc9964` da branch `development` |
| **Ferramenta** | OWASP ZAP `2.17.0` |
| **Modalidade** | Sessão única, autenticada, com spider, importação OpenAPI e análise passiva |
| **Período** | 10/08/2026, das 17:23:59 às 17:25:58 (`America/Sao_Paulo`, UTC−03:00) |
| **Frontend** | `http://127.0.0.1:5173` |
| **Backend** | `http://127.0.0.1:8000` |
| **Serviços emulados** | Firebase Authentication em `127.0.0.1:9099` e Firestore em `127.0.0.1:8080` |
| **Autorização** | Código do próprio grupo, executado apenas no computador local |

O objeto da verificação foi o próprio **ThesisFlow**. Como as credenciais do projeto Firebase real não estavam disponíveis, Firebase Authentication e Firestore foram substituídos pela **Firebase Local Emulator Suite**. Essa limitação não foi ocultada: o frontend React/Vite e o backend FastAPI analisados são os componentes reais do projeto; somente os serviços externos de identidade e banco de dados foram emulados para viabilizar uma sessão autenticada e reproduzível sem acessar produção.

Nenhum sistema de terceiros foi incluído no escopo e nenhuma credencial, token de sessão ou senha foi preservado nas evidências.

## 2. Ambiente e configuração básica

| Componente | Versão ou identificação |
| :--- | :--- |
| ThesisFlow | commit `486219c46ffce643e567a76b737e1f7b4cfc9964` |
| Frontend | React/Vite, porta local `5173` |
| Backend | FastAPI, porta local `8000` |
| Firebase CLI | `14.27.0` |
| Projeto descartável do emulador | `demo-thesisflow-e5` |
| OWASP ZAP | `2.17.0`, imagem `ghcr.io/zaproxy/zaproxy:stable` |
| Proxy/API local do ZAP | `127.0.0.1:8090` |
| Gateway do host visto pelo contêiner | `192.168.65.254` |

O endereço `192.168.65.254` mostrado pelo ZAP é o gateway do Docker Desktop para os serviços que executavam no próprio computador. Ele não representa um alvo externo. O escopo continha somente as portas locais `5173`, `8000` e `9099`.

Foram criados adaptadores locais mínimos, não versionados no ThesisFlow, para conectar o frontend ao Auth Emulator e o backend ao Firestore Emulator. Antes da sessão, os testes do projeto foram executados:

- frontend: `45` testes aprovados em `13` arquivos;
- backend: `271` testes aprovados, com um aviso de depreciação de dependência;
- integração local: autenticação, sincronização do papel `coordinator` e consulta protegida ao backend aprovadas.

## 3. Procedimento executado

A sessão foi iniciada com o ZAP em modo daemon e sem Active Scan. Na mesma sessão foram realizadas as seguintes ações:

1. acesso às páginas `/`, `/login` e `/dashboard` do frontend;
2. autenticação de um usuário descartável no Auth Emulator;
3. sincronização das claims e confirmação do papel `coordinator`;
4. envio, pelo proxy do ZAP, de `18` requisições `GET` autenticadas a rotas do backend, todas com resposta `HTTP 200`;
5. importação do contrato OpenAPI do backend;
6. spider tradicional até `100%`;
7. espera até a fila de análise passiva chegar a zero;
8. geração dos relatórios HTML e JSON da mesma sessão.

As rotas autenticadas incluíram estudantes, orientadores, projetos, atividades, auditoria, alertas, suporte e relatórios. O objetivo foi obter cobertura representativa sem alterar dados e sem executar exploração completa, conforme permitido pelo enunciado.

A configuração declarativa está em [`relatorios/zap.yaml`](relatorios/zap.yaml), e o registro sanitizado da execução está em [`relatorios/log-da-execucao.txt`](relatorios/log-da-execucao.txt).

## 4. Resultado geral

A sessão registrou `104` URLs. A API do ZAP contabilizou `62` instâncias de alerta:

| Risco | Instâncias | Tipos únicos no relatório HTML |
| :--- | ---: | ---: |
| Alto | `0` | `0` |
| Médio | `14` | `2` |
| Baixo | `39` | `4` |
| Informativo | `9` | `3` |

Os números representam métricas diferentes: a API conta cada ocorrência em cada URL, enquanto o resumo HTML agrupa ocorrências pelo tipo de alerta. Foram observados nove tipos únicos no conjunto da sessão.

## 5. Evidências preservadas

- [Relatório HTML original do ZAP](relatorios/relatorio-zap.html)
- [Relatório JSON original do ZAP](relatorios/relatorio-zap.json)
- [Log sanitizado da sessão](relatorios/log-da-execucao.txt)
- [Configuração declarativa do escopo](relatorios/zap.yaml)
- [Tela de login do ThesisFlow](capturas-de-tela/01-thesisflow-login.jpg)
- [Painel autenticado do ThesisFlow](capturas-de-tela/02-thesisflow-dashboard.jpg)
- [Resumo dos alertas do ZAP](capturas-de-tela/03-zap-resumo.jpg)

Os relatórios possuem conteúdo não vazio, e o JSON foi validado por desserialização antes da análise.

## 6. Achados selecionados

| ID | Alerta ou condição | Evidência | Classificação | Correção proposta |
| :---: | :--- | :--- | :--- | :--- |
| `A01` | `Content Security Policy (CSP) Header Not Set` | Plugin `10038`; risco médio; confiança alta; `7` ocorrências no frontend | OWASP A05:2025 e CWE-693 | Implantar CSP em `Report-Only`, ajustar origens legítimas e então impor política restritiva |
| `A02` | `Missing Anti-clickjacking Header` | Plugin `10020`; risco médio; confiança média; `7` ocorrências no frontend | OWASP A05:2025 e CWE-1021 | Definir `frame-ancestors 'none'` na CSP e `X-Frame-Options: DENY` como compatibilidade |
| `A03` | Identificadores inválidos provocam `HTTP 500` | Plugins `90022` e `10023`; risco baixo; confiança média; rotas `/advisors/advisor_id` e `/students/student_id` | OWASP A05:2025, CWE-550 e CWE-1295 | Validar o identificador e responder `404` ou `422`; centralizar exceções e manter detalhes somente no log interno |

A interpretação completa e a relação com os riscos anteriores estão na [Seção 15 do documento acadêmico](../../docs/etapas/etapa-5/sec15-verificacao-vulnerabilidades.md).

## 7. Interpretação, descartes e possíveis falsos positivos

Os alertas não foram tratados como prova automática de exploração:

- o `A01` comprova ausência de CSP, mas não comprova a existência de XSS;
- o `A02` comprova falta de proteção contra enquadramento, mas nenhum clique enganoso foi executado;
- no `A03`, o comportamento `HTTP 500` diante de identificadores inválidos é real, porém o corpo observado foi apenas `Internal Server Error`. Não houve stack trace, caminho local ou segredo. Assim, a parte de “divulgação de erro” é um possível falso positivo ou uma sobreposição entre os plugins `90022` e `10023`; permanece válida a falha de tratamento de entrada e erro.

Alertas de `X-Powered-By` e cabeçalhos ausentes na porta `9099` foram descartados da avaliação do ThesisFlow porque pertencem ao Auth Emulator, que não é o serviço implantado em produção. Os alertas informativos `Modern Web Application`, `Authentication Request Identified` e `Session Management Response Identified` descrevem tecnologia ou fluxo observado, sem representar vulnerabilidade por si sós. O cabeçalho `X-Content-Type-Options` ausente é relevante para endurecimento, mas não foi selecionado entre os três achados porque se sobrepõe ao tema de cabeçalhos defensivos já coberto por `A01` e `A02`.

## 8. Limitações

- Firebase Authentication e Firestore foram emulados; configurações exclusivas do projeto Firebase real não foram avaliadas.
- A sessão foi passiva e não destrutiva; não houve Active Scan nem exploração completa.
- As requisições autenticadas usaram o papel de coordenação; não houve matriz comparativa completa entre todos os perfis.
- O conjunto de dados local era mínimo e descartável.
- Ausência de alerta não comprova ausência de vulnerabilidade.

A ordem recomendada de tratamento é `A01` → `A02` → `A03`. Depois das correções, uma nova sessão deve confirmar a remoção dos alertas e a ausência de regressões.

## 9. Referências

- [ZAP — Content Security Policy Header Not Set](https://www.zaproxy.org/docs/alerts/10038/)
- [ZAP — Missing Anti-clickjacking Header](https://www.zaproxy.org/docs/alerts/10020/)
- [ZAP — Application Error Disclosure](https://www.zaproxy.org/docs/alerts/90022/)
- [OWASP Top 10:2025 — A05 Security Misconfiguration](https://owasp.org/Top10/2025/A05_2025-Security_Misconfiguration/)
- [CWE-693](https://cwe.mitre.org/data/definitions/693.html), [CWE-1021](https://cwe.mitre.org/data/definitions/1021.html), [CWE-550](https://cwe.mitre.org/data/definitions/550.html) e [CWE-1295](https://cwe.mitre.org/data/definitions/1295.html)
