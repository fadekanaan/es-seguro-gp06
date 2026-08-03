# Etapa 1 — Seção 5: Casos de Abuso

## 6. Casos de abuso

### Diagrama de Casos de Abuso

![Diagrama de Casos de Abuso](../../diagramas/diagrama-casos-de-abuso.png)

---

### CA01 — Forja de comprovante para validação indevida de créditos

**Identificador:** CA01

**Ator malicioso:** Estudante mal-intencionado.

**Objetivo do abuso:** Obter validação de créditos por meio de um comprovante falso ou de um documento legítimo de outra pessoa.

**Condições necessárias:**
- O sistema aceita upload de arquivos sem verificar o conteúdo ou autenticidade do documento.
- A URL de acesso ao arquivo no Firebase Storage não possui controle de imutabilidade após o upload.
- O orientador não possui mecanismo de verificação adicional além da visualização do arquivo.

**Sequência de ações:**
1. O estudante registra uma atividade creditável no sistema com dados corretos (tipo, descrição, data).
2. O estudante faz upload de um comprovante que pode ser falso (documento adulterado) ou de terceiro (comprovante roubado ou copiado).
3. O sistema aceita o arquivo e associa a URL ao registro da atividade.
4. O orientador recebe notificação e visualiza o arquivo — que aparenta ser legítimo.
5. O orientador valida a atividade sem perceber a fraude.
6. O sistema registra os créditos como válidos na conta do estudante.

**Impacto esperado:** O estudante obtém créditos acadêmicos sem ter realizado a atividade correspondente, o que compromete a integridade do programa e pode permitir que ele avance para a defesa sem cumprir os requisitos reais.

**Categorias STRIDE relacionadas:** Tampering, Repudiation.

---

### CA02 — Acesso indevido a dados de outro estudante via IDOR

**Identificador:** CA02

**Ator malicioso:** Estudante autenticado no sistema.

**Objetivo do abuso:** Acessar informações privadas de outros estudantes — plano de trabalho, status acadêmico, produções registradas — sem autorização.

**Condições necessárias:**
- A API não verifica se o recurso solicitado pertence ao usuário autenticado.
- Os identificadores de recursos (IDs de estudante, IDs de atividade) são sequenciais ou previsíveis.
- A resposta da API retorna o objeto completo sem filtragem por proprietário.

**Sequência de ações:**
1. O estudante autentica-se normalmente com suas próprias credenciais.
2. O estudante acessa um recurso próprio e observa o identificador utilizado na URL ou no corpo da requisição (ex.: `GET /students/{student_id}/activities`).
3. O estudante modifica o identificador na requisição (ex.: incrementa o valor ou testa outros IDs).
4. A API processa a requisição sem verificar se o `student_id` pertence ao usuário autenticado.
5. O sistema retorna os dados do estudante correspondente ao ID modificado.
6. O estudante repete a operação sistematicamente, coletando dados de múltiplos estudantes.

**Impacto esperado:** Exposição de dados pessoais e acadêmicos de terceiros, violação de privacidade com implicações legais (LGPD), e possível uso das informações para fraudes ou pressão sobre outros estudantes.

**Categorias STRIDE relacionadas:** Information Disclosure.

---

### CA03 — Cadastro de falso orientador para obter acesso a dados de estudantes

**Identificador:** CA03

**Ator malicioso:** Atacante externo que deseja se passar por orientador.

**Objetivo do abuso:** Obter o papel de orientador no sistema para acessar dados privados de estudantes e potencialmente validar atividades ou influenciar o progresso acadêmico de outros usuários.

**Condições necessárias:**
- O sistema permite cadastro de orientadores sem validar o vínculo real com a instituição.
- O processo de criação de conta de orientador não exige confirmação por parte de um coordenador.
- O atacante conhece o domínio de e-mail utilizado por professores da instituição ou consegue criar um e-mail similar.

**Sequência de ações:**
1. O atacante cria uma conta no Firebase Authentication com um e-mail plausível (ex.: com domínio institucional ou similar).
2. O atacante registra-se no sistema como orientador, informando dados falsos de nome e vínculo.
3. O sistema aceita o cadastro sem verificação adicional.
4. O atacante é associado a um ou mais estudantes como orientador.
5. O atacante passa a ter acesso aos dados pessoais, plano de trabalho e comprovantes dos estudantes orientados.
6. O atacante pode validar atividades indevidamente ou coletar dados para outros fins.

**Impacto esperado:** Exposição de dados pessoais de estudantes, comprometimento da confidencialidade de documentos acadêmicos, validações fraudulentas e perda de confiança no sistema.

