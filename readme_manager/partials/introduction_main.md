# Clock Work

This WhatsApp clone project provides a comprehensive chat application with various advanced features. Below are the main components and functionalities of the project.

## Project Features

1. **Account Functionality:** Complete account management.
2. **PostgreSql Integration:** Utilized as a database.
3. **AWS S3/MinIO Integration:** For file storage.
4. **Redis Integration:** Utilized for caching and message pub/sub.
5. **Autocomplete JS Library:** Implemented for enhanced user experience.
6. **MailJet Integration:** Used for email services.
7. **Dockerized Project:** Fully containerized for easy deployment.
8. **Kubernetes-native** Kubernetes support also available.
9. **CI/CD Pipeline:** Continuous integration and deployment included using Jenkins.

## Email Scheduler 

1.	Task Scheduling with Celery Beat: Implemented Celery Beat to schedule emails as reminders, ensuring timely delivery based on predefined schedules.
2.	Async Operations in Signals: Utilized async-io within Django signals to prevent conflicts with sync_to_async, ensuring smooth task execution without interference.
3.	Task Completion Notification: Upon task completion, an automatic notification is sent to the user, keeping them informed in real-time.
4.	Progress Tracking: A progress bar is implemented to visually display the progress of both scheduled and non-scheduled emails, providing users with real-time status updates.
5.	Redis as a Message Broker: Redis is employed as the message broker, facilitating the efficient handling and distribution of tasks to Celery workers.
6.	Email Task Workflow:
•	Immediate Email Requests: When a user requests to send notes via email, the Django application sends a task to the Redis broker. This task is processed by Celery, with progress being saved in the CELERY_RESULT_BACKEND. Users can track progress via two methods:
•	AJAX Calls: Users can continuously query the status, though this may increase server load.
•	WebSockets and Channels: A WebSocket connection is established upon loading the webpage, allowing the server to push status updates directly to the frontend without repeated user requests. Redis is used in the channel layer for quick response and real-time progress updates.
7.	Scheduled Email Reminders: For scheduled email reminders, the Django view creates a cron task, which is assigned to Celery Beat. When the scheduled time arrives, the task is passed to the broker, and then to Celery for execution. Upon task completion, a notification is sent through channels to the frontend, informing the user of the task’s completion.
8.	Admin Notifications: Admins can broadcast notifications to all users through Django channels. These notifications can be scheduled via cron and Celery Beat, and when the time arrives, the task is processed and sent to users connected to the channels, ensuring real-time updates.

[alt text](https://github.com/arpansahu/clock_work/blob/master/explanation.png?raw=true)

