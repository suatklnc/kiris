import typer
import inquirer
import numpy as np
from rich.console import Console
from rich.table import Table
from beam_analysis.beam import Beam
from beam_analysis.loads import PointLoad, UDL
from beam_analysis.plotter import ASCIIPlotter

app = typer.Typer(
    help="Beam Analysis CLI - Saha Mühendisleri için Pratik Kiriş Analiz Aracı"
)
console = Console()


def display_input_summary(beam, loads):
    table = Table(title="Girdi Özeti")
    table.add_column("Parametre", style="cyan")
    table.add_column("Değer", style="magenta")

    table.add_row("Kiriş Uzunluğu", f"{beam.length} m")
    table.add_row("Mesnetler", f"{beam.supports}")

    for i, load in enumerate(loads):
        if isinstance(load, PointLoad):
            table.add_row(
                f"Yük {i+1} (Tekil)",
                f"Kuvvet: {load.force} kN, Konum: {load.location} m",
            )
        elif isinstance(load, UDL):
            table.add_row(f"Yük {i+1} (UDL)", f"Miktar: {load.magnitude} kN/m")

    console.print(table)


def display_results(engine):
    console.print("\n[bold]Analiz Sonuçları[/bold]")

    # Reactions
    reactions = engine.calculate_reactions()
    r_table = Table(title="Mesnet Reaksiyonları")
    r_table.add_column("Konum (m)", style="cyan")
    r_table.add_column("Kuvvet (kN)", style="green")
    for loc, force in reactions.items():
        r_table.add_row(f"{loc}", f"{force:.2f}")
    console.print(r_table)

    # Max Values
    max_v, x_v = engine.get_max_shear_info()
    max_m, x_m = engine.get_max_moment_info()

    m_table = Table(title="Kritik Değerler")
    m_table.add_column("Parametre", style="cyan")
    m_table.add_column("Değer", style="magenta")
    m_table.add_column("Konum (m)", style="yellow")

    m_table.add_row("Maksimum Kesme (Vmax)", f"{abs(max_v):.2f} kN", f"{x_v:.2f}")
    m_table.add_row("Maksimum Moment (Mmax)", f"{max_m:.2f} kNm", f"{x_m:.2f}")

    console.print(m_table)

    # Diagrams
    plotter = ASCIIPlotter(width=console.width - 10 if console.width > 20 else 60)
    x_points = np.linspace(0, engine.beam.length, 200)

    v_points = np.array([engine.get_shear_force(x) for x in x_points])
    console.print(
        plotter.plot(x_points, v_points, title="Kesme Kuvveti Diyagramı (SFD) [kN]")
    )

    m_points = np.array([engine.get_bending_moment(x) for x in x_points])
    console.print(
        plotter.plot(x_points, m_points, title="Eğilme Momenti Diyagramı (BMD) [kNm]")
    )


def get_beam_info():
    questions = [
        inquirer.Text(
            "length",
            message="Kiriş uzunluğunu girin (m)",
            validate=lambda _, x: float(x) > 0,
        )
    ]
    answers = inquirer.prompt(questions)
    length = float(answers["length"])
    # Basit mesnetli varsayımı: 0 ve L noktalarında mesnetler
    return Beam(length=length, supports=(0.0, length))


def get_loads(beam_length: float):
    loads = []
    while True:
        choices = [
            ("Tekil Yük (Point Load)", "point"),
            ("Düzgün Yayılı Yük (UDL)", "udl"),
            ("Analizi Başlat", "analyze"),
        ]
        questions = [
            inquirer.List(
                "type", message="Eklemek istediğiniz yük tipini seçin", choices=choices
            )
        ]
        answers = inquirer.prompt(questions)

        if answers["type"] == "analyze":
            break

        if answers["type"] == "point":
            q_point = [
                inquirer.Text(
                    "force",
                    message="Yük miktarını girin (kN, aşağı yönlü için pozitif)",
                    validate=lambda _, x: x.replace("-", "", 1)
                    .replace(".", "", 1)
                    .isdigit(),
                ),
                inquirer.Text(
                    "location",
                    message=f"Yükün konumunu girin (0 - {beam_length} m arası)",
                    validate=lambda _, x: 0 <= float(x) <= beam_length,
                ),
            ]
            ans_point = inquirer.prompt(q_point)
            loads.append(
                PointLoad(
                    force=float(ans_point["force"]),
                    location=float(ans_point["location"]),
                )
            )

        elif answers["type"] == "udl":
            q_udl = [
                inquirer.Text(
                    "magnitude",
                    message="UDL miktarını girin (kN/m, aşağı yönlü için pozitif)",
                    validate=lambda _, x: x.replace("-", "", 1)
                    .replace(".", "", 1)
                    .isdigit(),
                )
            ]
            ans_udl = inquirer.prompt(q_udl)
            loads.append(UDL(magnitude=float(ans_udl["magnitude"])))

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

    console.print("\n[bold green]Analiz Tamamlandı![/bold green]")
    display_results(engine)


if __name__ == "__main__":
    app()
