# Etapa 6 — Monitoramento e Detecção de Intrusões

## 1. Introdução

A prevenção de incidentes de segurança busca reduzir a possibilidade de que ameaças identificadas sejam exploradas. Entretanto, mesmo com controles preventivos, não é possível garantir que todas as tentativas de ataque serão impedidas. Por esse motivo, o monitoramento e a detecção de comportamentos suspeitos são componentes importantes da segurança do sistema.

Nesta etapa é definido um roteiro de detecção de intrusões para o ThesisFlow, tomando como referência os riscos identificados e priorizados nas etapas anteriores do trabalho. O objetivo não é implementar um sistema de detecção de intrusões (IDS), mas estabelecer quais eventos devem ser observados, quais comportamentos podem indicar uma tentativa de ataque e quais ações iniciais devem ser tomadas quando um alerta for gerado.

## 2. Prevenção e detecção de intrusões

Prevenção e detecção atuam de forma complementar.

Os mecanismos de **prevenção** têm como objetivo impedir que uma ação indevida seja concluída. Controles de autenticação, autorização, validação de entradas e limitação de requisições são exemplos de medidas preventivas.

A **detecção**, por outro lado, busca identificar comportamentos suspeitos ou tentativas de violação que estejam ocorrendo ou que já tenham ocorrido. Para isso, o sistema deve registrar eventos relevantes e permitir que determinados padrões de comportamento sejam reconhecidos.

Por exemplo, uma tentativa de acessar uma funcionalidade sem a permissão necessária pode ser bloqueada pelo mecanismo de autorização. Mesmo que o acesso seja impedido, a tentativa deve ser registrada, pois várias ocorrências semelhantes em um curto período podem indicar uma tentativa deliberada de exploração.

Dessa forma, impedir uma ação maliciosa não elimina a necessidade de monitorá-la. Os registros produzidos pelo sistema podem auxiliar na identificação de ataques, na investigação de incidentes e na definição de respostas adequadas.

## 3. Eventos que devem ser monitorados no ThesisFlow

Considerando os riscos levantados anteriormente para o ThesisFlow, alguns eventos possuem maior relevância para o monitoramento de segurança.

Devem ser registrados, sempre que possível:

- tentativas de autenticação malsucedidas;
- tentativas de acesso a recursos sem autorização;
- tentativas de um usuário acessar informações pertencentes a outro usuário;
- tentativas de execução de operações incompatíveis com o papel atribuído ao usuário;
- aumento anormal no número de requisições realizadas por um mesmo usuário ou origem;
- bloqueios realizados por mecanismos de autorização ou limitação de requisições;
- alterações administrativas ou operações sensíveis realizadas no sistema;

## 4. Regras de detecção

A partir dos riscos identificados nas etapas anteriores, foram definidas três regras de detecção para comportamentos considerados relevantes no contexto do ThesisFlow.

As regras não substituem os controles preventivos já definidos. Seu objetivo é permitir que tentativas de exploração, mesmo quando bloqueadas, sejam registradas e tratadas como possíveis eventos de segurança.

### 4.1 D01 — Tentativas de acesso indevido a recursos de outro estudante

**Risco relacionado:** R07 — acesso indevido a dados de outro estudante.

**Fonte de dados:** registros de autenticação, autorização e auditoria das requisições realizadas ao sistema.

**Condição de alerta:** mais de três tentativas, dentro de um intervalo de cinco minutos, nas quais um estudante autenticado tente acessar um recurso associado a outro estudante.

**Resposta inicial:** negar a operação, registrar as tentativas e gerar um alerta para análise. Caso o comportamento continue, a sessão ou o usuário poderá ser temporariamente restringido até que a ocorrência seja verificada.

### 4.2 D02 — Volume anormal de requisições

**Risco relacionado:** R09 — indisponibilidade causada por flooding de requisições.

**Fonte de dados:** registros das requisições HTTP e dos mecanismos de limitação de requisições do sistema.

**Condição de alerta:** mais de dez requisições, em um período de um minuto, realizadas pelo mesmo usuário ou origem contra uma funcionalidade sensível ou que demande maior processamento.

**Resposta inicial:** aplicar limitação temporária às requisições provenientes da origem identificada, registrar o evento e acompanhar a continuidade do comportamento.

### 4.3 D03 — Tentativa de elevação de privilégios

**Risco relacionado:** R11 — tentativa de execução de funcionalidades com privilégio superior ao autorizado.

**Fonte de dados:** registros de autenticação, autorização e auditoria das operações protegidas por perfil de acesso.

**Condição de alerta:** qualquer tentativa de um usuário com perfil de estudante ou orientador executar uma operação restrita ao perfil de coordenador.

**Resposta inicial:** negar imediatamente a operação, registrar o usuário, recurso e ação solicitada e gerar um alerta para investigação. Ocorrências repetidas devem ser tratadas como comportamento suspeito e podem justificar o encerramento preventivo da sessão.
- erros ou exceções relacionados aos mecanismos de autenticação e autorização.

Para que esses registros sejam úteis na detecção de comportamentos suspeitos, cada evento deve conter informações suficientes para sua análise, como data e horário, usuário ou origem da requisição, recurso acessado, ação solicitada e resultado da operação.

Esses eventos servirão como fonte de dados para as regras de detecção definidas na próxima seção.
