# Etapa 7 — Roteiro Estruturado do Vídeo Final e Apresentação

## 1. Instruções e Link do Vídeo Gravado

> 🎬 **Link do Vídeo Final no YouTube:** [https://www.youtube.com/watch?v=q2SbaZeJSAw](https://www.youtube.com/watch?v=q2SbaZeJSAw)

Para atender aos critérios de avaliação da disciplina, este roteiro serviu como guia para a gravação da apresentação em vídeo do grupo (duração preferencial entre **5 e 8 minutos**, estimada em ~6:30).

- **Total de Integrantes:** 6 membros (Marcus Vinicius, Bernardo, Gustavo, Fade, Rodrigo e Artur).
- **Distribuição de Conteúdo:** 12 slides no total, alocando **exatamente 2 slides por integrante** (~35 segundos de fala por slide).
- **Divisão das Falas:**
  - **Marcus Vinicius Morini Querol Junior:** Slide 01 (Introdução) e Slide 02 (O Sistema Escolhido)
  - **Bernardo Gomes Dorneles:** Slide 03 (Principais Ameaças & Casos de Abuso) e Slide 04 (Riscos Prioritários & NIST CSF 2.0)
  - **Gustavo Fernandes dos Anjos:** Slide 05 (Decisões de Arquitetura Segura) e Slide 06 (Práticas de Código Seguro & Testes)
  - **Fade Hassan Husein Kanaan:** Slide 07 (Principais Resultados da Verificação) e Slide 08 (Regras de Detecção & Monitoramento)
  - **Rodrigo Thoma da Silva:** Slide 09 (Pipeline DevSecOps Proposto) e Slide 10 (Evolução do Software na Disciplina)
  - **Artur Wahlbrink Kraemer:** Slide 11 (O Que o Grupo Aprendeu) e Slide 12 (Conclusão & Encerramento)

---

## 2. Estrutura Resumida da Apresentação

| Slide | Título / Tema | Tópico do Enunciado | Apresentador | Tempo Estimado |
| :---: | :--- | :--- | :--- | :---: |
| **01** | **Introdução & Integrantes** | Apresentação do Grupo e Contexto | Marcus Vinicius | 0:00 - 0:35 |
| **02** | **O Sistema Escolhido: ThesisFlow** | O sistema escolhido | Marcus Vinicius | 0:35 - 1:10 |
| **03** | **Principais Ameaças & Casos de Abuso** | As principais ameaças e casos de abuso | Bernardo | 1:10 - 1:45 |
| **04** | **Riscos Prioritários & NIST CSF 2.0** | Os riscos prioritários | Bernardo | 1:45 - 2:20 |
| **05** | **Decisões de Arquitetura Segura** | As decisões de arquitetura | Gustavo | 2:20 - 2:55 |
| **06** | **Práticas de Código Seguro & Testes** | As práticas de código seguro | Gustavo | 2:55 - 3:30 |
| **07** | **Principais Resultados da Verificação** | Os principais resultados da verificação | Fade | 3:30 - 4:05 |
| **08** | **Regras de Detecção & Monitoramento** | As regras de detecção | Fade | 4:05 - 4:40 |
| **09** | **Pipeline DevSecOps Proposto** | O pipeline DevSecOps proposto | Rodrigo | 4:40 - 5:15 |
| **10** | **Evolução do Software na Disciplina** | Evolução do software na disciplina | Rodrigo | 5:15 - 5:50 |
| **11** | **O Que o Grupo Aprendeu** | O que o grupo aprendeu | Artur | 5:50 - 6:25 |
| **12** | **Conclusão & Agradecimentos** | Encerramento e repositório | Artur | 6:25 - 7:00 |

---

## 3. Roteiro e Norteamento de Apresentação (Slide a Slide)

---

### Slide 01: Introdução & Integrantes
- **Tempo Estimado:** 0:00 - 0:35 (35s)
- **Apresentador:** Marcus Vinicius Morini Querol Junior
- **Recurso Visual na Tela:** Slide com o título do trabalho, logo UNIPAMPA e nome dos 6 integrantes do Grupo 06.
- **Norteamento da Fala / Pontos-Chave:**
  - Cumprimentar a audiência e apresentar formalmente os 6 integrantes do Grupo 06.
  - Introduzir o objetivo da apresentação: demonstrar a análise e implementação de segurança cibernética no sistema **ThesisFlow**.
  - Destacar que o trabalho cobriu da modelagem de ameaças e gestão de riscos até a arquitetura segura, testes automatizados e pipeline DevSecOps.

---

### Slide 02: O Sistema Escolhido: ThesisFlow
- **Tempo Estimado:** 0:35 - 1:10 (35s)
- **Apresentador:** Marcus Vinicius Morini Querol Junior
- **Recurso Visual na Tela:** Visão geral do ThesisFlow (Acompanhamento acadêmico de pós-graduação em 24 meses) e seus 3 perfis de usuário (Estudantes, Orientadores e Coordenadores).
- **Norteamento da Fala / Pontos-Chave:**
  - Explicar a finalidade do ThesisFlow na gestão de prazos, atividades creditáveis e plano de trabalho acadêmico.
  - Apresentar os 3 perfis de acesso e a dinâmica entre eles.
  - Justificar a escolha: sistema real e autoral que manipula dados pessoais sensíveis (LGPD) e documentos oficiais que requerem validação e proteção.

---

### Slide 03: Principais Ameaças e Casos de Abuso (Etapa 1)
- **Tempo Estimado:** 1:10 - 1:45 (35s)
- **Apresentador:** Bernardo Gomes Dorneles
- **Recurso Visual na Tela:** Matriz STRIDE e cartões destacando o Caso de Abuso de IDOR e Upload Forjado.
- **Norteamento da Fala / Pontos-Chave:**
  - Mencionar a aplicação da metodologia STRIDE para mapear 12 ameaças ao longo da API.
  - Destacar os 2 casos de abuso mais relevantes:
    1. **IDOR (Information Disclosure):** tentativa de alteração de parâmetros REST por estudantes para espionar dados confidenciais de outros colegas.
    2. **Forja de Upload (Tampering):** submissão de arquivos binários maliciosos ou renomeados para forjar créditos acadêmicos.

---

### Slide 04: Riscos Prioritários & NIST CSF 2.0 (Etapa 2)
- **Tempo Estimado:** 1:45 - 2:20 (35s)
- **Apresentador:** Bernardo Gomes Dorneles
- **Recurso Visual na Tela:** Matriz de Probabilidade vs Impacto e controles mapeados para as funções do NIST CSF 2.0 (Protect, Detect, Respond).
- **Norteamento da Fala / Pontos-Chave:**
  - Apresentar o processo de classificação de riscos com base no impacto e na probabilidade.
  - Destacar os riscos Críticos e Altos priorizados (R07 IDOR, R08 alteração não autorizada de status e R03 upload malicioso).
  - Explicar as medidas tomadas sob as funções Protect (controle de acesso estrito no backend), Detect (auditoria) e Respond.

---

### Slide 05: Decisões de Arquitetura Segura (Etapa 3)
- **Tempo Estimado:** 2:20 - 2:55 (35s)
- **Apresentador:** Gustavo Fernandes dos Anjos
- **Recurso Visual na Tela:** Diagrama de Arquitetura Segura exibindo a barreira de autenticação JWT e o middleware RBAC.
- **Norteamento da Fala / Pontos-Chave:**
  - Explicar a estratégia de Defesa em Profundidade adotada na solução.
  - Reforçar a premissa de não confiar no frontend e colocar toda a inteligência de autorização no servidor.
  - Detalhar a validação de tokens JWT do Firebase Auth combinada com regras RBAC (`@exige_perfil`) em cada *endpoint*.

---

### Slide 06: Práticas de Código Seguro & Testes (Etapa 4)
- **Tempo Estimado:** 2:55 - 3:30 (35s)
- **Apresentador:** Gustavo Fernandes dos Anjos
- **Recurso Visual na Tela:** Trechos de código Python (decorador RBAC, verificação de Magic Bytes) e execução da suíte no Pytest.
- **Norteamento da Fala / Pontos-Chave:**
  - Explicar a codificação em Python das diretrizes OWASP e CWE (validação de extensões, sanitização e Magic Bytes).
  - Enfatizar a postura *Security-First*, onde os testes de segurança no Pytest foram escritos antes da finalização do código.
  - Destacar a aprovação de 100% dos cenários de teste validando respostas HTTP 403 e 400 em invasões simuladas.

---

### Slide 07: Principais Resultados da Verificação (Etapa 5)
- **Tempo Estimado:** 3:30 - 4:05 (35s)
- **Apresentador:** Fade Hassan Husein Kanaan
- **Recurso Visual na Tela:** Relatório do escaneamento OWASP ZAP (DAST), achados de CORS/CSP e ações corretivas.
- **Norteamento da Fala / Pontos-Chave:**
  - Apresentar os resultados da análise dinâmica (DAST) realizada com o OWASP ZAP contra a API.
  - Comentar os alertas identificados: CORS permissivo em homologação e ausência de cabeçalhos rígidos (CSP, HSTS, X-Content-Type-Options).
  - Explicar o processo de triagem de falsos positivos e as correções aplicadas para restringir a origem de requisições e injetar os headers recomendados.

---

### Slide 08: Regras de Detecção & Monitoramento (Etapa 6)
- **Tempo Estimado:** 4:05 - 4:40 (35s)
- **Apresentador:** Fade Hassan Husein Kanaan
- **Recurso Visual na Tela:** Esquema das regras automatizadas D01 e D02 e formato da trilha de auditoria em JSON.
- **Norteamento da Fala / Pontos-Chave:**
  - Explicar o papel do monitoramento contínuo para complementar as medidas preventivas.
  - Apresentar a Regra D01 (alerta para tentativas repetidas de abuso de IDOR) e a Regra D02 (detecção de anomalias por flooding por IP).
  - Destacar a trilha de auditoria estruturada em JSON (timestamp, UID, IP, endpoint e status) para rápidas respostas a incidentes.

---

### Slide 09: Pipeline DevSecOps Proposto (Etapa 7)
- **Tempo Estimado:** 4:40 - 5:15 (35s)
- **Apresentador:** Rodrigo Thoma da Silva
- **Recurso Visual na Tela:** Diagrama da esteira CI/CD no GitHub Actions exibindo os 4 Quality Gates.
- **Norteamento da Fala / Pontos-Chave:**
  - Apresentar a automação da esteira de integração e entrega contínua (CI/CD) no GitHub Actions.
  - Explicar o funcionamento dos 4 Quality Gates: Secret Scanning (Gitleaks), SAST (Bandit), Testes Unitários/RBAC (Pytest) e DAST (OWASP ZAP).
  - Ressaltar que falhas de segurança bloqueiam automaticamente a aprovação de Pull Requests.

---

### Slide 10: Evolução do Software na Disciplina
- **Tempo Estimado:** 5:15 - 5:50 (35s)
- **Apresentador:** Rodrigo Thoma da Silva
- **Recurso Visual na Tela:** Linha do tempo do ThesisFlow comparando o estado inicial (MVP vulnerável) com o estado final (DevSecOps).
- **Norteamento da Fala / Pontos-Chave:**
  - Fazer um balanço da evolução técnica do ThesisFlow desde a Etapa 1 até a Etapa 7.
  - Contrastar as fragilidades do MVP inicial com a robustez atual (RBAC no backend, sanitização, testes de invasão e auditoria).
  - Destacar o aumento da maturidade de software do grupo durante a disciplina.

---

### Slide 11: O Que o Grupo Aprendeu
- **Tempo Estimado:** 5:50 - 6:25 (35s)
- **Apresentador:** Artur Wahlbrink Kraemer
- **Recurso Visual na Tela:** Pilares de aprendizado: Shift-Left Security, Segurança por Design e DevSecOps na Prática.
- **Norteamento da Fala / Pontos-Chave:**
  - Enfatizar a relevância prática do conceito de *Shift-Left Security* (tratar segurança no início economiza tempo e esforço).
  - Abordar o aprendizado sobre projetar arquiteturas seguras por design e automatizar a verificação sem engessar a equipe de desenvolvimento.
  - Resumir a importância do monitoramento e da resposta ativa a incidentes.

---

### Slide 12: Conclusão & Encerramento
- **Tempo Estimado:** 6:25 - 7:00 (35s)
- **Apresentador:** Artur Wahlbrink Kraemer
- **Recurso Visual na Tela:** Slide final de encerramento com o link do repositório GitHub e mensagem de agradecimento.
- **Norteamento da Fala / Pontos-Chave:**
  - Concluir a apresentação ressaltando que o ThesisFlow atinge um nível de maturidade pronto para produção.
  - Informar que todo o material (códigos, diagramas, suítes de testes e relatórios ZAP) encontra-se versionado no GitHub.
  - Finalizar com agradecimentos à professora e aos colegas.