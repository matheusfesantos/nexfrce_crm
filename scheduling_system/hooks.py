app_name = "scheduling_system"
app_title = "Scheduling System"
app_publisher = "Matheus"
app_description = "Sistema de agendamento de compromissos"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "matheus@example.com"
app_license = "MIT"

doctype_list = ["Appointment"]

calendar_views = {
    "Appointment": {
        "fields": {
            "start": "start_date",
            "end": "end_date",
            "title": "client_name"
        },
        "filters": {
            "status": "Scheduled"
        }
    }
}