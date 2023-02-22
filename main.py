import piecash as pc
import re

### Se der este erro:
#### sqlalchemy.exc.DatabaseError: (sqlite3.DatabaseError) file is not a database [SQL: 'SELECT gnclock.hostname, gnclock.pid \nFROM gnclock'] (Background on this error at: http://sqlalche.me/e/4xp6)
##### ir no programa do GNUCash -> Arquivo -> Gravar como... -> Formato -> { sqlite3 } -> Renomeie e Salve

# Comandos:
#   pip install piecash
#   python -i nome_do_arquivo.py

# =========================================================
path:str = r"caminho/para/o/arquivo.gnucash" # <-- Edite

book = pc.open_book(path, open_if_lock=True, readonly=True)
root = book.root_account

def filhos(conta=root):
    for acc in conta.children:
        print(acc)

def tree(conta=root, level=0):
    for i in conta.children[:]:
        print("║\t" * level + f"╠═ {i}")
        tree(i, level+1)


def account_att(acc=root.children[0]):
    print(f"Account name={acc.name}\n"
      f"        commodity={acc.commodity.namespace}/{acc.commodity.mnemonic}\n"
      f"        fullname={acc.fullname}\n"
      f"        type={acc.type}")
    

def balance(iter=root.children):
    for acc in root.children:
        print(f"Saldo da conta para {acc.name}: {acc.get_balance()} (sem inversão de sinal: {acc.get_balance(natural_sign=False)}")


def search_transac(regex=".*"):
    regex_filter = re.compile(regex)

    transactions = [
        tr
        for tr in book.transactions
        if (regex_filter.search(tr.description)
            or 
            any(regex_filter.search(spl.memo) for spl in tr.splits)
        )
        # and tr.post_date.date() >= datetime.date(2014, 11, 1)
    ]  # e com post_date depois de novembro.


    print(
        [f"Transações com o critério de pesquisa: {regex_filter.pattern}", "==== Todas as transações:"][regex_filter.pattern == '.*']
    )
    

    for tr in transactions:
        print(f"- {tr.post_date:%d/%m/%Y} : {tr.description}")
        for spl in tr.splits:
            print(
                "\tR$ {valor},00  {direcao}  {conta} : {memo}".format(
                    valor=abs(spl.value),
                    direcao="-->" if spl.value > 0 else "<--",
                    conta=spl.account.fullname,
                    memo=spl.memo,
                )
            )
