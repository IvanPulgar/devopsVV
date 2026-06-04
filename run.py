import os
from dotenv import load_dotenv
from app.app import create_app

load_dotenv()

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('DEBUG', 'true').lower() == 'true'
    print(f"  Task Manager corriendo en http://{host}:{port}")
    print(f"  Ambiente: {os.getenv('APP_ENV', 'development')}")
    app.run(host=host, port=port, debug=debug)
