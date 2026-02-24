import pandas as pd
from django.core.management.base import BaseCommand
from trade_registry.models import Ticker

class Command(BaseCommand):
    help = 'Bulk ingest tickers from a CSV file. Required columns: symbol, name'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        """Receives symbol and name fron csv, bulk saves to db with last_price = 0.0"""
        file_path = options['csv_file']
        
        try:
            self.stdout.write(self.style.SUCCESS(f"Reading file: {file_path}"))
            df = pd.read_csv(file_path)

            required_columns = ['symbol', 'name']
            if not all(col in df.columns for col in required_columns):
                self.stdout.write(self.style.ERROR("Missing columns in CSV. Required: symbol, name"))
                return

            ticker_objects = []
            
            for _, row in df.iterrows():
                symbol = str(row['symbol']).strip().upper()
                name = str(row['name']).strip()

                ticker_objects.append(Ticker(
                    symbol=symbol,
                    name=name,
                    last_price=0.0
                ))

            Ticker.objects.bulk_create(
                ticker_objects,
                ignore_conflicts=True
            )

            self.stdout.write(self.style.SUCCESS(f"Successfully processed {len(ticker_objects)} tickers."))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))