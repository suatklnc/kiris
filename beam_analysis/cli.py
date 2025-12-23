import typer
import inquirer
from rich.console import Console
from rich.table import Table
from beam_analysis.beam import Beam
from beam_analysis.loads import PointLoad, UDL

app = typer.Typer(help="Beam Analysis CLI - Saha Mühendisleri için Pratik Kiriş Analiz Aracı")
console = Console()

def display_input_summary(beam, loads):
    table = Table(title="Girdi Özeti")
    table.add_column("Parametre", style="cyan")
    table.add_column("Değer", style="magenta")
    
    table.add_row("Kiriş Uzunluğu", f"{beam.length} m")
    table.add_row("Mesnetler", f"{beam.supports}")
    
    for i, load in enumerate(loads):
        if isinstance(load, PointLoad):
            table.add_row(f"Yük {i+1} (Tekil)", f"Kuvvet: {load.force} kN, Konum: {load.location} m")
        elif isinstance(load, UDL):
            table.add_row(f"Yük {i+1} (UDL)", f"Miktar: {load.magnitude} kN/m")
            
    console.print(table)

def get_beam_info():
    questions = [
        inquirer.Text('length', message="Kiriş uzunluğunu girin (m)", validate=lambda _, x: float(x) > 0)
    ]
    answers = inquirer.prompt(questions)
    length = float(answers['length'])
    # Basit mesnetli varsayımı: 0 ve L noktalarında mesnetler
    return Beam(length=length, supports=(0.0, length))

def get_loads(beam_length: float):
    loads = []
    while True:
        choices = [
            ('Tekil Yük (Point Load)', 'point'),
            ('Düzgün Yayılı Yük (UDL)', 'udl'),
            ('Analizi Başlat', 'analyze')
        ]
        questions = [
            inquirer.List('type', message="Eklemek istediğiniz yük tipini seçin", choices=choices)
        ]
        answers = inquirer.prompt(questions)
        
        if answers['type'] == 'analyze':
            break
            
        if answers['type'] == 'point':
            q_point = [
                inquirer.Text('force', message="Yük miktarını girin (kN, aşağı yönlü için negatif)", validate=lambda _, x: x.replace('-','',1).replace('.','',1).isdigit()),
                inquirer.Text('location', message=f"Yükün konumunu girin (0 - {beam_length} m arası)", validate=lambda _, x: 0 <= float(x) <= beam_length)
            ]
            ans_point = inquirer.prompt(q_point)
            loads.append(PointLoad(force=float(ans_point['force']), location=float(ans_point['location'])))
            
        elif answers['type'] == 'udl':
            q_udl = [
                inquirer.Text('magnitude', message="UDL miktarını girin (kN/m, aşağı yönlü için negatif)", validate=lambda _, x: x.replace('-','',1).replace('.','',1).isdigit())
            ]
            ans_udl = inquirer.prompt(q_udl)
            loads.append(UDL(magnitude=float(ans_udl['magnitude'])))
            
        console.print(f"[green]Yük eklendi. Toplam yük sayısı: {len(loads)}[/green]")
        
    return loads

@app.command()
def main():
    """
    Kiriş analiz sihirbazını başlatır.
    """
    console.print("[bold blue]Beam Analysis CLI[/bold blue]")
    console.print("Bu araç basit mesnetli kirişlerin analizini yapar.")
    
    beam = get_beam_info()
    loads = get_loads(beam.length)
    
    display_input_summary(beam, loads)
    
    # Analyze button
    if not loads:
        console.print("[yellow]Hiç yük eklenmedi. Analiz iptal edildi.[/yellow]")
        return

    from beam_analysis.engine import AnalysisEngine
    engine = AnalysisEngine(beam)
    for load in loads:
        engine.add_load(load)
    
    console.print("\n[bold green]Analiz Hazır![/bold green]")

if __name__ == "__main__":
    app()
