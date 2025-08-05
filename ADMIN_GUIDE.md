# 🔐 SkillBazar Admin Panel Guide

## 📋 Admin Credentials

| Field | Value |
|-------|-------|
| **Username** | `admin` |
| **Password** | `admin123` |
| **Email** | `admin@skillbazar.com` |
| **Admin URL** | `http://localhost:8000/admin/` |

## 🚀 How to Access Admin Panel

1. **Start the Django server:**
   ```bash
   python manage.py runserver
   ```

2. **Open your browser and go to:**
   ```
   http://localhost:8000/admin/
   ```

3. **Login with the credentials above**

## 📊 Admin Panel Features

### 👥 User Management
- **CustomUser Model**: Manage all users (freelancers, buyers, admins)
- **User Types**: Filter by freelancer, buyer, or admin
- **Profile Management**: Edit user profiles, skills, ratings, earnings
- **Account Status**: Activate/deactivate user accounts

### 🎯 Gig Management
- **Categories**: Create and manage gig categories
- **Gigs**: View, edit, and manage all gigs
- **Gig Status**: Activate/deactivate gigs
- **Gig Analytics**: View views, ratings, and reviews

### 💼 Order Management
- **Orders**: Track all orders and their status
- **Order Details**: View order amounts, buyers, freelancers
- **Order Status**: Update order status (pending, completed, cancelled)

### ⭐ Review System
- **Reviews**: Manage all gig reviews
- **Rating Management**: View and moderate ratings
- **Review Analytics**: Track review statistics

### 💬 Messaging System
- **Conversations**: Monitor user conversations
- **Messages**: View message history
- **Message Status**: Track read/unread messages

## 🔧 Admin Actions

### Creating New Admin Users
```bash
python manage.py createsuperuser
```

### Changing Admin Password
```bash
python manage.py changepassword admin
```

### Database Management
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create demo data
python manage.py populate_demo_data
```

## 📈 Admin Dashboard Features

### User Analytics
- Total users count
- User type distribution
- User registration trends
- Active/inactive users

### Gig Analytics
- Total gigs count
- Category-wise gig distribution
- Popular gigs
- Gig performance metrics

### Order Analytics
- Total orders
- Revenue tracking
- Order status distribution
- Payment analytics

### Review Analytics
- Average ratings
- Review count
- Rating distribution
- Review trends

## 🛡️ Security Features

- **CSRF Protection**: All forms are CSRF protected
- **Session Management**: Secure session handling
- **Permission System**: Role-based access control
- **Audit Trail**: Track admin actions

## 📱 Admin Panel Customization

The admin panel is fully customized for SkillBazar with:

- **Custom User Admin**: Enhanced user management interface
- **Gig Admin**: Specialized gig management features
- **Order Admin**: Comprehensive order tracking
- **Review Admin**: Review moderation tools
- **Messaging Admin**: Conversation management

## 🚨 Important Notes

1. **Change Default Password**: Change the default password after first login
2. **Backup Database**: Regularly backup your database
3. **Monitor Activity**: Keep track of admin actions
4. **User Privacy**: Respect user privacy when accessing data
5. **Regular Updates**: Keep Django and dependencies updated

## 🔗 Quick Links

- **Main Site**: `http://localhost:8000/`
- **Admin Panel**: `http://localhost:8000/admin/`
- **User Dashboard**: `http://localhost:8000/users/dashboard/`
- **Gig List**: `http://localhost:8000/gigs/`

## 📞 Support

If you encounter any issues with the admin panel:
1. Check Django logs
2. Verify database connections
3. Ensure all migrations are applied
4. Contact the development team

---

**⚠️ Security Reminder**: Always use strong passwords and change the default admin password immediately after setup! 