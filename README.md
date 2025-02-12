# Institutional Carbon Footprint Calculator

This project is a Django-based web application designed to help institutions calculate and manage their carbon footprint. The application allows users to input data related to energy consumption, fuel usage, transportation, water usage, and waste management, and provides insights into their environmental impact.

## Features

- User registration and authentication
- Institution registration and management
- Input forms for various emission sources
- Calculation and display of total emissions
- Detailed breakdown of emissions by category
- Charts for visual representation of emissions data

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/InstitutionalCarbonFootprintCalculator.git
   cd InstitutionalCarbonFootprintCalculator
   ```

2. Create and activate a virtual environment:

   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. Install the dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Apply the migrations:

   ```sh
   python manage.py migrate
   ```

5. Create a superuser:

   ```sh
   python manage.py createsuperuser
   ```

6. Run the development server:

   ```sh
   python  runserver
   ```

7. Open your browser and navigate to `http://127.0.0.1:8000/` to access the application.

## Usage

- Register a new user account or log in with an existing account.
- Register your institution and provide the necessary details.
- Input data for various emission sources such as energy consumption, fuel usage, transportation, water usage, and waste management.
- View the calculated total emissions and detailed breakdown by category.
- Edit or update the input data as needed.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
