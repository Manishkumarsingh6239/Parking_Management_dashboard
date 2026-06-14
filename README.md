# 🅿 ParkEase — Vibrant Parking Management System

A full-stack web application for managing parking lots, slots, reservations, and payments — built with **Django**, **Django REST Framework**, **SQLite**, and **Tailwind CSS**.

ParkEase digitizes the entire parking workflow: customers can browse and book parking slots online, parking owners can manage their lots, and admins get a complete overview of the system — all with conflict-free, real-time slot booking.

---

## ✨ Features

- 🔐 **Role-based authentication** — Admin, Parking Owner, and Customer roles with separate dashboards
- 🏢 **Parking lot & slot management** — Owners can add lots and slots (Car/Bike/Truck) with custom hourly rates
- 📅 **Smart reservation system** — Automatic overlap detection prevents double-booking of the same slot
- 💰 **Automatic price calculation** — Total cost computed based on duration × hourly rate
- 💳 **Payment workflow** — Simulated payment processing with unique transaction IDs
- 📊 **Role-specific dashboards** — Admin (system stats), Owner (lots & bookings), Customer (booking history)
- 🔌 **REST API** — Built with DRF, supports filtering, search, ordering, and pagination
- 🎨 **Responsive UI** — Built with Tailwind CSS

---

## 🛠 Tech Stack

| Layer            | Technology                              |
|------------------|------------------------------------------|
| Backend          | Django 4.2.7                            |
| REST API         | Django REST Framework 3.14.0            |
| Database         | SQLite                                  |
| Frontend         | Tailwind CSS (CDN)                      |
| Filtering        | django-filter 23.3                      |
| Image Handling   | Pillow 10.1.0                           |
| Language         | Python 3.10+                            |

---

## 🏗 Architecture

The project follows Django's **MVT (Model-View-Template)** pattern, organized into 6 modular apps:

```
parking_management/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── parking_project/      # Project settings, URLs, DRF router
├── accounts/             # Custom user model, vehicle registration, auth
├── parking/               # Parking lots & slots, owner management, API
├── reservations/          # Booking logic with overlap detection, API
├── payments/              # Payment processing
├── core/                  # Landing page, role-based dashboard router
├── notifications/         # Reserved for future email/SMS alerts
└── templates/             # HTML templates (base + app-specific)
```

### Data Flow — Booking a Slot
```
Browse Lots → Select Slot → Submit Booking
   → Overlap Check (start_time / end_time)
   → Calculate Amount (duration × hourly_rate)
   → Save Reservation (status: PENDING)
   → Payment Page → Confirm Payment
   → Payment Created (transaction_id) → Reservation (status: CONFIRMED)
   → Success Page
```

---

## 🗄 Data Models

| Model         | Key Fields                                                       |
|---------------|-------------------------------------------------------------------|
| `CustomUser`  | username, email, role (Admin/Owner/Customer), phone               |
| `Vehicle`     | owner, plate_number (unique), vehicle_type                         |
| `ParkingLot`  | owner, name, address, city, total_slots, is_active                 |
| `ParkingSlot` | lot, slot_number, slot_type (Car/Bike/Truck), hourly_rate, is_active |
| `Reservation` | customer, slot, vehicle, start_time, end_time, total_amount, status |
| `Payment`     | reservation, amount, status, transaction_id, paid_at               |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# 1. Create project folder & virtual environment
mkdir parking_management && cd parking_management
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py makemigrations accounts parking reservations payments
python manage.py makemigrations
python manage.py migrate

# 5. Create a superuser (admin access)
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

Visit **http://127.0.0.1:8000** in your browser.

---

## 🔗 Important URLs

| URL                              | Description                  |
|-----------------------------------|-------------------------------|
| `/`                                | Landing page                  |
| `/accounts/register/`             | User registration             |
| `/accounts/login/`                | User login                    |
| `/dashboard/`                     | Role-based dashboard router   |
| `/parking/`                       | Browse parking lots           |
| `/parking/create/`                | Create a parking lot (Owner)  |
| `/reservations/book/<slot_id>/`   | Book a parking slot           |
| `/payments/<reservation_id>/`     | Payment page                  |
| `/admin/`                         | Django admin panel            |
| `/api/`                           | DRF browsable API root         |

---

## 🔌 REST API Endpoints

| Method      | Endpoint                  | Description                                  | Auth |
|-------------|----------------------------|-----------------------------------------------|------|
| GET         | `/api/parking-lots/`       | List all active parking lots (filter/search) | No   |
| POST        | `/api/parking-lots/`       | Create a parking lot                          | Owner |
| GET         | `/api/parking-lots/{id}/`  | Get lot details with nested slots             | No   |
| GET         | `/api/parking-slots/`      | List slots (filter by type, lot, active)      | Yes  |
| GET         | `/api/reservations/`       | List reservations (admin: all, customer: own) | Yes  |
| POST        | `/api/reservations/`       | Create a reservation                          | Yes  |

---

## 🧪 Key Logic — Overlap Detection

To prevent double-booking, the system checks for overlapping time ranges before confirming a reservation:

```python
overlap = Reservation.objects.filter(
    slot=slot,
    status__in=['PENDING', 'CONFIRMED'],
    start_time__lt=end,
    end_time__gt=start
).exists()

if overlap:
    # Reject booking — slot already reserved for that time
```

---

## 🔮 Future Enhancements

- [ ] Real payment gateway integration (Razorpay / Stripe)
- [ ] Mobile app using the existing REST API
- [ ] Real-time slot availability via WebSockets (Django Channels)
- [ ] Email/SMS booking notifications
- [ ] Google Maps integration for lot locations
- [ ] QR code-based entry/exit
- [ ] Analytics dashboard (revenue trends, occupancy rates)

---

## 📄 License

This project is built for educational/academic purposes.

---

## 🙌 Acknowledgements

Built with Django, Django REST Framework, and Tailwind CSS.
