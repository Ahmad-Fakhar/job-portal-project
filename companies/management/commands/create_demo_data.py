# companies/management/commands/create_demo_data.py
"""
Management command to create demo data for the job portal.
Run: python manage.py create_demo_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from companies.models import Company, Job
from jobs.models import JobSeeker, Application, SavedJob
from notifications.models import Notification

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates demo data for the job portal'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Creating demo data...'))

        # Create Admin User
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@jobportal.com',
                password='admin123',
                user_type='admin'
            )
            self.stdout.write(self.style.SUCCESS('✓ Admin user created'))
        else:
            admin = User.objects.get(username='admin')
            self.stdout.write(self.style.WARNING('Admin user already exists'))

        # Create Company Users and Companies
        companies_data = [
            {
                'username': 'securecorp',
                'email': 'hr@securecorp.com',
                'company_name': 'SecureCorp Ltd',
                'registration_number': 'REG001',
                'phone': '+44 123 456 7890',
                'city': 'London',
                'state': 'England',
                'description': 'Leading security services provider with over 20 years of experience.',
                'status': 'approved'
            },
            {
                'username': 'guardpro',
                'email': 'info@guardpro.co.uk',
                'company_name': 'GuardPro Security',
                'registration_number': 'REG002',
                'phone': '+44 987 654 3210',
                'city': 'Manchester',
                'state': 'England',
                'description': 'Professional security guard services for commercial and residential properties.',
                'status': 'approved'
            },
            {
                'username': 'elitesecurity',
                'email': 'contact@elitesecurity.com',
                'company_name': 'Elite Security Services',
                'registration_number': 'REG003',
                'phone': '+44 555 123 4567',
                'city': 'Edinburgh',
                'state': 'Scotland',
                'description': 'Elite security solutions for high-profile clients and events.',
                'status': 'pending'
            }
        ]

        for comp_data in companies_data:
            if not User.objects.filter(username=comp_data['username']).exists():
                user = User.objects.create_user(
                    username=comp_data['username'],
                    email=comp_data['email'],
                    password='company123',
                    user_type='company'
                )
                
                company = Company.objects.create(
                    user=user,
                    company_name=comp_data['company_name'],
                    registration_number=comp_data['registration_number'],
                    email=comp_data['email'],
                    phone=comp_data['phone'],
                    address=f'{comp_data["company_name"]} Headquarters',
                    city=comp_data['city'],
                    state=comp_data['state'],
                    description=comp_data['description'],
                    status=comp_data['status']
                )
                
                if comp_data['status'] == 'approved':
                    company.approved_date = timezone.now()
                    company.save()
                
                self.stdout.write(self.style.SUCCESS(f'✓ Created company: {comp_data["company_name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Company {comp_data["username"]} already exists'))

        # Create Job Postings for approved companies
        approved_companies = Company.objects.filter(status='approved')
        
        jobs_data = [
            {
                'title': 'Security Guard - Night Shift',
                'description': 'We are looking for a reliable and experienced security guard for night shift duties. The role involves monitoring premises, conducting patrols, and ensuring the safety of the property.',
                'requirements': '- Minimum 2 years experience\n- SIA License required\n- Good communication skills\n- Ability to work night shifts',
                'responsibilities': '- Monitor CCTV systems\n- Conduct regular patrols\n- Check identification of visitors\n- Report any suspicious activities\n- Maintain security logs',
                'location': 'Central London',
                'job_type': 'full-time',
                'category': 'Security Guard',
                'salary_min': 25000,
                'salary_max': 30000,
                'experience_required': '1-3',
                'vacancies': 3
            },
            {
                'title': 'Security Manager',
                'description': 'Seeking an experienced Security Manager to oversee our security operations. The ideal candidate will have strong leadership skills and extensive experience in security management.',
                'requirements': '- 5+ years in security management\n- Excellent leadership skills\n- SIA Advanced License\n- First Aid certified',
                'responsibilities': '- Manage security team\n- Develop security protocols\n- Conduct risk assessments\n- Train security staff\n- Liaise with management',
                'location': 'Manchester City Centre',
                'job_type': 'full-time',
                'category': 'Security Manager',
                'salary_min': 40000,
                'salary_max': 55000,
                'experience_required': '5+',
                'vacancies': 1
            },
            {
                'title': 'Security Officer - Retail',
                'description': 'Security Officer needed for busy retail environment. Must be customer-friendly while maintaining security standards.',
                'requirements': '- SIA License\n- Retail security experience preferred\n- Customer service skills\n- Conflict resolution abilities',
                'responsibilities': '- Monitor store premises\n- Prevent theft and shoplifting\n- Handle incidents professionally\n- Assist customers when needed\n- Report to management',
                'location': 'Shopping Centre, Manchester',
                'job_type': 'part-time',
                'category': 'Security Officer',
                'salary_min': 12,
                'salary_max': 15,
                'experience_required': '0-1',
                'vacancies': 5
            },
            {
                'title': 'Event Security Coordinator',
                'description': 'Coordinate security for large-scale events. Experience in event management and crowd control essential.',
                'requirements': '- Event security experience\n- Crowd management skills\n- SIA License\n- Excellent communication\n- Driving license',
                'responsibilities': '- Plan event security\n- Coordinate security teams\n- Manage crowd control\n- Liaise with event organizers\n- Handle emergencies',
                'location': 'Various Locations',
                'job_type': 'contract',
                'category': 'Security Coordinator',
                'salary_min': 35000,
                'salary_max': 45000,
                'experience_required': '3-5',
                'vacancies': 2
            },
            {
                'title': 'CCTV Operator',
                'description': 'CCTV Operator needed to monitor surveillance systems. Must have sharp observation skills and attention to detail.',
                'requirements': '- CCTV operation experience\n- SIA CCTV License\n- Good observation skills\n- Report writing abilities\n- Computer literate',
                'responsibilities': '- Monitor CCTV systems\n- Identify suspicious activities\n- Record incidents\n- Communicate with security teams\n- Maintain equipment',
                'location': 'Control Room, London',
                'job_type': 'full-time',
                'category': 'CCTV Operator',
                'salary_min': 23000,
                'salary_max': 28000,
                'experience_required': '1-3',
                'vacancies': 2
            }
        ]

        for i, company in enumerate(approved_companies):
            # Create 2-3 jobs per company
            for j in range(min(3, len(jobs_data))):
                job_data = jobs_data[(i * 3 + j) % len(jobs_data)]
                
                if not Job.objects.filter(
                    company=company,
                    title=job_data['title']
                ).exists():
                    job = Job.objects.create(
                        company=company,
                        city=company.city,
                        deadline=timezone.now().date() + timedelta(days=30),
                        **job_data
                    )
                    job.posted_date = timezone.now() - timedelta(days=j)
                    job.save()
                    
                    self.stdout.write(self.style.SUCCESS(f'✓ Created job: {job.title} for {company.company_name}'))

        # Create Job Seeker Users
        jobseekers_data = [
            {
                'username': 'john_doe',
                'email': 'john.doe@email.com',
                'full_name': 'John Doe',
                'phone': '+44 7700 900123',
                'city': 'London',
                'skills': 'Security operations, CCTV monitoring, First Aid, Conflict resolution',
                'education': 'Secondary School Certificate\nSecurity Training Course - 2020',
                'experience': 'Security Guard at Mall Security Ltd (2020-2023)\n- Conducted regular patrols\n- Monitored CCTV systems\n- Handled incidents professionally'
            },
            {
                'username': 'sarah_smith',
                'email': 'sarah.smith@email.com',
                'full_name': 'Sarah Smith',
                'phone': '+44 7700 900456',
                'city': 'Manchester',
                'skills': 'Team management, Risk assessment, Emergency response, Customer service',
                'education': 'Bachelor in Security Management\nAdvanced SIA License',
                'experience': 'Security Supervisor at SecureNow Ltd (2018-2024)\n- Managed team of 10 guards\n- Conducted security audits\n- Implemented new protocols'
            },
            {
                'username': 'mike_johnson',
                'email': 'mike.johnson@email.com',
                'full_name': 'Mike Johnson',
                'phone': '+44 7700 900789',
                'city': 'Birmingham',
                'skills': 'Access control, Patrol operations, Report writing, Communication',
                'education': 'High School Diploma\nSIA Door Supervisor License',
                'experience': 'Door Supervisor at Various Venues (2021-Present)\n- Managed venue entry\n- Checked IDs\n- Maintained order'
            }
        ]

        for seeker_data in jobseekers_data:
            if not User.objects.filter(username=seeker_data['username']).exists():
                user = User.objects.create_user(
                    username=seeker_data['username'],
                    email=seeker_data['email'],
                    password='jobseeker123',
                    user_type='jobseeker'
                )
                
                jobseeker = JobSeeker.objects.create(
                    user=user,
                    full_name=seeker_data['full_name'],
                    email=seeker_data['email'],
                    phone=seeker_data['phone'],
                    address=f'{seeker_data["full_name"]} Address',
                    city=seeker_data['city'],
                    skills=seeker_data['skills'],
                    education=seeker_data['education'],
                    experience=seeker_data['experience']
                )
                
                self.stdout.write(self.style.SUCCESS(f'✓ Created job seeker: {seeker_data["full_name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Job seeker {seeker_data["username"]} already exists'))

        # Create Sample Applications
        jobseekers = User.objects.filter(user_type='jobseeker')
        jobs = Job.objects.filter(is_active=True)[:5]

        for seeker in jobseekers:
            for i, job in enumerate(jobs[:2]):  # Each seeker applies to 2 jobs
                if not Application.objects.filter(job=job, applicant=seeker).exists():
                    Application.objects.create(
                        job=job,
                        applicant=seeker,
                        cover_letter=f'I am writing to express my interest in the {job.title} position at {job.company.company_name}. With my experience and skills in security services, I believe I would be a valuable addition to your team. I am passionate about maintaining safety and security, and I am confident in my ability to contribute effectively to your organization.',
                        status=['submitted', 'under_review', 'shortlisted'][i % 3]
                    )
                    self.stdout.write(self.style.SUCCESS(f'✓ Created application: {seeker.username} -> {job.title}'))

        # Create Notifications
        for company_user in User.objects.filter(user_type='company'):
            try:
                company = company_user.company_profile
                if company.status == 'approved':
                    Notification.objects.get_or_create(
                        user=company_user,
                        title='Company Approved',
                        message=f'Congratulations! Your company "{company.company_name}" has been approved. You can now post jobs.',
                        notification_type='approval'
                    )
            except Company.DoesNotExist:
                pass

        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('Demo data created successfully!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(self.style.WARNING('\nLogin Credentials:'))
        self.stdout.write(self.style.WARNING('Admin: admin / admin123'))
        self.stdout.write(self.style.WARNING('Company: securecorp / company123'))
        self.stdout.write(self.style.WARNING('Job Seeker: john_doe / jobseeker123'))
        self.stdout.write(self.style.SUCCESS('='*50))