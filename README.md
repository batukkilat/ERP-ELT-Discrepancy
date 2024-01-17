# Capstone Project : Create DBT Discrepancy model and Airflow Scheduling

## 💻 Scenario
C.V. Untung yang selama ini menggunakan pencatatan penjualan di spreadsheet baru saja beralih menggunakan sistem ERP.

Stakeholder C.V. Untung perlu melakukan monitoring apakah ada perbedaan pencatatan antara sistem ERP dan pencatatan di spreadsheet.

Dengan adanya analisis perbedaan (discrepancy) antara sistem ERP dan spreadsheet, maka stakeholder bisa memutuskan:

- Apakah sistem ERP sudah berjalan dengan baik dan bisa menggantikan pencatatan di spreadsheet
- Apakah ada SOP yang perlu diperbaiki
- Apakah data dari sistem ERP bisa dipakai untuk kepentingan analiisis.
- Apakah perbaikan sistem ERP dan perbaikan SOP mengurangi, atau justru menambah discrepancy secara total.

## ⚔️ Challenge

- Data terpisah berasal dari multiple source seperti db, excel, dan data source yg lain.
- Constraint setiap problem akan spesifik ditentukan pada bagian project description.

## 🎯 Goals

- Melakukan pengambilan data, include orchestration, transformation. i.e., ETL) (Mandatory)
- Melakukan pengambilan data agregasi dari db + excel (Mandatory)
- Melakukan penerapan replication & sharding (Poin plus)
- Mengambil data secara real time (Poin plus)
- Membuat visualisasi (Poin plus)

## ⚒️ Tools
- Airbyte (Ingestion)
- Airflow (Orchestration)
- SQL (Data Source 1)
- .CSV (Data Source 2)
- Postgres (Data Warehouse)
- Citus (Data Base)

## 📈 ETL
- Data source 1 (SQL) :

```
  ┌───────────┐        ┌──────────────┐        ┌─────────────┐
  │           │        │              │        │             │
  │    SQL    ├────────┤    Airbyte   ├────────┤    Citus    │
  │           │        │              │        │             │
  └───────────┘        └──────────────┘        └─────────────┘
```

- Data source 2 (CSV) :

```
  ┌───────────┐        ┌──────────────┐        ┌─────────────┐
  │           │        │              │        │             │
  │    CSV    ├────────┤    Airbyte   ├────────┤    Citus    │
  │           │        │              │        │             │
  └───────────┘        └──────────────┘        └─────────────┘
```

## ⌚ Orchestrating
Orchestrating di airflow dilakukan dengan cara scheduling task ingesting dan transform
```
  ┌───────────┐        ┌──────────────┐        
  │           │        │              │        
  │   Ingest  ├───────>|  Transform   |
  │           │        │              │       
  └───────────┘        └──────────────┘        
```

# Clone this project:
```bash
git clone https://github.com/iwangmoeslem/ALTA-Capstone-Project.git
```



# Start Docker Compose
Click [here](docker-compose.yml) to see the content

```bash
docker compose up -d
```

# Install DBT locally:
Sesuaikan versi dbt dengan kebutuhan

```bash
pip install dbt-core 1.7.4
```

## Setup DBT profiles
- Buat sebuah folder untuk menyimpan direktori file profiles.yml
- Jangan lupa untuk menjalankan command export di bawah setiap akan mengoperasikan dbt
```bash
cd docker-dep/airflow-dag/dbt-profiles
export DBT_PROFILES_DIR=$(pwd)
```
- Untuk mengecek apakah direktori sudah tersimpan, jalankan perintah ini:

```bash
echo $DBT_PROFILES_DIR
```
- Jika output dari perintah di atas adalah alamat menuju profiles.yml, maka value DBT_PROFILES_DIR sudah tersimpan

## Setup DBT project configuration
Konfigurasi project DBT adalah sebuah file untuk mengatur bagaimana skema atau alur dari sebuah project DBT, file ini bisa ditemukan di:
`docker-dep/airflow-dag/dbt-project/dbt_project.yml`

Konfigurasi DBT di project ini adalah seperti berikut:

```yml
models:
  dbt-project:
    # Config indicated by + and applies to all files under models/example/
    postgres:
      +schema: public
      +database: postgres
    sales_discrepancy:
      +materialized: table
      +schema: sales_discrepancy
      +database: postgres
    sales_detail_discrepancy:
      +materialized: table
      +schema: sales_detail_discrepancy
      +database: postgres
    daily_sales_discrepancy:
      +materialized: table
      +schema: daily_sales_discrepancy
      +database: postgres
    monthly_sales_discrepancy:
      +materialized: table
      +schema: monthly_sales_discrepancy
      +database: postgres
```
Terdapat 4 model yang akan dibuat sesuai dengan Goals project ini yaitu discrepancy dari kedua data source:

- Sales discrepancy 
- Sales detail discrepancy
- Daily sales discrepancy
- Monthly sales discrepancy

## Setup source
Source bisa ditemukan di `airflow-dag/store/schema.yml`


## Models
4 model bisa ditemukan di `airflow-dag/dbt-project/models`
