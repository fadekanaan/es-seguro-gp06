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
- erros ou exceções relacionados aos mecanismos de autenticação e autorização.

Para que esses registros sejam úteis na detecção de comportamentos suspeitos, cada evento deve conter informações suficientes para sua análise, como data e horário, usuário ou origem da requisição, recurso acessado, ação solicitada e resultado da operação.

Esses eventos servirão como fonte de dados para as regras de detecção definidas na próxima seção.

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

## 5. Fluxo de resposta após um alerta

A geração de um alerta representa o início do processo de resposta e não significa, por si só, que um incidente de segurança foi confirmado. O evento deve ser analisado para determinar sua causa, gravidade e possíveis impactos.

Para o ThesisFlow, é proposto o seguinte fluxo de resposta:

1. **Detecção:** uma das regras de monitoramento identifica um comportamento que atende às condições definidas para geração de alerta.

2. **Registro:** o sistema registra as informações disponíveis sobre o evento, incluindo data e horário, usuário ou origem da requisição, recurso envolvido, ação solicitada e resultado da operação.

3. **Triagem:** o alerta é analisado para verificar se representa um comportamento legítimo, erro operacional ou possível tentativa de ataque.

4. **Contenção:** caso a atividade seja considerada suspeita, podem ser adotadas medidas temporárias para limitar sua continuidade, como restrição de requisições, encerramento de sessão ou bloqueio temporário do usuário.

5. **Análise:** são avaliados os registros relacionados ao evento para identificar sua origem, extensão e possíveis recursos afetados.

6. **Correção:** quando necessário, são aplicadas medidas para corrigir a causa do incidente ou reduzir a possibilidade de novas ocorrências.

7. **Encerramento e registro da ocorrência:** após o tratamento, o incidente deve ser documentado, incluindo o que ocorreu, quais medidas foram tomadas e quais melhorias podem ser incorporadas ao sistema.

Caso a análise indique exposição ou comprometimento de dados pessoais, a equipe responsável deverá avaliar também as medidas adicionais previstas pelas políticas institucionais e pela legislação aplicável.

O fluxo pode ser representado de forma resumida como:

```text
Evento suspeito
      ↓
Regra de detecção
      ↓
Geração e registro do alerta
      ↓
Triagem
      ↓
Contenção
      ↓
Análise
      ↓
Correção
      ↓
Registro da ocorrência
```

## 6. Considerações finais

O roteiro de detecção proposto complementa os mecanismos preventivos definidos nas etapas anteriores do trabalho. Enquanto controles como autenticação, autorização e limitação de requisições buscam impedir determinadas ações, o monitoramento permite identificar tentativas de exploração e comportamentos anormais que mereçam investigação.

As regras D01, D02 e D03 foram associadas aos riscos R07, R09 e R11 e estabelecem fontes de dados, condições objetivas para geração de alertas e respostas iniciais para cada cenário.

A proposta não pressupõe a implementação de um IDS completo no ThesisFlow. Seu objetivo é definir quais informações deveriam ser registradas e como esses registros poderiam ser utilizados para apoiar a identificação e o tratamento de possíveis incidentes de segurança.
