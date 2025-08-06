import pika
from app.core.config import settings
from fastapi import BackgroundTasks
from typing import Optional


class NotificationService:
    def __init__(self):
        self.connection = None
        self.channel = None

    async def connect(self):
        """Установка соединения с RabbitMQ"""
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=settings.RABBITMQ_HOST,
                    port=settings.RABBITMQ_PORT,
                    credentials=pika.PlainCredentials(
                        settings.RABBITMQ_USER,
                        settings.RABBITMQ_PASSWORD
                    )
                )
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='notifications', durable=True)

    async def send_notification(self, user_id: int, message: str):
        """Отправка уведомления в очередь"""
        await self.connect()
        self.channel.basic_publish(
            exchange='',
            routing_key='notifications',
            body=f"{user_id}:{message}".encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )

    async def send_email_notification(self, email: str, subject: str, message: str):
        """Отправка email-уведомления (заглушка)"""
        print(f"Sending email to {email}: {subject} - {message}")
        # В реальном проекте подключить SendGrid/Mailgun


async def background_notification(service: NotificationService, user_id: int, message: str):
    """Фоновая задача для отправки уведомлений"""
    await service.send_notification(user_id, message)


def get_notification_service():
    """DI для сервиса уведомлений"""
    return NotificationService()