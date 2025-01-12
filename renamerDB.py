import os
import sys
import time
import requests
import logging
from datetime import datetime
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskID
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import print as rprint

class SteamGameRenamer:
    def __init__(self):
        self.STEAM_API_KEY = ''  # Votre clé API Steam
        self.console = Console()
        self.stats = {"success": 0, "failed": 0, "skipped": 0}
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            filename=f'steam_renamer_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def print_header(self):
        title = Text()
        title.append("🎮 ", style="green")
        title.append("Steam Game Renamer ", style="bold cyan")
        title.append("v2.0", style="yellow")
        
        subtitle = Text()
        subtitle.append("\n📅 ", style="blue")
        subtitle.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), style="cyan")
        subtitle.append("\n🔧 ", style="yellow")
        subtitle.append("Développé par Arizaki", style="magenta")
        
        panel = Panel(
            title + subtitle,
            border_style="cyan",
            padding=(1, 2)
        )
        self.console.print(panel)

    def get_steam_game_info(self, appid: str) -> dict:
        url = f"http://store.steampowered.com/api/appdetails"
        params = {
            "appids": appid,
            "key": self.STEAM_API_KEY
        }
        
        try:
            with self.console.status(f"[cyan]📡 Récupération des informations pour AppID {appid}..."):
                response = requests.get(url, params=params, timeout=10)
                data = response.json()
                
                if str(appid) in data and data[str(appid)]['success']:
                    game_data = data[str(appid)]['data']
                    return {
                        "name": game_data['name'],
                        "type": game_data.get('type', 'Unknown'),
                        "release_date": game_data.get('release_date', {}).get('date', 'Unknown'),
                        "developers": game_data.get('developers', ['Unknown'])[0]
                    }
                return None
        except Exception as e:
            logging.error(f"Erreur API Steam pour AppID {appid}: {str(e)}")
            return None

    def sanitize_filename(self, filename: str) -> str:
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename.strip()

    def process_file(self, file: str, progress: Progress, task: TaskID) -> bool:
        if not file.endswith('.zip'):
            return False
            
        appid = file[:-4]
        if not appid.isdigit():
            self.console.print(f"[red]❌ AppID invalide: {file}")
            return False
            
        game_info = self.get_steam_game_info(appid)
        if not game_info:
            self.console.print(f"[red]❌ Impossible de récupérer les informations pour: {file}")
            return False
            
        # Modification du format du nom de fichier ici - plus de crochets
        new_filename = f"{game_info['name']} {appid}.zip"
        new_filename = self.sanitize_filename(new_filename)
        
        try:
            os.rename(
                os.path.join(self.zip_directory, file),
                os.path.join(self.zip_directory, new_filename)
            )
            self.display_game_info(game_info, appid, new_filename)
            progress.update(task, advance=1)
            return True
        except Exception as e:
            logging.error(f"Erreur lors du renommage de {file}: {str(e)}")
            return False

    def display_game_info(self, info: dict, appid: str, new_name: str):
        table = Table(show_header=False, box=None)
        table.add_row("🎮 Nom", info['name'])
        table.add_row("🔢 AppID", appid)
        table.add_row("📁 Nouveau nom", new_name)
        table.add_row("🏷️ Type", info['type'])
        table.add_row("📅 Date de sortie", info['release_date'])
        table.add_row("👨‍💻 Développeur", info['developers'])
        
        panel = Panel(
            table,
            title="[bold green]✅ Renommage réussi",
            border_style="green"
        )
        self.console.print(panel)

    def display_summary(self):
        table = Table(title="📊 Résumé des opérations", border_style="cyan")
        table.add_column("Statut", style="cyan", justify="right")
        table.add_column("Nombre", style="green", justify="center")
        
        table.add_row("✅ Réussis", str(self.stats["success"]))
        table.add_row("❌ Échoués", str(self.stats["failed"]))
        table.add_row("⏭️ Ignorés", str(self.stats["skipped"]))
        table.add_row("📝 Total", str(sum(self.stats.values())))
        
        self.console.print(table)

    def run(self, directory: str):
        self.zip_directory = directory
        self.print_header()
        
        if not os.path.exists(directory):
            self.console.print(f"[red]❌ Le répertoire {directory} n'existe pas!")
            return
            
        files = [f for f in os.listdir(directory) if f.endswith('.zip')]
        if not files:
            self.console.print("[yellow]⚠️ Aucun fichier .zip trouvé!")
            return
            
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ) as progress:
            task = progress.add_task(
                "[cyan]🔄 Traitement des fichiers...", 
                total=len(files)
            )
            
            for file in files:
                if self.process_file(file, progress, task):
                    self.stats["success"] += 1
                else:
                    self.stats["failed"] += 1
                    
        self.display_summary()
        rprint("\n[green]✨ Opération terminée![/green]")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <dossier_zip>")
        sys.exit(1)
        
    renamer = SteamGameRenamer()
    renamer.run(sys.argv[1])