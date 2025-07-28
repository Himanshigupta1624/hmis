from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db import models
from datetime import timedelta
import logging
import traceback

logger=logging.getLogger(__name__)

@shared_task
def send_email_task(subject,message,recipient_list):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        logger.info(f"Email sent successfully to {recipient_list}")
        return f"Email sent to {len(recipient_list)} recipients"
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        traceback.print_exc()
    raise    
@shared_task
def send_daily_annoucement():
    from announcement.models import Announcement
    from customeruser.models import CustomUser
    
    try:
        today=timezone.now()
        annoucements=Announcement.objects.filter(
            is_active=True,
            start_date__lte=today
        ).filter(
            models.Q(end_date__isnull=True) | models.Q(end_date__gte=today)
        )
        if annoucements.exists():
            users=CustomUser.objects.filter(is_active=True)
        
        for announcement in annoucements :
            if announcement.audience!='all':
                target_users=users.filter(role=announcement.audience)   
            else:
                target_users=users
            email_list=[user.email for user in target_users if user.email]  
            
            if email_list:
                send_email_task.delay(
                    subject=f"Announcement: {announcement.title}",
                    message=announcement.content,
                    recipient_list=email_list
                )     
        logger.info("Daily announcement task completed")   
        return "Daily announcements processed"     
    except Exception as e :
        logger.error(f"Error in daily annoucement task: {str(e)}")
        raise 

@shared_task
def generate_daily_reports():
    try:
        from patient.models import Patient,PatientVisit
        from billing.models import Invoice,Payment
        from pharmacy.models import Prescription   
        from laboratory.models import LabOrder
        
        today=timezone.now().date()
        new_patients=Patient.objects.filter(created_at__date=today).count()
        patient_visits=PatientVisit.objects.filter(visit_date__date=today).count()
        new_invoices=Invoice.objects.filter(created_at__date=today).count()
        payments_received=Payment.objects.filter(payment_date__date=today).count()
        prescriptions=Prescription.objects.filter(created_at__date=today).count()
        lab_orders=LabOrder.objects.filter(created_at__date=today).count()
        report_content = f"""
        Daily Report for {today}
        
        Patient Activity:
        - New Patients: {new_patients}
        - Patient Visits: {patient_visits}
        
        Billing Activity:
        - New Invoices: {new_invoices}
        - Payments Received: {payments_received}
        
        Clinical Activity:
        - Prescriptions: {prescriptions}
        - Lab Orders: {lab_orders}
        """
        
        # Send report to administrators
        from customeruser.models import CustomUser
        admins = CustomUser.objects.filter(role='admin', is_active=True)
        admin_emails = [admin.email for admin in admins if admin.email]
        
        if admin_emails:
            send_email_task.delay(
                subject=f"Daily Report - {today}",
                message=report_content,
                recipient_list=admin_emails
            )
        
        logger.info(f"Daily report generated for {today}")
        return f"Daily report generated and sent to {len(admin_emails)} administrators"
    
    except Exception as e:
        logger.error(f"Error generating daily report: {str(e)}")
        raise
        