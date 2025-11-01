from django.db import models

class Hecho(models.Model):
    descripcion = models.CharField(max_length=255)
    pregunta = models.CharField(max_length=255)  # Ejemplo: "¿El computador enciende?"

    def __str__(self):
        return self.descripcion


class Regla(models.Model):
    hecho = models.CharField(max_length=100, blank=True, blank=True)    # condición única (ej: "no_enciende")
    conclusion = models.CharField(max_length=100)  # ej: "Fallo en fuente de poder"
    peso = models.IntegerField(default=1)
    explicacion_humana = models.TextField(blank=True, null=True, help_text="Explicación amigable para el usuario")

    def __str__(self):
        return f"SI {self.hecho} ENTONCES {self.conclusion} (Peso: {self.peso})"

