import random
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from tasks.models import Skill, Task, UserProfile

# ------------------------------------
# Define your static data
# ------------------------------------
skills_list = [
    "Plumbing", "Electrical", "Carpentry", "Painting", "Cleaning", "Landscaping", 
    "Gardening", "Cooking", "Tutoring", "Pet Sitting", "Babysitting"
]

locations_with_coords = [
    {"name": "LPU Main Gate, Phagwara", "lat": 31.2554, "lng": 75.7050},
    {"name": "Chaheru Railway Station, Phagwara", "lat": 31.2637, "lng": 75.7203},
    {"name": "Jalandhar Bus Stand", "lat": 31.3260, "lng": 75.5762},
    {"name": "Model Town, Jalandhar", "lat": 31.3134, "lng": 75.5918},
    {"name": "Urban Estate Phase 2, Jalandhar", "lat": 31.3085, "lng": 75.5939},
    {"name": "GT Road, Phagwara", "lat": 31.2230, "lng": 75.7698},
    {"name": "Hoshiarpur Road, Jalandhar", "lat": 31.3380, "lng": 75.5971},
    {"name": "Railway Road, Phagwara", "lat": 31.2215, "lng": 75.7718},
    {"name": "Punjab Institute of Medical Sciences", "lat": 31.3261, "lng": 75.5791},
    {"name": "Jalandhar Cantt", "lat": 31.3048, "lng": 75.6167},
    {"name": "Adampur, Jalandhar", "lat": 31.4320, "lng": 75.7140},
    {"name": "Phagwara Junction", "lat": 31.2273, "lng": 75.7736},
    {"name": "Maqsudan, Jalandhar", "lat": 31.3421, "lng": 75.5684},
]

# ------------------------------------
# Populate Skills
# ------------------------------------
def populate_skills():
    for skill_name in skills_list:
        Skill.objects.get_or_create(name=skill_name)
    print(f"✅ {len(skills_list)} skills ensured in database.")

# ------------------------------------
# Populate Users
# ------------------------------------
def populate_users(num_users=50):
    for i in range(num_users):
        username = f'user{i}'
        email = f'user{i}@example.com'
        password = 'password123'
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, email=email, password=password)
            user_profile = user.userprofile
            user_profile.latitude = random.uniform(31.2, 31.4)  # Roughly around Jalandhar/Phagwara
            user_profile.longitude = random.uniform(75.5, 75.8)
            user_profile.save()

            # Assign 3-6 random skills
            user_skills = random.sample(list(Skill.objects.all()), random.randint(3, 6))
            user_profile.skills.set(user_skills)

            print(f"✅ Created user {username} with skills {[s.name for s in user_skills]}")
    print(f"\n🎯 {num_users} users populated successfully.\n")

# ------------------------------------
# Populate Tasks
# ------------------------------------
def populate_tasks():
    all_users = list(User.objects.all())
    all_skills = list(Skill.objects.all())

    task_data = []
    task_skills_mapping = []

    for location in locations_with_coords:
        creator = random.choice(all_users)
        selected_skill = random.choice(all_skills)

        task_title = f"{selected_skill.name} work at {location['name']}"
        task_description = f"Need someone skilled in {selected_skill.name.lower()} around {location['name']}."

        task_info = {
            "title": task_title,
            "description": task_description,
            "latitude": location['lat'],
            "longitude": location['lng'],
            "location": location['name'],
            "available_from": timezone.now(),
            "available_to": timezone.now() + timedelta(days=random.randint(1, 5)),
            "payment": round(random.uniform(1000, 5000), 2),
            "duration_in_minutes": random.randint(60, 240),
            "status": random.choice(['available', 'in_progress']),
            "creator": creator,
        }

        task_data.append(task_info)
        task_skills_mapping.append([selected_skill])

    # Save tasks
    for idx, task_info in enumerate(task_data):
        task = Task.objects.create(
            title=task_info["title"],
            description=task_info["description"],
            latitude=task_info["latitude"],
            longitude=task_info["longitude"],
            location=task_info["location"],
            available_from=task_info["available_from"],
            available_to=task_info["available_to"],
            payment=task_info["payment"],
            duration_in_minutes=task_info["duration_in_minutes"],
            status=task_info["status"],
            creator=task_info["creator"],
        )

        task.skills.set(task_skills_mapping[idx])
        print(f"✅ Created task: {task.title} with skills {[skill.name for skill in task_skills_mapping[idx]]}")

    print("\n🎯 All tasks created successfully with correct skill mapping!\n")

# ------------------------------------
# MAIN FUNCTION TO CALL
# ------------------------------------
def run():
    populate_skills()
    populate_users(10)
    populate_tasks()

