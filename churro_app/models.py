from django.db import models

class Churro(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    imageUrl = models.URLField()

    def __str__(self):
        return self.name

class Survey(models.Model):
    experience = models.CharField(max_length=200)
    feedback = models.TextField()

    def __str__(self):
        return f"Survey {self.id} - {self.experience}"

class Career(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')

    def __str__(self):
        return self.name

class Contact(models.Model):
    method = models.CharField(max_length=50)  
    name = models.CharField(max_length=100, null=True, blank=True)  
    email = models.EmailField(null=True, blank=True)  
    message = models.TextField()

    def __str__(self):
        return f"{self.method} - {self.name or ''}"

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    items = models.ManyToManyField(MenuItem, through='OrderItem')

    def __str__(self):
        return f"Order {self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.item.name} x {self.quantity}"


class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    eventType = models.CharField(max_length=100)
    date = models.DateField()
    additionalInfo = models.TextField()

    def __str__(self):
        return f"Booking for {self.eventType} on {self.date} by {self.name}"