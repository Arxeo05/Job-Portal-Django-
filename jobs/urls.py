from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # User
    path("user_login/", views.user_login, name="user_login"),
    path("signup/", views.signup, name="signup"),
    path("edit_pass/",views.edit_pass, name="edit_pass"),
    path("user_homepage/", views.user_homepage, name="user_homepage"),
    path("edituser/", views.edituser, name="edituser"),
    path("logout/", views.Logout, name="logout"),
    path("all_jobs/", views.all_jobs, name="all_jobs"),
    path("job_detail/<int:myid>/", views.job_detail, name="job_detail"),
    path("job_apply/<int:myid>/", views.job_apply, name="job_apply"),

    # Company
    path("company_signup/", views.company_signup, name="company_signup"),
    path("company_homepage/", views.company_homepage, name="company_homepage"),
    path("edit_company/", views.edit_company, name="editcompany"),
    path("add_job/", views.add_job, name="add_job"),
    path("job_list/", views.job_list, name="job_list"),
    path("edit_job/<int:myid>/", views.edit_job, name="edit_job"),
    path("delete_job/<int:myid>/",views.delete_job,name="delete_job"),
    path("company_logo/<int:myid>/", views.company_logo, name="company_logo"),
    path("all_applicants/", views.all_applicants, name="all_applicants"),
    path("company_changepass/",views.company_changepass, name="company_changepass"),

    # admin
    path("view_applicants/", views.view_applicants, name="view_applicants"),
    path("delete_applicant/<int:aid>/", views.delete_applicant, name="delete_applicant"),
    path("applicant_info/<int:aid>/", views.applicant_info, name="applicant_info"),
    path("pending_companies/", views.pending_companies, name="pending_companies"),
    path("accepted_companies/", views.accepted_companies, name="accepted_companies"),
    path("rejected_companies/", views.rejected_companies, name="rejected_companies"),
    path("all_companies/", views.all_companies, name="all_companies"),
    path("change_status/<int:myid>/", views.change_status, name="change_status"),
    path("delete_company/<int:myid>/", views.delete_company, name="delete_company"),
    path("listed_jobs/",views.listed_jobs,name="listed_jobs"),
    path("accepted_jobs/",views.accepted_jobs,name="accepted_jobs"),
    path("pending_jobs/",views.pending_jobs,name="pending_jobs"),
    path("rejected_jobs/",views.rejected_jobs,name="rejected_jobs"),
    path("edit_applicant/<int:aid>/",views.edit_applicant,name="edit_applicant"),
    path("admin_editjob/<int:myid>/",views.admin_editjob,name="admin_editjob"),
    path("admin_deletejob/<int:myid>/",views.admin_deletejob,name="admin_deletejob"),
    path("admin_editpass/<int:uid>/",views.admin_editpass, name="admin_editpass"),
    path("activity_logs/",views.activity_logs, name="activity_logs"),
]