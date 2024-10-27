import config
from datetime import datetime
import typer
import google.generativeai as genai
from rich import print
from rich.table import Table

def main():
    # Configure the API key
    genai.configure(api_key=config.api_key)

    print("[bold green]ChatGPT API en python[/bold green]")

    table = Table("Comando", "Descripcion")
    table.add_row("exit", "Salir de la aplicacion")
    table.add_row("new", "Nueva conversacion")
    table.add_row("history", "Ver historial del chat")

    print(table)

    # Create the model
    model = genai.GenerativeModel('gemini-pro')

    def start_new_chat():
        """Function to initialize a new chat session"""
        chat = model.start_chat(history=[])
        chat.send_message("Eres un asistente muy útil que recuerda el contexto de la conversación.")
        print("[bold green]¡Nueva conversación iniciada![/bold green]")
        return chat

    # Initialize first chat session
    chat = start_new_chat()

    # Function to display chat history
    def display_history():
        print("\n[bold blue]=== Historial del Chat ===[/bold blue]")
        if not chat.history:
            print("[italic]No hay historial disponible.[/italic]")
            return
        
        for message in chat.history:
            timestamp = datetime.now().strftime("%H:%M:%S")
            role = "[bold cyan]Asistente[/bold cyan]" if message.role == "model" else "[bold yellow]Usuario[/bold yellow]"
            print(f"[{timestamp}] {role}: {message.parts[0].text}")
        print("=" * 30 + "\n")

    try:
        while True:
            # Get user input
            prompt = typer.prompt("\n¿Sobre qué quieres hablar? ")

            # Check for commands
            if prompt.lower() in ['exit', 'quit', 'salir']:
                # Confirm exit
                if typer.confirm("¿Estás seguro de que quieres salir?"):
                    display_history()
                    print("[bold red]¡Hasta luego![/bold red]")
                    raise typer.Exit()  # Raise typer.Exit to exit cleanly

            if prompt.lower() == 'history':
                display_history()
                continue
                
            if prompt.lower() == 'new':
                # Start new chat session
                chat = start_new_chat()
                continue
            
            # Generate response
            response = chat.send_message(prompt)
            print("\n[bold cyan] > [/bold cyan]" + f"[green]{response.text}[/green]")

    except Exception as e:
        print(f"[bold red]An error occurred: {str(e)}[/bold red]")

if __name__ == "__main__":
    typer.run(main)
