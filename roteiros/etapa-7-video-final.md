# Etapa 7 — Roteiro do Vídeo Final

## 1. Instruções para Gravação

Para atender aos critérios de avaliação estipulados no enunciado (Duração de **5 a 8 minutos** e apresentação que reflita as decisões e aprendizados de todas as etapas), estruturamos o roteiro em **Partes**. 

A divisão por "Apresentadores" (Apresentador 1, 2, 3...) é ilustrativa. Como todos os 6 membros do Grupo 06 (Artur, Marcus, Bernardo, Gustavo, Fade e Rodrigo) precisam participar, a sugestão é que as partes mais longas sejam divididas, ou que cada um assuma um dos blocos lógicos. 

**Recomendações Visuais:**
- Utilize slides limpos que mostrem apenas as imagens chave (Diagramas STRIDE, Fluxos de Arquitetura, Capturas de Tela do ZAP).
- Não leiam os slides; usem o texto sugerido abaixo como guia para a fala.

---

## 2. Roteiro de Gravação Detalhado

### Parte 1: Introdução e Contexto
**Tempo Estimado:** 0:00 - 1:00 (1 minuto)
**Apresentador:** Apresentador 1
**Recurso Visual na Tela:** Slide de título com o nome "ThesisFlow", logotipos das tecnologias (React, FastAPI, Firebase) e os integrantes do grupo.

**Fala Sugerida:**
> "Olá a todos! Nós somos o Grupo 06 e vamos apresentar a jornada de segurança que aplicamos no sistema **ThesisFlow**. 
> O ThesisFlow é uma plataforma acadêmica desenvolvida por nós para acompanhar o progresso de estudantes de mestrado ao longo de seus 24 meses de curso. Escolhemos ele porque é um sistema real, que transaciona dados pessoais sensíveis, comprovantes documentais e envolve três perfis distintos de usuários: Estudantes, Orientadores e Coordenadores. 
> Nosso objetivo aqui é demonstrar como tiramos a segurança do papel e a aplicamos desde a modelagem até o pipeline DevSecOps, garantindo proteção contra vazamento de dados, alterações fraudulentas e abusos."

---

### Parte 2: Modelagem de Ameaças e Riscos (Etapas 1 e 2)
**Tempo Estimado:** 1:00 - 2:30 (1 minuto e meio)
**Apresentador:** Apresentador 2
**Recurso Visual na Tela:** Tabela resumo do STRIDE (mostrando IDOR, Falso Orientador e Forja de Comprovante) e matriz de probabilidade e impacto.

**Fala Sugerida:**
> "Na primeira etapa da disciplina, realizamos a Modelagem de Ameaças baseada na metodologia **STRIDE**. A ideia não era apenas teórica; mergulhamos no contexto do ThesisFlow para listar abusos reais. 
> Dois casos de abuso nos chamaram muito a atenção: o primeiro foi a possibilidade de um estudante explorar uma falha de **IDOR** (Information Disclosure) na API para listar dados confidenciais de outros estudantes da turma. O segundo, categorizado como **Tampering**, seria a substituição fraudulenta de um arquivo de upload para obter créditos de uma atividade acadêmica não realizada.
> Na Etapa 2, usamos as matrizes do **NIST CSF 2.0** para classificar essas ameaças. Riscos como o IDOR receberam nível **Crítico**, exigindo controles imediatos das funções 'Protect' e 'Detect' para impedir a quebra de privacidade prevista pela LGPD."

---

### Parte 3: Arquitetura Segura (Etapa 3)
**Tempo Estimado:** 2:30 - 3:30 (1 minuto)
**Apresentador:** Apresentador 3
**Recurso Visual na Tela:** Diagrama de Arquitetura Segura detalhando a barreira de Autenticação (Firebase Auth) e o Aspecto de Autorização.

**Fala Sugerida:**
> "Com os riscos na mesa, nós arquitetamos a defesa. Nossa principal decisão de arquitetura para barrar as ameaças de Elevação de Privilégios e IDOR foi centralizar a validação em decoradores de autorização no Backend. 
> *[Apontar para o slide]* Como vocês podem ver neste diagrama, qualquer requisição passa pela verificação do token JWT pelo Firebase e, imediatamente, cruza uma camada Role-Based Access Control (RBAC). 
> Dessa forma, garantimos um dos nossos principais requisitos de segurança: um estudante nunca conseguirá processar uma requisição restrita ao coordenador, pois o *endpoint* validará o papel no servidor antes de qualquer transação."

---

### Parte 4: Práticas de Código Seguro e Testes (Etapa 4)
**Tempo Estimado:** 3:30 - 4:45 (1 minuto e 15 segundos)
**Apresentador:** Apresentador 4
**Recurso Visual na Tela:** Captura de tela com os testes do Pytest rodando (`test_authorization.py` passando com 100% de sucesso).

**Fala Sugerida:**
> "A teoria precisava virar código. Focamos em duas práticas principais recomendadas pela OWASP. A primeira foi implementar de fato o decorador de autorização que citei na arquitetura, blindando nossos endpoints.
> A segunda foi a proteção contra a injeção de arquivos maliciosos, que era o nosso risco de forja de comprovantes. 
> E o mais importante: aplicamos testes automatizados de segurança usando **Pytest** *antes* de finalizar o código. Nós injetamos cenários maliciosos simulados no ambiente de testes, e comprovamos, como mostra a tela, que a nossa lógica barra ativamente os acessos indevidos e valida as extensões dos arquivos."

---

### Parte 5: Verificação e Monitoramento (Etapas 5 e 6)
**Tempo Estimado:** 4:45 - 6:00 (1 minuto e 15 segundos)
**Apresentador:** Apresentador 5
**Recurso Visual na Tela:** Print dos alertas (ex: CSP e CORS) encontrados no ZAP e o esquema de fluxo de Resposta a Incidentes.

**Fala Sugerida:**
> "Seguindo a esteira, usamos o **OWASP ZAP** para fazer uma varredura dinâmica (DAST) em nosso ambiente de testes. O ZAP levantou alguns alertas interessantes, como a configuração permissiva de CORS e a ausência de cabeçalhos rígidos de Content Security Policy (CSP). Nós analisamos criticamente esses achados e propusemos soluções graduais para fechar essas brechas sem quebrar a aplicação React.
> E para a operação, criamos regras rígidas de monitoramento. Caso um estudante tente abusar do sistema (por exemplo, forçando URLs de terceiros repetidamente), os logs de auditoria irão registrar, acionando a nossa contenção de incidentes."

---

### Parte 6: DevSecOps e Conclusão (Etapa 7)
**Tempo Estimado:** 6:00 - 7:00 (1 minuto)
**Apresentador:** Apresentador 6
**Recurso Visual na Tela:** Diagrama em blocos do Pipeline CI/CD (mostrando os Quality Gates).

**Fala Sugerida:**
> "Para garantir que essa proteção não se perca nas futuras atualizações do ThesisFlow, estruturamos nosso **Pipeline DevSecOps**. Ele possui *Quality Gates* severos: um *Pull Request* não é aprovado se houver credenciais vazadas no código, se o ZAP apontar novas vulnerabilidades críticas ou se os testes do Pytest falharem. A segurança agora bloqueia ativamente vulnerabilidades.
> **Para concluir:** Esta disciplina nos ensinou que a segurança não é um remendo que colocamos no final do software. Vimos na prática como modelar a ameaça antes de escrever a primeira linha de código poupa refatorações dolorosas e, principalmente, protege os dados dos usuários de ponta a ponta. Agradecemos a atenção de todos!"

---