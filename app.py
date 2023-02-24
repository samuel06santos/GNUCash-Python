import flet
from flet import Page, Column, Container, Text, TextField
from flet.plotly_chart import PlotlyChart
import plotly.graph_objects as go

import piecash as pc

def Pie(labels, values):
    labels:list[str] = labels
    values:list[int|float] = values
    return go.Figure(data=[go.Pie(labels= labels, values= values, textinfo='percent')])
    


def main(page: Page):
    page.title = "Gráficos - GNUCash"
    page.theme_mode = "light"
    page.scroll = "adaptive"
    page.padding = 10
    page.window_height = 625
    page.window_center()


    def get_values(e):
        path = text_field.value
        book = pc.open_book(path, open_if_lock=True, readonly=True)
        root = book.root_account

        lista_names, lista_values = [], []
        for acc in root.children:
            lista_names.append(acc.name)
            lista_values.append(acc.get_balance())

        figure = Pie(lista_names, lista_values)
        graph.figure = figure
        graph.visible = True
        page.update()
        
        return lista_names, lista_values



    text_field = TextField(
        hint_text= "caminho/para/o/arquivo.gnucash",
        label= "Caminho do arquivo gnucash",
        label_style= flet.TextStyle(size=14),
        text_style= flet.TextStyle(size=18),
        # text_size= 14,
        content_padding= flet.padding.only(left=10),
        height= 42,
        width=page.window_width,
        data="",
        value= r"",
        on_submit= get_values
    )



    graph = PlotlyChart(
        visible= False,
    )

    page.add(
        Column(
        controls=
            [
                # Header
                Container(
                    margin= flet.margin.symmetric(horizontal=10),
                    content=
                        Column(
                            controls=
                            [
                                Text("Gráfico Balanço patrimônial", size= 30, weight="bold"),
                                text_field,
                            ]
                        )
                ),
                # Body            
                Container(
                    content=
                        Column(
                            controls=
                                [
                                    graph
                                ]
                        )
                )
            ]
        )
    )

flet.app(target=main)
