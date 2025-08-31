# Roadmap — Refúgio dos Sonhos

Este issue/roadmap descreve próximos passos e melhorias sugeridas para o sistema.

## Funcionais
- [ ] Modificar reserva (UI): editar datas de uma reserva ativa, respeitando disponibilidade.
- [ ] Cálculo de valor total da reserva (diárias x preço do quarto) e exibição no UI.
- [ ] Regras de datas: explicitar política de intervalo (check-in incluso, check-out exclusivo), validar datas passadas.
- [ ] Bloquear remoção de cliente com reservas futuras (não só ativas atualmente).
- [ ] CRUD de quartos no UI (adicionar/editar/remover preço/tipo), com validação de reservas existentes ao remover.
- [ ] Busca e ordenação nas tabelas (clientes, quartos, reservas).
- [ ] Cancelamento com motivo e registro do timestamp de cancelamento.
- [ ] Exportar comprovante/recibo (PDF) da reserva (opcional).

## Técnicos
- [ ] Internacionalização de moeda/data (pt-BR), formatação consistente.
- [ ] Persistência alternativa opcional via SQLite (ex.: SQLModel/SQLAlchemy) mantendo a interface do gerenciador.
- [ ] Testes unitários do domínio (`gerenciador`, `utils.overlaps`, serialização dos modelos).
- [ ] Workflow CI (GitHub Actions) para lint/format/test (flake8/ruff + black + pytest).
- [ ] Logging estruturado no `gerenciador` (níveis INFO/WARN/ERROR) e tratamento de exceções no UI.

## UX/UI
- [ ] Indicar claramente disponibilidade por período (visual) ao escolher datas.
- [ ] Feedbacks e mensagens de erro/sucesso consistentes (snackbars), com acessibilidade.
- [ ] Confirmação antes de ações destrutivas (remover cliente, cancelar reserva).

## Observações
- Qualquer alteração que mude o formato dos dados deve prever migração dos JSON (ou instruções de limpeza da pasta `data/`).
- Manter o foco educativo e o código simples; evitar overengineering.
