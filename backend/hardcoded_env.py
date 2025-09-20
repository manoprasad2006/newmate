"""
Hardcoded environment configuration for branch1
This file contains all the environment variables hardcoded for easy deployment
"""

import os

# Set hardcoded environment variables
os.environ['SUPABASE_URL'] = 'https://kjoqiorgzdiinamsauzb.supabase.co'
os.environ['SUPABASE_ANON_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtqb3Fpb3JnemRpaW5uYW1zYXV6YiI0LCJyb2xlIjoiYW5vbiIsImlhdCI6MTc1ODM5NDI1MiwiZXhwIjoyMDczOTcwMjUyfQ.X44ZMzJtMN2d2vADbu5hww9tkKLxyVAdTtklqPVQUpA'
os.environ['SUPABASE_SERVICE_ROLE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtqb3Fpb3JnemRpaW5uYW1zYXV6YiI0LCJyb2xlIjoic2VydmljZV9yb2xlIiwiaWF0IjoxNzU4Mzk0MjUyLCJleHAiOjIwNzM5NzAyNTJ9.N_dH6KMFI9UTuH5ht9S5Uu2CJ8f4C1LEuWNHVakN1Ic'
os.environ['POSTGRES_USER'] = 'certverifier'
os.environ['POSTGRES_PASSWORD'] = 'your-db-password-here'
os.environ['POSTGRES_DB'] = 'certificate_verification'
os.environ['SECRET_KEY'] = 'your-super-secret-key-for-production-hardcoded'
os.environ['DEBUG'] = 'False'
os.environ['ENVIRONMENT'] = 'production'
os.environ['BACKEND_PORT'] = '8000'
os.environ['FRONTEND_PORT'] = '3000'
os.environ['STORAGE_BUCKET'] = 'certificates'
os.environ['MAX_FILE_SIZE'] = '10485760'
os.environ['USE_GPU'] = 'false'
os.environ['GEMINI_API_KEY'] = 'AIzaSyApje8wDzq4SwS0yjDxhy4ss2wVeH3rjts'

print("✅ Hardcoded environment variables set successfully!")
