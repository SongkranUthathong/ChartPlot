from rich import print
from rich.pretty import Pretty
from rich.panel import Panel
pretty = Pretty(locals())
panel = Panel(pretty)


def msgPrint(str):
    print(str)