## Running the Project with Docker

This project provides a Docker setup for running the Flask application in an isolated environment. Below are the key details and instructions specific to this project:
Most of this readme was genereated using ChatGPT so the infroamtion here is kinda bad.
### Project-Specific Docker Requirements
- **Python Version:** 3.12 (as specified in the Dockerfile: `python:3.12-slim`)
- **System Dependencies:**
  - `gcc`, `default-libmysqlclient-dev`,'libcairo2-dev','libcups2-dev','python3-dev', `build-essential` (for MySQL client support and building Python packages)
- **Python Dependencies:** Installed from `requirements.txt` inside a virtual environment (`.venv`)

### Environment Variables
- `FLASK_APP=flaskTest.py` (set in Dockerfile)
- `FLASK_RUN_HOST=0.0.0.0` (set in Dockerfile)
- No additional environment variables are required unless you add a database service (see below).

### Build and Run Instructions
1. **Build and Start the Application:**
   ```sh
   docker compose up --build
   ```
  This will build the image and start the Flask app in a container named `python-app`.

2. **Only build the image**
   ```sh
   docker build -t szkot .
   ```
3. **To run built application from the image**
    ```sh
    docker run -it --rm -p 5000:5000 --name flask-app szkot
    ```
    Rm causes container to delete itself after exiting out of it as far as I understand it so be careful
3. **Access the Application:**
   - The Flask app will be available at [http://localhost:5000](http://localhost:5000)

### Ports
- **Flask Application:**
  - Exposes port `5000` (mapped to host port `5000`)

### Special Configuration
- The application runs as a non-root user (`appuser`) inside the container for improved security.
- The `templates/` directory and `flaskTest.py` are included in the container; if you need to include `the_one_that_does_it_all.py`, uncomment the relevant line in the Dockerfile.
- If you require a MySQL database, an example service is provided in the `docker-compose.yml` (commented out). Uncomment and configure as needed, and update your Flask app's database connection settings accordingly.

### Notes
- No `.env` file is required by default, but you can add one and uncomment the `env_file` line in the compose file if needed.
- The `venv/` directory is not used inside the container; a fresh virtual environment is created during the build process.

---

*Update this section if you modify the Docker or Compose setup.*