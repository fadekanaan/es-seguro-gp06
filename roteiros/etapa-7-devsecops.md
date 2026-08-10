# Etapa 7 — Pipeline DevSecOps

## 1. Introdução ao DevSecOps no ThesisFlow

A adoção de práticas de **DevSecOps** tem como objetivo principal integrar a segurança de forma contínua e automatizada em todo o ciclo de vida de desenvolvimento de software (SDLC). No contexto do sistema **ThesisFlow**, em que dados acadêmicos sensíveis e documentos comprobatórios trafegam de forma contínua, a segurança não pode ser um evento isolado verificado apenas no momento do deploy.

As abordagens tradicionais frequentemente tratam a segurança como uma validação de fim de ciclo. O pipeline que propomos a seguir "desloca a segurança para a esquerda" (*shift-left*), garantindo que desde a concepção (modelagem STRIDE) até a operação (monitoramento e logs), todas as ações estejam sob a governança de métricas de segurança claras e testáveis.

---

## 2. Visão Geral do Pipeline

A esteira de integração e entrega contínua (CI/CD) idealizada para o ThesisFlow possui mecanismos de contenção de falhas (os chamados *Quality Gates*). Esses portões garantem que o código só avançará para o ambiente de produção se, e somente se, respeitar os requisitos técnicos extraídos das Etapas anteriores.

### Diagrama Textual do Pipeline

```text
Commit / Pull Request
      │
      ▼
┌─────────────────────────────────┐
│ 1. Code Review e Análise SAST   │  ← Quality Gate 1: Sem chaves vazadas e SAST OK
└─────────────────────────────────┘
      │ (Aprovado)
      ▼
┌─────────────────────────────────┐
│ 2. Testes de Segurança (Pytest) │  ← Quality Gate 2: Testes RBAC / Upload aprovados
└─────────────────────────────────┘
      │ (Aprovado)
      ▼
┌─────────────────────────────────┐
│ 3. Build & Análise de Dep.      │  ← Quality Gate 3: Nenhuma CVE Crítica pendente
└─────────────────────────────────┘
      │ (Aprovado)
      ▼
┌─────────────────────────────────┐
│ 4. Verificação Dinâmica (DAST)  │  ← Quality Gate 4: ZAP Baseline Scan OK
└─────────────────────────────────┘
      │ (Aprovado)
      ▼
┌─────────────────────────────────┐
│ 5. Deploy e Operação            │  ← Operação: Monitoramento ativo (IDOR, Flooding)
└─────────────────────────────────┘
```

---

## 3. Matriz de Atividades de Segurança

A tabela a seguir aprofunda os momentos ilustrados acima, detalhando as ferramentas teóricas aplicadas e os vínculos com as etapas do NIST CSF e vulnerabilidades OWASP catalogadas.

| Momento | Atividade de segurança | Ferramenta / Método | Evidência produzida | Condição para continuar |
|---|---|---|---|---|
| **Planejamento** | Análise de ameaças (STRIDE) e categorização de riscos (NIST Govern/Identify). | Sessões de modelagem e matriz de risco | Documentação das Ameaças (T01-T12) e Diagrama de Arquitetura. | Aprovação formal dos riscos aceitos pela equipe. |
| **Desenvolvimento (SAST)** | Escaneamento de código fonte para detectar injeções (CWE-89) e vazamento de segredos. | *SonarQube* / *Gitleaks* | Relatório de Análise Estática. | Código limpo de credenciais e senhas em modo texto (*hardcoded*). |
| **Integração (Testes)** | Validação da implementação segura de autorização (RS01) e upload seguro (RS03). | Scripts automatizados no *Pytest* | Logs de aprovação de CI (ex: GitHub Actions) indicando 100% de sucesso. | Os testes `test_authorization.py` não podem falhar. |
| **Verificação (DAST)** | Escaneamento dinâmico buscando falhas de configuração (CSP, CORS permissivo). | *OWASP ZAP* | Relatório HTML/JSON com alertas. | Nenhum alerta *Crítico* ou *Alto* sem a devida correção ou mitigação documentada. |
| **Deploy e Operação** | Monitoramento de tentativas de *IDOR* (CA02) e ataques de *Flooding* (CA04). | *Cloud Audit Logs* / Alertas Customizados | Dashboards de tráfego e logs de autenticação. | Resposta rápida a anomalias conforme roteiro da Etapa 6. |

---

## 4. Quality Gates e Condições Impeditivas

Para garantir que a integração contínua não introduza falhas, o pipeline do ThesisFlow possui **condições estritas de bloqueio**. O processo de automação deverá interromper e rejeitar o *Pull Request* nas seguintes situações:

1. **Vazamento de Segredos (Secrets Exposure):**
   - *Por quê:* Tokens, senhas de banco de dados e chaves do *Firebase* armazenadas no código-fonte comprometem instantaneamente o sistema.
   - *Comportamento:* A etapa inicial (Gitleaks) acusa o vazamento e bloqueia o build, forçando o desenvolvedor a usar variáveis de ambiente.

2. **Falha nos Testes de Controle de Acesso (RBAC):**
   - *Por quê:* O aspecto `@authorize` foi definido na Etapa 4 para impedir que estudantes executem funções de coordenadores (CA06). 
   - *Comportamento:* Se os testes unitários falharem (indicando que a proteção foi burlada ou desativada acidentalmente), a esteira falha.

3. **Verificação Dinâmica com Achados Críticos (DAST):**
   - *Por quê:* A Etapa 5 demonstrou a eficiência do ZAP para detectar configurações expostas (como CSP e CORS ausentes).
   - *Comportamento:* Se o ZAP retornar qualquer alerta mapeado como de Severidade Alta (*High*) que não seja um falso-positivo devidamente listado numa *whitelist*, o deploy é barrado.

4. **Ausência de Decoradores de Auditoria:**
   - *Por quê:* Como visto na ameaça de Repudiação (T05), endpoints sensíveis não podem existir sem logs.
   - *Comportamento:* A esteira roda uma checagem estática no repositório garantindo que toda função que altera o banco de dados (ex: `POST /activities`) esteja acompanhada do decorator `@audit`.

---

## 5. Considerações Finais do Pipeline

Com a elaboração deste Pipeline DevSecOps, fechamos o ciclo de engenharia de software seguro do ThesisFlow. O processo deixou de ser puramente reativo para se tornar **preventivo** e **automatizado**. As camadas de proteção (Prevenção e Detecção) descritas na Etapa 6, aliadas a essas verificações de CI/CD, fortalecem as funções de *Protect* e *Detect* propostas pelo framework NIST CSF 2.0, estabelecendo uma fundação sólida para a evolução da plataforma acadêmica.
