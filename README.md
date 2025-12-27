# SkillBazar - Nepal's Freelance Marketplace

SkillBazar is a comprehensive freelance marketplace platform designed specifically for Nepal, similar to Fiverr but tailored for the Nepali market. The platform supports both Khalti and eSewa payment methods and features a modern, responsive design with a blue gradient theme.

## Features

### User System
- **User Registration & Authentication**: Signup with email, username, and password
- **Profile Management**: Edit bio, skills, profile picture, banner, and social links
- **User Types**: Support for freelancers, buyers, and users who can be both
- **Password Reset**: Email-based password reset functionality

### Freelancer Features
- **Gig Creation**: Create gigs with title, description, category, price, delivery time, and images
- **Gig Management**: Edit and delete gigs from dashboard
- **Order Management**: View and manage received orders
- **Earnings Dashboard**: Track earnings and performance metrics

### Buyer Features
- **Gig Discovery**: Search gigs by keyword, category, and price range
- **Order Placement**: Order gigs with requirements specification
- **Payment Integration**: Support for Khalti and eSewa (demo integration)
- **Messaging**: Chat with freelancers
- **Reviews & Ratings**: Leave reviews and ratings for completed orders

### Platform Features
- **Responsive Design**: Mobile-friendly interface using Bootstrap 5
- **Modern UI**: Blue gradient theme with FontAwesome icons
- **Search & Filter**: Advanced search and filtering capabilities
- **Pagination**: Efficient browsing with pagination
- **Admin Panel**: Comprehensive admin interface for content moderation

## Technology Stack

- **Backend**: Django 4.2.7
- **Frontend**: Bootstrap 5, FontAwesome Icons
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Authentication**: Django Allauth
- **Forms**: Django Crispy Forms with Bootstrap 5
- **Image Handling**: Pillow
- **Payment**: Khalti and eSewa integration (demo)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Skillbazar
   ```

2. **Create virtual environment**
   ```bash
   python -m venv skillbazar_env
   ```

3. **Activate virtual environment**
   - Windows:
     ```bash
     skillbazar_env\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source skillbazar_env/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Populate demo data**
   ```bash
   python manage.py populate_demo_data
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Main site: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

## Demo Content

The platform comes pre-populated with demo content including:

### Demo Users (Nepali Names)
**Male Names**: Prashant, Shishir, Milan, Prasoon, Subodh, Swroop, Shayad, Sakshyam, Kok, Anil, Sabin, Mohammed, Bishow, Dipesh, Sujan, Binaya, Nishan, Samyog, Emon, Buddhi, Pukar, Nischal, Bikal, Nabin, Shreekrishna, Pratap, Dipjung, Ujjwal, Shrijal

**Female Names**: Sonisha, Sayana, Sadikshya, Amisha, Shristi, Aashika, Supriya, Shishila, Ishu

### Demo Gigs
- Logo Design
- Web Development
- Data Entry
- Voice Over in Nepali
- Resume Design
- Python Script Writing
- Photo Editing
- Proofreading
- Digital Marketing for Facebook
- WordPress Website Setup
- Motion Graphics in After Effects
- Content Writing
- Social Media Management
- Excel Data Processing
- Video Editing
- Translation Services
- UI/UX Design
- SEO Optimization
- Database Management
- E-commerce Website
- Brand Identity Design
- Blog Writing
- Video Animation
- Google Ads Management
- PDF to Word Conversion
- Mobile App Development
- Business Card Design
- Technical Writing

## Project Structure

```
Skillbazar/
├── skillbazar/          # Main Django project
│   ├── settings.py      # Project settings
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py          # WSGI configuration
├── users/               # User management app
│   ├── models.py        # Custom user model
│   ├── views.py         # User views
│   └── forms.py         # User forms
├── gigs/                # Gig management app
│   ├── models.py        # Gig and category models
│   ├── views.py         # Gig views
│   └── forms.py         # Gig forms
├── orders/              # Order management app
│   ├── models.py        # Order and review models
│   └── views.py         # Order views
├── messaging/           # Messaging app
│   ├── models.py        # Conversation and message models
│   └── views.py         # Messaging views
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   └── gigs/           # Gig templates
├── static/              # Static files (CSS, JS, images)
├── media/               # User uploaded files
└── manage.py           # Django management script
```

## Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Payment Integration
The platform includes demo payment buttons for Khalti and eSewa. For production:

1. **Khalti Integration**: Add your Khalti merchant credentials
2. **eSewa Integration**: Add your eSewa merchant credentials
3. **Webhook Handling**: Implement webhook endpoints for payment verification

## Deployment

### Production Settings
1. Set `DEBUG = False`
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving
4. Configure email backend
5. Set up proper security settings

### Docker Deployment
```bash
# Build image
docker build -t skillbazar .

# Run container
docker run -p 8000:8000 skillbazar
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## Roadmap

- [ ] Real payment integration
- [ ] Advanced search filters
- [ ] Mobile app development
- [ ] Video calling feature
- [ ] Escrow system
- [ ] Dispute resolution
- [ ] Analytics dashboard
- [ ] API development
- [ ] Multi-language support

---

**SkillBazar** - Connecting Nepal's talented professionals with global opportunities! 🇳🇵 
