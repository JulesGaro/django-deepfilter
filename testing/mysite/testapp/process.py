from csv import DictReader
from pathlib import Path

from .pydantic_models import VariantModel


def pre_parser(filename: Path):
    with open(filename, "r") as data:
        data_list = data.read().split("\n")

    header = data_list[0]
    data_list.pop(0)

    clean_header = ";".join(
        [col[1:-1].replace(".", "_").upper() for col in header.split(";")]
    )

    data_list.insert(0, clean_header)

    with open(filename, "w") as data:
        data.write("\n".join(data_list))


def parser(filename: Path) -> VariantModel:
    with open(filename, "r") as data:
        data_reader = DictReader(data, delimiter=",", quotechar='"')
        for line in data_reader:
            print(line.keys())
            variant = VariantModel(
                CHR=str(line["Chr"]),
                START=float(line["Start"]),
                REF=str(line["Ref"]),
                ALT=str(line["Alt"]),
                FUNC_REFGENE=str(line["Func.refGene"]),
                FILTERS=str(line["FILTERS"]),
                OMIM=str(line["OMIM"]),
                INHERITANCE=str(line["INHERITANCE"]),
                GNOMAD_GENOME_ALL=str(line["gnomAD_genome_ALL"]),
            )

            yield variant
