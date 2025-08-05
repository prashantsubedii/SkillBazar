from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from gigs.models import Category, Gig
from decimal import Decimal
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate database with demo data for SkillBazar'

    def handle(self, *args, **options):
        self.stdout.write('Creating demo data for SkillBazar...')

        # Create categories
        categories_data = [
            {'name': 'Web Development', 'slug': 'web-development', 'icon': 'fas fa-code'},
            {'name': 'Graphic Design', 'slug': 'graphic-design', 'icon': 'fas fa-palette'},
            {'name': 'Digital Marketing', 'slug': 'digital-marketing', 'icon': 'fas fa-bullhorn'},
            {'name': 'Data Entry', 'slug': 'data-entry', 'icon': 'fas fa-database'},
            {'name': 'Voice Over', 'slug': 'voice-over', 'icon': 'fas fa-microphone'},
            {'name': 'Video Editing', 'slug': 'video-editing', 'icon': 'fas fa-video'},
            {'name': 'Content Writing', 'slug': 'content-writing', 'icon': 'fas fa-pen'},
            {'name': 'Translation', 'slug': 'translation', 'icon': 'fas fa-language'},
            {'name': 'Other', 'slug': 'other', 'icon': 'fas fa-ellipsis-h'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'icon': cat_data['icon'],
                    'description': f'Professional {cat_data["name"].lower()} services'
                }
            )
            categories[cat_data['slug']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Demo users data
        male_names = [
            'Prashant', 'Shishir', 'Milan', 'Prasoon', 'Subodh', 'Swroop', 'Shayad', 
            'Sakshyam', 'Kok', 'Anil', 'Sabin', 'Mohammed', 'Bishow', 'Dipesh', 'Sujan', 
            'Binaya', 'Nishan', 'Samyog', 'Emon', 'Buddhi', 'Pukar', 'Nischal', 'Bikal', 
            'Nabin', 'Shreekrishna', 'Pratap', 'Dipjung', 'Ujjwal', 'Shrijal'
        ]
        
        female_names = [
            'Sonisha', 'Sayana', 'Sadikshya', 'Amisha', 'Shristi', 'Aashika', 
            'Supriya', 'Shishila', 'Ishu'
        ]

        # Demo gigs data
        gigs_data = [
            {'title': 'Logo Design', 'category': 'graphic-design', 'price': 2500, 'delivery': 3},
            {'title': 'Web Development', 'category': 'web-development', 'price': 15000, 'delivery': 7},
            {'title': 'Data Entry', 'category': 'data-entry', 'price': 800, 'delivery': 2},
            {'title': 'Voice Over in Nepali', 'category': 'voice-over', 'price': 1200, 'delivery': 1},
            {'title': 'Resume Design', 'category': 'graphic-design', 'price': 1500, 'delivery': 2},
            {'title': 'Python Script Writing', 'category': 'web-development', 'price': 5000, 'delivery': 5},
            {'title': 'Photo Editing', 'category': 'graphic-design', 'price': 1000, 'delivery': 1},
            {'title': 'Proofreading', 'category': 'content-writing', 'price': 800, 'delivery': 2},
            {'title': 'Digital Marketing for Facebook', 'category': 'digital-marketing', 'price': 3000, 'delivery': 4},
            {'title': 'WordPress Website Setup', 'category': 'web-development', 'price': 8000, 'delivery': 6},
            {'title': 'Motion Graphics in After Effects', 'category': 'video-editing', 'price': 12000, 'delivery': 7},
            {'title': 'Content Writing', 'category': 'content-writing', 'price': 1500, 'delivery': 3},
            {'title': 'Social Media Management', 'category': 'digital-marketing', 'price': 5000, 'delivery': 5},
            {'title': 'Excel Data Processing', 'category': 'data-entry', 'price': 1200, 'delivery': 2},
            {'title': 'Video Editing', 'category': 'video-editing', 'price': 8000, 'delivery': 5},
            {'title': 'Translation Services', 'category': 'translation', 'price': 2000, 'delivery': 3},
            {'title': 'UI/UX Design', 'category': 'graphic-design', 'price': 15000, 'delivery': 10},
            {'title': 'SEO Optimization', 'category': 'digital-marketing', 'price': 4000, 'delivery': 4},
            {'title': 'Database Management', 'category': 'data-entry', 'price': 3000, 'delivery': 3},
            {'title': 'E-commerce Website', 'category': 'web-development', 'price': 25000, 'delivery': 14},
            {'title': 'Brand Identity Design', 'category': 'graphic-design', 'price': 8000, 'delivery': 7},
            {'title': 'Blog Writing', 'category': 'content-writing', 'price': 2000, 'delivery': 3},
            {'title': 'Video Animation', 'category': 'video-editing', 'price': 15000, 'delivery': 10},
            {'title': 'Google Ads Management', 'category': 'digital-marketing', 'price': 6000, 'delivery': 5},
            {'title': 'PDF to Word Conversion', 'category': 'data-entry', 'price': 500, 'delivery': 1},
            {'title': 'Mobile App Development', 'category': 'web-development', 'price': 35000, 'delivery': 21},
            {'title': 'Business Card Design', 'category': 'graphic-design', 'price': 1000, 'delivery': 1},
            {'title': 'Technical Writing', 'category': 'content-writing', 'price': 3000, 'delivery': 4},
        ]

        # Create demo users and gigs
        all_names = male_names + female_names
        created_users = []

        for i, name in enumerate(all_names[:30]):  # Create 30 users
            username = name.lower()
            email = f'{username}@skillbazar.com'
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': name,
                    'last_name': '',
                    'user_type': 'freelancer',
                    'bio': f'Professional freelancer with expertise in various fields. {name} is a skilled professional ready to help with your projects.',
                    'skills': 'Professional, Reliable, Creative, Detail-oriented',
                    'hourly_rate': Decimal(random.randint(500, 2000)),
                    'rating': Decimal(random.uniform(4.0, 5.0)).quantize(Decimal('0.01')),
                    'total_reviews': random.randint(5, 50),
                }
            )
            created_users.append(user)
            if created:
                self.stdout.write(f'Created user: {user.username}')

        # Create gigs
        for i, gig_data in enumerate(gigs_data):
            user = created_users[i % len(created_users)]
            category = categories[gig_data['category']]
            
            gig, created = Gig.objects.get_or_create(
                title=gig_data['title'],
                freelancer=user,
                defaults={
                    'category': category,
                    'slug': slugify(f"{gig_data['title']}-{user.username}"),
                    'description': f"Professional {gig_data['title'].lower()} service. I provide high-quality work with quick delivery. Contact me for your {gig_data['title'].lower()} needs.",
                    'price': Decimal(gig_data['price']),
                    'delivery_time': gig_data['delivery'],
                    'rating': Decimal(random.uniform(4.0, 5.0)).quantize(Decimal('0.01')),
                    'total_reviews': random.randint(3, 25),
                    'views': random.randint(10, 200),
                }
            )
            if created:
                self.stdout.write(f'Created gig: {gig.title} by {gig.freelancer.username}')

        self.stdout.write(
            self.style.SUCCESS('Successfully created demo data for SkillBazar!')
        ) 