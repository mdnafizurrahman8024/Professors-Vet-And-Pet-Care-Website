import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import ClinicInfo, NoticeOffer
from appointments.models import DoctorSchedule, Appointment
from gallery.models import SurgeryCategory, SurgeryCase
from shop.models import Category, Product
from accounts.models import Pet

User = get_user_model()

class Command(BaseCommand):
    help = "Seeds initial database for Professor's Vet & Pet Care"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting database seeding..."))

        # 1. Admin Superuser
        admin_email = "bhuyan@ru.ac.bd"
        admin_phone = "+8801316254500"
        admin_user = User.objects.filter(email=admin_email).first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                username="admin",
                email=admin_email,
                phone=admin_phone,
                password="admin",
                first_name="Abdulla Al Mamun",
                last_name="Bhuyan"
            )
            self.stdout.write(self.style.SUCCESS(f"Superuser created: {admin_email} (Password: admin)"))
        else:
            self.stdout.write("Superuser already exists.")

        # 2. Clinic Info
        clinic, created = ClinicInfo.objects.get_or_create(id=1)
        clinic.clinic_name = "Professor's Vet & Pet Care"
        clinic.doctor_name = "Dr. Abdulla Al Mamun Bhuyan"
        clinic.doctor_degrees = "DVM, MS (BAU), Dr.sc.hum (Germany)"
        clinic.doctor_designation = "Associate Professor, Department of Veterinary and Animal Sciences"
        clinic.doctor_institution = "University of Rajshahi, Rajshahi-6205, Bangladesh"
        clinic.cell_number = "+8801316254500"
        clinic.email = "bhuyan@ru.ac.bd"
        clinic.chamber_address = "Department of Veterinary and Animal Sciences, University of Rajshahi, Rajshahi-6205, Bangladesh."
        clinic.clinic_physical_address = "138 Debishing Para, Madrashar More, Rajshahi"
        clinic.save()
        self.stdout.write(self.style.SUCCESS("Clinic Information updated with Dr. Bhuyan's credentials."))

        # 3. Live Notice & Offer Board
        notices = [
            {
                'title': "Winter Vaccination & Rabies Immunity Drive",
                'content': "Cold chain protected core vaccinations available at discounted rates with free health checkup.",
                'badge_text': "HEALTH CAMP",
                'badge_type': "CAMP",
                'is_marquee': True,
                'is_banner': True,
                'discount_code': "VACCINE10",
                'discount_percentage': 10,
                'priority': 10
            },
            {
                'title': "Dr. Bhuyan's Clinical Chamber Hours",
                'content': "Chamber is open Saturday through Thursday 04:00 PM - 09:30 PM & Friday from 10:00 AM.",
                'badge_text': "CHAMBER OPEN",
                'badge_type': "NOTICE",
                'is_marquee': True,
                'is_banner': True,
                'priority': 8
            },
            {
                'title': "Flat 15% OFF on Premium Dog & Cat Food",
                'content': "Get 15% instant discount on Royal Canin, Drools, Me-O, and Reflex foods across Rajshahi.",
                'badge_text': "HOT OFFER",
                'badge_type': "OFFER",
                'is_marquee': True,
                'is_banner': True,
                'discount_code': "PETFOOD15",
                'discount_percentage': 15,
                'priority': 9
            },
            {
                'title': "24/7 Emergency Veterinary Trauma Hotline",
                'content': "For urgent poison cases, acute fractures, or difficult labor, call +8801316254500 immediately.",
                'badge_text': "EMERGENCY",
                'badge_type': "EMERGENCY",
                'is_marquee': True,
                'is_banner': True,
                'priority': 15
            }
        ]
        for n in notices:
            NoticeOffer.objects.get_or_create(title=n['title'], defaults=n)
        self.stdout.write(self.style.SUCCESS("Notice & Offer Board announcements seeded."))

        # 4. Doctor Weekly Schedules (Sat - Fri)
        schedules = [
            (5, "Saturday", "16:00", "21:30"),
            (6, "Sunday", "16:00", "21:30"),
            (0, "Monday", "16:00", "21:30"),
            (1, "Tuesday", "16:00", "21:30"),
            (2, "Wednesday", "16:00", "21:30"),
            (3, "Thursday", "16:00", "21:30"),
            (4, "Friday", "10:00", "20:00"),
        ]
        for day_code, day_name, start, end in schedules:
            DoctorSchedule.objects.get_or_create(
                day_of_week=day_code,
                defaults={
                    'start_time': start,
                    'end_time': end,
                    'slot_duration_minutes': 20,
                    'is_available': True,
                    'notes': f"Clinical Hours: {day_name}"
                }
            )
        self.stdout.write(self.style.SUCCESS("Doctor weekly consultation schedule initialized."))

        # 5. Surgery Categories & Documented Cases
        cat_ortho, _ = SurgeryCategory.objects.get_or_create(name="Orthopedic Surgery", slug="orthopedic", defaults={'description': "Bone plating, pinning, joint stabilization, and fracture repair."})
        cat_soft, _ = SurgeryCategory.objects.get_or_create(name="Soft Tissue Surgery", slug="soft-tissue", defaults={'description': "Tumor excision, foreign body removal, wound reconstructive surgery."})
        cat_dental, _ = SurgeryCategory.objects.get_or_create(name="Dental & Oral Surgery", slug="dental", defaults={'description': "Ultrasonic plaque scaling, tooth extraction, and oral tumor management."})
        cat_general, _ = SurgeryCategory.objects.get_or_create(name="General Clinical Procedures", slug="general-clinical", defaults={'description': "Spaying, neutering, abscess drainage, and diagnostic laparotomy."})

        cases = [
            {
                'title': "Femur Shaft Fracture Intramedullary Pinning in 2-Year-Old German Shepherd",
                'category': cat_ortho,
                'pet_name': "Rocky",
                'pet_species': "Dog",
                'pet_breed': "German Shepherd",
                'chief_surgeon': "Dr. Abdulla Al Mamun Bhuyan",
                'case_summary': "Rocky presented following an auto-rickshaw trauma in Rajshahi with complete inability to bear weight on the right hindlimb. Radiographs revealed a transverse mid-diaphyseal femur fracture with severe soft tissue swelling.",
                'procedure_details': "Under general inhalation anaesthesia and sterile surgical scrub, open reduction was performed. An appropriate Steinmann pin was retrograded across the femoral canal, achieving anatomical reduction with cerclage wire reinforcement.",
                'recovery_outcome': "Rocky was ambulatory on three limbs within 48 hours post-op and achieved complete radiological bone union and four-limb normal locomotion at 6 weeks.",
                'outcome': "Full Bone Union & Recovery",
                'treatment_date': datetime.date(2026, 8, 14),
                'is_featured': True,
                'is_published': True,
            },
            {
                'title': "Emergency Gastric Foreign Body Extraction (Rubber Ball) in Persian Cat",
                'category': cat_soft,
                'pet_name': "Snowy",
                'pet_species': "Cat",
                'pet_breed': "Persian Cat",
                'chief_surgeon': "Dr. Abdulla Al Mamun Bhuyan",
                'case_summary': "Snowy suffered from persistent projectile vomiting, dehydration, and complete anorexia for 3 days. Abdominal palpation and ultrasonography revealed a dense acoustic shadowing mass lodged in the pyloric antrum.",
                'procedure_details': "Emergency midline exploratory celiotomy was executed. A longitudinal gastrotomy incising the hypovascular area between the greater and lesser curvatures allowed safe extraction of an intact rubber toy ball without mucosal ischemia.",
                'recovery_outcome': "Snowy initiated fluid diet at 18 hours post-operation. Complete suture removal occurred on Day 10 with total restoration of normal feline vigor.",
                'outcome': "Complete Healing Without Complications",
                'treatment_date': datetime.date(2026, 9, 2),
                'is_featured': True,
                'is_published': True,
            },
            {
                'title': "Severe Periodontitis Ultrasonic Scaling and Canines Restoration",
                'category': cat_dental,
                'pet_name': "Coco",
                'pet_species': "Dog",
                'pet_breed': "Golden Retriever",
                'chief_surgeon': "Dr. Abdulla Al Mamun Bhuyan",
                'case_summary': "Coco presented with severe halitosis, bleeding gingiva, and reluctance to chew solid kibble due to Stage-3 periodontal calculus accumulation.",
                'procedure_details': "Full dental scaling using piezoceramic ultrasonic instruments, subgingival curettage, followed by fluoride polishing and extraction of two non-viable mobile premolars.",
                'recovery_outcome': "Normal eating resumed the following morning with healthy, non-inflamed gingival borders and complete resolution of halitosis.",
                'outcome': "Oral Health Restored",
                'treatment_date': datetime.date(2026, 9, 22),
                'is_featured': True,
                'is_published': True,
            }
        ]
        for c in cases:
            SurgeryCase.objects.get_or_create(title=c['title'], defaults=c)
        self.stdout.write(self.style.SUCCESS("Documented surgery gallery cases populated."))

        # 6. E-Commerce Product Categories & Realistic Catalog
        cat_food, _ = Category.objects.get_or_create(name="Pet Food", slug="pet-food", defaults={'icon': 'bone', 'description': "Nutritional diets and dry kibbles for dogs and cats."})
        cat_med, _ = Category.objects.get_or_create(name="Veterinary Medicine", slug="veterinary-medicine", defaults={'icon': 'pill', 'description': "Prescription medicines, antibiotics, wound sprays, and dewormers."})
        cat_acc, _ = Category.objects.get_or_create(name="Accessories & Collars", slug="accessories", defaults={'icon': 'tag', 'description': "Harnesses, leashes, cat litter boxes, and feeding bowls."})
        cat_toys, _ = Category.objects.get_or_create(name="Toys & Play", slug="toys", defaults={'icon': 'smile', 'description': "Chew ropes, interactive laser pointers, and squeaky balls."})

        products = [
            {
                'name': "Royal Canin Maxi Adult Dog Food (4 kg)",
                'slug': "royal-canin-maxi-adult-4kg",
                'sku': "RC-MAXI-4K",
                'category': cat_food,
                'target_pet': "DOG",
                'short_description': "Complete nutrition for large breed adult dogs with high protein & joint support.",
                'description': "Formulated with optimal digestive tolerance and EPA-DHA fatty acids to help support healthy bones and joints in large adult dogs.",
                'price': 4200.00,
                'discount_price': 3850.00,
                'stock_quantity': 18,
                'is_prescription_required': False,
                'is_featured': True,
                'manufacturer': "Royal Canin France",
            },
            {
                'name': "Reflex Plus Adult Cat Food - Chicken & Rice (1.5 kg)",
                'slug': "reflex-plus-cat-food-1-5kg",
                'sku': "RFLX-CAT-15",
                'category': cat_food,
                'target_pet': "CAT",
                'short_description': "Super premium complete cat food enriched with Xylo-oligosaccharides (XOS).",
                'description': "Promotes urinary tract health, hairball control, and immune resilience with balanced omega 3 & 6 fatty acids.",
                'price': 1450.00,
                'discount_price': 1290.00,
                'stock_quantity': 25,
                'is_prescription_required': False,
                'is_featured': True,
                'manufacturer': "Lider Pet Food",
            },
            {
                'name': "Cefpet 200mg (Cefpodoxime Proxetil) Veterinary Antibiotic",
                'slug': "cefpet-200mg-antibiotic",
                'sku': "MED-CFP-200",
                'category': cat_med,
                'target_pet': "ALL",
                'short_description': "Broad-spectrum oral cephalosporin antibiotic for canine & feline skin, wound, and post-op infections.",
                'description': "Prescribed for bacterial dermatitis, respiratory tract infections, deep abscesses, and orthopedic surgical prophylaxis. Must be administered under veterinary dosage guidelines.",
                'price': 650.00,
                'discount_price': 580.00,
                'stock_quantity': 30,
                'is_prescription_required': True,
                'is_featured': True,
                'manufacturer': "Vetoquinol Animal Health",
            },
            {
                'name': "Bravecto Chewable Tick & Flea Protection for Dogs (10-20kg)",
                'slug': "bravecto-chewable-10-20kg",
                'sku': "MED-BRV-1020",
                'category': cat_med,
                'target_pet': "DOG",
                'short_description': "12 weeks of continuous protection against ticks, fleas, and mites with 1 single tasty chew.",
                'description': "Fast-acting fluralaner formula that kills adult fleas before they lay eggs and breaks the infestation cycle for 3 full months.",
                'price': 2850.00,
                'discount_price': 2600.00,
                'stock_quantity': 8,
                'is_prescription_required': False,
                'is_featured': True,
                'manufacturer': "MSD Animal Health",
            },
            {
                'name': "Bioline Ear Care Drops for Dogs & Cats (50 ml)",
                'slug': "bioline-ear-care-drops",
                'sku': "MED-BIO-EAR",
                'category': cat_med,
                'target_pet': "ALL",
                'short_description': "Gentle ear canal cleaner to dissolve wax, prevent ear mite irritation, and neutralize odor.",
                'description': "Soothes ear itching and prevents bacterial/fungal otitis externa in cats and dogs.",
                'price': 380.00,
                'discount_price': 340.00,
                'stock_quantity': 15,
                'is_prescription_required': False,
                'is_featured': False,
                'manufacturer': "Bioline Pets",
            },
            {
                'name': "Adjustable Reflective Nylon Dog Harness & Leash Set",
                'slug': "reflective-dog-harness-leash",
                'sku': "ACC-HRN-REF",
                'category': cat_acc,
                'target_pet': "DOG",
                'short_description': "No-pull ergonomic harness with 3M reflective stitching for safe nighttime walking.",
                'description': "Padded breathable mesh lining reduces chest strain and prevents tracheal choking on vigorous walks.",
                'price': 750.00,
                'discount_price': 650.00,
                'stock_quantity': 12,
                'is_prescription_required': False,
                'is_featured': True,
                'manufacturer': "Professor's Pet Accessories",
            },
            {
                'name': "Interactive Automatic Laser Pointer Toy for Cats",
                'slug': "interactive-laser-toy-cats",
                'sku': "TOY-LSR-AUTO",
                'category': cat_toys,
                'target_pet': "CAT",
                'short_description': "360-degree rotating red laser toy that keeps indoor cats fit, stimulated, and agile.",
                'description': "Features variable circular trajectories, auto-timer shutdown, and rechargeable USB battery.",
                'price': 890.00,
                'discount_price': 780.00,
                'stock_quantity': 4, # Low stock demo!
                'is_prescription_required': False,
                'is_featured': True,
                'manufacturer': "PetFun Innovations",
            },
            {
                'name': "Dental Rubber Chew Bone with Mint Flavor (Indestructible)",
                'slug': "dental-rubber-chew-bone",
                'sku': "TOY-DNT-BONE",
                'category': cat_toys,
                'target_pet': "DOG",
                'short_description': "Natural rubber teeth-cleaning chew toy with soft nubs to massage gums.",
                'description': "Cleans teeth and massages gums while dogs play, preventing plaque and tartar buildup.",
                'price': 420.00,
                'discount_price': 370.00,
                'stock_quantity': 0, # Out of stock demo!
                'is_prescription_required': False,
                'is_featured': False,
                'manufacturer': "Kong Canine Gear",
            }
        ]

        for p in products:
            Product.objects.get_or_create(slug=p['slug'], defaults=p)
        self.stdout.write(self.style.SUCCESS("E-Commerce product catalog seeded with stock counts and prices."))

        # 7. Sample Pet and Booking Demo
        demo_pet, _ = Pet.objects.get_or_create(
            name="Charlie",
            owner=admin_user,
            defaults={
                'species': "Dog",
                'breed': "Labrador Retriever",
                'gender': "Male",
                'age_years': 3,
                'age_months': 4,
                'weight_kg': 26.5,
                'medical_history': "Vaccinations up-to-date with DHPPi & Anti-Rabies in May 2026. Routine ear cleaning required."
            }
        )

        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        Appointment.objects.get_or_create(
            booking_id="APT-2610-DEMO1",
            defaults={
                'user': admin_user,
                'pet': demo_pet,
                'owner_name': "Tanvir Rahman",
                'owner_phone': "+8801711223344",
                'owner_email': "tanvir@example.com",
                'owner_address': "Kazihata, Rajshahi",
                'pet_name': "Charlie",
                'pet_species': "Dog",
                'pet_breed': "Labrador Retriever",
                'service_type': "General Health Checkup",
                'appointment_date': tomorrow,
                'appointment_time': datetime.time(17, 0),
                'symptoms': "Annual health assessment, preventative deworming booster, and dental inspection.",
                'status': 'CONFIRMED',
                'doctor_advice': "Scheduled for 5:00 PM slot. Maintain normal diet before checkup."
            }
        )
        self.stdout.write(self.style.SUCCESS("Demo appointment and pet profile initialized."))

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
