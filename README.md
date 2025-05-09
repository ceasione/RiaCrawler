
# RiaCrawler

A daily crawler that scrapes used car ads from RIA and stores the data in a local database.

---

##  Project Structure

- **`crawler.py`** – Visits each advertisement, collects data, and sends it to the database.
- **`db.py`** – Manages database connections and inserts collected data.
- **`feeder.py`** – Navigates the search pages, gathers advertisement URLs, and handles pagination.
- **`main.py`** – Entry point that ties all components together.
- **`networker.py`** – Provides a networking abstraction layer.
- **`scheduler.py`** – Schedules jobs based on the times set in the `.env` file.

---

##  Getting Started

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ceasione/RiaCrawler.git
   
2. **Prepare the environment variables:**

- Copy the **.env_example** file and fill in your **USER_AGENT** and **cookies**.
- Rename the file to **.env**.
   
3. **Navigate to the project directory:**

   ```bash
   cd RiaCrawler
   
4. **Build and run the project using Docker Compose:**

   ```bash
   docker-compose up --build
   
