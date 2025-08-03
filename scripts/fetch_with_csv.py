import os
import zipfile
from dotenv import load_dotenv
from itertools import islice
from concurrent.futures import ProcessPoolExecutor
from django.db import transaction


def read_csv(file_path: str, batch_size: int):
    with open(file_path, "r", encoding="latin1") as file:
        import csv

        reader = csv.reader(file, delimiter=';')
        while True:
            batch = list(islice(reader, batch_size))

            if not batch:
                return

            yield batch

def process_batch(batch):
    from django.db import connection
    from companies.models import Company

    connection.connect()
    new_companies = []

    for element in batch:
        if not element or len(element) < 7:
            continue

        new_companies.append(Company(
            basic_cnpj=element[0],
            company_name=element[1],
            legal_nature=element[2],
            qualification_of_the_person_in_charge=element[3],
            share_company_capital=element[4],
            company_size=element[5],
            federal_entity_responsible=element[6],
        ))

    new_companies_by_cnpj = { company.basic_cnpj: company for company in new_companies }
    cnpjs = list(new_companies_by_cnpj.keys())

    existing_by_cnpj = Company.objects.in_bulk(cnpjs, field_name="basic_cnpj")

    to_create = []
    to_update = []

    for cnpj, new_company in new_companies_by_cnpj.items():
        existing = existing_by_cnpj.get(cnpj)

        if not existing:
            to_create.append(new_company)
        else:
            has_changes = (
                existing.company_name != new_company.company_name or
                existing.legal_nature != new_company.legal_nature or
                existing.qualification_of_the_person_in_charge != new_company.qualification_of_the_person_in_charge or
                existing.share_company_capital != new_company.share_company_capital or
                existing.company_size != new_company.company_size or
                existing.federal_entity_responsible != new_company.federal_entity_responsible
            )

            if has_changes:
                existing.company_name = new_company.company_name
                existing.legal_nature = new_company.legal_nature
                existing.qualification_of_the_person_in_charge = new_company.qualification_of_the_person_in_charge
                existing.share_company_capital = new_company.share_company_capital
                existing.company_size = new_company.company_size
                existing.federal_entity_responsible = new_company.federal_entity_responsible

                to_update.append(existing)

    with transaction.atomic():
        if to_create:
            Company.objects.bulk_create(to_create, batch_size=5_000)
        if to_update:
            Company.objects.bulk_update(
                to_update,
                fields=[
                    "company_name", "legal_nature", 
                    "qualification_of_the_person_in_charge", "share_company_capital",
                    "company_size", "federal_entity_responsible"
                ],
                batch_size=5_000
            )

def run(*args):
    load_dotenv()

    file_path = os.path.join(os.getcwd(), os.getenv('CSV_FILE_NAME'))
    compressed_file_name = os.getenv('COMPRESSED_FILE_NAME')
    compressed_file_path = os.path.join(os.getcwd(), compressed_file_name)
    compressed_file_url = os.getenv('CSV_FILE_URL')

    batch_size = 100_000
    max_workers = max((os.cpu_count() or 2) // 2, 1)

    if not os.path.isfile(file_path):
        if os.path.isfile(compressed_file_path):
            try:
                print(f"\033[96mUnpacking file: {compressed_file_name}\033[0m")

                with zipfile.ZipFile(compressed_file_name, "r") as file:
                    file.extractall(os.getcwd())
            except:
                print('\033[91mAn error occurred while unpacking the zip file!\033[0m')
                return
            finally:
                print("\033[92mFile extracted successfully!\033[0m")
        else:
            print(f"\033[91m{compressed_file_name} not detected!\033[0m")        
            print(f"Link to download: {compressed_file_url}")        
            print(f"Place the {compressed_file_name} in the project root.")
            return


    if len(args) > 0:
        if 'batch-size=' in args[0]:
            try:
                batch_size = int(args[0].split('=')[1])
            except:
                print('\033[91mInvalid parameter!\033[0m')
                return
        
    with ProcessPoolExecutor(max_workers = max_workers) as executor:
        for _ in executor.map(process_batch, read_csv(file_path, batch_size)):
            pass