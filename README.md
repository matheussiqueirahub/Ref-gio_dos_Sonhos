# Refúgio dos Sonhos — Sistema de Reservas

[![GitHub](https://img.shields.io/badge/GitHub-Refugio__dos__Sonhos-181717?logo=github)](https://github.com/matheussiqueirahub/Refugio_dos_Sonhos)

Aplicativo de gerenciamento de reservas para um hotel boutique, com interface em Flet e modelo orientado a objetos em Python.

## Funcionalidades
- Cadastro e edição de clientes
- Catálogo de quartos com disponibilidade
- Criação, modificação e cancelamento de reservas
- Persistência local em JSON
- Conceitos de POO: herança, polimorfismo, encapsulamento

## Requisitos
- Python 3.10+
- Dependências Python: ver `requirements.txt`

## Instalação
```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

## Execução
```bash
python app.py
```

## Estrutura
- `app.py`: app Flet
- `refugio/`: domínio e serviços
  - `models/`: classes de domínio (Pessoa, Cliente, Quarto, Reserva)
  - `gerenciador.py`: orquestra reservas/clientes/quartos
  - `storage.py`: persistência em JSON
- `data/`: arquivos JSON persistidos

## Roadmap
Consulte `ROADMAP.md` para melhorias sugeridas e próximos passos.

## Observações
- Dados são salvos automaticamente ao criar/editar/cancelar.
- Datas no formato `DD/MM/AAAA` no UI.
- Projeto educativo; sem concorrência/lock de arquivo.

## Issues
- Abrir issue de roadmap (pré-preenchido):
  https://github.com/matheussiqueirahub/Refugio_dos_Sonhos/issues/new?title=Roadmap%20-%20Ref%C3%BAgio%20dos%20Sonhos&body=Consulte%20o%20arquivo%20%60Refugio_dos_Sonhos/ROADMAP.md%60%20no%20reposit%C3%B3rio%20para%20a%20lista%20completa%20de%20tarefas%20e%20prioridades.
- Reportar bug: https://github.com/matheussiqueirahub/Refugio_dos_Sonhos/issues/new?template=bug_report.yml
- Sugerir feature: https://github.com/matheussiqueirahub/Refugio_dos_Sonhos/issues/new?template=feature_request.yml
