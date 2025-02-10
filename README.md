# onTime - Transit Delay Tracker
onTime is an app which allows users to selectively look at bus stations in Lübeck and get a score on the upcoming departures based on the historical delays of the bus lines.
Website: https://ontime-e0281.web.app/

## Introduction
When coming from a larger city to Lübeck, the limited availability of public transportation can be surprising. Instead of an urban rail network, Lübeck relies solely on a system of bus lines to provide alternatives to cars and bicycles. However, regular bus users will quickly notice that delays are common, and occasional unannounced cancellations are not unusual.

But is this perception truly reflective of reality, or is judgment distorted by rare but overly salient negative experiences? This project aims to answer this question and, at the same time, assist public and private sector stakeholders in making better decisions regarding public transportation—whether for personal use or for planning and implementing measures to strengthen the transport network.

## Concept
Achieving these objectives requires the development of two interlinked components. The first involves setting up a database to collect all bus delays and cancellations. This database categorizes data by bus stop, bus line, and delay duration. Additionally, it records various environmental factors that might contextualize delays and prevent misinterpretations.

The second component is a web-based application that allows users to interact with the collected data in multiple ways. A numerical score provides a quick assessment of a bus line's reliability. Furthermore, the application offers detailed statistics, visual representations, and filtering options based on specific environmental factors.

## Implementation
Currently, there is no centralized dataset available on bus delays in Lübeck, which presents a challenge for implementation. To overcome this, our system retrieves real-time data from the interactive network map provided by Stadtwerke Lübeck via API requests. This data includes scheduled and actual arrival times for all buses. Additionally, environmental conditions at the time of data collection are obtained using the OpenMeteo API based on the station coordinates. The collected data is then stored in a dedicated database.

The application is primarily designed for mobile use. However, to ensure accessibility across all platforms, we chose a "Mobile First" approach by developing a website using Vue.js with Tailwind CSS. For maps and charts, we integrated the open-source UI components Leaflet and ApexCharts, which offer excellent adaptability and compatibility with Vue.js and mobile views.

### Code Overview
The project consists of two main parts: the backend, responsible for data collection and storage, and the frontend, providing a user-friendly interface for data visualization.

#### Backend (Python + Flask)
The backend is built using Python and Flask and consists of the following key components:
- `srv_run.py`: The main entry point for running the backend server.
- `srv_setup.py`: Handles initial database setup and configuration.
- `srv_data/`: Contains modules for data retrieval and processing.
  - `srv_firebase/`: Manages interactions with Firebase for real-time data storage.
  - `srv_json/`: Handles JSON-based data transformations.
  - `srv_logging/`: Implements logging mechanisms for debugging and monitoring.

#### Frontend (Vue.js + Tailwind CSS)
The frontend is a Vue.js application structured as follows:
- `src/`: Contains the main application logic.
  - `components/`: Houses reusable UI components.
  - `views/`: Defines different pages of the application.
  - `store/`: Manages application-wide state using Vuex.
- `public/`: Contains static assets such as images and icons.
- `firebase.json`: Configuration file for Firebase deployment.
- `tailwind.config.js`: Tailwind CSS configuration file for styling.

### Key Features
- **Real-time Data Collection:** The backend retrieves live bus schedule data from Stadtwerke Lübeck and records delays.
- **Environmental Context:** The system integrates weather data from OpenMeteo to provide insights into delay causes.
- **Interactive Data Visualization:** Users can explore bus stop reliability through maps and statistical charts.
- **Mobile-First Design:** The Vue.js frontend is optimized for both mobile and desktop usage.

## Conclusion & Outlook
Data-driven analysis can contribute to making public transportation more transparent and enabling informed decisions for its improvement. By systematically collecting and evaluating delays while incorporating external factors, our project aims to create a more objective picture of Lübeck’s public transport situation and provide a foundation for targeted optimization measures.

During the hackathon, we successfully developed a functional database and a prototype web application that assesses the reliability of bus stops and lines based on environmental conditions. 

The website currently provides essential functionality, but several potential enhancements could be implemented in the future. For instance, bus stop markers could be color-coded to visually represent reliability scores on the map, allowing users to quickly distinguish between more or less reliable stops. Additionally, more environmental factors could be considered, such as nearby construction sites or passenger numbers, to provide further context for recorded delays. Another useful feature would be an overview of optimal and problematic conditions for specific bus lines or stops, making route planning easier. Furthermore, optimizing the database structure could enable an even more detailed analysis of the relationships between various environmental factors and delays.

---

## Project by:
- Nicolai Zorn
- Birk Reimann
- Bennet Hut

## Software & Resources Used:
- [Stadtwerke Lübeck Public Transport API](https://www.swhl.de/mobil/fahrplanauskunft/haltestellen/)
- [Open-Meteo API](https://open-meteo.com/)
- [Vue.js](https://vuejs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [ApexCharts](https://apexcharts.com/)

### Keywords:
"Hackathon", "Bus", "Public Transport", "Traffic", "Delay", "Weather", "Score", "Lübeck"