**Categorias STRIDE relacionadas:** Spoofing, Information Disclosure, Elevation of Privilege.

---

### CA04 — Ataque de flooding ao motor de inferência durante período crítico

**Identificador:** CA04

**Ator malicioso:** Atacante externo com acesso autenticado ou com credenciais comprometidas.

**Objetivo do abuso:** Tornar o sistema indisponível durante um período crítico do calendário acadêmico (ex.: período de qualificações, defesas ou entrega de relatórios semestrais).

**Condições necessárias:**
- O sistema não possui limitação de taxa de requisições (rate limiting) nos endpoints da API.
- O motor de inferência lógica realiza operações computacionalmente intensas a cada invocação.
- Não há mecanismo de cache para resultados já calculados recentemente.

**Sequência de ações:**
1. O atacante autentica-se no sistema (com credenciais próprias ou roubadas).
2. O atacante identifica os endpoints que invocam o motor lógico (ex.: `GET /students/{id}/status`, `GET /students/{id}/eligibility`).
3. O atacante escreve um script que envia requisições em alta frequência para esses endpoints.
4. O motor de inferência é invocado repetidamente, consumindo CPU e memória do servidor.
5. O sistema começa a responder com lentidão ou erros para todos os usuários.
6. Estudantes e orientadores não conseguem acessar o sistema durante o período crítico.

**Impacto esperado:** Indisponibilidade do sistema, perda de prazos acadêmicos por parte de estudantes legítimos, aumento de carga administrativa e possível prejuízo ao calendário do programa.

**Categorias STRIDE relacionadas:** Denial of Service.

---

### CA05 — Orientador nega ter aprovado validação de crédito

**Identificador:** CA05

**Ator malicioso:** Orientador desonesto ou com interesses conflitantes.

**Objetivo do abuso:** Negar a responsabilidade por uma validação de crédito já realizada, seja para prejudicar o estudante, para encobrir um erro próprio ou para evitar consequências de uma aprovação indevida.

**Condições necessárias:**
- O aspecto `@audit` pode ser desabilitado via flag de configuração (`ASPECTS_ENABLED["audit"] = False`).
- Os logs de auditoria não são imutáveis ou podem ser alterados por quem tem acesso ao banco de dados.
- Não há assinatura digital ou mecanismo criptográfico que vincule a validação ao orientador.

**Sequência de ações:**
1. O orientador valida a atividade de um estudante no sistema.
2. O sistema registra a operação via `@audit`, associando-a ao token JWT do orientador.
3. Posteriormente, o orientador afirma não ter realizado a validação (negação).
4. Se os logs forem incompletos, alteráveis ou não incluírem identificação suficiente do usuário, não há prova da ação.
5. A contestação não pode ser resolvida, e o estudante pode ter seus créditos contestados ou cancelados.

**Impacto esperado:** Prejuízo acadêmico direto ao estudante, impossibilidade de responsabilização do orientador, comprometimento da credibilidade do sistema e necessidade de processos administrativos para resolução da disputa.

**Categorias STRIDE relacionadas:** Repudiation.

---

### CA06 — Estudante eleva seus próprios privilégios para coordenador

**Identificador:** CA06

**Ator malicioso:** Estudante com conhecimento técnico sobre APIs REST.

**Objetivo do abuso:** Contornar o controle de acesso baseado em papel (RBAC) para acessar funcionalidades restritas a coordenadores, como criação de tipos de atividades, aprovação de extensões ou acesso a relatórios gerenciais.

**Condições necessárias:**
- Existe um endpoint administrativo sem o decorator `@authorize(role="coordinator")` ou com verificação insuficiente.
- O estudante consegue descobrir a URL de um endpoint restrito (via exploração da documentação da API, erros expostos ou ferramentas de análise de tráfego).
- O sistema depende apenas do papel registrado no token JWT, mas não verifica consistência no servidor.

**Sequência de ações:**
1. O estudante autentica-se normalmente.
2. O estudante explora a API em busca de endpoints não protegidos (ex.: usando a documentação Swagger em `/docs`, disponível em ambiente de desenvolvimento).
3. O estudante identifica o endpoint `POST /activity-types` ou similar.
4. O estudante envia uma requisição com seu token JWT válido de estudante para o endpoint restrito.
5. Se a verificação for ausente ou falha, o sistema processa a requisição.
6. O estudante cria ou altera configurações do sistema, afetando outros usuários.

**Impacto esperado:** Alteração de configurações do programa, criação de tipos de atividades falsas que permitem validações indevidas, comprometimento da integridade do sistema e exposição de dados de outros usuários.

**Categorias STRIDE relacionadas:** Elevation of Privilege, Tampering.
