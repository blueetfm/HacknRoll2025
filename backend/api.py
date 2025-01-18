import os
from dotenv import load_dotenv
from supabase_py import create_client, Client

class Supabase:
    def __init__(self, toggle: bool):
        """Initialises Supabase Backend

        Args:
            toggle (bool): If True, Supabase will be instantiated. Disables Supabase functionality if False
        """
        if toggle:
            # Load environment variables from the .env file
            dotenv_path = os.path.join("venv", ".env")  # Adjust path if needed
            load_dotenv(dotenv_path)

            # Retrieve environment variables
            self.url: str = os.environ.get("SUPABASE_URL")
            self.key: str = os.environ.get("SUPABASE_KEY")

            if not self.url or not self.key:
                raise ValueError("Supabase URL or Key is missing in the .env file")

            # Instantiate the Supabase client
            self.supabase: Client = create_client(self.url, self.key)

            # Log success
            print(f"Supabase client initialized with URL: {self.url}")
        else:
            self.supabase = None
            print("Supabase functionality disabled")
    def insert_data(self, table_name:str,data:dict):
        try:
            # Insert data into the specified table
            response = self.supabase.table(table_name).insert(data).execute()
            
            # Check for errors in the response
            if response.get("status_code") not in [200, 201]:
                return {"error": f"Failed to insert data: {response}"}
            
            return {"success": response.get("data")}
        except Exception as e:
            return {"error": str(e)}
    def retrieve_data(self, table_name:str):
        response = self.supabase.table(table_name).select("*").execute()
        return response

# Usage Example
supabase_instance = Supabase(toggle=True)


if supabase_instance.supabase:
    data = supabase_instance.retrieve_data("countries")
    print(data)





