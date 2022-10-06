from pathlib import Path


def clean_csv(filein: Path, fileout: Path) -> None:
    with open(filein) as f_in:
        with open(fileout, "a") as f_out:
            count = 0
            for line in f_in:
                clean_line = line.rstrip()
                clean_line = clean_line.replace(", ", ",None")
                clean_line = clean_line.replace("'", "")
                clean_line = clean_line.replace('"', "")
                clean_line = clean_line.replace(" ", "")
                clean_line = clean_line.replace("	", "")
                clean_line = clean_line + "\n"

                f_out.write(clean_line)
                count += 1
                if count == 1000:
                    print("1000 line done")
                    count = 0
