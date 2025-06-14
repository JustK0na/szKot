## Dockerized Setup
###  Services
- **`web`**: Flask app in Python 3.12
- **`db`**: MySQL 8.x
- **`updater`**: Python Slim 3.12

### Build and Run Instructions
1. **Build and Start the Application:**
   ```sh
   docker-compose up --build
   ```
   This will build the image and start the Flask app in a container named `szkot-web` or however your project folder is named.
2. **In case of any changes to dump.sql used by docker you need to use this command before building it again:**
   ```sh
   docker-compose down
   ```
  3. **Access the Application:**
   - The Flask app will be available at [http://localhost:5000](http://localhost:5000)

### Logins to database users
1. **Admin**
   Username: root
   Password: root
2. **Przewoznicy**
   Username: can be found using script insert_przewoznicy example username: pkpintercity,kolejeśląski,polregio etc...
   Password: 123 
   Password is the same for every przewoznik by default
3. **Pasażerowie**
   Email: can be found in a dump
   Password: 123 
   Password is the same for every przewoznik by default
### Ports
- **Flask Application:**
  - Exposes port `5000` (mapped to host port `5000`)

