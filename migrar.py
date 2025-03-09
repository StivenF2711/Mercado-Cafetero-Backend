import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')  # Ajusta el nombre de tu proyecto
django.setup()

from django.core.management import call_command

print("🔄 Ejecutando migraciones en Railway...")
call_command('migrate')
print("✅ Migraciones aplicadas correctamente.")
