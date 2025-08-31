# Refúgio dos Sonhos — Sistema de Reservas

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

## Observações
- Dados são salvos automaticamente ao criar/editar/cancelar.
- Datas no formato `DD/MM/AAAA` no UI.
- Projeto educativo; sem concorrência/lock de arquivo.
