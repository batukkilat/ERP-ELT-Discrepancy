# Project Brief Template Data Engineering

## 💻 Technical Brief

## Contraints

- Data terpisah berasal dari multiple source seperti db, excel, dan data source yg lain.
- Constraint setiap problem akan spesifik ditentukan pada bagian project description.

### Requirements

- Melakukan pengambilan data, include orchestration, transformation. i.e., ETL) (Mandatory)
- Melakukan pengambilan data agregasi dari db + excel (Mandatory)
- Melakukan penerapan replication & sharding (Poin plus)
- Mengambil data secara real time (Poin plus)
- Membuat visualisasi (Poin plus)

### Project Description and Expected Deliverables

#### Background

C.V. Untung yang selama ini menggunakan pencatatan penjualan di spreadsheet baru saja beralih menggunakan sistem ERP.

Stakeholder C.V. Untung perlu melakukan monitoring apakah ada perbedaan pencatatan antara sistem ERP dan pencatatan di spreadsheet.

Dengan adanya analisis perbedaan (discrepancy) antara sistem ERP dan spreadsheet, maka stakeholder bisa memutuskan:

- Apakah sistem ERP sudah berjalan dengan baik dan bisa menggantikan pencatatan di spreadsheet
- Apakah ada SOP yang perlu diperbaiki
- Apakah data dari sistem ERP bisa dipakai untuk kepentingan analiisis.
- Apakah perbaikan sistem ERP dan perbaikan SOP mengurangi, atau justru menambah discrepancy secara total.

#### Expected Deliverable

##### Detail Discrepancy

- Model `sales_discrepancy` dengan kolom-kolom sebagai berikut:
    - `system_order_id`
    - `system_datetime`
    - `system_total_discount`
    - `system_total_shipping`
    - `system_total_transaction`
    - `spreadsheet_order_id`
    - `spreadsheet_datetime`
    - `spreadsheet_total_discount`
    - `spreadsheet_total_shipping`
    - `spreadsheet_total_transaction`
    - `discrepancy`: `abs(system_total_transaction - spreadsheet_total_transaction)`
    - (Optional) `is_inequal_total_discount`
    - (Optional) `is_inequal_total_shipping`
    - (Optional) `is_invalid_system_calculation`
    - (Optional) `is_invalid_spreadsheet_calculation`
    - (Optional) `is_missing_system_item`: Apakah ada missing item di `system_sales_item`
    - (Optional) `is_missing_spreadhseet_item`: Apakah ada missing item di `spreadsheet_sales_item`

- Model `sales_detail_discrepancy` dengan kolom-kolom sebagai berikut:
    - `system_order_id`
    - `system_item_id`
    - `system_qty`
    - `system_price`
    - `system_subtotal`
    - `spreadsheet_order_id`
    - `spreadsheet_item_id`
    - `spreadheet_qty`
    - `spreadheet_price`
    - `spreadheet_subtotal`

##### Summary Discrepancy Harian

- Model `daily_sales_discrepancy` dengan kolom-kolom sebagai berikut:
    - `day_bucket`: Data harian dengan acuan `system_datetime`
    - `total_discrepancy`
    - (Optional) `inequal_total_discount_dicrepancy`
    - (Optional) `inequal_total_shipping_dicrepancy`
    - (Optional) `invalid_spreadsheet_calculation_dicrepancy`
    - (Optional) `invalid_system_calculation_dicrepancy`

Penambahan angka detail discrepancy bisa membantu stakeholder untuk menentuk fitur mana yang perlu diprioritaskan untuk diperbaiki.

##### Summary Discrepancy Bulanan

- Model `monthly_sales_discrepancy` dengan kolom-kolom sebagai berikut:
    - `day_bucket`: Data harian dengan acuan `system_datetime`
    - `total_discrepancy`
    - (Optional) `inequal_total_discount_dicrepancy`
    - (Optional) `inequal_total_shipping_dicrepancy`
    - (Optional) `invalid_spreadsheet_calculation_dicrepancy`
    - (Optional) `invalid_system_calculation_dicrepancy`

#### Success Criteria

- (Wajib) Ada sistem ELT untuk menciptakan expected deliverables.
- (Wajib) Setiap kali sistem ELT berjalan, maka model-model dicrepancies akan terupdate sesuai kondisi terkini.
- (Optional) Perubahan model terjadi secara real time.
- (Optional) Analisis penyebab discrepancy
    - Ada barang yang tercatat di penjualan manual, tapi tidak ada di sistem ERP.
    - Ada barang yang tercatat di sistem ERP, tapi tidak ada di manual.


#### Documentation

```
  ┌───────────┐        ┌──────────────┐        ┌─────────────┐
  │           │1   Many│              │Many   1│             │
  │  Product  ├────────┤  Sales Item  ├────────┤   Sales     │
  │           │        │              │        │             │
  └───────────┘        └──────────────┘        └─────────────┘
```


#### Assets

- sql (mewakili data di sistem ERP)
    - [ddl.sql](ddl.sql)
    - [products.sql](product.sql)
    - [sales.sql](sales.sql)
    - [sales_item.sql](sales_item.sql)
- csv (mewakili data di spreadsheet)
    - [products.csv](products.csv)
    - [sales.csv](sales.csv)
    - [sales_item.csv](sales_item.csv)

## 📆 Schedule Meeting and Format Mentoring

### Schedule Mentoring

- Mentoring dilakukan 3x dalam sepekan dengan alokasi 60 menit mentoring tiap sesi.
- Jadwal Mentoring dapat menyesuaikan jadwal mentor dan disepakati bersama dengan team, jika ada perubahan mentor dan tim terkait bisa langsung mengkomunikasikan.
- Mentoring bisa dilakukan hari senin-jumat atau sabtu-minggu sesuai availability mentor dan team.

### Mentoring Alocation

| Mentoring | Allocation Time | Agenda                                                      |
| --------- | --------------- | ----------------------------------------------------------- |
| Part 1    | 15 minutes      | Update Team in General                                      |
|           |                 | Update Every Member of The Team                             |
|           |                 | Showing Progress Based On Project Management Tools (Trello) |
| Part 2    | 45 minutes      | Discussion topics according to the problem at hand          |

## ⚠️ General Rules

### Hal-hal yang harus dilakukan oleh Mentees dan Team

- Setiap individu wajib berkontribusi & aktif berkomunikasi dalam team (yang tidak berkontribusi maka tidak mendapatkan nilai, nilai diberikan kenapa yang berkontribusi aktif).
- Setiap team wajib memiliki group komunikasi (membuat group telegram).
- Setiap team wajib menggunakan trello untuk management task & membagi task dg proporsional setiap member.
- Setiap team wajib mengadakan daily meeting setiap hari untuk berkoordinasi.

### Tindakan yang dianggap sebagai pelanggaran bagi Mentees dan Team

- Individu yang tidak aktif atau slow response dalam berkomunikasi dg tim (tidak membalas komunikasi team lebih dari 2 jam saat jam aktif: 9 am - 9 pm).
- Individu tidak ikut berkontribusi dalam mengerjakan task.
- Tim yang tidak membuat group komunikasi.
- Tim tidak menggunakan trello.
- Tim tidak melakukan pembagian tugas.
- Tim yang tidak mengadakan daily meeting.
