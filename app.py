from refugio.gerenciador import GerenciadorDeReservas
from refugio.models.quarto import TipoQuarto
from refugio.utils import parse_date, format_date
import flet as ft


def main(page: ft.Page):
    page.title = "Refúgio dos Sonhos - Reservas"
    page.window_width = 1100
    page.window_height = 720
    page.theme_mode = ft.ThemeMode.LIGHT

    manager = GerenciadorDeReservas()

    # ---------- Helpers de UI ----------
    def snackbar(msg: str, error: bool = False):
        page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=ft.colors.RED_200 if error else ft.colors.GREEN_200)
        page.snack_bar.open = True
        page.update()

    # ---------- Aba: Quartos ----------
    quartos_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Número")),
            ft.DataColumn(ft.Text("Tipo")),
            ft.DataColumn(ft.Text("Preço/diária")),
            ft.DataColumn(ft.Text("Disponível")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=[],
    )

    def refresh_quartos():
        quartos_table.rows = []
        for q in manager.listar_quartos():
            disponivel = "Sim" if manager.quarto_disponivel(q.numero) else "Ocupado"

            def make_btn(quarto_num):
                return ft.ElevatedButton(
                    "Reservar",
                    on_click=lambda e: open_reserva_form(quarto_num),
                    disabled=(disponivel != "Sim"),
                )

            quartos_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(q.numero))),
                        ft.DataCell(ft.Text(q.tipo.value)),
                        ft.DataCell(ft.Text(f"R$ {q.preco_diaria:.2f}")),
                        ft.DataCell(ft.Text(disponivel)),
                        ft.DataCell(make_btn(q.numero)),
                    ]
                )
            )
        page.update()

    quartos_view = ft.Column([
        ft.Row([ft.Text("Quartos", style=ft.TextThemeStyle.HEADLINE_MEDIUM)]),
        quartos_table,
    ], expand=True)

    # ---------- Aba: Clientes ----------
    clientes_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Telefone")),
            ft.DataColumn(ft.Text("E-mail")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=[],
    )

    nome_input = ft.TextField(label="Nome", width=260)
    telefone_input = ft.TextField(label="Telefone", width=180)
    email_input = ft.TextField(label="E-mail", width=260)
    cliente_editing_id: str | None = None

    def limpar_form_cliente():
        nonlocal cliente_editing_id
        cliente_editing_id = None
        nome_input.value = ""
        telefone_input.value = ""
        email_input.value = ""
        page.update()

    def carregar_form_cliente(cid: str):
        nonlocal cliente_editing_id
        c = manager.obter_cliente(cid)
        if not c:
            snackbar("Cliente não encontrado", True)
            return
        cliente_editing_id = cid
        nome_input.value = c.nome
        telefone_input.value = c.telefone
        email_input.value = c.email
        page.update()

    def salvar_cliente(e=None):
        nome = (nome_input.value or "").strip()
        tel = (telefone_input.value or "").strip()
        em = (email_input.value or "").strip()
        if not nome:
            snackbar("Nome é obrigatório", True)
            return
        if cliente_editing_id:
            manager.editar_cliente(cliente_editing_id, nome=nome, telefone=tel, email=em)
            snackbar("Cliente atualizado")
        else:
            manager.adicionar_cliente(nome=nome, telefone=tel, email=em)
            snackbar("Cliente adicionado")
        limpar_form_cliente()
        refresh_clientes()

    def remover_cliente(cid: str):
        # Permite remover apenas se não há reservas ativas do cliente
        if any(r.cliente_id == cid and r.ativa for r in manager.listar_reservas()):
            snackbar("Cliente possui reservas ativas", True)
            return
        manager.remover_cliente(cid)
        snackbar("Cliente removido")
        refresh_clientes()

    def make_actions_clientes(cid: str):
        return ft.Row([
            ft.IconButton(ft.icons.EDIT, tooltip="Editar", on_click=lambda e: carregar_form_cliente(cid)),
            ft.IconButton(ft.icons.DELETE, tooltip="Remover", on_click=lambda e: remover_cliente(cid)),
        ])

    def refresh_clientes():
        clientes_table.rows = []
        for c in manager.listar_clientes():
            clientes_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(c.id)),
                    ft.DataCell(ft.Text(c.nome)),
                    ft.DataCell(ft.Text(c.telefone or "-")),
                    ft.DataCell(ft.Text(c.email or "-")),
                    ft.DataCell(make_actions_clientes(c.id)),
                ])
            )
        page.update()

    clientes_view = ft.Column([
        ft.Row([ft.Text("Clientes", style=ft.TextThemeStyle.HEADLINE_MEDIUM)]),
        ft.Row([nome_input, telefone_input, email_input, ft.ElevatedButton("Salvar", on_click=salvar_cliente), ft.OutlinedButton("Limpar", on_click=lambda e: limpar_form_cliente())]),
        clientes_table,
    ], expand=True)

    # ---------- Aba: Reservas (lista) ----------
    reservas_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Cliente")),
            ft.DataColumn(ft.Text("Quarto")),
            ft.DataColumn(ft.Text("Check-in")),
            ft.DataColumn(ft.Text("Check-out")),
            ft.DataColumn(ft.Text("Status")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=[],
    )

    def cancelar_reserva(rid: str):
        ok = manager.cancelar_reserva(rid)
        if ok:
            snackbar("Reserva cancelada")
            refresh_reservas()
            refresh_quartos()
        else:
            snackbar("Reserva não encontrada", True)

    def make_actions_reservas(rid: str):
        return ft.Row([
            ft.IconButton(ft.icons.CANCEL, tooltip="Cancelar", on_click=lambda e: cancelar_reserva(rid))
        ])

    def refresh_reservas():
        reservas_table.rows = []
        for r in manager.listar_reservas():
            c = manager.obter_cliente(r.cliente_id)
            cliente_nome = c.nome if c else "-"
            reservas_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(r.id)),
                    ft.DataCell(ft.Text(cliente_nome)),
                    ft.DataCell(ft.Text(str(r.quarto_numero))),
                    ft.DataCell(ft.Text(format_date(r.checkin))),
                    ft.DataCell(ft.Text(format_date(r.checkout))),
                    ft.DataCell(ft.Text("Ativa" if r.ativa else "Cancelada")),
                    ft.DataCell(make_actions_reservas(r.id)),
                ])
            )
        page.update()

    reservas_view = ft.Column([
        ft.Row([ft.Text("Reservas", style=ft.TextThemeStyle.HEADLINE_MEDIUM)]),
        reservas_table,
    ], expand=True)

    # ---------- Aba: Nova Reserva (form) ----------
    drp_cliente = ft.Dropdown(label="Cliente", width=320, options=[])
    drp_quarto = ft.Dropdown(label="Quarto", width=180, options=[])
    drp_tipo = ft.Dropdown(
        label="Filtrar por tipo",
        width=180,
        options=[ft.dropdown.Option(t.value) for t in TipoQuarto],
    )
    in_checkin = ft.TextField(label="Check-in (DD/MM/AAAA)", width=180)
    in_checkout = ft.TextField(label="Check-out (DD/MM/AAAA)", width=180)

    def carregar_clientes_dropdown():
        drp_cliente.options = [ft.dropdown.Option(key=c.id, text=c.nome) for c in manager.listar_clientes()]
        page.update()

    def carregar_quartos_dropdown():
        # Filtra por tipo e disponibilidade se datas preenchidas
        tipo = drp_tipo.value
        ci = parse_date(in_checkin.value) if in_checkin.value else None
        co = parse_date(in_checkout.value) if in_checkout.value else None
        drp_quarto.options = []
        for q in manager.listar_quartos():
            if tipo and q.tipo.value != tipo:
                continue
            if ci and co:
                if not manager.verificar_disponibilidade(q.numero, ci, co):
                    continue
            drp_quarto.options.append(ft.dropdown.Option(str(q.numero)))
        page.update()

    def open_reserva_form(quarto_numero: int | None = None):
        tabs.selected_index = 1
        carregar_clientes_dropdown()
        if quarto_numero is not None:
            drp_quarto.value = str(quarto_numero)
        carregar_quartos_dropdown()
        page.update()

    def criar_reserva(e=None):
        if not drp_cliente.value:
            snackbar("Selecione um cliente", True)
            return
        if not drp_quarto.value:
            snackbar("Selecione um quarto", True)
            return
        try:
            ci = parse_date(in_checkin.value)
            co = parse_date(in_checkout.value)
        except ValueError:
            snackbar("Datas inválidas. Use DD/MM/AAAA", True)
            return
        num = int(drp_quarto.value)
        res = manager.criar_reserva(drp_cliente.value, num, ci, co)
        if res is None:
            snackbar("Quarto indisponível para o período", True)
            return
        snackbar("Reserva criada com sucesso")
        refresh_reservas()
        refresh_quartos()

    reserva_view = ft.Column([
        ft.Row([ft.Text("Nova Reserva", style=ft.TextThemeStyle.HEADLINE_MEDIUM)]),
        ft.Row([drp_cliente, drp_tipo, drp_quarto]),
        ft.Row([in_checkin, in_checkout, ft.ElevatedButton("Criar Reserva", on_click=criar_reserva)]),
        ft.Text("Dica: selecione as datas para filtrar quartos disponíveis."),
    ], expand=False)

    # Atualiza dropdowns quando campos mudarem
    drp_tipo.on_change = lambda e: carregar_quartos_dropdown()
    in_checkin.on_change = lambda e: carregar_quartos_dropdown()
    in_checkout.on_change = lambda e: carregar_quartos_dropdown()

    # ---------- Tabs ----------
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="Quartos", content=quartos_view),
            ft.Tab(text="Reserva", content=reserva_view),
            ft.Tab(text="Clientes", content=clientes_view),
            ft.Tab(text="Reservas", content=reservas_view),
        ],
        expand=1,
    )

    page.add(tabs)

    # Inicializa dados
    refresh_quartos()
    refresh_clientes()
    refresh_reservas()
    carregar_clientes_dropdown()
    carregar_quartos_dropdown()


if __name__ == "__main__":
    ft.app(target=main)

