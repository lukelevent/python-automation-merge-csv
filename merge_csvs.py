# Dosya/klasör yollarını güvenli şekilde yönetmek için Path kullanır
from pathlib import Path

# CSV dosyalarını okumak ve birleştirmek için pandas kullanır
import pandas as pd

# Bu script dosyasının bulunduğu klasörü baz alır
BASE_DIR = Path(__file__).resolve().parent

# Giriş (input) ve çıkış (output) klasör yollarını tanımlar
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"

# output klasörü yoksa oluşturur (varsa hiçbir şey yapmaz)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# input klasörü yoksa net hata verir
if not INPUT_DIR.exists():
    raise FileNotFoundError(
        f"'input' klasörü bulunamadı: {INPUT_DIR}"
    )

# input klasöründeki tüm .csv dosyalarını bulur
csv_files = sorted(INPUT_DIR.glob("*.csv"))

# Hiç CSV yoksa net hata verir
if not csv_files:
    raise FileNotFoundError(
        f"input klasöründe CSV dosyası yok: {INPUT_DIR}"
    )

# Her CSV dosyasını okuyup bir listeye koyar
frames = []
for file_path in csv_files:
    # CSV'yi tabloya çevirir
    df = pd.read_csv(file_path)

    # Hangi dosyadan geldiğini görmek için kaynak dosya adını ekler
    df["__source_file"] = file_path.name

    # Listeye ekler
    frames.append(df)

# Tüm tabloları alt alta birleştirir
merged = pd.concat(frames, ignore_index=True)

# Çıktı dosyasının yolunu belirler
output_path = OUTPUT_DIR / "merged.csv"

# Birleştirilmiş tabloyu kaydeder
merged.to_csv(output_path, index=False)

# Terminale kısa sonuç yazdırır
print(f"OK: {len(csv_files)} dosya birleşti -> {output_path}")

