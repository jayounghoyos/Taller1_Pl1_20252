import argparse
import sys
from pathlib import Path

import pandas as pd


def read_csv_with_fallback(csv_path: Path) -> pd.DataFrame:
	"""Read a CSV trying UTF-8 first, then falling back to latin-1 if needed."""
	try:
		return pd.read_csv(
			csv_path,
			encoding="utf-8",
			on_bad_lines="warn",
			engine="python",
		)
	except UnicodeDecodeError:
		return pd.read_csv(
			csv_path,
			encoding="latin-1",
			on_bad_lines="warn",
			engine="python",
		)


def convert_csv_to_json(input_csv: Path, output_json: Path) -> int:
	"""Convert a CSV file to JSON (array of records). Returns number of records written."""
	if not input_csv.exists():
		raise FileNotFoundError(f"No se encontró el archivo CSV: {input_csv}")

	df = read_csv_with_fallback(input_csv)

	# Export as an array of JSON objects (one per row)
	# orient='records' => cada fila del DataFrame se guarda como un registro JSON.
	output_json.parent.mkdir(parents=True, exist_ok=True)
	df.to_json(output_json, orient="records", force_ascii=False, indent=2)
	return len(df)


def parse_args(argv: list[str]) -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description=(
			"Convierte un archivo CSV de películas a JSON (orient='records')."
		)
	)
	parser.add_argument(
		"--input",
		"-i",
		type=Path,
		default=Path("movies_initial.csv"),
		help="Ruta al archivo CSV de entrada",
	)
	parser.add_argument(
		"--output",
		"-o",
		type=Path,
		default=Path("movies.json"),
		help="Ruta del archivo JSON de salida",
	)
	return parser.parse_args(argv)


def main(argv: list[str]) -> int:
	args = parse_args(argv)
	try:
		num_rows = convert_csv_to_json(args.input, args.output)
		print(
			f"Conversión exitosa: {num_rows} registros guardados en '{args.output}'."
		)
		return 0
	except Exception as exc:  # noqa: BLE001 - simple CLI script
		print(f"Error durante la conversión: {exc}", file=sys.stderr)
		return 1


if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))


