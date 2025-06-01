## Dockerized Setup
###  Services
- **`web`**: Flask app in Python 3.12
- **`db`**: MySQL 8.x

### Build and Run Instructions
1. **Build and Start the Application:**
   ```sh
   docker compose up --build
   ```
  This will build the image and start the Flask app in a container named `szkot-web` or however your project folder is named.
3. **Access the Application:**
   - The Flask app will be available at [http://localhost:5000](http://localhost:5000)

### Ports
- **Flask Application:**
  - Exposes port `5000` (mapped to host port `5000`)

