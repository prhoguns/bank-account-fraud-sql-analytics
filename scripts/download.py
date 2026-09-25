from pathlib import Path
import shutil
import kagglehub

ROOT = Path(__file__).resolve().parents[1]
destination = ROOT / 'data/raw/Base.csv'
destination.parent.mkdir(parents=True, exist_ok=True)
source = Path(kagglehub.dataset_download(
    'sgpjesus/bank-account-fraud-dataset-neurips-2022', path='Base.csv'))
shutil.copy2(source, destination)
print(f'Downloaded {destination} ({destination.stat().st_size:,} bytes)')
