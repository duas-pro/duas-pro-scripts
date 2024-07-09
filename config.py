import os
from supabase import create_client
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv('../.env')

supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

openai = OpenAI()
