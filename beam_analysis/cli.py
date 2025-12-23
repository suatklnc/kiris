import typer
import inquirer
from rich.console import Console
from beam_analysis.beam import Beam

app = typer.Typer(help="Beam Analysis CLI - Saha Mühendisleri için Pratik Kiriş Analiz Aracı")
console = Console()

def get_beam_info():
    questions = [
        inquirer.Text('length', message="Kiriş uzunluğunu girin (m)", validate=lambda _, x: float(x) > 0)
    ]
    answers = inquirer.prompt(questions)
    length = float(answers['length'])
    # Basit mesnetli varsayımı: 0 ve L noktalarında mesnetler
    return Beam(length=length, supports=(0.0, length))

@app.command()
def main():
    """
    Kiriş analiz sihirbazını başlatır.
    """
    console.print("[bold blue]Beam Analysis CLI[/bold blue]")
    console.print("Bu araç basit mesnetli kirişlerin analizini yapar.")
    
    beam = get_beam_info()
    console.print(f"Kiriş oluşturuldu: {beam}")

if __name__ == "__main__":
    app()
